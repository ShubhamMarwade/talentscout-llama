import json
import re
import random
import math
import streamlit as st

from llm import chat_completion, OLLAMA_MODEL, OLLAMA_HOST
from prompts import SYSTEM_PROMPT, TECH_Q_PROMPT
from data_store import (
    save_candidate_report,
    generate_candidate_id,
    get_all_candidates,
    get_candidate_by_id,
    delete_candidate,
    get_stats,
)
from styles import PREMIUM_CSS
from components import (
    top_bar,
    sidebar_brand,
    sidebar_divider,
    recruiter_pill,
    step_indicator,
    premium_header,
    glass_card,
    feature_cards_row,
    section_label,
    stat_tile,
    stats_grid,
    candidate_row,
    badge,
    question_card,
    word_indicator,
    score_card,
    recommendation_banner,
    completion_ring,
    evaluating_panel,
    thank_you_hero,
    hero_section,
    detail_list,
    profile_grid,
)

# ================================================================
# PAGE CONFIG
# ================================================================

st.set_page_config(
    page_title="TalentScout — AI Hiring Assistant",
    page_icon="🎯",
    layout="wide",
)

st.markdown(PREMIUM_CSS, unsafe_allow_html=True)
st.markdown(top_bar(), unsafe_allow_html=True)

# ================================================================
# CREDENTIALS
# ================================================================

RECRUITER_EMAIL    = "recruiter@demo.com"
RECRUITER_PASSWORD = "demopass123"

# ================================================================
# SESSION STATE
# ================================================================

INITIAL_STATE = {
    "phase": "PROFILE",
    "profile": None,
    "tech_questions": None,
    "flat_questions": None,
    "current_q_idx": 0,
    "tech_answers": [],
    "evaluation": None,
    "_raw_evaluation": None,
    "_generation_attempts": 0,
    "_candidate_id": None,
    "recruiter_logged_in": False,
    "recruiter_view": "dashboard",
    "recruiter_selected_id": None,
}

for _k, _v in INITIAL_STATE.items():
    if _k not in st.session_state:
        st.session_state[_k] = _v

# ================================================================
# HELPERS
# ================================================================

def validate_email(email: str) -> bool:
    return bool(re.match(
        r"^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$",
        email.strip(),
    ))


def validate_phone(phone: str) -> bool:
    cleaned = re.sub(r"[\s\-\(\)\+]", "", phone.strip())
    return cleaned.isdigit() and 7 <= len(cleaned) <= 15


def categorize_tech_stack(raw_list: list[str]) -> dict:
    LANGUAGES = {
        "python","javascript","typescript","java","go","rust","c","c++","c#",
        "ruby","php","swift","kotlin","scala","r","bash","shell","perl","dart",
        "elixir","haskell","lua","objective-c","clojure","groovy","matlab","julia",
    }
    DATABASES = {
        "postgresql","postgres","mysql","sqlite","mongodb","redis","cassandra",
        "dynamodb","elasticsearch","neo4j","mariadb","oracle","mssql","sql server",
        "firebase","supabase","cockroachdb","couchdb","influxdb","clickhouse",
    }
    TOOLS = {
        "docker","kubernetes","k8s","git","github","gitlab","jenkins","terraform",
        "ansible","aws","gcp","azure","nginx","linux","ci/cd","airflow","kafka",
        "rabbitmq","prometheus","grafana","celery","jira","confluence","helm",
        "argocd","datadog","vercel","netlify","heroku","postman","swagger","github actions",
    }
    result = {"languages": [], "frameworks": [], "databases": [], "tools": []}
    for item in raw_list:
        key = item.strip().lower()
        if key in LANGUAGES:
            result["languages"].append(item.strip())
        elif key in DATABASES:
            result["databases"].append(item.strip())
        elif key in TOOLS:
            result["tools"].append(item.strip())
        else:
            result["frameworks"].append(item.strip())
    return result


def flatten_questions(blocks: list) -> list[dict]:
    flat = []
    for block in blocks:
        tech = block.get("technology", "General")
        for q in block.get("questions", []):
            if isinstance(q, str) and q.strip():
                flat.append({"technology": tech, "question": q.strip()})
    return flat


def score_badge_variant(score: int) -> str:
    if score >= 7: return "hire"
    if score >= 5: return "maybe"
    return "reject"

# ================================================================
# EVALUATION ENGINE  (unchanged from original)
# ================================================================

EVAL_SYSTEM = "You are a JSON API. Output ONLY raw JSON. No prose, no markdown."

