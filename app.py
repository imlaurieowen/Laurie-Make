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
            if response.status_code == 404:
                return {"error": "Webhook URL not found. Please check if the scenario is activated in Make.com"}
            elif response.status_code == 500:
                return {"error": "Server error in Make.com scenario. Check the scenario configuration."}
            else:
                return {"error": f"Error: Status code {response.status_code}. Response: {response.text}"}
            
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
                    overview = results.get("Overview", "")
                    if overview:
                        # Remove any ## from the start of the text
                        if overview.startswith("##"):
                            overview = overview.split("##")[1]
                        st.markdown(overview)
                
                # Display Recent News
                with st.expander("Recent News"):
                    # Try to extract Recent News section
                    overview = results.get("Overview", "")
                    if "Recent News:" in overview:
                        news = overview.split("Recent News:")[1].split("Investment Analysis:")[0]
                        st.markdown(news)
                    else:
                        st.markdown("No recent news available")
                
                # Display Investment Analysis
                with st.expander("Investment Analysis"):
                    # Try to extract Investment Analysis section
                    overview = results.get("Overview", "")
                    if "Investment Analysis:" in overview:
                        analysis = overview.split("Investment Analysis:")[1]
                        st.markdown(analysis)
                    else:
                        st.markdown("No investment analysis available")
                
                # Display Competitors
                with st.expander("Competitors"):
                    competitors = results.get("Competitors", "")
                    if competitors:
                        # Clean up the competitors text and display as bullet points
                        comp_list = competitors.replace("-", "•").split("\n")
                        for comp in comp_list:
                            if comp.strip():
                                st.markdown(comp.strip())
                    else:
                        st.markdown("No competitors information available")
                
                # Debug Information
                with st.expander("Debug Information", expanded=False):
                    st.subheader("Raw Response")
                    st.json(results)
    else:
        st.warning("Please enter both company name and website.")

st.markdown("---")
st.markdown("Built with Streamlit & Make.com")
