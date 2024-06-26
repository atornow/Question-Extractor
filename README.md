# Question Extractor

This Python script extracts questions from a Word document (.doc, .docx) or PDF file, and saves them to a CSV file along with their question numbers, multiple choice status, and answer options.

### Prerequisites

- Python 3.x
- Required Python packages:
  - python-docx
  - anthropic
  - python-dotenv
  - PyPDF2

### Setup/Usage

1. Install the required Python packages:
  ```
   pip install python-docx anthropic python-dotenv PyPDF2
  ```
2. Set up your Anthropic API key:
- Create a file named `main.env` in the same directory as the script.
- Add your Anthropic API key to the file in the following format:
  ```
   ANTHROPIC_API_KEY=your_api_key_here
  ```
3. Run the script from the command line with the file path as an argument:
  ```
  python question_extractor.py <file_path>
 ```
- Or to run a specific model from anthropic:
 ```
  python question_extractor.py <file_path> <model_name>
```
- Replace `<file_path>` with the path to your Word document or PDF file and `<model_name>` with any valid model name from Anthropic.

### Output

The script will generate a CSV file in working directory, with name `<file_name>_questions.csv`

The CSV file will have the following columns:
- `question_text`: The text of the question.
- `question_number`: The question number. For subquestions like "b." under question 2.6, it will be formatted as "2.6.b".
- `is_multiple_choice`: 1 if the question has multiple choice options, 0 if not.
- `answer_options`: If `is_multiple_choice` is 1, this column will contain a slash (/) delimited list of the possible answer options. For yes/no questions, it will be formatted as "yes/no". This column will be blank if the question is not multiple choice.

### Example CSV Output

 ```
question_text,question_number,is_multiple_choice,answer_options
"What is the capital of France?",1,1,"Paris/London/Berlin/Madrid"
"Is the Earth flat?",2,1,"yes/no"
"Explain the theory of relativity.",3,0,
 ```
### Error Handling

The script will print any errors encountered during text extraction or API calls. If an error occurs, the script will continue to the next step or exit gracefully.

### Notes

- The script uses the Anthropic API to extract questions and answer options from the text. Make sure you have a valid API key and sufficient API quota.
- The script assumes a specific format for the input documents (doc, docx or PDF) and may need modifications to handle different formats or question styles.
