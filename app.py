from flask import Flask, render_template, request, jsonify, send_file
from generate_notes import generate_notes, generate_pdf, generate_doc
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_notes', methods=['POST'])
def generate():
    novel_name = request.form['novelName']
    author_name = request.form['authorName']
    
    # Generate notes using multiple prompts with Gemini AI
    notes = generate_notes(novel_name, author_name)
    
    # Save the notes in a session or temporary storage for download
    with open("downloads/notes.txt", "w") as f:
        f.write(notes)
    
    return jsonify({'notes': notes})

@app.route('/download/<file_type>', methods=['GET'])
def download(file_type):
    if file_type == 'pdf':
        generate_pdf("downloads/notes.txt", "downloads/notes.pdf")
        return send_file("downloads/notes.pdf", as_attachment=True)
    elif file_type == 'doc':
        generate_doc("downloads/notes.txt", "downloads/notes.docx")
        return send_file("downloads/notes.docx", as_attachment=True)
    else:
        return "Invalid file type", 400

if __name__ == '__main__':
    if not os.path.exists('downloads'):
        os.makedirs('downloads')
    app.run(debug=True)
