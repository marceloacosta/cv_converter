import os
from docx import Document
from PyPDF2 import PdfReader
from langchain.agents import load_tools
from langchain.tools import tool
from crewai import Agent, Task, Process, Crew
from dotenv import load_dotenv, find_dotenv
from langchain_openai import ChatOpenAI
import markdown
import pdfkit
from weasyprint import HTML, CSS
import datetime
from datetime import date
import os
from dotenv import load_dotenv, find_dotenv

# Load environment variable
_ = load_dotenv(find_dotenv())
openai_api_key = os.environ.get("OPENAI_API_KEY")


def markdown_to_pdf(markdown_text, output_filename):
    # Convert Markdown to HTML
    html = markdown.markdown(markdown_text)
    
    # Get the logo URL from the .env file
    logo_url = os.environ.get("LOGO_URL")
    
    # Add the logo at the beginning and align it to the right
    html = f'<div style="text-align: right;"><img src="{logo_url}" alt="Logo" width="50px" style="width: 30%;"></div>\n{html}'
    
    # Get the current date
    current_date = date.today().strftime('%B %d, %Y')

    # Add a CSS style to use a specific font
    css = CSS(string=f"""
    body {{
        font-family: 'Arial';
    }}
    @page {{
        @bottom-right {{
            content: "Date: {current_date}";
        }}
    }}
    """)
    # Create the output folder if it doesn't exist
    output_folder = 'output'
    os.makedirs(output_folder, exist_ok=True)
    print(f"Output folder: {output_folder}")

    # Set the output file path
    output_path = os.path.join(output_folder, output_filename)
    print(f"Output path: {output_path}")

    # Convert HTML to PDF and save to the output folder
    HTML(string=html).write_pdf(output_path, stylesheets=[css])
    print("PDF generated successfully.")

    # Read the created PDF and return its binary content
    with open(output_path, 'rb') as file:
        pdf_data = file.read()
    return pdf_data

def handle_exception(e):
    print(f"Error in markdown_to_pdf: {e}")

try:
    # Code that may raise an exception
    pass
except Exception as e:
    handle_exception(e)



class ReaderTool:
    @tool("Gets text from CV")
    def extract_text_from_file(file_path):
        """This is used to extract text from .txt, pdf or docx files"""
        file_path = uploaded_file.name
        _, file_extension = os.path.splitext(file_path)
        cv_text = ""

        if file_extension == ".txt":
            with uploaded_file as file:
                    cv_text = file.read()
        elif file_extension == ".docx":
            doc = Document(file_path)
            for para in doc.paragraphs:
                print(f"Paragraph: {para.text}")  # Add this line
                cv_text += para.text
        elif file_path.endswith(".pdf"):
            pdf_file_obj = uploaded_file
            pdf_reader = PdfReader(pdf_file_obj)
            num_pages = len(pdf_reader.pages)
            for page in pdf_reader.pages:
                cv_text += page.extract_text()
            pdf_file_obj.close()
        else:
            print("Unsupported file type")

        return cv_text
    
           

# To load Human in the loop
human_tools = load_tools(["human"])


cv_transcriber = Agent(
    role="Senior Researcher",
    goal=f"Find and explore all the relevant sections and information in the CV in the collected CV text",
    backstory=f"""You are an Expert recruiter who can find the most relevant information in a CV.
    """,
    verbose=True,
    allow_delegation=False,
    tools=[ReaderTool().extract_text_from_file],
    llm = ChatOpenAI(model= "gpt-4", temperature=0),   
)

cv_editor = Agent(
    role="Senior Editor",
    goal=f"Find and explore the resulting CV and eliminate all redundancies and sections or subsections where information is empty or not specified",
    backstory=f"""You are an Expert Editor who can review and correct any CV and leave it without redundancies not parts where information is not specific or empty.
    """,
    verbose=True,
    allow_delegation=False,
    llm = ChatOpenAI(model= "gpt-4", temperature=0),   
)



task_write_cv = Task(
    description=f"""Use the text extracted from the CV text and write comprehensive personal information, job experience and education sections. Make sure you include all job experiences and education details.
    For your Outputs use the following markdown format (If any of the requested information can not be found or it is Not Specified don't include that subsection. Do not invent, guess or assume any information.):
    If Skill level is not specified, leave it empty. If any of the requested information can not be found or it is Not Specified don't include that subsection. Do not invent, guess or assume any information.

    # [Name]
    - **Email:** [Email]
    - **Phone:** [Phone number]
    - **Address:** [Address]
    - **Linkedin:** [LinkedIn profile]
    - **Github:** [Github profile]
    - **Personal website:**[Personal website]
    # About me
    <div style="text-align: justify"> 
    - [Description of yourself]
    </div>
    # Job experience
    ## [Company name]
    ### [Position] 
    - Duration
    - Location
    ##[Responsibilities]
    <div style="text-align: justify"> 
    - Description of responsibilities
    - Description of achievements in that position
    - Description of technologies, stack or skills used in that position
    </div>

    # Education
    ## [Institution name]
    ### [Degree] 
    - Duration
    - Location
    ##[Description]
    - Description of degree
    # Additional information
    ## Languages
    - [Languages] [Skill level]
    ## Skills
    - [Programming languages] [Skill level]
    - [Technologies] 
    - [Other skills]  
   
   
    """,
    agent=cv_transcriber,
)


