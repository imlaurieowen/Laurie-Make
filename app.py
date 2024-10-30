import streamlit as st
import requests
import json

def run_research(company_name, website):
    WEBHOOK_URL = "https://hook.eu2.make.com/wxfp1tgeko8o8odmpx1blpxlhqejut50"
    
    try:
        payload = {
            "company_name": company_name,
            "website": website
        }
        
        headers = {
            "Content-Type": "application/json"
        }
        
        response = requests.post(WEBHOOK_URL, json=payload, headers=headers)
        return {
            "status": response.status_code,
            "text": response.text,
            "data": response.json() if response.status_code == 200 else None
        }
            
    except Exception as e:
        return {"error": str(e)}

st.set_page_config(page_title="Company Research Assistant", layout="wide")

st.title("Company Research Assistant 🔍")
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    company_name = st.text_input("Company Name", placeholder="Enter company name...")
with col2:
    website = st.text_input("Website", placeholder="Enter company website...")

if st.button("Run Research Analysis", type="primary"):
    if company_name and website:
        with st.spinner('Analyzing company data...'):
            response = run_research(company_name, website)
            
            # Always show raw response when debugging
            with st.expander("Debug Information", expanded=True):
                st.write("Status:", response.get("status"))
                st.write("Raw Response:", response.get("text"))
                if "error" in response:
                    st.write("Error:", response["error"])
                
            if response.get("data"):
                st.success("Analysis Complete!")
                content = response["data"].get("data", "")
                
                # Display sections
                sections = content.split("##")
                for section in sections:
                    if section.strip():
                        title = section.split("\n")[0].strip(":")
                        if title:
                            with st.expander(title, expanded=True):
                                content = "\n".join(section.split("\n")[1:]).strip()
                                st.markdown(content)
    else:
        st.warning("Please enter both company name and website.")

st.markdown("---")
st.markdown("Built with Streamlit & Make.com")
