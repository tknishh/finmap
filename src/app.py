import streamlit as st
from utils import load_context_data
from model import get_response
import os
import dotenv

dotenv.load_dotenv()
API_KEY = os.getenv('OPENAI_API_KEY')

def main():
    st.title('Finmap')
    st.subheader('Your Financial Companion')

    # Load context data
    context_data = load_context_data('data')

    st.sidebar.title("User Input")
    user_input = st.sidebar.text_input("Enter your financial query:")
    
    uploaded_cibil_report = st.sidebar.file_uploader("Upload your CIBIL report", type=['pdf'])
    if uploaded_cibil_report is not None:
        st.sidebar.write("CIBIL report uploaded")

    if st.sidebar.button('Get Response'):
        if user_input or uploaded_cibil_report:
            try:
                if uploaded_cibil_report:
                    cibil_report_path = os.path.join("uploads", uploaded_cibil_report.name)
                    with open(cibil_report_path, "wb") as f:
                        f.write(uploaded_cibil_report.getbuffer())
                else:
                    cibil_report_path = None

                response = get_response(user_input, context_data, cibil_report_path, API_KEY)
                if response:
                    st.success("Response received!")
                    st.write(response)
                else:
                    st.error("No relevant information found.")
            except Exception as e:
                st.error(f"An error occurred: {str(e)} - {type(e).__name__}")
        else:
            st.error("Please enter a query or upload a CIBIL report to get a response.")

if __name__ == "__main__":
    main()
