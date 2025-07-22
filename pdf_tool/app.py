import os
import uuid
import tempfile
from flask import Flask, render_template, request, jsonify, send_file, session
from werkzeug.utils import secure_filename
import PyPDF2
from gtts import gTTS
import json
import re

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['AUDIO_FOLDER'] = 'audio'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['AUDIO_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_pdf(pdf_path):
    """Extract text from PDF file"""
    text = ""
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
    except Exception as e:
        print(f"Error extracting text: {e}")
        return None
    return text

def summarize_text(text, max_length=500):
    """Simple summarization by extracting key sentences"""
    if not text:
        return "No text could be extracted from the PDF."
    
    # Clean the text
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Split into sentences
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
    
    if not sentences:
        return "No readable text found in the PDF."
    
    # Simple summarization: take first few sentences and key sentences
    summary_sentences = []
    current_length = 0
    
    # Add first sentence
    if sentences:
        summary_sentences.append(sentences[0])
        current_length += len(sentences[0])
    
    # Add sentences with important keywords
    important_words = ['important', 'key', 'summary', 'conclusion', 'main', 'primary', 'essential']
    
    for sentence in sentences[1:]:
        if current_length >= max_length:
            break
        
        # Check if sentence contains important words or is reasonably long
        if any(word in sentence.lower() for word in important_words) or len(sentence) > 50:
            summary_sentences.append(sentence)
            current_length += len(sentence)
    
    # If we don't have enough content, add more sentences
    if len(summary_sentences) < 3 and len(sentences) > 3:
        for sentence in sentences[1:4]:
            if sentence not in summary_sentences and current_length < max_length:
                summary_sentences.append(sentence)
                current_length += len(sentence)
    
    summary = '. '.join(summary_sentences)
    if not summary.endswith('.'):
        summary += '.'
    
    return summary

def text_to_speech(text, filename, language='en'):
    """Convert text to speech and save as audio file"""
    try:
        tts = gTTS(text=text, lang=language, slow=False)
        audio_path = os.path.join(app.config['AUDIO_FOLDER'], filename)
        tts.save(audio_path)
        return audio_path
    except Exception as e:
        print(f"Error in text-to-speech: {e}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file and allowed_file(file.filename):
        # Generate unique filename
        unique_id = str(uuid.uuid4())
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{unique_id}_{filename}")
        
        file.save(file_path)
        
        # Extract text from PDF
        text = extract_text_from_pdf(file_path)
        if not text:
            return jsonify({'error': 'Could not extract text from PDF'}), 400
        
        # Store in session
        session['pdf_text'] = text
        session['pdf_filename'] = filename
        session['unique_id'] = unique_id
        
        return jsonify({
            'success': True,
            'filename': filename,
            'text_length': len(text),
            'preview': text[:200] + '...' if len(text) > 200 else text
        })
    
    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/summarize', methods=['POST'])
def summarize():
    text = session.get('pdf_text')
    if not text:
        return jsonify({'error': 'No PDF text available'}), 400
    
    summary = summarize_text(text)
    
    # Store summary in session
    session['summary'] = summary
    
    return jsonify({
        'success': True,
        'summary': summary,
        'original_length': len(text),
        'summary_length': len(summary)
    })

@app.route('/convert-to-speech', methods=['POST'])
def convert_to_speech():
    data = request.get_json()
    text_type = data.get('type', 'full')  # 'full' or 'summary'
    language = data.get('language', 'en')
    
    if text_type == 'summary':
        text = session.get('summary')
        if not text:
            return jsonify({'error': 'No summary available. Please summarize first.'}), 400
    else:
        text = session.get('pdf_text')
        if not text:
            return jsonify({'error': 'No PDF text available'}), 400
    
    unique_id = session.get('unique_id')
    if not unique_id:
        return jsonify({'error': 'No PDF session found'}), 400
    
    # Generate audio filename
    audio_filename = f"{unique_id}_{text_type}_{language}.mp3"
    
    # Convert to speech
    audio_path = text_to_speech(text, audio_filename, language)
    if not audio_path:
        return jsonify({'error': 'Failed to convert text to speech'}), 500
    
    # Store audio info in session
    session['audio_filename'] = audio_filename
    session['audio_type'] = text_type
    
    return jsonify({
        'success': True,
        'audio_filename': audio_filename,
        'text_type': text_type,
        'language': language
    })

@app.route('/download/<filename>')
def download_audio(filename):
    audio_path = os.path.join(app.config['AUDIO_FOLDER'], filename)
    if os.path.exists(audio_path):
        return send_file(audio_path, as_attachment=True)
    return jsonify({'error': 'Audio file not found'}), 404

@app.route('/audio/<filename>')
def serve_audio(filename):
    audio_path = os.path.join(app.config['AUDIO_FOLDER'], filename)
    if os.path.exists(audio_path):
        return send_file(audio_path, mimetype='audio/mpeg')
    return jsonify({'error': 'Audio file not found'}), 404

@app.route('/clear-session', methods=['POST'])
def clear_session():
    session.clear()
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 