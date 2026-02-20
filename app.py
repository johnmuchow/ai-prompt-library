import streamlit as st
import json
from datetime import datetime

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Prompt Library — Growth Stock Traders",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── Theme init ────────────────────────────────────────────────────────────────
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True

dark = st.session_state.dark_mode

# ── Theme tokens ──────────────────────────────────────────────────────────────
if dark:
    T = {
        "bg":           "#0d0d14",
        "bg2":          "#101018",
        "bg3":          "#0a0a10",
        "border":       "#1e1e2e",
        "border2":      "#2a2a3e",
        "border3":      "#1a1a28",
        "text":         "#ffffff",
        "text2":        "#9999bb",
        "text3":        "#6666aa",
        "text4":        "#aaaacc",
        "accent":       "#00c896",
        "accent2":      "#00e0aa",
        "accent_bg":    "rgba(0,200,150,0.08)",
        "accent_bdr":   "rgba(0,200,150,0.25)",
        "accent_bdr2":  "rgba(0,200,150,0.3)",
        "cat_bg":       "rgba(99,102,241,0.08)",
        "cat_bdr":      "rgba(99,102,241,0.25)",
        "cat_text":     "#8888ff",
        "post_bg":      "rgba(255,255,255,0.04)",
        "tag_bg":       "rgba(255,255,255,0.03)",
        "input_bg":     "#101018",
        "input_color":  "#e0e0f0",
        "placeholder":  "#333355",
        "hover_shadow": "rgba(0,200,150,0.08)",
        "toggle_icon":  "☀️",
        "toggle_label": "Switch to Light",
    }