task_edit_cv = Task(
    description=f"""Use the resulting CV markdown text and Find and explore the resulting CV. Carefully review each section and subsection and eliminate all redundancies and sections or subsections where information is empty or not specified.
    For your Outputs use the following markdown format below (include sections only whenever applicable):
    Do not include in your output any commentary or notes. Only include the CV text in markdown format.
    If Skill level is not specified, leave it empty. If any of the requested information can not be found or it is Not Specified don't include that subsection. Do not invent, guess or assume any information.
    # [Name]
    - **Email:** [Email]
    - **Phone:** [Phone number]
    - **Address:** [Address]
    - **Linkedin:** [LinkedIn profile]
    - **Github:** [Github profile]
    - **Personal website:**[Personal website]
    # About me
    <div style="text-align: justify"> 
    - [Description of yourself]
    </div>
    # Job experience
    ## [Company name]
    ### [Position] 
    - Duration
    - Location
    ##[Responsibilities]
    <div style="text-align: justify"> 
    - Description of responsibilities
    - Description of achievements in that position
    - Description of technologies, stack or skills used in that position
    </div>

    # Education
    ## [Institution name]
    ### [Degree] 
    - Duration
    - Location
    ##[Description]
    - Description of degree
    # Additional information
    ## Languages
    - [Languages] [Skill level]
    ## Skills
    - [Programming languages] [Skill level]
    - [Technologies] 
    - [Other skills] 
   

   
    """,
    agent= cv_editor,
)





# instantiate crew of agents
crew = Crew(
    agents=[cv_transcriber, cv_editor],
    tasks=[task_write_cv, task_edit_cv],
    verbose=2,
    process=Process.sequential,  # Sequential process will have tasks executed one after the other and the outcome of the previous one is passed as extra content into this next.
)

import streamlit as st

# Function to handle PDF download
def handle_pdf_download():
    if 'result' in st.session_state and st.session_state['result']:
        # Generate PDF from Markdown
        pdf_data = markdown_to_pdf(st.session_state['result'], 'output.pdf')
        if pdf_data:
            st.download_button(label="Download PDF", data=pdf_data, file_name='output.pdf', mime='application/pdf')
        else:
            st.error("Error in generating PDF file.")
    else:
        st.error("No data to generate PDF.")

# Function to generate PDF from edited markdown
def generate_and_download_pdf(edited_markdown, filename):
    pdf_data = markdown_to_pdf(edited_markdown, filename)
    if pdf_data:
        print("PDF data generated successfully.")
        return pdf_data
    else:
        print("Failed to generate PDF data.")
        return None

# Display a text area for editing the markdown
if 'result' in st.session_state and st.session_state['result']:
    edited_markdown = st.text_area('Edit the markdown here:', value=st.session_state['result'], height=300)

    # Combined button for generating and downloading the PDF
    if st.button('Save'):
        pdf_data = generate_and_download_pdf(edited_markdown, 'edited_output.pdf')
        if pdf_data:
            st.download_button(label="Download Edited PDF", data=pdf_data, file_name='edited_output.pdf', mime='application/pdf')
        else:
            st.error("Error in generating PDF file.")








# Initialize session state variables
if 'uploaded_file' not in st.session_state:
    st.session_state['uploaded_file'] = None
if 'result' not in st.session_state:
    st.session_state['result'] = None

st.title('CV Format Standardizer')

# File uploader
uploaded_file = st.file_uploader("Choose a file", type=['txt', 'pdf', 'docx'])
if uploaded_file is not None:
    st.session_state['uploaded_file'] = uploaded_file

# Process button
if st.button('Process') and st.session_state['uploaded_file'] is not None:
    st.session_state['result'] = crew.kickoff()
    st.write(st.session_state['result'])
    st.markdown(st.session_state['result'])

  # Direct Download PDF button
    if 'result' in st.session_state and st.session_state['result']:
        pdf_data = markdown_to_pdf(st.session_state['result'], 'output.pdf')
        if pdf_data:
            st.download_button(label="Download PDF", data=pdf_data, file_name='output.pdf', mime='application/pdf')