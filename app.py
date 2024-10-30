import streamlit as st
import requests
import json

def run_research(company_name, website):
    WEBHOOK_URL = "https://hook.eu2.make.com/wxfp1tgeko8o8dmpx1blpxlhqejut50"
    
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
            try:
                # Parse the text response
                result_text = response.text
                # Try to parse it as JSON
                try:
                    result = json.loads(result_text)
                except json.JSONDecodeError:
                    # If it's not JSON, treat it as text
                    result = {
                        "Company Name": company_name,
                        "Analysis": result_text
                    }
                return result
            except Exception as e:
                return {"error": f"Error processing response: {str(e)}"}
        else:
            return {"error": f"Error: Status code {response.status_code}"}
            
    except Exception as e:
        return {"error": f"Error: {str(e)}"}

# Set page config
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
                
                # Display Company Name
                st.header(results.get("Company Name", company_name))
                
                # Display Overview
                with st.expander("Company Overview", expanded=True):
                    st.markdown(results.get("Overview", "No overview available"))
                
                # Display Competitors
                with st.expander("Competitors"):
                    st.markdown(results.get("Competitors", "No competitors information available"))
                
                # For debugging, show both raw response and processed parts
                with st.expander("Debug Information", expanded=False):
                    st.subheader("Raw Response")
                    st.code(str(results))
                    
                    st.subheader("Response Status")
                    st.code(f"Status Code: {response.status_code}")
                    
                    st.subheader("Headers")
                    st.json(dict(response.headers))
                    
                    st.subheader("Full Response Text")
                    st.code(response.text)
    else:
        st.warning("Please enter both company name and website.")

st.markdown("---")
st.markdown("Built with Streamlit & Make.com")