else:
    T = {
        "bg":           "#ffffff",
        "bg2":          "#f9f9f9",
        "bg3":          "#f4f4f4",
        "border":       "#e8e8e8",
        "border2":      "#d0d0d0",
        "border3":      "#eeeeee",
        "text":         "#111111",
        "text2":        "#555555",
        "text3":        "#888888",
        "text4":        "#444444",
        "accent":       "#00916e",
        "accent2":      "#00a878",
        "accent_bg":    "#f0fdf8",
        "accent_bdr":   "#00c896",
        "accent_bdr2":  "#00916e",
        "cat_bg":       "#f5f5ff",
        "cat_bdr":      "#c8c8ff",
        "cat_text":     "#5555aa",
        "post_bg":      "#f9f9f9",
        "tag_bg":       "#f5f5f5",
        "input_bg":     "#ffffff",
        "input_color":  "#111111",
        "placeholder":  "#aaaaaa",
        "hover_shadow": "rgba(0,0,0,0.06)",
        "toggle_icon":  "🌙",
        "toggle_label": "Switch to Dark",
    }

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
  @import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=DM+Sans:wght@300;400;500;600;700&display=swap');

  html, body, [class*="css"] {{
    font-family: 'DM Sans', sans-serif;
    background-color: {T['bg']} !important;
    color: {T['text']} !important;
  }}

  #MainMenu {{visibility: hidden;}}
  footer {{visibility: hidden;}}
  header {{visibility: hidden;}}

  .stApp {{ background-color: {T['bg']} !important; }}

  .main .block-container {{
    padding: 2rem 8rem 4rem;
    max-width: 960px !important;
    margin: 0 auto !important;
    background-color: {T['bg']} !important;
  }}

  section.main > div {{
    max-width: 960px !important;
    margin: 0 auto !important;
    padding-left: 8rem !important;
    padding-right: 8rem !important;
  }}

  .accent-bar {{
    height: 4px;
    background: linear-gradient(90deg, #00a878, #00c896, #34d399);
    margin: -2rem -3rem 2.5rem;
  }}

  .header-section {{
    margin-bottom: 2.5rem;
    padding-bottom: 2rem;
    border-bottom: 1px solid {T['border']};
  }}

  .header-badge {{
    display: inline-flex;
    align-items: center;
    gap: 7px;
    background: {T['accent_bg']};
    border: 1px solid {T['accent_bdr2']};
    color: {T['accent']};
    font-family: 'DM Mono', monospace;
    font-size: 11px;
    font-weight: 500;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    padding: 4px 12px;
    border-radius: 2px;
    margin-bottom: 12px;
  }}

  .header-title {{
    font-size: 52px;
    font-weight: 700;
    color: {T['text']};
    letter-spacing: -0.02em;
    line-height: 1.2;
    margin-bottom: 8px;
  }}

  .header-meta {{
    font-family: 'DM Mono', monospace;
    font-size: 11px;
    color: {T['text2']};
    letter-spacing: 0.06em;
  }}

  .header-meta a {{
    color: {T['accent']};
    text-decoration: none;
  }}

  .prompt-card {{
    background: {T['bg2']};
    border: 1px solid {T['border']};
    border-left: 4px solid {T['accent']};
    padding: 24px 28px;
    margin-bottom: 16px;
  }}

  .prompt-card:hover {{
    border-color: {T['border2']};
    border-left-color: {T['accent2']};
    box-shadow: 0 2px 20px {T['hover_shadow']};
  }}

  .card-top {{
    display: flex;
    flex-direction: column;
    margin-bottom: 12px;
    gap: 10px;
  }}

  .card-title {{
    font-size: 26px;
    font-weight: 700;
    color: {T['text']};
    letter-spacing: -0.01em;
    margin-bottom: 4px;
  }}

  .card-use-case {{
    font-size: 18px;
    color: {T['text2']};
    line-height: 1.5;
  }}

  .card-badges {{
    display: flex;
    gap: 6px;
    flex-wrap: wrap;
  }}

  .badge-tool {{
    background: {T['accent_bg']};
    border: 1px solid {T['accent_bdr']};
    color: {T['accent']};
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    padding: 3px 10px;
    border-radius: 2px;
  }}

  .badge-category {{
    background: {T['cat_bg']};
    border: 1px solid {T['cat_bdr']};
    color: {T['cat_text']};
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    padding: 3px 10px;
    border-radius: 2px;
  }}

  .badge-post {{
    background: {T['post_bg']};
    border: 1px solid {T['border']};
    color: {T['text3']};
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    padding: 3px 10px;
    border-radius: 2px;
  }}

  .prompt-box {{
    background: {T['bg3']};
    border: 1px solid {T['border']};
    padding: 16px 20px;
    margin: 14px 0;
    font-family: 'DM Mono', monospace;
    font-size: 12.5px;
    line-height: 1.8;
    color: {T['text4']};
    font-style: italic;
    border-radius: 2px;
  }}

  .prompt-box .ticker {{
    color: {T['accent']};
    font-style: normal;
    font-weight: 500;
  }}

  .card-footer {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-top: 14px;
    padding-top: 12px;
    border-top: 1px solid {T['border3']};
  }}

  .card-tags {{
    display: flex;
    gap: 6px;
    flex-wrap: wrap;
  }}

  .tag {{
    background: {T['tag_bg']};
    border: 1px solid {T['border2']};
    color: {T['text2']};
    font-family: 'DM Mono', monospace;
    font-size: 9px;
    letter-spacing: 0.06em;
    padding: 2px 8px;
    border-radius: 2px;
  }}

  .article-link {{
    color: {T['accent']};
    font-family: 'DM Mono', monospace;
    font-size: 11px;
    text-decoration: none;
    letter-spacing: 0.06em;
  }}

  .article-link:hover {{ text-decoration: underline; }}

  .stats-bar {{
    background: {T['bg2']};
    border: 1px solid {T['border']};
    padding: 14px 20px;
    margin-bottom: 24px;
    display: flex;
    gap: 32px;
    align-items: center;
  }}

  .stat-item {{ text-align: center; }}

  .stat-value {{
    font-family: 'DM Mono', monospace;
    font-size: 22px;
    font-weight: 500;
    color: {T['accent']};
    line-height: 1;
    margin-bottom: 3px;
  }}

  .stat-label {{
    font-family: 'DM Mono', monospace;
    font-size: 9px;
    color: {T['text3']};
    letter-spacing: 0.1em;
    text-transform: uppercase;
  }}

  .stat-divider {{
    width: 1px;
    height: 32px;
    background: {T['border']};
  }}

  .no-results {{
    text-align: center;
    padding: 48px 0;
    color: {T['text3']};
    font-size: 14px;
  }}

  .page-footer {{
    margin-top: 48px;
    padding-top: 24px;
    border-top: 1px solid {T['border']};
    display: flex;
    justify-content: space-between;
    align-items: center;
  }}

  .footer-text {{
    font-family: 'DM Mono', monospace;
    font-size: 11px;
    color: {T['text3']};
    letter-spacing: 0.06em;
  }}

  .footer-text a {{
    color: {T['accent']};
    text-decoration: none;
  }}

  .stTextInput > div > div > input {{
    background-color: {T['input_bg']} !important;
    border-color: {T['border']} !important;
    color: {T['input_color']} !important;
    border-radius: 2px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 14px !important;
  }}

  .stTextInput > div > div > input::placeholder {{
    color: {T['placeholder']} !important;
  }}

  .stSelectbox > div > div {{
    background-color: {T['input_bg']} !important;
    border-color: {T['border']} !important;
    color: {T['input_color']} !important;
    border-radius: 2px !important;
    font-family: 'DM Sans', sans-serif !important;
  }}

  .stSelectbox [data-baseweb="select"] > div {{
    background-color: {T['input_bg']} !important;
    border-color: {T['border']} !important;
    color: {T['input_color']} !important;
  }}

  .stButton > button {{
    background: {T['accent_bg']} !important;
    color: {T['accent']} !important;
    border: 1px solid {T['accent_bdr']} !important;
    border-radius: 2px !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 11px !important;
    letter-spacing: 0.08em !important;
    padding: 6px 16px !important;
    font-weight: 500 !important;
  }}

  .stButton > button:hover {{
    border-color: {T['accent']} !important;
  }}
