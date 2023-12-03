from auth0_component import login_button
import streamlit as st
from dotenv import load_dotenv
import os
import streamlit as st
import openai
from time import time
from datetime import datetime
from dotenv import load_dotenv
import os
from PIL import Image
import pdfplumber
import io



icon = Image.open('logo.png')
st.session_state.sidebar_state = 'expanded'
st.set_page_config(
    page_title=("Athena"),
    page_icon=(icon),
    initial_sidebar_state=st.session_state.sidebar_state
)
hide_st_style = """
            <style>
            #MainMenu {visibility: visable;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
load_dotenv()

clientId = os.environ['Norna_clientid']
domain = os.environ['Norna_domainid']

Forgiving_AI=os.path.join('System_prompts', 'System_grading-Forgiving.md')
harsh_AI=os.path.join('System_prompts', 'System_grading-Harsh.md')
Neutral_AI=os.path.join('System_prompts', 'System_grading-neutral.md')
Combiner=os.path.join('System_prompts', 'System_grading-neutral.md')


def save_file(filepath, content):
    with open(filepath, 'w', encoding='utf-8') as outfile:
        outfile.write(content)
def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as infile:
        return infile.read()
def chatbotGPT4(conversation, model="gpt-4-0613", temperature=0, max_tokens=2000):
    response = openai.ChatCompletion.create(model=model, messages=conversation, temperature=temperature, max_tokens=max_tokens)
    text = response['choices'][0]['message']['content']
    return text, response['usage']['total_tokens']
def chatbotGPT3(conversation, model="gpt-3.5-turbo-16k", temperature=0, max_tokens=2000):
    response = openai.ChatCompletion.create(model=model, messages=conversation, temperature=temperature, max_tokens=max_tokens)
    text = response['choices'][0]['message']['content']
    return text, response['usage']['total_tokens']



def main():

    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")

    # File uploader widget for assessment (text file)
    assessment = st.file_uploader("Upload Assessment (.txt)", type="txt")

    # File uploader widget for guide (PDF file)
    guide = st.file_uploader("Upload Guide (.pdf)", type="pdf", )

    # Check if both assessment and guide are uploaded
    if assessment and guide:
        # Read and decode the assessment text file
        assessment_content = assessment.read().decode()

        # Process the guide PDF file
        guide_bytes = io.BytesIO(guide.read())
        with pdfplumber.open(guide_bytes) as pdf:
            guide_content = ''.join(page.extract_text() for page in pdf.pages if page.extract_text() is not None)

        combined_content = f"Assessment Guidelines:\n{guide_content}\n\n\n Student Submission{assessment_content}"

        # Store both contents in a dictionary in the session state
        st.session_state['Guide-Assessment'] = combined_content
        

    if st.sidebar.button("📜Generate Report📜"):
        current_time = datetime.now().strftime("%S-%M-%H-%d-%m-%y")

        Grading_report_forgiving = [{'role': 'system', 'content': open_file(Forgiving_AI)}, {'role': 'user', 'content': st.session_state.get('Guide-Assessment', '')}]
        report_forgiving, total_tokens = chatbotGPT4(Grading_report_forgiving)

        Grading_report_harsh = [{'role': 'system', 'content': open_file(harsh_AI)}, {'role': 'user', 'content': st.session_state.get('Guide-Assessment', '')}]
        report_harsh, total_tokens = chatbotGPT4(Grading_report_harsh)

        Grading_report_neutral = [{'role': 'system', 'content': open_file(Neutral_AI)}, {'role': 'user', 'content': st.session_state.get('Guide-Assessment', '')}]
        report_neutral, total_tokens = chatbotGPT4(Grading_report_neutral)

        Grading_combined = f"Forgiving Teacher: \n\n{report_forgiving}\n\n\n\ Harsh teacher:\n\n{report_harsh}\n\n\n Neutral Report:\n\n{report_neutral}"

        Grades_Submission = f"{combined_content}\n\n\n\{Grading_combined}"

        st.session_state['combiner'] = Grades_Submission

        Grading_report = [{'role': 'system', 'content': open_file(Combiner)}, {'role': 'user', 'content': st.session_state.get('combiner', '')}]
        report_final, total_tokens = chatbotGPT4(Grading_report)

        Student_report = f"{assessment_content} \n\n\n\{Grading_combined}\n\n\n{report_final}"

        st.sidebar.download_button(
            label="Download Report",
            data=bytes(Student_report, encoding='utf-8'),  # Convert string to bytes
            file_name=f'Grading Report- {current_time}.txt',
            mime="text/plain"
        )
    st.sidebar.write("This will generate The Hypothesis, Clinical Assessment Guide and a list of Referral Recomendations")
    for _ in range(13
    ):  
        st.sidebar.write("")    

# Initialize session states if they don't exist
if 'Norna_logged_in' not in st.session_state:
    st.session_state.Norna_logged_in = False

if 'Norna_user_id' not in st.session_state:
    st.session_state.Norna_user_id = None

# If user is not logged in, show the login button
if not st.session_state.Norna_logged_in:
    user_info = login_button(clientId=clientId, domain=domain)
    if user_info:
        st.session_state.Norna_logged_in = True
        st.session_state.Norna_user_id = user_info.get('sub', None)  # Assuming 'sub' is a unique identifier for the user
        st.experimental_rerun()
        main()
elif st.session_state.Norna_user_id:
    # If user is already logged in, greet them
    main()
