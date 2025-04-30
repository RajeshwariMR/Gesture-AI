import whisper
import sounddevice as sd
import numpy as np
import queue
import json
import wave
import re
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Load Whisper model
model = whisper.load_model("base")

# Load word-to-videos mappings (letters, numbers, words)
with open("word_mappings.json", "r") as f:
    word_videos = json.load(f)

# Queue for real-time audio
audio_queue = queue.Queue()

def callback(indata, frames, time, status):
    """ Callback function to continuously capture microphone audio """
    if status:
        print(status)
    audio_queue.put(indata.copy())

def record_audio_stream(samplerate=16000):
    """ Records audio continuously and processes it in real-time """
    duration = 10  # Max recording time (seconds)
    filename = "live_audio.wav"

    # Start recording
    with sd.InputStream(samplerate=samplerate, channels=1, callback=callback, dtype=np.float32):
        audio_data = []
        for _ in range(int(duration * samplerate / 1024)):  # Record in chunks
            audio_data.append(audio_queue.get())

        audio_array = np.concatenate(audio_data, axis=0)  # Convert to numpy array
        audio_array = (audio_array * 32767).astype(np.int16)  # Convert to 16-bit PCM

    # Save as WAV file
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(samplerate)
        wf.writeframes(audio_array.tobytes())

    return filename

@app.route('/speech_to_text', methods=['POST'])
def speech_to_text():
    filename = record_audio_stream()  # Capture real-time audio
    result = model.transcribe(filename)

    text = result['text'].strip().lower()
    print(f"Recognized Text: {text}")

    return jsonify({"text": text})

@app.route('/process_text', methods=['POST'])
def process_text():
    text = request.form.get('text', '').lower()
    # ✅ Remove all special characters except alphabets and spaces
    text = re.sub(r'[^a-z\s]', '', text)
    words = text.split()

    # ✂️ Skip non-ASL function words
    skip_words = {
        # Articles
        "the", "a", "an",

        # Be verbs
        "is", "are", "was", "were", "am", "be", "being", "been",

        # Auxiliary verbs
        "does", "did", "have", "has", "had", "will", "would", "shall", "should",
        "can", "could", "may", "might", "must",

        # Prepositions (common ones usually skipped)
        "of", "to", "for", "from", "by", "with", "about", "over", "under", "into", "onto",
        "across", "through", "before", "around",

        # Conjunctions
        "that", "whom", "whose", "than", "yet", "although", "though", "unless",

        # Filler / placeholder
        "there", "as", "then", "just", "even", "really", "very", "quite", "maybe", "like", "almost", "often", "ever", "always",

        # Pronouns to skip (you have other pronouns animated)
        "this", "these", "those", "each", "anyone", "everyone", "someone", "something", "nothing",

        # Temporal (keep today if you animated it)
        "soon", "now", "later"
    }

    video_sequence = []

    for word in words:
        if word in skip_words:
            continue

        
        if word in word_videos and word_videos[word].strip():  # ✅ Skip empty words
            video_sequence.append(word_videos[word])
        else:  # ✅ Process letter-by-letter only if it's not an empty entry
            video_sequence.extend(
                [word_videos[char] for char in word if char in word_videos and word_videos[char].strip()]
            )

    return jsonify({"videos": video_sequence})



@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