</style>
""", unsafe_allow_html=True)


# ── Load data ─────────────────────────────────────────────────────────────────
@st.cache_data
def load_prompts():
    with open("prompts.json", "r") as f:
        return json.load(f)

prompts = load_prompts()


# ── Helpers ───────────────────────────────────────────────────────────────────
def format_date(date_str):
    try:
        d = datetime.strptime(date_str, "%Y-%m-%d")
        return d.strftime("%b %d, %Y")
    except:
        return date_str

def highlight_ticker(prompt_text):
    return prompt_text.replace("[TICKER]", '<span class="ticker">[TICKER]</span>')


# ── Header ────────────────────────────────────────────────────────────────────
st.markdown('<div class="accent-bar"></div>', unsafe_allow_html=True)

col_header, col_toggle = st.columns([8, 1])

with col_header:
    st.markdown(f"""
    <div class="header-section">
      <div class="header-badge">📈 AI Tools for Growth Stock Traders</div>
      <div class="header-title">AI Prompt Library</div>
      <div class="header-meta">
        Published by <a href="https://x.com/JohnMuchow" target="_blank">@JohnMuchow</a> ·
        Each prompt links to the full article with live examples
      </div>
    </div>
    """, unsafe_allow_html=True)

with col_toggle:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    if st.button(f"{T['toggle_icon']} {T['toggle_label']}"):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()


# ── Stats bar ─────────────────────────────────────────────────────────────────
tools      = list(set(p["tool"] for p in prompts))
categories = list(set(p["category"] for p in prompts))
posts      = list(set(p["post_number"] for p in prompts))

st.markdown(f"""
<div class="stats-bar">
  <div class="stat-item">
    <div class="stat-value">{len(prompts)}</div>
    <div class="stat-label">Prompts</div>
  </div>
  <div class="stat-divider"></div>
  <div class="stat-item">
    <div class="stat-value">{len(tools)}</div>
    <div class="stat-label">AI Tools</div>
  </div>
  <div class="stat-divider"></div>
  <div class="stat-item">
    <div class="stat-value">{len(categories)}</div>
    <div class="stat-label">Categories</div>
  </div>
  <div class="stat-divider"></div>
  <div class="stat-item">
    <div class="stat-value">{len(posts)}</div>
    <div class="stat-label">Posts</div>
  </div>
