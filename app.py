from pathlib import Path

import streamlit as st

from utils.ai_assistant import answer_question
from utils.eligibility import check_eligibility
from utils.scheme_manager import load_schemes, search_schemes

st.set_page_config(page_title="CivicSathi AI", page_icon="🏛️", layout="wide", initial_sidebar_state="expanded")

def styles():
    try:
        with (Path(__file__).resolve().parent / "assets" / "style.css").open(encoding="utf-8") as f: st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except OSError: pass
styles()
schemes = load_schemes()
if "messages" not in st.session_state: st.session_state.messages = []

with st.sidebar:
    st.markdown("# 🏛️ CivicSathi")
    st.caption("Government schemes made simple")
    page = st.radio("Navigate", ["Home", "AI Assistant", "Explore Schemes", "Eligibility Checker", "Document Guide"], label_visibility="collapsed")
    st.divider()
    st.caption("Independent informational tool. Not an official government website.")


def scheme_card(s):
    with st.container():
        st.markdown(f"<div class='scheme-card'><span class='tag'>{s.get('category','Scheme')}</span><h3 style='margin-top:12px'>{s['name']}</h3><p>{s['description']}</p></div>", unsafe_allow_html=True)
        with st.expander("View details"):
            st.markdown("**Benefits**")
            for x in s.get("benefits", []): st.write("• " + x)
            st.markdown("**Eligibility**")
            for x in s.get("eligibility", []): st.write("• " + x)
            st.markdown("**Documents**")
            for x in s.get("documents", []): st.write("• " + x)
            st.markdown("**How to apply**")
            for i,x in enumerate(s.get("application_steps", []),1): st.write(f"{i}. {x}")
            st.link_button("Open official website ↗", s.get("official_url", "https://india.gov.in/"))
            st.caption("⚠️ " + s.get("verification_status", "Verify current rules on the official portal."))

if page == "Home":
    st.markdown("<div class='hero'><h1>Government schemes, made simpler.</h1><p>Understand benefits, check what may apply to you, and find the right official next step.</p></div>", unsafe_allow_html=True)
    a,b,c=st.columns(3)
    for col, val, label in [(a,len(schemes),"Scheme guides"),(b,"24/7","Ask anytime"),(c,"Official","Source links")]:
        col.markdown(f"<div class='metric'><strong>{val}</strong>{label}</div>",unsafe_allow_html=True)
    st.write("")
    st.subheader("Ask CivicSathi")
    prompt=st.chat_input("Try: Who can apply for PM-KISAN?")
    if prompt:
        with st.spinner("Checking the scheme guide…"):
            reply, source=answer_question(prompt,schemes)
        st.session_state.messages.extend([{"role":"user","content":prompt},{"role":"assistant","content":reply,"source":source}])
    if st.session_state.messages:
        for m in st.session_state.messages[-4:]:
            with st.chat_message(m["role"]):
                st.markdown(m["content"])
                if m.get("source"): st.caption("Answered with " + m["source"])
    st.subheader("Quick access")
    c1,c2,c3,c4=st.columns(4)
    for col,icon,title,desc in [(c1,"🔎","Explore schemes","Search six popular guides"),(c2,"✅","Check eligibility","Get cautious preliminary guidance"),(c3,"📄","Document guide","Learn common document uses"),(c4,"💬","AI assistant","Ask questions in simple English")]:
        col.markdown(f"<div class='info-card'><h3>{icon} {title}</h3><p>{desc}</p></div>",unsafe_allow_html=True)
    st.write("")
    st.subheader("Popular schemes")
    cols=st.columns(3)
    for i,s in enumerate(schemes[:3]):
        with cols[i]: scheme_card(s)
    st.subheader("How CivicSathi works")
    st.markdown("1. **Explore** a short guide.  2. **Ask** a question grounded in the guide.  3. **Verify** details on the official portal before acting.")

elif page == "AI Assistant":
    st.title("💬 AI Government Assistant")
    st.caption("Answers use the local scheme guide, with Gemini when configured. Verify current rules on official sources.")
    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])
            if m.get("source"): st.caption("Answered with " + m["source"])
    prompt=st.chat_input("Ask about a scheme, documents, or application steps")
    if prompt:
        st.session_state.messages.append({"role":"user","content":prompt})
        with st.chat_message("user"): st.markdown(prompt)
        with st.chat_message("assistant"):
            with st.spinner("Preparing a grounded answer…"):
                reply,source=answer_question(prompt,schemes)
            st.markdown(reply); st.caption("Answered with " + source)
        st.session_state.messages.append({"role":"assistant","content":reply,"source":source})

elif page == "Explore Schemes":
    st.title("🔎 Explore government schemes")
    query=st.text_input("Search schemes", placeholder="Try education, farmer, health…")
    found=search_schemes(query)
    st.caption(f"{len(found)} scheme guide(s)")
    if not found: st.info("No matching schemes. Try another keyword.")
    for start in range(0,len(found),2):
        cols=st.columns(2)
        for col,s in zip(cols,found[start:start+2]):
            with col: scheme_card(s)

elif page == "Eligibility Checker":
    st.title("✅ Preliminary eligibility checker")
    st.markdown("<div class='notice'>This gives preliminary guidance only. It is not an official eligibility decision and does not store your answers.</div>",unsafe_allow_html=True)
    selected=st.selectbox("Choose a scheme",schemes,format_func=lambda x:x["name"])
    c1,c2=st.columns(2)
    with c1: age=st.number_input("Age (optional)",min_value=0,max_value=120,value=0,help="Leave at 0 if you prefer not to enter it")
    with c2: state=st.text_input("State (optional)",max_chars=50)
    income=st.number_input("Annual family income (₹, optional)",min_value=0,value=0,step=10000)
    occupation=st.text_input("Occupation / relevant household details (optional)",max_chars=100)
    category=st.text_input("Category (optional)",max_chars=50)
    if st.button("Check preliminary guidance",type="primary"):
        result=check_eligibility(selected, age if age else None,state,income if income else None,occupation,category)
        st.subheader(result["result"])
        for x in result["reasons"]: st.write("• "+x)
        if result["missing"]: st.warning("Still needs checking: " + "; ".join(result["missing"]))
        with st.expander("Documents that may be needed"):
            for x in result["documents"]: st.write("• "+x)
        with st.expander("Suggested next steps"):
            for x in result["next_steps"]: st.write("• "+x)
        st.link_button("Verify on official portal ↗",result["official_url"])
    st.caption("Avoid entering Aadhaar numbers, bank account numbers, or other sensitive identifiers.")

else:
    st.title("📄 Common document guide")
    st.write("Documents vary by scheme, state, applicant category and current application cycle. Use the scheme's official checklist.")
    docs=[("Aadhaar card","Identity verification or account linking, where required."),("Income certificate","Documents household income for schemes with income criteria."),("Caste certificate","Supports category-based benefits where the selected scheme requires it."),("Bank passbook","Confirms account details for eligible direct benefit transfers."),("Educational certificates","Confirms course, marks, enrollment or progression for education schemes."),("Residence certificate","Supports state residence requirements where applicable."),("Passport-size photograph","Used for identity records or application forms when requested.")]
    cols=st.columns(2)
    for i,(name,why) in enumerate(docs):
        with cols[i%2]: st.markdown(f"<div class='info-card'><h3>📌 {name}</h3><p>{why}</p></div>",unsafe_allow_html=True); st.write("")
    st.info("Only submit documents through official government portals or authorized offices. Requirements can change.")

st.divider()
st.caption("CivicSathi AI is an independent informational MVP, not an official government service. Scheme information can change; verify details with the linked authority.")



