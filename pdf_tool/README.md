# PDF Tool - Summarize & Convert to Speech

An advanced yet simple Python tool that allows users to upload a PDF, choose to summarize or convert it to speech, listen to it offline, and optionally download the generated audio as a speech file.

## Features

- 📄 **PDF Upload**: Drag & drop or click to upload PDF files
- 📝 **Text Extraction**: Automatically extract text from PDF documents
- ✨ **Smart Summarization**: Generate concise summaries using intelligent text analysis
- 🎤 **Text-to-Speech**: Convert PDF text to natural-sounding speech
- 🌍 **Multi-language Support**: Support for 10+ languages including English, Spanish, French, German, and more
- 🎧 **Audio Player**: Built-in audio player for immediate playback
- 💾 **Download Audio**: Save generated audio files for offline listening
- 📱 **Responsive Design**: Beautiful, modern UI that works on all devices
- ⚡ **Real-time Processing**: Fast and efficient PDF processing

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Setup

1. **Clone or download this repository**
   ```bash
   git clone <repository-url>
   cd pdf_tool
   ```

2. **Install required dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Open your browser**
   Navigate to `http://localhost:5000`

## Usage

### Step 1: Upload PDF
- Drag and drop your PDF file onto the upload area, or click to browse and select a file
- The tool will automatically extract text from your PDF
- Maximum file size: 16MB

### Step 2: Choose Your Action

#### Option A: Summarize PDF
- Click the "Generate Summary" button
- The tool will create a concise summary of your PDF content
- View the summary with character count statistics

#### Option B: Convert to Speech
- Select whether to convert the full text or summary
- Choose your preferred language from the dropdown
- Click "Convert to Speech"
- The tool will generate an audio file

### Step 3: Listen & Download
- Use the built-in audio player to listen to your generated speech
- Click "Download Audio" to save the file for offline use
- Audio files are saved in MP3 format

## Supported Languages

- English (en)
- Spanish (es)
- French (fr)
- German (de)
- Italian (it)
- Portuguese (pt)
- Russian (ru)
- Japanese (ja)
- Korean (ko)
- Chinese (zh)

## Technical Details

### Backend Technologies
- **Flask**: Web framework for the backend API
- **PyPDF2**: PDF text extraction library
- **gTTS (Google Text-to-Speech)**: Text-to-speech conversion
- **Werkzeug**: File upload handling

### Frontend Technologies
- **HTML5**: Semantic markup
- **CSS3**: Modern styling with gradients and animations
- **JavaScript**: Interactive functionality
- **Font Awesome**: Icons
- **Responsive Design**: Mobile-first approach

### File Structure
```
pdf_tool/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── templates/
│   └── index.html        # Main web interface
├── uploads/              # Temporary PDF storage
└── audio/                # Generated audio files
```

## API Endpoints

- `GET /` - Main application page
- `POST /upload` - Upload and process PDF file
- `POST /summarize` - Generate PDF summary
- `POST /convert-to-speech` - Convert text to speech
- `GET /audio/<filename>` - Serve audio files
- `GET /download/<filename>` - Download audio files
- `POST /clear-session` - Clear current session

## Features in Detail

### Smart Summarization
The summarization algorithm:
- Extracts key sentences based on importance indicators
- Maintains context and readability
- Provides character count statistics
- Optimizes for readability and conciseness

### Text-to-Speech Conversion
- High-quality speech synthesis using Google's TTS service
- Multiple language support
- Configurable speech parameters
- MP3 format output for compatibility

### User Experience
- Drag-and-drop file upload
- Real-time progress indicators
- Error handling and user feedback
- Responsive design for all screen sizes
- Intuitive navigation and controls

## Troubleshooting

### Common Issues

1. **PDF text extraction fails**
   - Ensure the PDF contains selectable text (not just images)
   - Try a different PDF file
   - Check if the PDF is password-protected

2. **Audio generation fails**
   - Check your internet connection (required for TTS)
   - Ensure the text is not empty
   - Try a different language setting

3. **File upload issues**
   - Ensure the file is a valid PDF
   - Check file size (max 16MB)
   - Try refreshing the page

### Performance Tips

- For large PDFs, consider using the summary option first
- Close other browser tabs to free up memory
- Use a stable internet connection for TTS conversion

## Contributing

Feel free to contribute to this project by:
- Reporting bugs
- Suggesting new features
- Submitting pull requests
- Improving documentation

## License

This project is open source and available under the MIT License.

## Support

If you encounter any issues or have questions, please:
1. Check the troubleshooting section above
2. Review the error messages in the browser console
3. Ensure all dependencies are properly installed

---

**Enjoy using your PDF Tool!** 🎉 