SCORE_ONE_PROMPT = (
    "Score this interview answer. Return ONLY JSON.\n\n"
    "Technology: {technology}\n"
    "Question: {question}\n"
    "Answer: {answer}\n\n"
    '{{\"score\": 7, \"note\": \"one sentence observation\"}}\n\n'
    "score is an integer 1-10. note is one short sentence. "
    "Output only the JSON object."
)

EVAL_FALLBACK = {
    "technical_depth": 5, "practical_knowledge": 5, "communication": 5,
    "overall_score": 5, "recommendation": "Maybe",
    "strengths": ["Candidate completed the screening process."],
    "weaknesses": ["Automated evaluation could not be completed."],
    "summary": "Manual review recommended.",
    "per_question_scores": [], "completion_rate": 0,
}


def _score_one_answer(question_text: str, answer: str, technology: str) -> dict:
    from llm import safe_json_extract, _stream_ollama
    if answer.strip() == "[Skipped]":
        return {"score": 1, "note": "Question was skipped by the candidate."}
    payload = {
        "model": OLLAMA_MODEL, "keep_alive": "10m", "format": "json",
        "messages": [
            {"role": "system", "content": EVAL_SYSTEM},
            {"role": "user", "content": SCORE_ONE_PROMPT.format(
                technology=technology, question=question_text, answer=answer,
            )},
        ],
        "options": {"temperature": 0.1, "num_predict": 80},
    }
    try:
        raw    = _stream_ollama(payload)
        parsed = safe_json_extract(raw)
        if isinstance(parsed, dict) and "score" in parsed:
            sc = max(1, min(10, int(parsed["score"])))
            return {"score": sc, "note": str(parsed.get("note", ""))}
    except Exception:
        pass
    return {"score": 5, "note": "Default score — could not parse model response."}


def _run_evaluation() -> tuple:
    answers = st.session_state.tech_answers
    if not answers:
        return "No answers.", EVAL_FALLBACK

    scored_answers = []
    progress = st.progress(0, text="Scoring answers…")

    for i, qa in enumerate(answers):
        progress.progress(
            (i + 1) / len(answers),
            text=f"✨ Scoring {i + 1}/{len(answers)} — {qa['technology']}",
        )
        result = _score_one_answer(qa["question"], qa["answer"], qa["technology"])
        scored_answers.append({**qa, **result})

    progress.empty()

    scores = [sa["score"] for sa in scored_answers]
    n      = len(scores)
    overall = round(sum(scores) / n)

    if n >= 4:
        mid       = n // 2
        tech_depth = round(0.35 * sum(scores[:mid]) / mid + 0.65 * sum(scores[mid:]) / (n - mid))
    else:
        tech_depth = overall

    non_skipped   = [sa["score"] for sa in scored_answers if sa["answer"] != "[Skipped]"]
    prac_know     = round(sum(non_skipped) / len(non_skipped)) if non_skipped else overall
    comm_data     = [(sa["score"], len(sa["answer"].split())) for sa in scored_answers if sa["answer"] != "[Skipped]"]
    communication = round(sum(min(10, sc + min(2, wc / 50)) for sc, wc in comm_data) / len(comm_data)) if comm_data else max(1, overall - 2)

    overall       = max(1, min(10, overall))
    tech_depth    = max(1, min(10, tech_depth))
    prac_know     = max(1, min(10, prac_know))
    communication = max(1, min(10, communication))

    recommendation = "Hire" if overall >= 7 else ("Maybe" if overall >= 5 else "Reject")

    sorted_s   = sorted(scored_answers, key=lambda x: -x["score"])
    strengths  = [f"[{sa['technology']}] {sa['note']}" for sa in sorted_s[:3]  if sa["score"] >= 6 and sa.get("note")]
    weaknesses = [f"[{sa['technology']}] {sa['note']}" for sa in sorted_s[-2:] if sa["score"] <= 5 and sa.get("note")]

    total_qs = len(answers)
    skipped  = sum(1 for a in answers if a["answer"] == "[Skipped]")
    answered = total_qs - skipped
    profile  = st.session_state.profile

    summary = (
        f"{profile['full_name']} completed a {total_qs}-question screening "
        f"({answered} answered, {skipped} skipped). "
        f"Overall: {overall}/10. Recommendation: {recommendation}."
    )

    evaluation = {
        "technical_depth":      tech_depth,
        "practical_knowledge":  prac_know,
        "communication":        communication,
        "overall_score":        overall,
        "recommendation":       recommendation,
        "strengths":            strengths  or ["Candidate completed the screening."],
        "weaknesses":           weaknesses or ["No significant gaps identified."],
        "summary":              summary,
        "per_question_scores":  scored_answers,
        "completion_rate":      round(answered / total_qs * 100) if total_qs else 0,
    }

    debug = "\n".join(
        f"Q{i+1} [{sa['technology']}]: score={sa['score']} | {sa.get('note','')}"
        for i, sa in enumerate(scored_answers)
    )
    return debug, evaluation


