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
        
        response = requests.post(WEBHOOK_URL, json=payload, headers={"Content-Type": "application/json"})
        
        if response.status_code == 200:
            return response.json()
        return {"error": f"Error: Status code {response.status_code}"}
            
    except Exception as e:
        return {"error": str(e)}

st.set_page_config(page_title="Company Research Assistant", layout="wide")
st.title("Company Research Assistant 🔍")

col1, col2 = st.columns(2)
with col1:
    company_name = st.text_input("Company Name", placeholder="Enter company name...")
with col2:
    website = st.text_input("Website", placeholder="Enter company website...")

if st.button("Run Research Analysis", type="primary"):
    if company_name and website:
        with st.spinner('Analyzing company data...'):
            result = run_research(company_name, website)
            
            if "error" in result:
                st.error(result["error"])
            else:
                st.success("Analysis Complete!")
                
                # Display sections
                overview = result.get("data", {}).get("overview", "")
                
                # Company Overview
                st.header("Company Overview")
                if "Company Overview:" in overview:
                    st.write(overview.split("Company Overview:")[1].split("Recent News:")[0].strip())
                
                # Recent News
                st.header("Recent News")
                if "Recent News:" in overview:
                    st.write(overview.split("Recent News:")[1].split("Investment Analysis:")[0].strip())
                
                # Investment Analysis
                st.header("Investment Analysis")
                if "Investment Analysis:" in overview:
                    st.write(overview.split("Investment Analysis:")[1].strip())
                
                # Competitors
                st.header("Competitors")
                competitors = result.get("data", {}).get("competitors", "").strip()
                for comp in competitors.split(","):
                    if comp.strip():
                        st.markdown(f"• {comp.strip()}")

st.markdown("---")
st.markdown("Built with Streamlit & Make.com")
