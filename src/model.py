import openai
import PyPDF2

def extract_text_from_pdf(pdf_path):
    """
    Extract text from a PDF file.

    Parameters:
    pdf_path (str): The path to the PDF file.

    Returns:
    str: The extracted text from the PDF file.
    """
    text = ""
    try:
        with open(pdf_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            for page_num in range(len(reader.pages)):
                text += reader.pages[page_num].extract_text()
    except Exception as e:
        print(f"Error extracting text from PDF: {str(e)}")
    return text

def get_response(user_input, context_data, cibil_report_path, api_key):
    """
    Generate a response based on user input, context data, and optionally the CIBIL report.

    Parameters:
    user_input (str): The user's query or input.
    context_data (str): The context data loaded from files.
    cibil_report_path (str): The path to the uploaded CIBIL report, if any.
    api_key (str): The API key for the OpenAI GPT model.

    Returns:
    str: The generated response.
    """
    openai.api_key = api_key

    # Extract text from the CIBIL report if provided
    cibil_report_text = ""
    if cibil_report_path:
        cibil_report_text = extract_text_from_pdf(cibil_report_path)

    # Combine user input, context data, and CIBIL report text
    prompt = f"Context: {context_data}\n\nCIBIL Report: {cibil_report_text}\n\nUser Input: {user_input}\n\nResponse: should be in format "

    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that helps a user by providing them best financial suggestions based on their cibil report."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    
    except Exception as e:
        print(f"Error generating response: {str(e)}")
        return None
