"""
TalentScout — UI Components
Every function returns an HTML string that exactly matches the HTML prototype.
"""
import math


def top_bar() -> str:
    return '<div class="top-bar"></div>'


# ── Sidebar brand ─────────────────────────────────────────────────

def sidebar_brand() -> str:
    return (
        '<div class="sb-logo">'
        '<div class="sb-logo-mark">🎯</div>'
        '<div>'
        '<div class="sb-name">TalentScout</div>'
        '<div class="sb-sub">AI Hiring Assistant</div>'
        '</div>'
        '</div>'
    )


def sidebar_divider() -> str:
    return '<div class="sb-divider"></div>'


def recruiter_pill() -> str:
    return (
        '<div class="recruiter-pill">'
        '<div class="recruiter-pill-dot"></div>'
        '<div class="recruiter-pill-label">🔓 Recruiter Mode Active</div>'
        '</div>'
    )


# ── Step indicator (sidebar) ──────────────────────────────────────

def step_indicator(current: int) -> str:
    steps = [("1", "Profile"), ("2", "Technical Q&A"), ("3", "Complete")]
    html = '<div class="sb-section-title">Progress</div><div class="sb-steps">'
    for i, (num, label) in enumerate(steps, 1):
        if i < current:
            dot_cls, lbl_cls, dot_content = "done", "done", "✓"
        elif i == current:
            dot_cls, lbl_cls, dot_content = "active", "active", num
        else:
            dot_cls, lbl_cls, dot_content = "pending", "", num
        html += (
            f'<div class="sb-step">'
            f'<div class="sb-step-dot {dot_cls}">{dot_content}</div>'
            f'<div class="sb-step-label {lbl_cls}">{label}</div>'
            f'</div>'
        )
    html += '</div>'
    return html


# ── Page header ───────────────────────────────────────────────────

def premium_header(title: str, subtitle: str = "", eyebrow: str = "") -> str:
    eyebrow_h = f'<div class="page-eyebrow">{eyebrow}</div>' if eyebrow else ""
    sub_h     = f'<div class="page-desc">{subtitle}</div>' if subtitle else ""
    return (
        f'<div class="page-header anim1">'
        f'{eyebrow_h}'
        f'<div class="page-title"><span>{title}</span></div>'
        f'{sub_h}'
        f'</div>'
    )


# ── Glass card ────────────────────────────────────────────────────

def glass_card(content: str) -> str:
    return f'<div class="card">{content}</div>'


# ── Feature cards row ─────────────────────────────────────────────

def feature_cards_row() -> str:
    cards = [
        ("🎯", "Tailored Questions",  "Questions generated based on your exact tech stack & experience level"),
        ("⚡", "Instant Analysis",    "AI-powered evaluation engine scores every answer individually"),
        ("🔒", "Confidential",        "Your responses are secure and only visible to the hiring team"),
    ]
    items = "".join(
        f'<div class="feat-card">'
        f'<span class="feat-icon">{icon}</span>'
        f'<div class="feat-title">{title}</div>'
        f'<div class="feat-desc">{desc}</div>'
        f'</div>'
        for icon, title, desc in cards
    )
    return f'<div class="feat-grid anim2">{items}</div>'


# ── Section label ─────────────────────────────────────────────────

def section_label(text: str) -> str:
    return f'<div class="section-label">{text}</div>'


# ── Stats grid (dashboard) ────────────────────────────────────────

def stat_tile(icon: str, value, label: str, cls: str) -> str:
    return (
        f'<div class="stat-card {cls}">'
        f'<div class="stat-icon">{icon}</div>'
        f'<div class="stat-val">{value}</div>'
        f'<div class="stat-lbl">{label}</div>'
        f'</div>'
    )


def stats_grid(tiles: list[str]) -> str:
    return f'<div class="stats-grid">{"".join(tiles)}</div>'


# ── Candidate row (dashboard list) ───────────────────────────────