# ================================================================
# SIDEBAR
# ================================================================

def render_sidebar():
    st.sidebar.markdown(sidebar_brand(), unsafe_allow_html=True)
    st.sidebar.markdown(sidebar_divider(), unsafe_allow_html=True)

    if st.session_state.recruiter_logged_in:
        # ── Recruiter mode ────────────────────────────────────
        st.sidebar.markdown(recruiter_pill(), unsafe_allow_html=True)

        if st.sidebar.button("📊 Dashboard", use_container_width=True):
            st.session_state.recruiter_view        = "dashboard"
            st.session_state.recruiter_selected_id = None
            st.rerun()

        if st.sidebar.button("🚪 Logout", use_container_width=True):
            st.session_state.recruiter_logged_in   = False
            st.session_state.recruiter_view        = "dashboard"
            st.session_state.recruiter_selected_id = None
            st.rerun()

    else:
        # ── Step progress ─────────────────────────────────────
        phase_map = {"PROFILE": 1, "TECH_QA": 2, "EVALUATING": 3, "SHOW_EVALUATION": 3}
        current   = phase_map.get(st.session_state.phase, 1)
        st.sidebar.markdown(step_indicator(current), unsafe_allow_html=True)

        # Time estimate during Q&A
        if st.session_state.phase == "TECH_QA" and st.session_state.flat_questions:
            remaining = len(st.session_state.flat_questions) - st.session_state.current_q_idx
            est       = max(1, remaining * 2)
            st.sidebar.markdown(sidebar_divider(), unsafe_allow_html=True)
            st.sidebar.markdown(
                glass_card(
                    f'<div style="text-align:center;">'
                    f'<div style="font-size:1.2em;margin-bottom:4px;">⏱️</div>'
                    f'<div style="font-family:Syne,sans-serif;font-weight:800;font-size:22px;color:var(--t100);">~{est} min</div>'
                    f'<div style="font-family:Fira Code,monospace;font-size:9px;color:var(--t400);text-transform:uppercase;letter-spacing:2px;">{remaining} questions left</div>'
                    f'</div>'
                ),
                unsafe_allow_html=True,
            )

        st.sidebar.markdown(sidebar_divider(), unsafe_allow_html=True)

        # Recruiter login
        st.sidebar.markdown(
            '<div class="sb-section-title" style="margin-bottom:12px;">🔐 Recruiter Portal</div>',
            unsafe_allow_html=True,
        )
        with st.sidebar.form("recruiter_login", clear_on_submit=False):
            login_email = st.text_input("Email",    placeholder="recruiter@demo.com")
            login_pass  = st.text_input("Password", type="password", placeholder="••••••••")
            login_btn   = st.form_submit_button("🔑 Sign In", use_container_width=True)

        if login_btn:
            if (
                login_email.strip().lower() == RECRUITER_EMAIL
                and login_pass == RECRUITER_PASSWORD
            ):
                st.session_state.recruiter_logged_in = True
                st.session_state.recruiter_view      = "dashboard"
                st.rerun()
            else:
                st.sidebar.error("❌ Invalid credentials.")

        st.sidebar.markdown(
            '<div style="text-align:center;font-family:Fira Code,monospace;font-size:10px;color:var(--t500);margin-top:6px;">demo: recruiter@demo.com</div>',
            unsafe_allow_html=True,
        )

        if st.session_state.phase != "PROFILE":
            st.sidebar.markdown(sidebar_divider(), unsafe_allow_html=True)
            if st.sidebar.button("🔄 New Screening", use_container_width=True):
                was_recruiter = st.session_state.recruiter_logged_in
                st.session_state.clear()
                for k, v in INITIAL_STATE.items():
                    st.session_state[k] = v
                st.session_state.recruiter_logged_in = was_recruiter
                st.rerun()

    st.sidebar.markdown(sidebar_divider(), unsafe_allow_html=True)
    st.sidebar.markdown(
        f'<div style="text-align:center;">{badge("🤖 " + OLLAMA_MODEL, "muted")}</div>',
        unsafe_allow_html=True,
    )


# ================================================================
# RECRUITER: DASHBOARD
# ================================================================

