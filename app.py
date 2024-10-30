import streamlit as st
import requests

st.title("AI Research Assistant")

with st.form(key='input_form'):
    company_name = st.text_input("Company Name:")
    company_website = st.text_input("Company Website:")
    submit_button = st.form_submit_button(label='Run Research Analysis')

if submit_button:
    if company_name and company_website:
        with st.spinner('Running analysis...'):
            try:
                response = requests.post(
                    "https://hook.eu2.make.com/wxfp1tgeko8o8odmpx1blpxlhqejut50",
                    json={"company_name": company_name, "company_website": company_website},
                    headers={"Content-Type": "application/json"}
                )
                response.raise_for_status()
                
                result = response.json()
                if 'content' in result:
                    st.success("Analysis Complete!")
                    sections = result['content'].split('##')
                    
                    for section in sections:
                        if section.strip():
                            title, *content = section.split('\n', 1)
                            st.subheader(title.strip(':'))
                            if content:
                                st.write(content[0].strip())
            except Exception as e:
                st.error(f"Error: {str(e)}")
    else:
        st.warning("Please enter both Company Name and Website.")
