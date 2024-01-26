# Convert CVs to ZirconTech format

## Overview

This Python script provides a comprehensive solution for processing resumes (CVs) using various libraries and APIs. The script includes functionality to extract text from different file formats, convert Markdown to PDF, and employ AI agents to transcribe and edit CVs.

## Features

- **File Format Support**: Extracts text from `.txt`, `.pdf`, and `.docx` files.
- **Markdown to PDF Conversion**: Converts Markdown text to a styled PDF document.
- **AI-Powered Processing**: Utilizes Crew AI for transcribing and editing CVs with predefined roles and goals.

## Dependencies

- `os`
- `docx`
- `PyPDF2`
- `langchain`
- `crewai`
- `dotenv`
- `markdown`
- `pdfkit`
- `weasyprint`
- `datetime`

## Setup and Configuration

### Prerequisites

- Python 3.6 or later.
- Install required Python packages: 
    ```bash
    pip install python-docx PyPDF2 langchain crewai python-dotenv markdown pdfkit weasyprint
    ```

### Environment Variables

- An OpenAI API key is required. Set it in a `.env` file in the project directory.
    ```
    OPENAI_API_KEY=your_openai_api_key_here
    LOGO_URL='url to logo'
  
  ```

### File and Folder Structure

- Place the `.env` file in the root directory.
- Create a directory named `output` for the PDFs generated.
- Create a directory named `cvs_to_convert` for CV files to be processed.

## Usage

1. **Environment Setup**: Load environment variables, particularly the OpenAI API key.
   
2. **Markdown to PDF Function**: 
   - Converts Markdown text to HTML.
   - Adds a logo and current date to the document.
   - Saves the output as a PDF in the `output` folder.

3. **ReaderTool Class**: 
   - Defines a method to extract text from `.txt`, `.pdf`, and `.docx` files.
   - Handles different file formats and outputs the extracted text.

4. **Crew AI Agents**:
   - `cv_transcriber`: An agent designed to transcribe CVs.
   - `cv_editor`: An agent tasked with editing the transcribed CVs for redundancies and clarity.

5. **Tasks**:
   - Define tasks for transcribing and editing CVs.
   - Utilize the agents and process the text in Markdown format.

6. **Crew Initialization**:
   - Instantiate a crew of agents.
   - Define the process as sequential, where each task's output is passed to the next.

7. **Execution**: 
   - Kick off the crew process.
   - The result is printed and converted to a PDF file.

8. **Output**: 
   - The processed CV is saved as a PDF in the `output` folder.

## Notes

- The script assumes the presence of certain directories (`output`, `cvs_to_convert`).
- The API key and file paths must be correctly set for the script to work.
- The script can be modified to accommodate different file paths or additional functionalities as needed.

## License

MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.