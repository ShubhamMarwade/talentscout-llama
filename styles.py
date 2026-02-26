"""
TalentScout — Premium CSS Design System
Exact pixel-match of the HTML prototype UI.
"""

PREMIUM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=Figtree:wght@300;400;500;600;700&family=Fira+Code:wght@400;500&display=swap');

:root {
  --bg:#0A0A0F; --s1:#0E0E15; --s2:#13131C; --s3:#181824; --s4:#1E1E2E; --s5:#252538;
  --gb:rgba(255,255,255,0.04); --gb2:rgba(255,255,255,0.07);
  --gbdr:rgba(255,255,255,0.06); --gbdr2:rgba(255,255,255,0.11);
  --t100:#F2F2FA; --t200:#C8C8DC; --t300:#8E8EA8; --t400:#5C5C78; --t500:#3A3A52;
  --accent:#6EE7C7; --accent2:#818CF8; --accent3:#F472B6;
  --hire:#34D399; --maybe:#FBBF24; --reject:#F87171;
  --r-sm:8px; --r-md:12px; --r-lg:16px; --r-xl:22px; --r-full:9999px;
  --ease:cubic-bezier(0.16,1,0.3,1);
}

/* ── BASE ── */
.stApp { font-family:'Figtree',sans-serif !important; background-color:var(--bg) !important; color:var(--t100) !important; -webkit-font-smoothing:antialiased; }
#MainMenu,footer,.stDeployButton { visibility:hidden !important; display:none !important; }
header[data-testid="stHeader"] { background:transparent !important; }
.block-container { padding-top:2rem !important; padding-bottom:3rem !important; max-width:1060px !important; }

.stApp::before {
  content:''; position:fixed; inset:0; pointer-events:none; z-index:9999; opacity:.4;
  background-image:url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.03'/%3E%3C/svg%3E");
}

::-webkit-scrollbar{width:4px} ::-webkit-scrollbar-track{background:transparent}
::-webkit-scrollbar-thumb{background:var(--s5);border-radius:99px}
::-webkit-scrollbar-thumb:hover{background:var(--accent2)}

/* ── TOP BAR ── */
.top-bar {
  position:fixed; top:0; left:0; right:0; height:2px; z-index:9998;
  background:linear-gradient(90deg,var(--accent),var(--accent2),var(--accent3),var(--accent));
  background-size:300% 100%; animation:barFlow 4s linear infinite;
}
@keyframes barFlow{0%{background-position:0% 50%}100%{background-position:300% 50%}}

/* ── SIDEBAR ── */
section[data-testid="stSidebar"] { background:var(--s1) !important; border-right:1px solid var(--gbdr) !important; }
section[data-testid="stSidebar"] > div:first-child { padding-top:0 !important; }
[data-testid="collapsedControl"] { visibility:visible !important; display:flex !important; position:fixed !important; top:12px !important; left:12px !important; z-index:999999 !important; background:var(--s3) !important; border:1px solid var(--gbdr) !important; border-radius:var(--r-md) !important; width:40px !important; height:40px !important; align-items:center !important; justify-content:center !important; cursor:pointer !important; }
[data-testid="collapsedControl"]:hover { background:var(--s5) !important; border-color:var(--accent2) !important; }
[data-testid="stSidebar"] [data-testid="stSidebarCollapseButton"] { visibility:visible !important; opacity:1 !important; }

/* ── SIDEBAR BRAND ── */
.sb-logo { display:flex; align-items:center; gap:12px; margin-bottom:32px; padding:0 4px; }
.sb-logo-mark { width:40px; height:40px; border-radius:var(--r-md); background:linear-gradient(135deg,var(--accent2),var(--accent)); display:flex; align-items:center; justify-content:center; font-size:18px; flex-shrink:0; box-shadow:0 0 20px rgba(110,231,199,.15); }
.sb-name { font-family:'Syne',sans-serif; font-weight:800; font-size:16px; color:var(--t100); line-height:1.2; }
.sb-sub  { font-family:'Fira Code',monospace; font-size:9px; color:var(--t400); text-transform:uppercase; letter-spacing:2px; margin-top:2px; }
.sb-divider { height:1px; background:var(--gbdr); margin:20px 0; }
.sb-section-title { font-family:'Fira Code',monospace; font-size:9px; color:var(--t500); text-transform:uppercase; letter-spacing:3px; font-weight:500; margin-bottom:8px; padding:0 4px; }

