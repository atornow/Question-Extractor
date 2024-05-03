<?xml version="1.0" encoding="UTF-8" ?>
<readme>
    <title>Question Extractor</title>
    <description>
        This Python script extracts questions from text documents (PDF or DOCX), cleans them up, and adds answer options if available.
    </description>

    <usage>
        <title>Usage</title>
        <content>
            To run the script, execute the following command in your terminal:
            <code>
                python question_extractor.py &lt;file_path&gt;
            </code>
            Replace &lt;file_path&gt; with the path to the target document.
        </content>
    </usage>

    <dependencies>
        <title>Dependencies</title>
        <list>
            <item>Python 3.x</item>
            <item>docx</item>
            <item>PyPDF2</item>
            <item>anthropic</item>
            <item>dotenv</item>
        </list>
    </dependencies>

    <instructions>
        <title>Instructions</title>
        <steps>
            <step>
                <number>1</number>
                <content>Ensure Python 3.x and required dependencies are installed.</content>
            </step>
            <step>
                <number>2</number>
                <content>Set up an Anthropic API key and configure it in the main.env file.</content>
            </step>
            <step>
                <number>3</number>
                <content>Run the script with the target file path as an argument.</content>
            </step>
        </steps>
    </instructions>

    <output>
        <title>Output</title>
        <content>
            The script generates a CSV file containing extracted questions and, if available, their answer options.
        </content>
    </output>

    <note>
        <title>Note</title>
        <content>
            Ensure the input file is in PDF or DOCX format.
        </content>
    </note>

    <author>
        <name>Your Name</name>
        <email>your.email@example.com</email>
    </author>

    <license>
        <type>MIT License</type>
        <url>https://opensource.org/licenses/MIT</url>
    </license>
</readme>