def render_recruiter_dashboard():
    st.markdown(
        premium_header(
            "Recruiter Dashboard",
            "Manage candidates and review AI-powered evaluation reports",
            "OVERVIEW",
        ),
        unsafe_allow_html=True,
    )

    stats = get_stats()
    st.markdown(
        stats_grid([
            stat_tile("📋", stats["total"],     "Total",     "sc-total"),
            stat_tile("✅", stats["hire"],      "Hire",      "sc-hire"),
            stat_tile("⚠️", stats["maybe"],    "Maybe",     "sc-maybe"),
            stat_tile("✗",  stats["reject"],    "Reject",    "sc-reject"),
            stat_tile("⭐", stats["avg_score"], "Avg Score", "sc-avg"),
        ]),
        unsafe_allow_html=True,
    )

    candidates = get_all_candidates()

    if not candidates:
        st.markdown(
            hero_section(
                "📭",
                "No Candidates Yet",
                "Reports appear here automatically after candidates complete their screening.",
            ),
            unsafe_allow_html=True,
        )
        return

    # ── Filters ──────────────────────────────────────────────
    st.markdown(
        '<div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:16px;">'
        '<div style="font-family:Syne,sans-serif;font-weight:700;font-size:15px;color:var(--t100);">Candidates</div>'
        f'<span class="badge badge-muted">{len(candidates)} results</span>'
        '</div>',
        unsafe_allow_html=True,
    )

    fc1, fc2 = st.columns([3, 1])
    with fc1:
        search = st.text_input("", placeholder="🔍  Search by name or email…", label_visibility="collapsed")
    with fc2:
        rec_filter = st.selectbox("", ["All", "Hire", "Maybe", "Reject"], label_visibility="collapsed")

    filtered = candidates
    if search.strip():
        s = search.strip().lower()
        filtered = [
            c for c in filtered
            if s in c.get("profile", {}).get("full_name", "").lower()
            or s in c.get("profile", {}).get("email", "").lower()
        ]
    if rec_filter != "All":
        filtered = [c for c in filtered if c.get("evaluation", {}).get("recommendation") == rec_filter]

    if not filtered:
        st.warning("No candidates match your filters.")
        return

    for cand in filtered:
        prof    = cand.get("profile", {})
        eval_d  = cand.get("evaluation", {})
        cid     = cand.get("candidate_id", "???")
        ts      = cand.get("timestamp", "")[:16].replace("T", " ")
        rec     = eval_d.get("recommendation", "—")
        overall = eval_d.get("overall_score", 0)
        comp    = eval_d.get("completion_rate", 0)
        role    = ", ".join(prof.get("desired_positions", ["—"]))

        st.markdown(
            candidate_row(
                name=prof.get("full_name", "Unknown"),
                email=prof.get("email", "—"),
                role=role, timestamp=ts,
                score=overall if isinstance(overall, int) else 0,
                recommendation=rec, completion=comp,
            ),
            unsafe_allow_html=True,
        )
        if st.button("📋 View Report", key=f"view_{cid}", use_container_width=True):
            st.session_state.recruiter_view        = "report"
            st.session_state.recruiter_selected_id = cid
            st.rerun()


# ================================================================
# RECRUITER: SINGLE REPORT
# ================================================================

