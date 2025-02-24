# real-time-language-Translator
Real-Time Language Translator
Project Overview
The Real-Time Language Translator is a web-based application designed to translate text and speech between multiple languages in real-time. The system supports:

Text-to-Text Translation
Speech-to-Text Conversion
Text-to-Speech Synthesis
This project integrates Google Translator API, Google Speech Recognition, and gTTS (Google Text-to-Speech) to provide a seamless translation experience.

Features
✅ Text Translation – Translate text between multiple languages using Google Translate API
✅ Speech Recognition – Convert speech from an audio file to text using Google Speech API
✅ Text-to-Speech Conversion – Convert translated text into spoken audio using gTTS (Google Text-to-Speech)
✅ MP3 File Support – The system accepts MP3 files and converts them to text
✅ Interactive User Interface – Modern UI with animated elements for a smooth user experience

Tech Stack Used
Frontend:
HTML, CSS, JavaScript (Tailwind CSS) – For creating an interactive and visually appealing UI
Speech Recognition API – For real-time speech-to-text conversion
Backend:
FastAPI – Lightweight and efficient backend framework
Google Translator API – For translating text between multiple languages
Google Speech API – Converts speech audio to text
gTTS (Google Text-to-Speech) – Converts translated text into speech
FFmpeg – For audio file format conversion
Installation and Setup
Step 1: Clone the Repository
bash
Copy
Edit
git clone https://github.com/your-repo/real-time-translator.git
cd real-time-translator
Step 2: Install Required Dependencies
Make sure you have Python 3.8+ installed. Then, run:

bash
Copy
Edit
pip install -r requirements.txt
Step 3: Install FFmpeg (Required for Speech Processing)
For Windows: Download FFmpeg from here and add it to the system path
For Linux/macOS: Install it using:
bash
Copy
Edit
sudo apt install ffmpeg  # Ubuntu/Debian  
brew install ffmpeg      # macOS  
Step 4: Run the Application
bash
Copy
Edit
uvicorn app:app --reload
Your app will be accessible at: http://127.0.0.1:8000/

Project Structure
php
Copy
Edit
real-time-translator/
│── app.py                 # FastAPI backend logic
│── templates/
│   ├── index.html         # Frontend HTML with Tailwind CSS
│── static/                # CSS, JavaScript files
│── temp/                  # Temporary storage for audio files
│── requirements.txt       # List of dependencies
│── README.md              # Documentation file
Usage Instructions
1. Text Translation
Enter the text you want to translate
Select the source and target language
Click on Translate to get the translated text
2. Speech-to-Text
Click on Upload Audio and select an MP3 file
The system will process the audio and display the recognized text
3. Text-to-Speech
After translation, click on Download Audio
The translated text will be converted into speech and downloaded as an MP3 file
Future Enhancements
🔹 Support for More Languages
🔹 Offline Speech Processing
🔹 Enhanced UI with More Animations

