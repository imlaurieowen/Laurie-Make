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
                json={
                    "company_name": company_name, 
                    "website": company_website
                }
            )
            
            # Process the text response directly
            text = response.text
            sections = text.split('##')
            
            for section in sections:
                if section.strip():
                    # Get title and content
                    parts = section.split('\n', 1)
                    if len(parts) > 1:
                        title = parts[0].strip()
                        content = parts[1].strip()
                        # Display
                        st.subheader(title)
                        st.write(content)
                        
        except Exception as e:
            st.error(f"Error: {str(e)}")
            st.code(response.text)  # Show raw response for debugging
    else:
        st.warning("Please enter both Company Name and Website.")
