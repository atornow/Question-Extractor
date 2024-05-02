import docx
from pypdf import PdfReader
import sys
import os
import anthropic
from dotenv import load_dotenv
import csv

load_dotenv(os.path.join(os.path.dirname(__file__), 'main.env'))

api_key = os.environ.get('ANTHROPIC_API_KEY')
client = anthropic.Anthropic(api_key=api_key)

def extract_text_from_docx(file_path):
    doc = docx.Document(file_path)
    text = []
    for paragraph in doc.paragraphs:
        text.append(paragraph.text)
    return '\n'.join(text)

def extract_text_from_pdf(file_path):
    with open(file_path, 'rb') as file:
        reader = PdfReader(file)
        number_of_pages = len(reader.pages)
        text = ''.join([page.extract_text() for page in reader.pages])
        print(text)
        return text

def extract_text(file_path):
    if file_path.endswith('.doc') or file_path.endswith('.docx'):
        return extract_text_from_docx(file_path)
    elif file_path.endswith('.pdf'):
        return extract_text_from_pdf(file_path)
    else:
        raise ValueError('Unsupported file format')


def main(file_path):
    print(f"Processing file: {file_path}")
    try:
        text = extract_text(file_path)
    except Exception as e:
        print(f"Error extracting text: {str(e)}")
        return

    try:
        message = client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=2500,
            temperature=0,
            system="You are an AI assistant made to extract questions and answer options from documents. Your task is to process the user-provided text and output a CSV file containing all identified questions, output should include ONLY the CSV itself.\nFor each question, include the following columns in the CSV output:\n\nQuestion Text (with any commas or special characters escaped)\nQuestion Number (assign a default of '-' if missing)\nIs Multiple Choice (1) or Is Open Response (0)\nAnswer Options (a single CSV column containing options separated by '/', blank if none)\n\n Use NLP techniques to better understand the question semantics.\nHandle variations in question formatting and numbering by using flexible regex patterns. Extract answer options using these regex patterns as well as NLP to isolate the options based on context.\nPreprocess the extracted text to remove empty lines, irrelevant content, and handle common OCR errors. Use heuristics to identify and skip over non-question content like instructions and headers.\nFor questions with dependent sub-questions include the direct answer as the option for the parent question (ie. a yes or no question should still have options listed yes/no listed, or x/y/z with different sub-questions if x y or z should still list x/y/z as options for parent). Any subquestions (if yes, or if x/y/z type questions) should be included as their own CSV item with accurate numbering.\nClarify any ambiguous situations by referencing the techniques described above. If a question truly cannot be parsed, DO NOT return anything except the string: FALIURE - (give question or questions of issue),to avoid outputting bad data.\nThe output format should be a valid CSV with commas and special characters properly escaped. Aim to extract questions individually to avoid misparsing, but include the full text of each multi-part question. \nRemember, the goal is to produce a comprehensive, machine-readable set of questions and answer options to enable downstream analysis. Strive for accuracy and completeness, but also make reasonable judgments to handle the variety of formats found in real-world documents.",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": text
                        }
                    ]
                }
            ]
        )
        print(message.content)

        if message.content:
            # Save the output as a CSV file
            csv_output = "".join(content.text for content in message.content)
            file_name, _ = os.path.splitext(file_path)
            csv_file_path = f"{file_name}_questions.csv"
            with open(csv_file_path, "w", newline="") as csvfile:
                csvfile.write(csv_output)
            print(f"CSV file saved as: {csv_file_path}")
        else:
            print("No content received from API, unable to save CSV file.")

    except Exception as e:
        print(f'Error: {str(e)}')

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python question_extractor.py <file_path>")
        sys.exit(1)
    file_path = sys.argv[1]
    main(file_path)