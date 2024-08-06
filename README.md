Here's a comprehensive README file for your chatbot project:

---

# PDF Chatbot with Summary and Question Answering

## Overview
This project is a Flask-based web application that allows users to upload PDF files, receive a summary of the content, and ask questions about the document. The application utilizes NLP models to provide accurate summaries and answers.

## Features
- **PDF Upload**: Upload any PDF file to the application.
- **Text Extraction**: Extracts text content from the uploaded PDF.
- **Summarization**: Generates a concise summary of the extracted text.
- **Question Answering**: Allows users to ask questions about the PDF content and receive relevant answers.
- **Flask Frontend**: User-friendly web interface for interaction.

## Tech Stack
- **Backend**: Python, Flask
- **NLP Models**: Transformers, PyMuPDF (for PDF processing)
- **Frontend**: HTML, CSS (integrated with Flask templates)

## Installation
1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/pdf-chatbot.git
   cd pdf-chatbot
   ```

2. **Create a virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access the application**
   Open your browser and navigate to `http://127.0.0.1:5000`.

## Usage
1. **Upload PDF**: On the home page, upload your PDF file.
2. **View Summary**: Once uploaded, the application will display a summary of the PDF content.
3. **Ask Questions**: Use the provided input box to ask any question related to the PDF. The system will return an answer based on the content.

## File Structure
- `app.py`: Main application file.
- `templates/`: Folder containing HTML templates.
  - `index.html`: Main template for the web interface.
- `static/`: Folder for static files like CSS.
- `requirements.txt`: List of dependencies.

## Project Components
### PDFProcessor
Extracts text from the uploaded PDF using PyMuPDF.

### TextSummarizer
Generates a summary of the extracted text using a summarization pipeline from Hugging Face Transformers.

### QuestionAnswering
Handles question answering using a pre-trained question-answering model from Hugging Face Transformers.

### Flask Routes
- `/`: Renders the main page for file upload.
- `/upload`: Handles the PDF file upload and returns the summary.
- `/answer`: Takes a question and returns an answer based on the PDF content.

## Example
### app.py
```python
import fitz  # PyMuPDF
from transformers import pipeline
from flask import Flask, request, render_template, jsonify

class PDFProcessor:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.text = self.extract_text()

    def extract_text(self):
        doc = fitz.open(self.pdf_path)
        text = ""
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text += page.get_text()
        return text

class TextSummarizer:
    def __init__(self, text):
        self.text = text
        self.summarizer = pipeline("summarization")

    def summarize(self, max_length=150, min_length=50):
        summary = self.summarizer(self.text, max_length=max_length, min_length=min_length, do_sample=False)
        return summary[0]['summary_text']

class QuestionAnswering:
    def __init__(self, text):
        self.text = text
        self.qa_pipeline = pipeline("question-answering")

    def answer_question(self, question):
        answer = self.qa_pipeline(question=question, context=self.text)
        return answer['answer']

class PDFSummaryQA:
    def __init__(self, pdf_path):
        self.pdf_processor = PDFProcessor(pdf_path)
        self.text = self.pdf_processor.text
        self.summarizer = TextSummarizer(self.text)
        self.qa = QuestionAnswering(self.text)

    def get_summary(self):
        return self.summarizer.summarize()

    def get_answer(self, question):
        return self.qa.answer_question(question)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    if file:
        file_path = file.filename
        file.save(file_path)
        pdf_summary_qa = PDFSummaryQA(file_path)
        summary = pdf_summary_qa.get_summary()
        return jsonify({'summary': summary, 'pdf_path': file_path})

@app.route('/answer', methods=['POST'])
def answer():
    data = request.get_json()
    pdf_path = data['pdf_path']
    question = data['question']
    pdf_summary_qa = PDFSummaryQA(pdf_path)
    answer = pdf_summary_qa.get_answer(question)
    return jsonify({'answer': answer})

if __name__ == "__main__":
    app.run(debug=True)
```

## Contributing
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -am 'Add new feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Open a Pull Request.

## License
This project is licensed under the MIT License.

## Contact
**Mohit Sharma**
- [LinkedIn](https://www.linkedin.com/in/mohitsharmams/)
- [GitHub](https://github.com/Mohitsholey04/)
- [Portfolio](https://mohitdev.tech/)

---

This README provides an overview, installation instructions, usage details, and information about the project structure and components.
