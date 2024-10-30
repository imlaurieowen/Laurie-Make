import streamlit as st
import requests
import json

def run_research(company_name, website):
    # Replace this with your actual webhook URL from Make.com
    WEBHOOK_URL = "https://hook.eu2.make.com/wxfp1tgeko8o8odmpx1blpxlhqejut50"
    
    try:
        payload = {
            "company_name": company_name,
            "website": website
        }
        
        headers = {
            "Content-Type": "application/json"
        }
        
        # Add debug information
        st.write("Sending request to:", WEBHOOK_URL)
        st.write("Payload:", payload)
        
        response = requests.post(WEBHOOK_URL, json=payload, headers=headers)
        
        # Add response debugging
        st.write("Response Status Code:", response.status_code)
        st.write("Response Headers:", dict(response.headers))
        
        if response.status_code == 200:
            try:
                # Parse the text response
                result_text = response.text
                st.write("Raw Response Text:", result_text)
                
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
                
                # Show debug information when there's an error
                with st.expander("Debug Information", expanded=True):
                    st.write("Company Name:", company_name)
                    st.write("Website:", website)
                    st.write("Error Details:", results["error"])
            else:
            st.success("Analysis Complete!")
                
                # Display Company Name
                st.header(results.get("Company Name", company_name))
                
                # Display Overview
                with st.expander("Company Overview", expanded=True):
                    overview = results.get("Overview", "")
                    if overview:
                        # Split by sections
                        sections = overview.split("##")
                        for section in sections:
                            if section.strip():
                                st.markdown(f"## {section.strip()}")
                
                # Display Competitors as a clean list
                with st.expander("Competitors"):
                    competitors = results.get("Competitors", "")
                    if isinstance(competitors, list):
                        for comp in competitors:
                            st.markdown(f"• {comp.strip()}")
                    else:
                        st.markdown(competitors)
                
                # Display Investment Analysis
                with st.expander("Investment Analysis"):
                    analysis = results.get("Investment Analysis", "")
                    if analysis:
                        st.markdown(analysis)
                
                # Debug Information
                with st.expander("Debug Information", expanded=False):
                    st.subheader("Raw Response")
                    st.json(results)
    else:
        st.warning("Please enter both company name and website.")

st.markdown("---")
st.markdown("Built with Streamlit & Make.com")