def render_recruiter_report():
    cid    = st.session_state.recruiter_selected_id
    record = get_candidate_by_id(cid)

    if not record:
        st.error(f"❌ Record not found (ID: {cid})")
        if st.button("← Back"):
            st.session_state.recruiter_view = "dashboard"
            st.session_state.recruiter_selected_id = None
            st.rerun()
        return

    profile   = record.get("profile", {})
    eval_data = record.get("evaluation", {})
    answers   = record.get("answers", [])
    ts        = record.get("timestamp", "")[:16].replace("T", " ")

    if st.button("← Back to Dashboard"):
        st.session_state.recruiter_view        = "dashboard"
        st.session_state.recruiter_selected_id = None
        st.rerun()

    st.markdown(
        premium_header(
            profile.get("full_name", "Unknown"),
            f"Screened: {ts} · ID: {cid}",
            "EVALUATION REPORT",
        ),
        unsafe_allow_html=True,
    )

    # badges row
    rec = eval_data.get("recommendation", "Maybe")
    rec_v = {"Hire": "hire", "Maybe": "maybe", "Reject": "reject"}.get(rec, "muted")
    role  = ", ".join(profile.get("desired_positions", ["—"]))
    st.markdown(
        f'<div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:28px;">'
        f'{badge("🕐 " + ts, "muted")}'
        f'{badge("ID: " + cid, "muted")}'
        f'{badge("💼 " + role, "accent")}'
        f'{badge(rec, rec_v)}'
        f'</div>',
        unsafe_allow_html=True,
    )

    # ── Score tiles ───────────────────────────────────────────
    tech_d  = eval_data.get("technical_depth", 0)
    prac_k  = eval_data.get("practical_knowledge", 0)
    comm    = eval_data.get("communication", 0)
    overall = eval_data.get("overall_score", 0)

    st.markdown(
        f'<div class="score-tiles anim2">'
        f'{score_card("🧠", tech_d,  "Technical Depth")}'
        f'{score_card("🔧", prac_k,  "Practical Knowledge")}'
        f'{score_card("💬", comm,    "Communication")}'
        f'{score_card("⭐", overall, "Overall Score")}'
        f'</div>',
        unsafe_allow_html=True,
    )

    # ── Verdict ───────────────────────────────────────────────
    st.markdown(recommendation_banner(rec), unsafe_allow_html=True)

    # ── Completion + Summary ──────────────────────────────────
    comp_rate = eval_data.get("completion_rate", 100)
    cr1, cr2  = st.columns([1, 3])
    with cr1:
        st.markdown(completion_ring(comp_rate), unsafe_allow_html=True)
    with cr2:
        st.markdown(
            glass_card(
                section_label("📝 Summary")
                + f'<div style="color:var(--t200);font-size:13.5px;line-height:1.8;margin-top:12px;">'
                f'{eval_data.get("summary", "No summary available.")}'
                f'</div>'
            ),
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Strengths / Weaknesses ────────────────────────────────
    col_s, col_w = st.columns(2)
    with col_s:
        st.markdown(
            glass_card(
                section_label("✅ Strengths")
                + detail_list(eval_data.get("strengths", ["—"]), "var(--hire)")
            ),
            unsafe_allow_html=True,
        )
    with col_w:
        st.markdown(
            glass_card(
                section_label("⚠️ Areas for Improvement")
                + detail_list(eval_data.get("weaknesses", ["—"]), "var(--maybe)")
            ),
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Per-question breakdown ────────────────────────────────
    per_q = eval_data.get("per_question_scores", [])
    if per_q:
        st.markdown(section_label("📋 Per-Question Breakdown"), unsafe_allow_html=True)
        for i, qa in enumerate(per_q, 1):
            sc      = qa.get("score", 0)
            bv      = score_badge_variant(sc)
            tech    = qa.get("technology", "")
            q_text  = qa.get("question", "")
            note    = qa.get("note", "")
            ans     = qa.get("answer", "")
            short_q = q_text[:65] + ("…" if len(q_text) > 65 else "")

            with st.expander(f"Q{i}. [{tech}] — {short_q}  ·  {sc}/10", expanded=False):
                st.markdown(
                    f'<div style="display:flex;gap:8px;margin-bottom:16px;flex-wrap:wrap;">'
                    f'{badge(tech, "accent")} {badge(str(sc) + "/10", bv)}'
                    f'</div>',
                    unsafe_allow_html=True,
                )
                st.markdown(f"**Question:** {q_text}")
                st.markdown(f"**Evaluator Note:** _{note}_")
                st.divider()
                if ans == "[Skipped]":
                    st.caption("_(Candidate skipped this question)_")
                else:
                    st.markdown("**Candidate's Answer:**")
                    st.write(ans)

    if not per_q and answers:
        with st.expander("📄 Full Candidate Answers", expanded=False):
            for i, qa in enumerate(answers, 1):
                st.markdown(f"**Q{i}. [{qa.get('technology','')}]** {qa.get('question','')}")
                if qa.get("answer") == "[Skipped]":
                    st.caption("_(Skipped)_")
                else:
                    st.write(qa.get("answer", ""))
                if i < len(answers):
                    st.divider()

    # ── Candidate profile ─────────────────────────────────────
    ts_data = profile.get("tech_stack", {})
    with st.expander("👤 Candidate Profile", expanded=False):
        st.markdown(
            profile_grid([
                ("Name",         profile.get("full_name", "—")),
                ("Email",        profile.get("email", "—")),
                ("Phone",        profile.get("phone", "—")),
                ("Location",     profile.get("current_location") or "—"),
                ("Experience",   f"{profile.get('years_experience','—')} years"),
                ("Desired Role", ", ".join(profile.get("desired_positions", ["—"]))),
                ("Languages",    ", ".join(ts_data.get("languages", [])) or "—"),
                ("Frameworks",   ", ".join(ts_data.get("frameworks", [])) or "—"),
                ("Databases",    ", ".join(ts_data.get("databases", [])) or "—"),
                ("Tools",        ", ".join(ts_data.get("tools", [])) or "—"),
            ]),
            unsafe_allow_html=True,
        )

    # ── Export & Delete ───────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    col_export, col_delete = st.columns([3, 1])

    with col_export:
        export_data = {
            "candidate_id": cid,
            "timestamp":    record.get("timestamp", ""),
            "profile":      profile,
            "evaluation":   {k: v for k, v in eval_data.items() if k != "per_question_scores"},
            "answers":      answers,
        }
        safe_name = profile.get("full_name", "candidate").replace(" ", "_").lower()
        st.download_button(
            label="📥 Export Report as JSON",
            data=json.dumps(export_data, indent=2, default=str),
            file_name=f"report_{safe_name}.json",
            mime="application/json",
            use_container_width=True,
        )

    with col_delete:
        if st.button("🗑️ Delete", type="secondary", use_container_width=True):
            st.session_state[f"confirm_delete_{cid}"] = True
        if st.session_state.get(f"confirm_delete_{cid}"):
            st.markdown(
                f'<div style="background:rgba(248,113,113,.05);border:1px solid rgba(248,113,113,.15);'
                f'border-radius:12px;padding:12px;color:var(--reject);font-size:13px;margin-top:8px;">⚠️ This cannot be undone.</div>',
                unsafe_allow_html=True,
            )
            cd1, cd2 = st.columns(2)
            with cd1:
                if st.button("Yes, delete", key=f"yes_{cid}"):
                    delete_candidate(cid)
                    st.session_state.recruiter_view        = "dashboard"
                    st.session_state.recruiter_selected_id = None
                    st.session_state.pop(f"confirm_delete_{cid}", None)
                    st.rerun()
            with cd2:
                if st.button("Cancel", key=f"no_{cid}"):
                    st.session_state.pop(f"confirm_delete_{cid}", None)
                    st.rerun()

    with st.expander("🔬 Debug: raw scoring output", expanded=False):
        st.code(str(record.get("raw_debug", ""))[:5000], language="text")


# ================================================================
# CANDIDATE: PROFILE PHASE
# ================================================================

def render_profile_phase():
    st.markdown(
        premium_header(
            "TalentScout",
            "Complete your profile to begin a personalized AI-powered technical screening tailored to your exact skill set.",
            "AI HIRING ASSISTANT",
        ),
        unsafe_allow_html=True,
    )

    # Feature cards
    st.markdown(feature_cards_row(), unsafe_allow_html=True)

    # Profile form card — styled via CSS targeting the stForm container
    st.markdown("""
<style>
/* Card shell around the entire form */
div[data-testid="stForm"] {
    background: var(--gb) !important;
    border: 1px solid var(--gbdr) !important;
    border-radius: var(--r-xl) !important;
    padding: 28px !important;
    position: relative !important;
    overflow: hidden !important;
    animation: fadeUp .5s .16s var(--ease) both !important;
}
/* Top shine line */
div[data-testid="stForm"]::before {
    content: '' !important;
    position: absolute !important;
    top: 0 !important; left: 20% !important; right: 20% !important;
    height: 1px !important;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,.06), transparent) !important;
}
/* Remove default Streamlit form border/bg */
div[data-testid="stForm"] > div:first-child {
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
}
</style>
""", unsafe_allow_html=True)

    st.markdown(section_label("📝 Your Profile"), unsafe_allow_html=True)

    with st.form("candidate_form"):
        col1, col2 = st.columns(2)
        with col1:
            full_name = st.text_input("Full Name *",             placeholder="e.g. Jane Smith")
            email     = st.text_input("Email *",                 placeholder="e.g. jane@example.com")
            phone     = st.text_input("Phone *",                 placeholder="e.g. +1 555-123-4567")
            years     = st.number_input("Years of Experience *", min_value=0.0, max_value=50.0, step=0.5, value=0.0, help="Include internships and freelance work")
        with col2:
            position  = st.text_input("Desired Position *",      placeholder="e.g. Senior Backend Engineer")
            location  = st.text_input("Current Location",        placeholder="e.g. San Francisco, CA")
            tech_raw  = st.text_area(
                "Tech Stack * (comma-separated)",
                placeholder="e.g. Python, FastAPI, PostgreSQL, Docker, React, AWS",
                height=122,
                help="List all technologies you're comfortable being tested on",
            )

        st.markdown(
            '<div style="display:flex;align-items:center;gap:14px;margin-top:8px;">'
            '<span style="color:var(--t400);font-size:13px;">~15 questions · ~20 min</span>'
            '</div>',
            unsafe_allow_html=True,
        )
        submitted = st.form_submit_button("🚀 Start Technical Screening", use_container_width=True)

    if submitted:
        errors = []
        if not full_name.strip():       errors.append("Full Name is required.")
        if not email.strip():           errors.append("Email is required.")
        elif not validate_email(email): errors.append("Please enter a valid email address.")
        if not phone.strip():           errors.append("Phone is required.")
        elif not validate_phone(phone): errors.append("Valid phone number required (7–15 digits).")
        if not position.strip():        errors.append("Desired Position is required.")
        if not tech_raw.strip():        errors.append("Tech Stack is required.")

        if errors:
            for e in errors:
                st.error(e)
            st.stop()

        raw_list = [t.strip() for t in tech_raw.split(",") if t.strip()]
        if not raw_list:
            st.error("Enter at least one technology.")
            st.stop()
        if len(raw_list) > 20:
            st.warning("⚠️ Many technologies listed — we'll cap at 15 questions.")

        profile = {
            "full_name":         full_name.strip(),
            "email":             email.strip(),
            "phone":             phone.strip(),
            "years_experience":  years,
            "desired_positions": [position.strip()],
            "current_location":  location.strip(),
            "tech_stack":        categorize_tech_stack(raw_list),
        }
        st.session_state.profile              = profile
        st.session_state._candidate_id        = generate_candidate_id(profile)
        st.session_state.phase                = "TECH_QA"
        st.session_state._generation_attempts = 0
        st.rerun()


# ================================================================
# CANDIDATE: TECH Q&A PHASE
# ================================================================

def render_tech_qa_phase():
    profile = st.session_state.profile

    st.markdown(
        premium_header(
            "Technical Screening",
            f"Candidate: {profile['full_name']}",
            "ASSESSMENT",
        ),
        unsafe_allow_html=True,
    )

    # ── Generate questions ────────────────────────────────────
    if st.session_state.tech_questions is None:
        if st.session_state._generation_attempts >= 3:
            st.error("❌ Failed to generate questions after 3 attempts.")
            if st.button("🔄 Restart"):
                st.session_state.clear()
                for k, v in INITIAL_STATE.items():
                    st.session_state[k] = v
                st.rerun()
            st.stop()

        with st.spinner("⏳ Generating tailored technical questions…"):
            raw = chat_completion(
                system=SYSTEM_PROMPT,
                user=TECH_Q_PROMPT.format(
                    tech_stack_json=json.dumps(profile["tech_stack"], indent=2),
                    desired_positions=json.dumps(profile["desired_positions"]),
                    years_experience=str(profile["years_experience"]),
                ),
                response_format="json",
                _token_key="questions",
            )

        if not isinstance(raw, dict):
            st.session_state._generation_attempts += 1
            st.error(f"❌ Unexpected response (attempt {st.session_state._generation_attempts}/3). Retrying…")
            st.rerun()

        questions_list = raw.get("questions")
        if not isinstance(questions_list, list) or len(questions_list) == 0:
            st.session_state._generation_attempts += 1
            st.error(f"❌ No questions generated (attempt {st.session_state._generation_attempts}/3). Retrying…")
            st.rerun()

        flat = flatten_questions(questions_list)[:15]
        if not flat:
            st.session_state._generation_attempts += 1
            st.error(f"❌ Questions malformed (attempt {st.session_state._generation_attempts}/3). Retrying…")
            st.rerun()

        st.session_state.tech_questions  = questions_list
        st.session_state.flat_questions  = flat
        st.session_state.current_q_idx   = 0
        st.session_state.tech_answers    = []
        st.rerun()

    # ── Display current question ──────────────────────────────
    flat_qs = st.session_state.flat_questions
    idx     = st.session_state.current_q_idx
    total   = len(flat_qs)

    if idx < total:
        # Answered / skipped summary badges
        if idx > 0:
            answered_count = sum(1 for a in st.session_state.tech_answers if a["answer"] != "[Skipped]")
            skipped_count  = sum(1 for a in st.session_state.tech_answers if a["answer"] == "[Skipped]")
            st.markdown(
                f'<div class="answered-badges">'
                f'{badge("✅ " + str(answered_count) + " answered", "hire")} '
                f'{badge("⏭ " + str(skipped_count) + " skipped", "muted")} '
                f'{badge("📝 " + str(total - idx) + " left", "accent")}'
                f'</div>',
                unsafe_allow_html=True,
            )

        current = flat_qs[idx]

        # Question card (includes the progress bar)
        st.markdown(
            question_card(
                technology=current["technology"],
                question=current["question"],
                number=idx + 1,
                total=total,
            ),
            unsafe_allow_html=True,
        )

        # Answer textarea
        answer = st.text_area(
            "Your Answer",
            key=f"answer_{idx}",
            height=164,
            placeholder="Type your answer… Be specific, include real examples where possible.",
        )

        if answer:
            st.markdown(word_indicator(len(answer.split())), unsafe_allow_html=True)

        # Action buttons
        col_skip, col_submit = st.columns([1, 3])
        with col_skip:
            if st.button("⏭ Skip", use_container_width=True):
                st.session_state.tech_answers.append({
                    "technology": current["technology"],
                    "question":   current["question"],
                    "answer":     "[Skipped]",
                })
                st.session_state.current_q_idx += 1
                st.rerun()
        with col_submit:
            if st.button("✅ Submit Answer", use_container_width=True, type="primary"):
                if not answer.strip():
                    st.warning("Please provide an answer, or use Skip.")
                    st.stop()
                st.session_state.tech_answers.append({
                    "technology": current["technology"],
                    "question":   current["question"],
                    "answer":     answer.strip(),
                })
                st.session_state.current_q_idx += 1
                st.rerun()

        # Finish early
        if idx >= 5:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🏁 Finish Early & Submit", help="Skip remaining questions and evaluate now"):
                for rq in flat_qs[idx:]:
                    st.session_state.tech_answers.append({
                        "technology": rq["technology"],
                        "question":   rq["question"],
                        "answer":     "[Skipped]",
                    })
                st.session_state.phase = "EVALUATING"
                st.rerun()
    else:
        st.session_state.phase = "EVALUATING"
        st.rerun()


# ================================================================
# CANDIDATE: EVALUATING PHASE
# ================================================================

def render_evaluating_phase():
    st.markdown(
        premium_header("Evaluating Responses", "Scoring each answer individually…", "PROCESSING"),
        unsafe_allow_html=True,
    )

    total = len(st.session_state.tech_answers)
    st.markdown(
        glass_card(evaluating_panel(answers_count=total, scored=0)),
        unsafe_allow_html=True,
    )

    # Run the actual evaluation
    raw_evaluation, evaluation = _run_evaluation()

    st.session_state.evaluation      = evaluation
    st.session_state._raw_evaluation = raw_evaluation

    save_candidate_report(
        candidate_id=st.session_state._candidate_id,
        profile=st.session_state.profile,
        answers=st.session_state.tech_answers,
        evaluation=evaluation,
        raw_debug=raw_evaluation,
    )

    st.session_state.phase = "SHOW_EVALUATION"
    st.rerun()


# ================================================================
# CANDIDATE: RESULT
# ================================================================

def render_candidate_result():
    profile   = st.session_state.profile
    eval_data = st.session_state.evaluation

    # Thank-you hero
    st.markdown(thank_you_hero(profile["full_name"]), unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # Completion ring (centred)
    comp_rate = eval_data.get("completion_rate", 100)
    _, ring_col, _ = st.columns([1, 1, 1])
    with ring_col:
        st.markdown(
            f'<div class="completion-ring-wrap">{completion_ring(comp_rate)}</div>',
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # Success card
    st.markdown(
        f'<div class="success-card anim3">'
        f'<div class="success-title">🎉 Submitted Successfully</div>'
        f'<div class="success-desc">Our recruitment team will review your responses and be in touch within '
        f'<strong style="color:var(--t200);">3–5 business days</strong>.</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # Strengths highlights (no scores shown to candidate)
    strengths = eval_data.get("strengths", [])
    if strengths and "Automated evaluation" not in strengths[0]:
        cleaned = [re.sub(r"^\[.*?\]\s*", "", s) for s in strengths]
        st.markdown(
            glass_card(
                section_label("💡 Highlights from Your Screening")
                + detail_list(cleaned, "var(--hire)")
            ),
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # Review answers
    with st.expander("📄 Review Your Answers", expanded=False):
        for i, qa in enumerate(st.session_state.tech_answers, 1):
            st.markdown(f"**Q{i}. [{qa['technology']}]** {qa['question']}")
            if qa["answer"] == "[Skipped]":
                st.caption("_(Skipped)_")
            else:
                st.write(qa["answer"])
            if i < len(st.session_state.tech_answers):
                st.divider()

    # Footer
    st.markdown(
        glass_card(
            '<div style="text-align:center;padding:8px 0;">'
            '<div style="color:var(--t400);font-size:13px;">📧 A confirmation has been recorded. Thank you for your interest!</div>'
            '</div>'
        ),
        unsafe_allow_html=True,
    )

    st.balloons()


# ================================================================
# MAIN ROUTING
# ================================================================

render_sidebar()

if st.session_state.recruiter_logged_in:
    if st.session_state.recruiter_view == "report" and st.session_state.recruiter_selected_id:
        render_recruiter_report()
    else:
        render_recruiter_dashboard()
else:
    phase = st.session_state.phase
    if phase == "PROFILE":
        render_profile_phase()
    elif phase == "TECH_QA":
        render_tech_qa_phase()
    elif phase == "EVALUATING":
        render_evaluating_phase()
    elif phase == "SHOW_EVALUATION":
        render_candidate_result()