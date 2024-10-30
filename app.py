import streamlit as st
import requests

st.title("AI Research Assistant")

company_name = st.text_input("Company Name:")
company_website = st.text_input("Company Website:")

if st.button("Run Research Analysis"):
    if company_name and company_website:
        try:
            response = requests.post(
                "https://hook.eu2.make.com/wxfp1tgeko8o8odmpx1blpxlhqejut50",
                json={"company_name": company_name, "website": company_website}
            )
            
            # Display raw response for debugging
            st.code(response.text)
            
            # Process response if successful
            if response.status_code == 200:
                text = response.text
                if text:
                    sections = text.split('##')
                    for section in sections:
                        if section.strip():
                            st.markdown(section)
        except Exception as e:
            st.error(f"Error: {str(e)}")
