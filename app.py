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
        
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Error: Status code {response.status_code}"}
            
    except Exception as e:
        return {"error": f"Error: {str(e)}"}

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
            results = run_research(company_name, website)
            
            if "error" in results:
                st.error(results["error"])
            else:
                st.success("Analysis Complete!")
                
                # Display results in clean sections
                st.header(company_name)
                
                with st.expander("Overview", expanded=True):
                    st.markdown(results.get("overview", "").split("Company Overview:")[1].split("Recent News:")[0])
                
                with st.expander("Recent News"):
                    if "Recent News:" in results.get("overview", ""):
                        st.markdown(results.get("overview", "").split("Recent News:")[1].split("Investment Analysis:")[0])
                
                with st.expander("Investment Analysis"):
                    if "Investment Analysis:" in results.get("overview", ""):
                        st.markdown(results.get("overview", "").split("Investment Analysis:")[1])
                
                with st.expander("Competitors"):
                    competitors = results.get("competitors", "").strip()
                    if competitors:
                        comp_list = [c.strip() for c in competitors.split(',')]
                        for comp in comp_list:
                            st.markdown(f"• {comp}")
    else:
        st.warning("Please enter both company name and website.")

st.markdown("---")
st.markdown("Built with Streamlit & Make.com")
