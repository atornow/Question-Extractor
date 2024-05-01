import json
import re
import docx
import PyPDF2

def extract_text_from_docx(file_path):
    doc = docx.Document(file_path)
    text = []
    for paragraph in doc.paragraphs:
        text.append(paragraph.text)
    return '\n'.join(text)

def extract_text_from_pdf(file_path):
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfFileReader(file)
        text = []
        for page in range(reader.numPages):
            text.append(reader.getPage(page).extractText())
    return '\n'.join(text)
def extract_text(file_path):
    if file_path.endswith('.doc') or file_path.endswith('.docx'):
        return extract_text_from_docx(file_path)
    elif file_path.endswith('.pdf'):
        return extract_text_from_pdf(file_path)
    else:
        raise ValueError('Unsupported file format')
    
def extract_questions(text):
    questions = []
    lines = text.split('\n')
    current_question = None
    
    for line in lines:
        line = line.strip()
        
        if re.match(r'^\d+[.)]', line):
            if current_question:
                questions.append(current_question)
            current_question = {
                'question': line,
                'options': [],
                'answer_format': '',
                'location': ''
            }
        elif current_question:
            if re.match(r'^[a-z][.)]', line):
                current_question['options'].append(line)
            elif re.search(r'\([^)]+\)', line):
                current_question['answer_format'] = re.search(r'\(([^)]+)\)', line).group(1)
            else:
                current_question['question'] += ' ' + line
    
    if current_question:
        questions.append(current_question)
    
    return questions
