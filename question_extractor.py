import json
import re
import docx
import PyPDF2
import sys

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
    question_pattern = re.compile(
        r'^(?:\d+[\).]|[a-zA-Z][\).]|[IVX]+[\).]|#)\s+(.+(?:\n(?!\s*(?:[a-z][\).]|(?:Yes|No|N/A))).+)*)$', re.M)
    option_pattern = re.compile(r'^[a-z][\).]\s+(.+)$')

    for line in lines:
        line = line.strip()
        question_match = question_pattern.match(line)
        option_match = option_pattern.match(line)

        if question_match:
            if current_question:
                questions.append(current_question)
            question_text = question_match.group(1).replace('\n', ' ').strip()
            current_question = {
                'question': question_text,
                'options': [],
                'answer_format': '',
                'location': ''
            }
        elif option_match:
            if current_question:
                current_question['options'].append(option_match.group(1))
        elif current_question:
            if re.search(r'\([^)]+\)', line):
                current_question['answer_format'] = re.search(r'\(([^)]+)\)', line).group(1)
            else:
                current_question['question'] += ' ' + line.strip()

    if current_question:
        questions.append(current_question)

    return questions


def main(file_path):
    print(f"Processing file: {file_path}")
    try:
        text = extract_text(file_path)
    except Exception as e:
        print(f"Error extracting text: {str(e)}")
        return
    try:
        text = extract_text(file_path)
        questions = extract_questions(text)
        output = json.dumps(questions, indent=2)
        print(output)
    except Exception as e:
        print(f'Error: {str(e)}')

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python question_extractor.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    main(file_path)
