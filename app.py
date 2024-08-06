import fitz  # PyMuPDF
from transformers import pipeline, TFGPT2LMHeadModel, GPT2Tokenizer
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