def candidate_row(
    name: str, email: str, role: str, timestamp: str,
    score: int, recommendation: str, completion: int,
) -> str:
    rec_cls   = {"Hire": "hire", "Maybe": "maybe", "Reject": "reject"}.get(recommendation, "")
    score_b   = "hire" if score >= 7 else ("maybe" if score >= 5 else "reject")
    rec_b     = {"Hire": "hire", "Maybe": "maybe", "Reject": "reject"}.get(recommendation, "muted")
    initials  = "".join(w[0].upper() for w in name.split()[:2]) if name.strip() else "?"
    return (
        f'<div class="cand-row {rec_cls}">'
        f'<div class="cand-avatar">{initials}</div>'
        f'<div class="cand-info">'
        f'<div class="cand-name">{name}</div>'
        f'<div class="cand-meta">📧 {email} · 💼 {role} · 🕐 {timestamp}</div>'
        f'</div>'
        f'<div class="cand-badges">'
        f'<span class="badge badge-{score_b}">{score}/10</span>'
        f'<span class="badge badge-{rec_b}">{recommendation}</span>'
        f'<span class="badge badge-teal">{completion}%</span>'
        f'</div>'
        f'</div>'
    )


# ── Badge ─────────────────────────────────────────────────────────

def badge(text: str, variant: str = "accent") -> str:
    """variant: hire | maybe | reject | accent | teal | muted"""
    return f'<span class="badge badge-{variant}">{text}</span>'


# ── Question card ─────────────────────────────────────────────────

def question_card(technology: str, question: str, number: int, total: int) -> str:
    pct = round((number - 1) / total * 100) if total else 0
    return (
        f'<div class="q-progress-wrap anim2">'
        f'<div class="q-progress-info">'
        f'<span class="q-progress-label">Question {number} of {total}</span>'
        f'<span class="q-progress-fraction">{pct}% complete</span>'
        f'</div>'
        f'<div class="progress-bar-bg"><div class="progress-bar-fill" style="width:{pct}%"></div></div>'
        f'</div>'
        f'<div class="q-card anim3">'
        f'<div class="q-card-header">'
        f'<div class="q-number">{number}</div>'
        f'<div class="q-tech-pill">{technology}</div>'
        f'<div class="q-counter">{number} / {total}</div>'
        f'</div>'
        f'<div class="q-text">{question}</div>'
        f'</div>'
    )


# ── Word count indicator ──────────────────────────────────────────

def word_indicator(count: int) -> str:
    if count < 10:
        cls, icon, msg = "wc-low",  "✎", f"{count} words — elaborate more"
    elif count < 30:
        cls, icon, msg = "wc-mid",  "✍", f"{count} words — good start"
    else:
        cls, icon, msg = "wc-good", "✓", f"{count} words — solid detail"
    return f'<div class="wc-bar {cls}">{icon} {msg}</div>'


# ── Score card (report) ───────────────────────────────────────────

def score_card(icon: str, value: int, label: str, delay: int = 0) -> str:
    tier = "tile-high" if value >= 7 else ("tile-mid" if value >= 5 else "tile-low")
    return (
        f'<div class="score-tile {tier}">'
        f'<div class="score-tile-icon">{icon}</div>'
        f'<div class="score-tile-val">{value}</div>'
        f'<div class="score-tile-max">/10</div>'
        f'<div class="score-tile-label">{label}</div>'
        f'</div>'
    )


# ── Recommendation banner ─────────────────────────────────────────

def recommendation_banner(rec: str) -> str:
    cfg = {
        "Hire":   ("verdict-hire",   "✅", "Hire",   "Strong candidate — advance to the next interview round."),
        "Maybe":  ("verdict-maybe",  "⚠️", "Maybe",  "Borderline — follow-up interview recommended."),
        "Reject": ("verdict-reject", "✗",  "Reject", "Does not meet current requirements."),
    }
    cls, icon, label, desc = cfg.get(rec, cfg["Maybe"])
    return (
        f'<div class="verdict-banner {cls}">'
        f'<span class="verdict-icon">{icon}</span>'
        f'<div class="verdict-label">{label}</div>'
        f'<div class="verdict-desc">{desc}</div>'
        f'</div>'
    )


# ── Completion ring ───────────────────────────────────────────────

