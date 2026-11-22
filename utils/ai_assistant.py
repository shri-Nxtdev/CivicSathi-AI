import os
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

MODEL_NAME = "gemini-3.5-flash"

def answer_question(question, schemes):
    """Use Gemini when configured; otherwise answer from local scheme data."""
    context = "\n".join(
        f"{s.get('name')}: {s.get('description')} Eligibility: {'; '.join(s.get('eligibility', []))} Documents: {'; '.join(s.get('documents', []))} Apply: {'; '.join(s.get('application_steps', []))} Official: {s.get('official_url')}"
        for s in schemes
    )
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        try:
            import streamlit as st
            key = st.secrets.get("GEMINI_API_KEY", "")
        except Exception:
            key = ""
    if key:
        try:
            from google import genai
            client = genai.Client(api_key=key)
            prompt = f"You are CivicSathi AI, an informational assistant for Indian government schemes. Answer in simple English, concise and structured. Use ONLY the context below for scheme claims. Never infer eligibility, deadlines, amounts, or links. If missing, say verify on official website. Include relevant official URLs. This is not a government service.\n\nKNOWLEDGE BASE:\n{context}\n\nQUESTION: {question}"
            response = client.models.generate_content(model=MODEL_NAME, contents=prompt)
            if response.text:
                return response.text, "Gemini AI"
        except Exception:
            pass
    return local_answer(question, schemes), "Local knowledge base"

def local_answer(question, schemes):
    q = (question or "").casefold()
    matches = [s for s in schemes if any(term in q for term in [s.get("name", "").casefold(), s.get("id", "").replace("-", " ")])]
    # Add useful keyword matching for common requests.
    keywords = {"farmer":"pm-kisan", "kisan":"pm-kisan", "health":"pmjay", "ayushman":"pmjay", "scholarship":"nsp", "ssp":"karnataka-ssp", "ujjwala":"pmuy", "lpg":"pmuy", "mgnrega":"mgnrega", "employment":"mgnrega", "job card":"mgnrega"}
    for term, sid in keywords.items():
        if term in q:
            s = next((x for x in schemes if x.get("id") == sid), None)
            if s and s not in matches: matches.append(s)
    if not matches:
        return "I couldn't find a reliable answer in the local scheme guide. Please check the relevant official government portal, or ask about PM-KISAN, PM-JAY, scholarships, PMUY or MGNREGA. Eligibility and current rules need official verification."
    parts = []
    for s in matches[:2]:
        parts.append(f"**{s['name']}**\n{s.get('description','')}\n\n**Eligibility:** {' '.join(s.get('eligibility', []))}\n\n**Next step:** {s.get('application_steps',['Check official portal'])[0]}\n\n[Official website]({s.get('official_url')})")
    return "\n\n---\n\n".join(parts) + "\n\n*This is preliminary information; verify current rules with the official source.*"



