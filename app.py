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
                result_text = response.text
                try:
                    result = json.loads(result_text)
                except json.JSONDecodeError:
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

# Custom CSS for better formatting
st.markdown("""
    <style>
    .header-text {
        color: #1E88E5;
        font-size: 20px;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .section-text {
        font-size: 16px;
        line-height: 1.6;
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

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
                
                # Company Overview Section
                with st.expander("Company Overview", expanded=True):
                    if "Overview" in results:
                        sections = results["Overview"].split("\n\n")
                        for section in sections:
                            if section.strip():
                                if ":" in section:
                                    title, content = section.split(":", 1)
                                    st.markdown(f"**{title.strip()}:**")
                                    st.markdown(content.strip())
                                else:
                                    st.markdown(section.strip())
                
                # Recent News Section
                with st.expander("Recent News"):
                    if "Recent News" in results["Overview"]:
                        news_section = results["Overview"].split("Recent News:")[1].split("Investment Analysis:")[0]
                        st.markdown(news_section.strip())
                
                # Investment Analysis Section
                with st.expander("Investment Analysis"):
                    if "Investment Analysis" in results["Overview"]:
                        analysis_section = results["Overview"].split("Investment Analysis:")[1]
                        st.markdown(analysis_section.strip())
                
                # Competitors Section
                with st.expander("Competitors"):
                    if "Competitors" in results:
                        competitors = results["Competitors"]
                        # Clean up and format competitors list
                        if isinstance(competitors, str):
                            competitor_list = competitors.split(",")
                            for competitor in competitor_list:
                                st.markdown(f"• {competitor.strip()}")
                
                # Debug Information (hidden by default)
                with st.expander("Debug Information", expanded=False):
                    st.subheader("Raw Response")
                    st.code(str(results))

    else:
        st.warning("Please enter both company name and website.")

st.markdown("---")
st.markdown("Built with Streamlit & Make.com")
