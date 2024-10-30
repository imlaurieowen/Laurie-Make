import streamlit as st
import requests
import json

def run_research(company_name, website):
    # Replace this with your Make webhook URL once you have it
    WEBHOOK_URL = "https://hook.eu2.make.com/wxfp1tgeko8o8odmpx1blpxlhqejut50"
    
    try:
        payload = {
            "company_name": company_name,
            "website": website
        }
        
        response = requests.post(WEBHOOK_URL, json=payload)
        
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Error: Status code {response.status_code}"}
            
    except Exception as e:
        return {"error": f"Error: {str(e)}"}
      # Set page config
st.set_page_config(page_title="Company Research Assistant", layout="wide")

# Main app header
st.title("Company Research Assistant 🔍")
st.markdown("---")

# Input section
col1, col2 = st.columns(2)

with col1:
    company_name = st.text_input("Company Name", placeholder="Enter company name...")
    
with col2:
    website = st.text_input("Website", placeholder="Enter company website...")

# Run button
if st.button("Run Research Analysis", type="primary"):
    if company_name and website:
        with st.spinner('Analyzing company data...'):
            results = run_research(company_name, website)
            
            if "error" in results:
                st.error(results["error"])
            else:
                # Display results in an organized way
                st.success("Analysis Complete!")
                
                # Create expandable sections for different types of information
                with st.expander("Company Overview", expanded=True):
                    st.write(results.get("overview", "No overview available"))
                
                with st.expander("Market Analysis"):
                    st.write(results.get("market_analysis", "No market analysis available"))
                
                with st.expander("Key Findings"):
                    st.write(results.get("key_findings", "No key findings available"))
    else:
        st.warning("Please enter both company name and website.")

# Add footer
st.markdown("---")
st.markdown("Built with Streamlit & Make.com")