def completion_ring(pct: int) -> str:
    r     = 46
    circ  = 2 * math.pi * r
    offset = circ - (pct / 100) * circ
    color = "var(--hire)" if pct >= 80 else ("var(--maybe)" if pct >= 50 else "var(--reject)")
    return (
        f'<div class="ring-wrapper">'
        f'<svg width="110" height="110" viewBox="0 0 110 110">'
        f'<circle class="ring-bg" cx="55" cy="55" r="{r}" stroke-width="5"/>'
        f'<circle class="ring-progress" cx="55" cy="55" r="{r}" '
        f'stroke="{color}" stroke-width="5" '
        f'stroke-dasharray="{circ:.1f}" stroke-dashoffset="{offset:.1f}"/>'
        f'</svg>'
        f'<div class="ring-center">'
        f'<div class="ring-pct" style="color:{color}">{pct}%</div>'
        f'</div>'
        f'</div>'
        f'<div class="ring-lbl">Completion Rate</div>'
    )


# ── Evaluating panel ──────────────────────────────────────────────

def evaluating_panel(answers_count: int, scored: int = 0) -> str:
    def step(label: str, status: str) -> str:
        return (
            f'<div class="eval-step {status}">'
            f'<div class="eval-step-dot"></div>'
            f'{label}'
            f'</div>'
        )

    ring_html = (
        '<div class="eval-ring">'
        '<svg width="120" height="120" viewBox="0 0 120 120">'
        '<circle cx="60" cy="60" r="50" fill="none" stroke="var(--s4)" stroke-width="4"/>'
        '<circle cx="60" cy="60" r="50" fill="none" stroke="var(--accent2)" stroke-width="4"'
        ' stroke-linecap="round" stroke-dasharray="80 234"/>'
        '<circle cx="60" cy="60" r="50" fill="none" stroke="var(--accent)" stroke-width="4"'
        ' stroke-linecap="round" stroke-dasharray="40 274" stroke-dashoffset="-90"/>'
        '</svg>'
        '<div class="eval-ring-inner">⚡</div>'
        '</div>'
    )

    steps_html = (
        step("✓ Profile validated", "done")
        + step(f"✓ {answers_count} answers collected", "done")
        + step(f"Scoring answers ({scored}/{answers_count})…", "active")
        + step("Generating final report", "pending")
    )

    return (
        f'<div style="text-align:center;padding:40px 0;">'
        f'{ring_html}'
        f'<div class="eval-title">Evaluating Responses</div>'
        f'<div class="eval-desc">Our AI is scoring each answer individually based on '
        f'technical depth, accuracy, and communication quality.</div>'
        f'<div class="eval-steps">{steps_html}</div>'
        f'</div>'
    )


# ── Thank-you hero ────────────────────────────────────────────────

def thank_you_hero(name: str) -> str:
    return (
        f'<div style="text-align:center;" class="anim1">'
        f'<div class="result-check">✓</div>'
        f'<div class="page-title" style="justify-content:center;display:block;">Screening <span>Complete</span></div>'
        f'<div class="page-desc" style="max-width:480px;margin:10px auto 0;text-align:center;">'
        f'Thank you, <strong style="color:var(--t100);">{name}</strong>. Your responses have been submitted.</div>'
        f'</div>'
    )


# ── Hero / empty state ────────────────────────────────────────────

def hero_section(emoji: str, title: str, desc: str) -> str:
    return (
        f'<div style="text-align:center;padding:80px 40px;" class="anim1">'
        f'<div style="font-size:3em;margin-bottom:16px;">{emoji}</div>'
        f'<div style="font-family:Syne,sans-serif;font-weight:700;font-size:22px;color:var(--t100);margin-bottom:12px;">{title}</div>'
        f'<div style="color:var(--t300);font-size:14px;max-width:400px;margin:0 auto;line-height:1.7;">{desc}</div>'
        f'</div>'
    )


# ── Detail list (strengths/weaknesses) ───────────────────────────

def detail_list(items: list[str], dot_color: str = "var(--hire)") -> str:
    rows = ""
    for item in items:
        rows += (
            f'<div class="detail-item">'
            f'<div class="detail-dot" style="background:{dot_color};"></div>'
            f'<div class="detail-text">{item}</div>'
            f'</div>'
        )
    return rows


# ── Profile grid (report) ─────────────────────────────────────────

def profile_grid(fields: list[tuple[str, str]]) -> str:
    rows = "".join(
        f'<div class="profile-field">'
        f'<span class="profile-key">{k}</span>'
        f'<span class="profile-val">{v}</span>'
        f'</div>'
        for k, v in fields
    )
    return f'<div class="profile-grid">{rows}</div>'