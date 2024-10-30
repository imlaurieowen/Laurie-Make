import streamlit as st
import requests

# Streamlit App
st.title("AI Research Assistant")

# Form for User Input
with st.form(key='input_form'):
    company_name = st.text_input("Company Name:")
    company_website = st.text_input("Company Website:")
    submit_button = st.form_submit_button(label='Run Research Analysis')

# Function to send data to Make webhook
def send_to_make_webhook(company_name, company_website):
    webhook_url = "https://hook.eu2.make.com/wxfp1tgeko8o8odmpx1blpxlhqejut50"
    payload = {
        "company_name": company_name,
        "company_website": company_website
    }
    try:
        response = requests.post(webhook_url, json=payload)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None

# When form is submitted
if submit_button:
    if company_name and company_website:
        with st.spinner('Running analysis...'):
            response = send_to_make_webhook(company_name, company_website)
            
            if response and 'text' in response:
                st.success("Analysis Complete!")
                
                # Split the text into sections and display
                text = response['text']
                sections = text.split('##')
                
                for section in sections:
                    if section.strip():
                        # Get the section title and content
                        parts = section.strip().split('\n', 1)
                        if len(parts) > 1:
                            title = parts[0].strip(':')
                            content = parts[1].strip()
                            
                            # Display each section
                            st.subheader(title)
                            st.write(content)
    else:
        st.warning("Please enter both Company Name and Website.")