/* ── SIDEBAR STEPS ── */
.sb-steps { padding:4px 0; }
.sb-step  { display:flex; align-items:center; gap:10px; padding:8px 4px; position:relative; }
.sb-step:not(:last-child)::after { content:''; position:absolute; left:15px; top:32px; width:2px; height:16px; background:var(--gbdr); }
.sb-step-dot { width:22px; height:22px; border-radius:50%; flex-shrink:0; display:flex; align-items:center; justify-content:center; font-size:10px; font-weight:700; border:2px solid var(--s5); font-family:'Fira Code',monospace; transition:all .3s; }
.sb-step-dot.done    { background:var(--hire);   border-color:var(--hire);   color:#000; }
.sb-step-dot.active  { background:var(--accent2); border-color:var(--accent2); color:#fff; box-shadow:0 0 12px rgba(129,140,248,.3); animation:pulseDot 2s ease infinite; }
.sb-step-dot.pending { background:transparent; border-color:var(--s5); color:var(--t500); }
@keyframes pulseDot{0%,100%{box-shadow:0 0 12px rgba(129,140,248,.3)}50%{box-shadow:0 0 24px rgba(129,140,248,.6)}}
.sb-step-label        { font-size:12.5px; font-weight:500; color:var(--t300); }
.sb-step-label.active { color:var(--t100); font-weight:600; }
.sb-step-label.done   { color:var(--hire); }

/* ── RECRUITER PILL ── */
.recruiter-pill { display:flex; align-items:center; gap:8px; padding:10px 12px; border-radius:var(--r-md); background:rgba(52,211,153,.05); border:1px solid rgba(52,211,153,.12); margin-bottom:12px; }
.recruiter-pill-dot   { width:8px; height:8px; border-radius:50%; background:var(--hire); animation:pulseDot 2s ease infinite; }
.recruiter-pill-label { font-family:'Fira Code',monospace; font-size:9px; font-weight:600; color:var(--hire); text-transform:uppercase; letter-spacing:1.5px; }

/* ── PAGE HEADER ── */
.page-header { margin-bottom:40px; }
.page-eyebrow { font-family:'Fira Code',monospace; font-size:10px; color:var(--accent); text-transform:uppercase; letter-spacing:3px; margin-bottom:10px; font-weight:500; }
.page-title   { font-family:'Syne',sans-serif; font-weight:800; font-size:34px; color:var(--t100); line-height:1.1; letter-spacing:-0.5px; }
.page-title span { background:linear-gradient(135deg,var(--accent2),var(--accent)); -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text; }
.page-desc    { color:var(--t300); font-size:14.5px; margin-top:10px; line-height:1.65; max-width:560px; }

/* ── CARD ── */
.card { background:var(--gb); border:1px solid var(--gbdr); border-radius:var(--r-xl); padding:28px; position:relative; overflow:hidden; transition:all .3s var(--ease); }
.card::before { content:''; position:absolute; top:0; left:20%; right:20%; height:1px; background:linear-gradient(90deg,transparent,rgba(255,255,255,.06),transparent); }
.card:hover { border-color:var(--gbdr2); }
.card-sm { padding:18px 22px; border-radius:var(--r-lg); }

/* ── STATS GRID ── */
.stats-grid { display:grid; grid-template-columns:repeat(5,1fr); gap:14px; margin-bottom:36px; }
.stat-card { background:var(--gb); border:1px solid var(--gbdr); border-radius:var(--r-lg); padding:20px 16px; text-align:center; transition:all .25s; position:relative; overflow:hidden; }
.stat-card:hover { transform:translateY(-3px); border-color:var(--gbdr2); box-shadow:0 8px 24px rgba(0,0,0,.3); }
.stat-card::after { content:''; position:absolute; bottom:0; left:20%; right:20%; height:2px; border-radius:2px 2px 0 0; }
.stat-card.sc-total::after{background:var(--accent2)} .stat-card.sc-hire::after{background:var(--hire)}
.stat-card.sc-maybe::after{background:var(--maybe)}   .stat-card.sc-reject::after{background:var(--reject)}
.stat-card.sc-avg::after{background:var(--accent)}
.stat-icon { font-size:18px; margin-bottom:6px; }
.stat-val  { font-family:'Syne',sans-serif; font-weight:800; font-size:28px; line-height:1; letter-spacing:-1px; }
.stat-card.sc-hire .stat-val{color:var(--hire)} .stat-card.sc-maybe .stat-val{color:var(--maybe)}
.stat-card.sc-reject .stat-val{color:var(--reject)} .stat-card.sc-avg .stat-val{color:var(--accent)}
.stat-card.sc-total .stat-val{color:var(--t100)}
.stat-lbl { font-family:'Fira Code',monospace; font-size:9px; color:var(--t400); text-transform:uppercase; letter-spacing:2px; margin-top:6px; font-weight:500; }

/* ── CANDIDATE ROW ── */
.cand-row { display:flex; align-items:center; gap:16px; padding:16px 20px; border-radius:var(--r-lg); background:var(--gb); border:1px solid var(--gbdr); transition:all .2s var(--ease); position:relative; overflow:hidden; margin-bottom:8px; }
.cand-row::before { content:''; position:absolute; left:0; top:0; bottom:0; width:3px; opacity:.7; }
.cand-row.hire::before{background:var(--hire)} .cand-row.maybe::before{background:var(--maybe)} .cand-row.reject::before{background:var(--reject)}
.cand-row:hover { background:var(--gb2); border-color:var(--gbdr2); transform:translateX(4px); }
.cand-avatar { width:42px; height:42px; border-radius:var(--r-md); flex-shrink:0; background:linear-gradient(135deg,rgba(129,140,248,.15),rgba(110,231,199,.1)); border:1px solid rgba(129,140,248,.15); display:flex; align-items:center; justify-content:center; font-family:'Syne',sans-serif; font-weight:800; font-size:14px; color:var(--accent2); }
.cand-info   { flex:1; min-width:0; }
.cand-name   { font-weight:700; font-size:14px; color:var(--t100); }
.cand-meta   { font-size:12px; color:var(--t400); margin-top:2px; }
.cand-badges { display:flex; gap:6px; align-items:center; flex-shrink:0; flex-wrap:wrap; }

/* ── BADGES ── */
.badge { display:inline-flex; align-items:center; padding:3px 10px; border-radius:var(--r-full); font-family:'Fira Code',monospace; font-size:10px; font-weight:500; letter-spacing:.5px; border:1px solid; white-space:nowrap; }
.badge-hire  {background:rgba(52,211,153,.08);  color:var(--hire);   border-color:rgba(52,211,153,.18)}
.badge-maybe {background:rgba(251,191,36,.08);  color:var(--maybe);  border-color:rgba(251,191,36,.18)}
.badge-reject{background:rgba(248,113,113,.08); color:var(--reject); border-color:rgba(248,113,113,.18)}
.badge-accent{background:rgba(129,140,248,.08); color:var(--accent2);border-color:rgba(129,140,248,.18)}
.badge-teal  {background:rgba(110,231,199,.08); color:var(--accent); border-color:rgba(110,231,199,.18)}
.badge-muted {background:var(--gb); color:var(--t400); border-color:var(--gbdr)}

/* ── FEATURE CARDS ── */
.feat-grid { display:grid; grid-template-columns:repeat(3,1fr); gap:16px; margin:32px 0; }
.feat-card { padding:24px 20px; border-radius:var(--r-xl); background:var(--gb); border:1px solid var(--gbdr); transition:all .3s var(--ease); text-align:center; }
.feat-card:hover { transform:translateY(-4px); border-color:var(--gbdr2); box-shadow:0 12px 36px rgba(0,0,0,.3); }
.feat-icon  { font-size:24px; margin-bottom:12px; display:block; }
.feat-title { font-family:'Syne',sans-serif; font-weight:700; font-size:14.5px; color:var(--t100); margin-bottom:6px; }
.feat-desc  { font-size:12.5px; color:var(--t400); line-height:1.6; }

/* ── SECTION LABEL ── */
.section-label { font-family:'Fira Code',monospace; font-size:9.5px; font-weight:600; text-transform:uppercase; letter-spacing:3px; color:var(--t400); margin-bottom:14px; padding-bottom:10px; border-bottom:1px solid var(--gbdr); }

/* ── QUESTION CARD ── */
.q-card { padding:32px; border-radius:var(--r-xl); background:var(--s2); border:1px solid var(--gbdr); position:relative; overflow:hidden; margin-bottom:24px; }
.q-card::before { content:''; position:absolute; left:0; top:0; bottom:0; width:4px; background:linear-gradient(180deg,var(--accent2),var(--accent)); }
.q-card-header { display:flex; align-items:center; gap:12px; margin-bottom:20px; }
.q-number    { width:30px; height:30px; border-radius:var(--r-sm); background:var(--accent2); display:flex; align-items:center; justify-content:center; font-family:'Fira Code',monospace; font-weight:700; font-size:12px; color:#fff; flex-shrink:0; }
.q-tech-pill { font-family:'Fira Code',monospace; font-size:10px; font-weight:500; text-transform:uppercase; letter-spacing:2px; background:rgba(110,231,199,.08); color:var(--accent); border:1px solid rgba(110,231,199,.15); padding:4px 12px; border-radius:var(--r-full); }
.q-counter   { margin-left:auto; font-family:'Fira Code',monospace; font-size:10px; color:var(--t500); }
.q-text      { font-size:17px; color:var(--t100); line-height:1.65; font-weight:400; padding-left:4px; }

.q-progress-wrap { margin-bottom:28px; }
.q-progress-info { display:flex; justify-content:space-between; align-items:center; margin-bottom:8px; }
.q-progress-label    { font-size:12.5px; color:var(--t300); font-weight:500; }
.q-progress-fraction { font-family:'Fira Code',monospace; font-size:11px; color:var(--t400); }
.progress-bar-bg   { height:4px; background:var(--s4); border-radius:var(--r-full); overflow:hidden; }
.progress-bar-fill { height:100%; border-radius:var(--r-full); background:linear-gradient(90deg,var(--accent2),var(--accent)); transition:width .5s var(--ease); }

.answer-area { width:100%; min-height:160px; padding:16px; border-radius:var(--r-lg); background:var(--s2); border:1px solid var(--gbdr); color:var(--t100); font-size:14.5px; font-family:'Figtree',sans-serif; outline:none; transition:all .2s; resize:vertical; }
.answer-area:focus { border-color:var(--accent2); box-shadow:0 0 0 3px rgba(129,140,248,.1); background:var(--s3); }
.answer-area::placeholder { color:var(--t500); }

.wc-bar { display:inline-flex; align-items:center; gap:6px; padding:4px 12px; border-radius:var(--r-full); font-family:'Fira Code',monospace; font-size:10.5px; font-weight:500; border:1px solid; margin-top:8px; }
.wc-low  { background:rgba(248,113,113,.06); color:var(--reject); border-color:rgba(248,113,113,.15); }
.wc-mid  { background:rgba(251,191,36,.06);  color:var(--maybe);  border-color:rgba(251,191,36,.15); }
.wc-good { background:rgba(110,231,199,.06); color:var(--accent); border-color:rgba(110,231,199,.15); }
.answered-badges { display:flex; gap:8px; margin-bottom:20px; flex-wrap:wrap; }

/* ── EVALUATING ── */
.eval-ring { width:120px; height:120px; margin:0 auto 40px; position:relative; }
.eval-ring svg { animation:spin 2s linear infinite; }
@keyframes spin{to{transform:rotate(360deg)}}
.eval-ring-inner { position:absolute; inset:16px; background:var(--s2); border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:28px; }
.eval-title { font-family:'Syne',sans-serif; font-weight:800; font-size:26px; color:var(--t100); margin-bottom:12px; text-align:center; }
.eval-desc  { font-size:14px; color:var(--t300); text-align:center; max-width:400px; line-height:1.7; margin:0 auto; }
.eval-steps { display:flex; flex-direction:column; gap:10px; margin:36px auto 0; width:100%; max-width:360px; }
.eval-step  { display:flex; align-items:center; gap:12px; padding:12px 16px; border-radius:var(--r-md); background:var(--gb); border:1px solid var(--gbdr); font-size:13.5px; }
.eval-step.done   { color:var(--hire);   background:rgba(52,211,153,.05);  border-color:rgba(52,211,153,.12); }
.eval-step.active { color:var(--accent2); background:rgba(129,140,248,.05); border-color:rgba(129,140,248,.12); }
.eval-step.pending{ color:var(--t500); }
.eval-step-dot { width:8px; height:8px; border-radius:50%; flex-shrink:0; }
.eval-step.done .eval-step-dot   { background:var(--hire); }
.eval-step.active .eval-step-dot { background:var(--accent2); animation:pulseDot 1.5s ease infinite; }
.eval-step.pending .eval-step-dot{ background:var(--s5); }

/* ── RESULT ── */
.result-check { width:100px; height:100px; border-radius:50%; background:linear-gradient(135deg,var(--hire),var(--accent)); display:flex; align-items:center; justify-content:center; font-size:40px; margin:0 auto 28px; box-shadow:0 0 40px rgba(52,211,153,.25),0 0 80px rgba(52,211,153,.1); animation:checkPop .7s cubic-bezier(0.34,1.56,0.64,1) forwards; }
@keyframes checkPop{0%{transform:scale(0);opacity:0}60%{transform:scale(1.1)}100%{transform:scale(1);opacity:1}}
.completion-ring-wrap { display:flex; justify-content:center; margin:28px 0; }
.ring-wrapper { position:relative; width:110px; height:110px; margin:0 auto; }
.ring-wrapper svg { transform:rotate(-90deg); }
.ring-wrapper .ring-bg { stroke:var(--s4); fill:none; }
.ring-wrapper .ring-progress { fill:none; stroke-linecap:round; }
.ring-wrapper .ring-center { position:absolute; top:50%; left:50%; transform:translate(-50%,-50%); text-align:center; }
.ring-wrapper .ring-pct { font-family:'Syne',sans-serif; font-size:18px; font-weight:800; line-height:1; }
.ring-lbl { font-family:'Fira Code',monospace; font-size:9px; color:var(--t400); text-transform:uppercase; letter-spacing:2px; margin-top:6px; text-align:center; }
.success-card { background:rgba(52,211,153,.04); border:1px solid rgba(52,211,153,.12); border-radius:var(--r-xl); padding:28px; text-align:center; }
.success-title { font-family:'Syne',sans-serif; font-weight:700; font-size:18px; color:var(--hire); margin-bottom:8px; }
.success-desc  { font-size:13.5px; color:var(--t300); line-height:1.7; }

/* ── SCORE TILES ── */
.score-tiles { display:grid; grid-template-columns:repeat(4,1fr); gap:14px; margin-bottom:28px; }
.score-tile { background:var(--gb); border:1px solid var(--gbdr); border-radius:var(--r-xl); padding:28px 16px; text-align:center; position:relative; overflow:hidden; transition:all .3s var(--ease); }
.score-tile:hover { transform:translateY(-5px); box-shadow:0 16px 40px rgba(0,0,0,.4); }
.score-tile::after { content:''; position:absolute; bottom:0; left:15%; right:15%; height:3px; border-radius:3px 3px 0 0; }
.tile-high::after{background:linear-gradient(90deg,var(--hire),var(--accent))}
.tile-mid::after {background:linear-gradient(90deg,var(--maybe),#FB923C)}
.tile-low::after {background:linear-gradient(90deg,var(--reject),#FB7185)}
.score-tile-icon  { font-size:20px; margin-bottom:8px; }
.score-tile-val   { font-family:'Syne',sans-serif; font-weight:800; font-size:44px; line-height:1; letter-spacing:-2px; margin:8px 0; }
.tile-high .score-tile-val{color:var(--hire)} .tile-mid .score-tile-val{color:var(--maybe)} .tile-low .score-tile-val{color:var(--reject)}
.score-tile-max   { font-family:'Fira Code',monospace; font-size:11px; color:var(--t500); }
.score-tile-label { font-family:'Fira Code',monospace; font-size:9px; color:var(--t400); text-transform:uppercase; letter-spacing:2px; margin-top:10px; }

/* ── VERDICT BANNER ── */
.verdict-banner { border-radius:var(--r-xl); padding:36px 28px; text-align:center; border:1px solid; position:relative; overflow:hidden; margin-bottom:28px; }
.verdict-icon   { font-size:40px; display:block; margin-bottom:12px; }
.verdict-label  { font-family:'Syne',sans-serif; font-weight:800; font-size:22px; text-transform:uppercase; letter-spacing:2px; }
.verdict-desc   { font-size:13.5px; opacity:.7; margin-top:8px; }
.verdict-hire   { background:rgba(52,211,153,.04);  border-color:rgba(52,211,153,.12);  color:var(--hire);   box-shadow:0 0 40px rgba(52,211,153,.06); }
.verdict-maybe  { background:rgba(251,191,36,.04);  border-color:rgba(251,191,36,.12);  color:var(--maybe); }
.verdict-reject { background:rgba(248,113,113,.04); border-color:rgba(248,113,113,.12); color:var(--reject); box-shadow:0 0 40px rgba(248,113,113,.06); }

/* ── DETAIL ITEMS ── */
.detail-item { display:flex; align-items:baseline; gap:10px; padding:10px 0; border-bottom:1px solid var(--gbdr); }
.detail-item:last-child { border-bottom:none; }
.detail-dot  { width:6px; height:6px; border-radius:50%; flex-shrink:0; margin-top:6px; }
.detail-text { font-size:13.5px; color:var(--t200); line-height:1.5; }

/* ── TWO COL ── */
.two-col { display:grid; grid-template-columns:1fr 1fr; gap:16px; }

/* ── PROFILE GRID (report) ── */
.profile-grid { display:grid; grid-template-columns:1fr 1fr; gap:0; }
.profile-field { display:flex; flex-direction:column; gap:3px; padding:10px 0; border-bottom:1px solid var(--gbdr); }
.profile-field:nth-last-child(-n+2) { border-bottom:none; }
.profile-key { font-size:10px; font-weight:600; text-transform:uppercase; letter-spacing:1px; color:var(--t500); }
.profile-val { font-size:13px; color:var(--t200); }

/* ── ANIMATIONS ── */
@keyframes fadeUp{from{opacity:0;transform:translateY(16px)}to{opacity:1;transform:translateY(0)}}
.anim1{animation:fadeUp .5s var(--ease) both}
.anim2{animation:fadeUp .5s .08s var(--ease) both}
.anim3{animation:fadeUp .5s .16s var(--ease) both}
.anim4{animation:fadeUp .5s .24s var(--ease) both}
.anim5{animation:fadeUp .5s .32s var(--ease) both}

/* ── STREAMLIT WIDGET OVERRIDES ── */
.stProgress > div > div > div { background:linear-gradient(90deg,var(--accent2),var(--accent)) !important; border-radius:var(--r-full) !important; height:4px !important; }
.stProgress > div > div { background:var(--s4) !important; border-radius:var(--r-full) !important; height:4px !important; }

.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stNumberInput > div > div > input {
  background:var(--s2) !important; border:1px solid var(--gbdr) !important;
  border-radius:var(--r-md) !important; color:var(--t100) !important;
  font-family:'Figtree',sans-serif !important; font-size:14px !important; transition:all .2s !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus,
.stNumberInput > div > div > input:focus {
  border-color:var(--accent2) !important; box-shadow:0 0 0 3px rgba(129,140,248,.1) !important; background:var(--s3) !important;
}
.stTextInput > div > div > input::placeholder,
.stTextArea > div > div > textarea::placeholder { color:var(--t500) !important; }
.stTextInput label,.stTextArea label,.stNumberInput label,.stSelectbox label {
  font-family:'Figtree',sans-serif !important; font-size:11px !important; font-weight:600 !important;
  color:var(--t300) !important; text-transform:uppercase !important; letter-spacing:.8px !important;
}
.stButton > button { border-radius:var(--r-md) !important; font-family:'Figtree',sans-serif !important; font-weight:600 !important; transition:all .25s var(--ease) !important; }
.stButton > button:hover { transform:translateY(-2px) !important; }
.stButton > button[kind="primary"] { background:linear-gradient(135deg,var(--accent2),var(--accent)) !important; border:none !important; color:#fff !important; box-shadow:0 4px 20px rgba(129,140,248,.25) !important; }
.stButton > button[kind="primary"]:hover { box-shadow:0 8px 30px rgba(129,140,248,.4) !important; }
.streamlit-expanderHeader { background:var(--s2) !important; border:1px solid var(--gbdr) !important; border-radius:var(--r-md) !important; font-family:'Figtree',sans-serif !important; font-weight:500 !important; color:var(--t200) !important; transition:all .2s !important; }
.streamlit-expanderHeader:hover { background:var(--gb2) !important; border-color:var(--gbdr2) !important; }
[data-baseweb="select"] > div { background:var(--s2) !important; border-color:var(--gbdr) !important; border-radius:var(--r-md) !important; color:var(--t100) !important; }
[data-baseweb="popover"] ul { background:var(--s3) !important; }
[data-baseweb="option"]:hover { background:var(--s5) !important; }
.stDownloadButton > button { border-radius:var(--r-md) !important; font-family:'Figtree',sans-serif !important; font-weight:600 !important; background:var(--gb) !important; border:1px solid var(--gbdr) !important; color:var(--t200) !important; transition:all .2s !important; }
.stDownloadButton > button:hover { background:var(--gb2) !important; border-color:var(--gbdr2) !important; transform:translateY(-2px) !important; }
hr { border-color:var(--gbdr) !important; margin:20px 0 !important; }
.stMarkdown p { color:var(--t200); line-height:1.7; }
.stMarkdown strong { color:var(--t100); }
code { background:var(--s4) !important; color:var(--accent) !important; padding:2px 7px !important; border-radius:5px !important; font-family:'Fira Code',monospace !important; }
</style>
"""