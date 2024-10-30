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
        
        # Always return raw response for debugging
        try:
            data = response.json()
        except:
            data = None
            
        return {
            "status_code": response.status_code,
            "raw_text": response.text,
            "data": data
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
            with st.expander("Debug Information", expanded=True):
                st.write("Status Code:", result.get("status_code"))
                st.write("Raw Response Text:")
                st.code(result.get("raw_text"))
                
            if result.get("data"):
                st.success("Analysis Complete!")
                data = result["data"]
                
                with st.expander("Company Overview", expanded=True):
                    st.markdown(data.get("Overview", "No overview available"))
                    
                with st.expander("Recent News"):
                    st.markdown(data.get("News", "No news available"))
                    
                with st.expander("Competitors"):
                    comp_text = data.get("Competitors", "")
                    comp_list = [c.strip() for c in comp_text.split('\n') if c.strip()]
                    for comp in comp_list:
                        st.markdown(f"• {comp}")
    else:
        st.warning("Please enter both company name and website.")

st.markdown("---")
st.markdown("Built with Streamlit & Make.com")
