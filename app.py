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
            "status_code": response.status_code,
            "raw_text": response.text,
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
            result = run_research(company_name, website)
            
            # Debug section
            with st.expander("Debug Information", expanded=False):
                st.write("Status Code:", result.get("status_code"))
                st.write("Raw Response Text:")
                st.code(result.get("raw_text"))
            
            try:
                if result.get("raw_text"):
                    # Try to clean and parse the response
                    text = result["raw_text"].strip()
                    if text.startswith('{') and text.endswith('}'):
                        sections = text.split('##')
                        
                        st.success("Analysis Complete!")
                        
                        # Display sections
                        for section in sections:
                            section = section.strip()
                            if section:
                                if "Company Overview:" in section:
                                    with st.expander("Company Overview", expanded=True):
                                        st.markdown(section.replace("Company Overview:", "").strip())
                                elif "Recent News:" in section:
                                    with st.expander("Recent News", expanded=True):
                                        st.markdown(section.replace("Recent News:", "").strip())
                                elif "Investment Analysis:" in section:
                                    with st.expander("Investment Analysis", expanded=True):
                                        st.markdown(section.replace("Investment Analysis:", "").strip())
                                elif "Competitors:" in section:
                                    with st.expander("Competitors", expanded=True):
                                        comp_text = section.replace("Competitors:", "").strip()
                                        for comp in comp_text.split('\n'):
                                            if comp.strip():
                                                st.markdown(f"• {comp.strip()}")
            except Exception as e:
                st.error(f"Error processing response: {str(e)}")
    else:
        st.warning("Please enter both company name and website.")

st.markdown("---")
st.markdown("Built with Streamlit & Make.com")
