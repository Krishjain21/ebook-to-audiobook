from flask import Flask, request, jsonify
import json
from flask_cors import CORS, cross_origin

import PyPDF2
import pyttsx3

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/convert/pdf-to-text', methods=['GET','POST'])
@cross_origin()
def convert_pdf_to_text():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    pdf_file = request.files['file']
    c=str(pdf_file)
    print(c,"\n")
    x=c.split("'")
    print(x[1])
    z=x[1].split(".")
    # Provide the output text file path
    text_file = 'text_files/' + z[0] + '.txt'
    print(text_file)
    # Convert the PDF to a text file
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text_content = ""

    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text_content += page.extract_text()
    print(len(text_content))
    with open(text_file, 'w', encoding='utf-8') as file:
        file.write(text_content)
    print("bye")
    output_file = 'audiobooks/' + z[0] + '.mp3'

    # Initialize pyttsx3
    engine = pyttsx3.init()

    # Set properties for the audio output
    engine.setProperty('rate', 150)  # Adjust the speaking rate (words per minute)
    engine.setProperty('volume', 0.8)  # Adjust the volume (0.0 to 1.0)
    print("here")
    # Open and read the eBook file
    with open(text_file, 'r', encoding='utf-8') as file:
        ebook_text = file.read()
    print("there")
    # Save the audiobook as an MP3 file
    engine.save_to_file(ebook_text, output_file)
    print("done")
    # Run the text-to-speech conversion
    engine.runAndWait()

    return {
            'message': 'eBook converted to audiobook successfully.',
            'filename': z[0] + '.mp3',
        }, 200
if __name__ == '__main__':
    app.run()
    
    
    # (strings + image file + Date) = 1 FormData
    # application/json -> strings