</div>
""", unsafe_allow_html=True)


# ── Filters ───────────────────────────────────────────────────────────────────
col1, col2, col3 = st.columns([3, 1.5, 1.5])

with col1:
    search = st.text_input("Search", placeholder="🔍  Search prompts...", label_visibility="collapsed")

with col2:
    all_tools = ["All Tools"] + sorted(list(set(p["tool"] for p in prompts)))
    selected_tool = st.selectbox("Tool", all_tools, label_visibility="collapsed")

with col3:
    all_cats = ["All Categories"] + sorted(list(set(p["category"] for p in prompts)))
    selected_cat = st.selectbox("Category", all_cats, label_visibility="collapsed")

st.markdown("<br>", unsafe_allow_html=True)


# ── Filter logic ──────────────────────────────────────────────────────────────
filtered = prompts

if search:
    s = search.lower()
    filtered = [
        p for p in filtered
        if s in p["title"].lower()
        or s in p["use_case"].lower()
        or s in p["prompt"].lower()
        or s in " ".join(p["tags"]).lower()
        or s in p.get("example_ticker", "").lower()
    ]

if selected_tool != "All Tools":
    filtered = [p for p in filtered if p["tool"] == selected_tool]

if selected_cat != "All Categories":
    filtered = [p for p in filtered if p["category"] == selected_cat]


# ── Prompt cards ──────────────────────────────────────────────────────────────
if not filtered:
    st.markdown('<div class="no-results">No prompts found. Try a different search or filter.</div>', unsafe_allow_html=True)
else:
    for prompt in filtered:
        tags_html   = "".join([f'<span class="tag">#{t}</span>' for t in prompt["tags"]])
        prompt_html = highlight_ticker(prompt["prompt"])

        st.markdown(f"""
        <div class="prompt-card">
          <div class="card-top">
            <div>
              <div class="card-title">{prompt["title"]}</div>
              <div class="card-use-case">{prompt["use_case"]}</div>
            </div>
            <div class="card-badges">
              <span class="badge-tool">{prompt["tool"]}</span>
              <span class="badge-category">{prompt["category"]}</span>
              <span class="badge-post">Post {prompt["post_number"]}</span>
            </div>
          </div>
          <div class="prompt-box">{prompt_html}</div>
          <div class="card-footer">
            <div class="card-tags">{tags_html}</div>
            <a class="article-link" href="{prompt["article_url"]}" target="_blank">→ Read full article</a>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # One-click copy button
        accent      = T["accent"]
        accent_dark = T["accent2"]
        escaped     = prompt["prompt"].replace("\\", "\\\\").replace("`", "\\`")
        copy_html   = f"""
        <div style="display:flex; justify-content:flex-end; margin-top:-8px; margin-bottom:8px;">
          <button onclick="
            navigator.clipboard.writeText(`{escaped}`).then(function() {{
              var btn = document.getElementById('btn_{prompt['id']}');
              btn.innerText = '✓ Copied!';
              btn.style.background = '{accent_dark}';
              setTimeout(function() {{
                btn.innerText = 'Copy Prompt';
                btn.style.background = '{accent}';
              }}, 2000);
            }});
          "
          id="btn_{prompt['id']}"
          style="
            background: {accent};
            color: white;
            border: none;
            padding: 6px 18px;
            font-family: 'DM Mono', monospace;
            font-size: 11px;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            cursor: pointer;
            border-radius: 2px;
            font-weight: 500;
          ">Copy Prompt</button>
        </div>
        """
        st.components.v1.html(copy_html, height=50)
        st.markdown("<br>", unsafe_allow_html=True)


# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="page-footer">
  <div class="footer-text">
    Built by <a href="https://x.com/JohnMuchow" target="_blank">@JohnMuchow</a> ·
    <a href="https://leveluptools.net" target="_blank">LevelUpTools.net</a>
  </div>
</div>
""", unsafe_allow_html=True)
