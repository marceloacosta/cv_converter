# CV Format Standardizer

## Overview

CV Format Standardizer is an application designed for organizations receiving CVs in various formats, aiming to standardize them into a specified, branded format. This tool streamlines the process of formatting resumes, ensuring consistency and professionalism in the presentation of applicant information.

## Features

- **Multiple File Format Support:** Handles `.txt`, `.pdf`, and `.docx` files, extracting text for processing.
- **Automated CV Transcription and Editing:** Utilizes AI agents for transcribing and refining CV content.
- **Custom Branding:** Integrates company logo and standardized formatting in the final output.
- **PDF Generation:** Converts standardized CV content into a professional PDF format.
- **Interactive Web Interface:** Built with Streamlit, providing an easy-to-use platform for file uploads and downloads.

## Installation

### Prerequisites

Before running this project, you need to have `wkhtmltopdf` installed on your system as it's required by the `pdfkit` library to convert HTML to PDF.

#### Installation Instructions

- **Linux (Debian/Ubuntu):**

  ```bash
  sudo apt-get install wkhtmltopdf
  ```

To set up CV Format Standardizer, follow these steps:

1. **Clone the Repository:**
   ```bash
   git clone [repository-link]
   ```
2. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

   This will install necessary libraries such as `docx`, `PyPDF2`, `streamlit`, and others.

3. **Set Environment Variables:**
   Create a `.env` file in the root directory and add the following keys:
   ```
   OPENAI_API_KEY=[Your OpenAI API Key]
   LOGO_URL=[URL of your company logo]
   ```
   Replace the placeholders with your actual API key and logo URL.

## Usage

To run the application:

1. Start the Streamlit server:
   ```bash
   streamlit run app.py
   ```
2. Navigate to the displayed URL in your web browser.
3. Upload a CV in one of the supported formats.
4. Click 'Process' to standardize the format and view the result.
5. Optionally, edit the markdown content and download the standardized CV as a PDF.

## How it Works

- **File Upload:** Users upload a CV, which the system reads and processes.
- **Text Extraction:** The `ReaderTool` class extracts text from the uploaded file.
- **AI-Driven Processing:** AI agents (`cv_transcriber` and `cv_editor`) analyze and edit the CV content, ensuring relevance and conciseness.
- **Markdown to PDF Conversion:** The application converts the final markdown content into a stylized PDF, incorporating the company logo and date.
  **Note:** The file can be manually edited onscreen and downloaded if a human deems necessary to make any correction or addition.

## Make it fly!

Deploy to [fly.io](https://fly.io)!

### Build the docker image (optional)

`docker build -t cv-converter .`

### Set the app secrets

`fly secrets set OPENAI_API_KEY='sk-your-key-here'`

### Deploy the app

`fly deploy`

## Contributing

Contributions to CV Format Standardizer are welcome. Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Submit a pull request with a clear description of your changes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For support or queries, please contact [contact-email].

---

**Note:** This README is a guide for setting up and using the CV Format Standardizer. Modify it as necessary to match the specifics of your repository and project structure.
