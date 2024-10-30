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
                result = response.json()
            except json.JSONDecodeError:
                # If JSON parsing fails, return the raw text for debugging
                return {
                    "error": "JSON parsing error",
                    "raw_response": response.text
                }
            return result
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
                if "raw_response" in results:
                    with st.expander("Debug Information", expanded=True):
                        st.text("Raw Response:")
                        st.code(results["raw_response"])
            else:
                st.success("Analysis Complete!")
                
                # Display Company Name
                st.header(results.get("company_name", company_name))
                
                # Display Overview
                with st.expander("Company Overview", expanded=True):
                    overview = results.get("overview", "")
                    if "Company Overview:" in overview:
                        overview = overview.split("Company Overview:")[1].split("Recent News:")[0]
                    st.markdown(overview.strip())
                
                # Display News
                with st.expander("Recent News"):
                    news_text = results.get("news", "")
                    if news_text:
                        st.markdown(news_text)
                    else:
                        overview = results.get("overview", "")
                        if "Recent News:" in overview:
                            news = overview.split("Recent News:")[1].split("Investment Analysis:")[0]
                            st.markdown(news.strip())
                        else:
                            st.markdown("No news available")
                
                # Display Investment Analysis
                with st.expander("Investment Analysis"):
                    overview = results.get("overview", "")
                    if "Investment Analysis:" in overview:
                        analysis = overview.split("Investment Analysis:")[1].split("Competitors:")[0]
                        st.markdown(analysis.strip())
                    else:
                        st.markdown("No investment analysis available")
                
                # Display Competitors
                with st.expander("Competitors"):
                    competitors = results.get("competitors", "")
                    if competitors:
                        comp_list = [c.strip() for c in competitors.split('\n') if c.strip() and not c.strip().startswith('-')]
                        for comp in comp_list:
                            st.markdown(f"• {comp}")
                    else:
                        st.markdown("No competitors available")
                
                # Debug
                with st.expander("Debug Information", expanded=False):
                    st.subheader("Raw Response")
                    st.json(results)
                    st.subheader("Response Text")
                    st.code(response.text)
    else:
        st.warning("Please enter both company name and website.")

st.markdown("---")
st.markdown("Built with Streamlit & Make.com")
