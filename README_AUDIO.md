Audio input/output for the ‘brain’ assistant 🔊

Quick start
-----------
1. Install recommended packages:

   pip install -r requirements.txt

2. On Windows you may need PyAudio for microphone support. If pip install pyaudio fails, try:

   pip install pipwin
   pipwin install pyaudio

3. (Optional) To enable OpenAI-powered answers, set your API key:

   setx OPENAI_API_KEY "your_api_key_here"

4. Run:

   python main.py

Usage notes
-----------
- The script attempts to use your microphone; if no mic or the microphone library isn't available, it falls back to typed input.
- For text-to-speech it uses `pyttsx3` (offline). If `pyttsx3` is not installed it will print replies instead of speaking.

Troubleshooting
---------------
- Microphone not working: ensure your system microphone is available and that PyAudio is installed.
- If you want better offline speech recognition, consider installing a local ASR engine (e.g., VOSK) and updating `main.py`.

Security & privacy
------------------
- If you enable OpenAI, audio/text will be sent to OpenAI for transcription/response according to their policies.
- Do not share sensitive information while using cloud-based services.

If you'd like, I can add a button, GUI, or integrate Whisper/Whisper.cpp for local transcription. ✅
