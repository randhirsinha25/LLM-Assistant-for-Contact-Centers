import streamlit as st
from data_processing import prepare_data_text, prepare_data_audio,prepare_data
import os
from pathlib import Path
# Set the title of the app
st.title("LLM Assistant for Contact Centers")
# Set upload directory
UPLOAD_DIR = "uploaded_files"
Path(UPLOAD_DIR).mkdir(exist_ok=True)
def data_clean(processed_text):
    line_count = processed_text.count('\n') + 1  # Add 1 to count the last line if no \n
    line_height = 20  # Approximate height in pixels per line
    
    # Cap the height to avoid overgrowth
    max_height = 1000
    min_height = 300
    
    # Final calculated height
    dynamic_height = min(max_height, max(min_height, line_count * line_height))
    
    # Display text area
    st.text_area("Output", value=processed_text, height=dynamic_height)
def download():
        # Path to your file
    file_path = "reply_recordings.xlsx"
    
    # Read file content
    with open(file_path, "rb") as f:
        file_bytes = f.read()
    
    # Create download button
    st.download_button(
        label="Download File",
        data=file_bytes,
        file_name="reply_recordings.xlsx",  # name the file for download
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"      # set appropriate MIME type
    )
with st.sidebar:
    # Sidebar panel
    st.sidebar.header("Options Panel")

    # Dropdown in sidebar
    option = st.sidebar.selectbox(
        "User Input Type",
        ("Audio", "CSV", "User Input")
    )
    if option in  ("Audio",  "User Input"):
        option2 = st.sidebar.selectbox(
            "Type of Voice",
            (  "Complaint", "Technical Issue", "Compliment", "Order Placement","Product Inquiry")
        )

    # Display the selectedoption in main area
   
    
    # File uploader based on selection
    if option == "Audio":
        uploaded_file = st.file_uploader("Upload an audio file", type=["mp3", "wav", "ogg"])
    elif option == "CSV":
        uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
    else:
        uploaded_file = None  # No uploader for 'User Input'


# Show a text input box if "User Input" is selected
if option == "User Input":
    user_text = st.text_input("Enter your text below:")
    if user_text:
        processed_text = f"You entered: {user_text}"  # Replace this with your own processing logic
        # st.write("You entered:", user_text,option,option2)
        processed_text = prepare_data_text(user_text,option2)
        # Calculate number of lines (rough approximation)
                # Calculate number of lines (rough approximation)
        data_clean(processed_text)
        
        # Add a submit button
if st.button("Submit"):
    if uploaded_file is not None:
        file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
        
        # Save the uploaded file to the upload directory
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        if option=="Audio":
            # If a file is uploaded, play it
            if uploaded_file is not None:
                st.audio(uploaded_file, format='audio/mp3')  # Use correct format (mp3, wav, etc.)
            processed_text,transcript= prepare_data_audio(file_path,option2)
            processed_text = f"Transcript :\n {transcript}\n\n AI Reply: \n{processed_text}"
            data_clean(processed_text)
            st.success(f"File saved at: {file_path}")
            st.write(f"✅ Uploaded file path: `{file_path}`")
        elif option=="CSV":
            prepare_data(file_path)
            download()
            st.success(f"File saved at: {file_path}")
            st.write(f"✅ Uploaded file path: `{file_path}`")
    elif option == "User Input" and user_text:
        st.success("Text input submitted successfully.")
        data_clean(processed_text)
    else:
        st.warning("Please upload a file or enter text before submitting.")
       