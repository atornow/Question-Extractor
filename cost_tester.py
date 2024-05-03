import sys
from extraction_utils import extract_text, extract_questions, clean_csv, extract_answer_options
import anthropic
from dotenv import load_dotenv
import os

load_dotenv(os.path.join(os.path.dirname(__file__), 'main.env'))

api_key = os.environ.get('ANTHROPIC_API_KEY')
client = anthropic.Anthropic(api_key=api_key)

def process_file(file_path, model):
    print(f"Processing file with {model}: {file_path}")
    try:
        text = extract_text(file_path)
    except Exception as e:
        print(f"Error extracting text: {str(e)}")
        return None

    try:
        questions_csv = extract_questions(text, client, model)
        print(f"Questions extracted with {model}:")
        print(questions_csv)

        cleaned_questions_csv = clean_csv(questions_csv, client, model)
        print(f"CSV cleaned with {model}:")
        print(cleaned_questions_csv)

        final_csv = extract_answer_options(text, cleaned_questions_csv, client, model)
        print(f"Answer options added with {model}:")
        print(final_csv)

        return final_csv

    except Exception as e:
        print(f'Error with {model}: {str(e)}')
        return None

def main(file_path):
    models = ["claude-3-sonnet-20240229", "claude-3-opus-20240229", "claude-3-haiku-20240307"]

    for model in models:
        final_csv = process_file(file_path, model)

        if final_csv:
            file_name, _ = os.path.splitext(file_path)
            csv_file_path = f"{file_name}_{model}_questions.csv"
            with open(csv_file_path, "w", newline="") as csvfile:
                csvfile.write(final_csv)
            print(f"CSV file saved as: {csv_file_path}")
        else:
            print(f"No content received from API for {model}, unable to save CSV file.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python cost_tester.py <file_path>")
        sys.exit(1)
    file_path = sys.argv[1]
    main(file_path)