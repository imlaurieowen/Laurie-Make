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
                
                try:
                    # Attempt to parse the response as text
                    analysis_text = results.get("Analysis", str(results))
                    
                    # Create expandable sections for each part of the analysis
                    parts = analysis_text.split("\n\n")  # Split by double newlines
                    
                    for part in parts:
                        if part.strip():  # Only process non-empty parts
                            # Try to identify section headers
                            if "Company Name:" in part:
                                with st.expander("Company Details", expanded=True):
                                    st.markdown(part)
                            elif "Company Overview:" in part:
                                with st.expander("Company Overview", expanded=True):
                                    st.markdown(part)
                            elif "Recent News:" in part:
                                with st.expander("Recent News", expanded=True):
                                    st.markdown(part)
                            elif "Investment Analysis:" in part:
                                with st.expander("Investment Analysis", expanded=True):
                                    st.markdown(part)
                            elif "Competitors:" in part:
                                with st.expander("Competitors", expanded=True):
                                    st.markdown(part)
                            else:
                                st.markdown(part)
                    
                    # For debugging, show the raw response
                    with st.expander("Debug - Raw Response", expanded=False):
                        st.code(str(results))
                        
                except Exception as e:
                    st.error(f"Error displaying results: {str(e)}")
                    st.code(str(results))  # Show raw results for debugging
    else:
        st.warning("Please enter both company name and website.")

st.markdown("---")
st.markdown("Built with Streamlit & Make.com")
