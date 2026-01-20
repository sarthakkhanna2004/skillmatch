import streamlit as st
from pdfextractor import text_extractor
from langchain_google_genai import ChatGoogleGenerativeAI
import os

# First lets configure the model
gemini_api_key = os.getenv('Google_api_key1')
model = ChatGoogleGenerativeAI(
    model = 'gemini-2.5-flash-lite',
    api_key = gemini_api_key,
    temperature = 0.9
)


# Lets create the sidebar to upload the resume
st.sidebar.title(':red[UPLOAD YOUR RESUME (Only PDF)]')
file = st.sidebar.file_uploader('Resume',type=['pdf'])
if file:
    file_text = text_extractor(file)
    st.sidebar.success('File Uploaded Successfuly')

# Create the name page of the application 

st.title(':orange[SKILLMATCH:-] :rainbow[AI Assisted Skill Match]')
st.markdown(' #### This application will match and analyze your resume and the job description provided')
tips = '''
Follow these steps:-
1. Upload your resume (PDF only) in side bar
2. Copy and paste the job description below
3. Click on submit to run the application'''
st.write(tips)

job_desc= st.text_area(':red[Give your job description over here.]', max_chars=60000)
if st.button("Submit"):
    prompt=f'''
    <Role> You are an expert in analyzing resume and matching it with the job description.
    <Goal> Match the resume and the job description provided by the applicant.
    <Context> The following content has been provided by the applicant:
    * Resume: {file_text}'
    * Job Description: {job_desc}
    <Format> The report should follow these steps:
    * Give a  brief description of the applicant in 3-5 lines.
    * Describe in percentage what are the chances of this resume getting selected.
    * Need not be exact percentage, you can give range of the match. 
    * Give the expected ATS Score along with matching and non matching keywords.
    * Perform SWOT Analysis and explain each parameter, i.e Strength, Weakness, Oppurtunities and Threat.
    * give what all sections in the current resume are required to be changed in the current resume in  order to improve the ATS Score and selection percentage.
    * Show both, current version and improved version of the section.
    * Create 2 sample resume which can maximise the ATS Score

    <Instructions>
    * Use bullet points for explaination whenever possible.
    * Create tables for descriptio where ever required.
    * Strictly do not add any new skill in sample resume.
    * The format of sample resume should be in such a way that they can be copied and pasted directly in word. 
     '''

# Now we create a submit button to run the application


    response = model.invoke(prompt)
    st.write(response.content)

