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
                    if "Analysis" in result:
                        # If we have nested JSON in Analysis, parse it
                        result = json.loads(result["Analysis"])
                except json.JSONDecodeError:
                    # If it's not JSON, treat it as text
                    result = {
                        "Company Name": company_name,
                        "Overview": result_text
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
                        # Try to clean up the markdown
                        sections = overview.split("##")
                        for section in sections:
                            if section.strip():
                                if "Company Name:" not in section and "Company Overview:" not in section:
                                    st.markdown(section.strip())
                                else:
                                    # Remove the header if it's the main sections
                                    content = section.split(":", 1)
                                    if len(content) > 1:
                                        st.markdown(content[1].strip())
                
                # Display Recent News
                with st.expander("Recent News"):
                    if "Recent News:" in overview:
                        news = overview.split("Recent News:")[1].split("Investment Analysis:")[0]
                        st.markdown(news.strip())
                    elif "News" in results:
                        st.markdown(results["News"])
                    else:
                        st.markdown("No recent news available")
                
                # Display Investment Analysis
                with st.expander("Investment Analysis"):
                    if "Investment Analysis:" in overview:
                        analysis = overview.split("Investment Analysis:")[1].split("Competitors:")[0]
                        st.markdown(analysis.strip())
                    else:
                        st.markdown("No investment analysis available")
                
                # Display Competitors
                with st.expander("Competitors"):
                    competitors = results.get("Competitors", "")
                    if competitors:
                        # Clean up competitors text
                        comp_lines = competitors.replace("-", "•").split("\n")
                        for line in comp_lines:
                            if line.strip() and not line.strip().startswith("Competitors:"):
                                st.markdown(line.strip())
                    else:
                        st.markdown("No competitors information available")
                
                # Debug Information
                with st.expander("Debug Information", expanded=False):
                    st.subheader("Raw Response")
                    st.json(results)
                    st.subheader("Original Response Text")
                    st.code(response.text)
    else:
        st.warning("Please enter both company name and website.")

st.markdown("---")
st.markdown("Built with Streamlit & Make.com")
