import sys
import os
from dotenv import load_dotenv
import anthropic
from extraction_utils import extract_text, extract_questions, clean_csv, extract_answer_options

load_dotenv(os.path.join(os.path.dirname(__file__), 'main.env'))

api_key = os.environ.get('ANTHROPIC_API_KEY')
client = anthropic.Anthropic(api_key=api_key)

def main(file_path):
    print(f"Processing file: {file_path}")
    try:
        text = extract_text(file_path)
    except Exception as e:
        print(f"Error extracting text: {str(e)}")
        return

    try:
        questions_csv = extract_questions(text, client)
        print("Questions extracted:")
        print(questions_csv)

        cleaned_questions_csv = clean_csv(questions_csv, client)
        print("CSV cleaned:")
        print(cleaned_questions_csv)

        final_csv = extract_answer_options(text, cleaned_questions_csv, client)
        print("Answer options added:")
        print(final_csv)

        if final_csv:
            file_name, _ = os.path.splitext(file_path)
            csv_file_path = f"{file_name}_questions.csv"
            with open(csv_file_path, "w", newline="") as csvfile:
                csvfile.write(final_csv)
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