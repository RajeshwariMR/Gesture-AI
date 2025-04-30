## Gesture AI – Speech to Sign Language Converter                       
🎯*Empowering communication for the deaf community using AI and animated gestures.*


## About Gesture AI

**Gesture AI** is an AI-powered tool that:

🎤 Captures spoken words via microphone  
🧠 Converts speech to text using AI  
✋ Matches the words to animated **sign language gestures** created in Blender  
🔤 Spells out words letter-by-letter if no sign exists  
✏️ Allows users to **review and edit** the transcribed text before playback  

## Demo Video

Watch the demo of the **Gesture AI** website in action:  
📽️ [Project Demo Video](https://drive.google.com/file/d/1EZV3Vn5-lqS7SihfFC5NVT2tdz5jgcgl/view?usp=sharing)

## How to Run Locally


1. **Clone the repository**
   ```bash
   git clone https://github.com/RajeshwariMR/Gesture-AI.git
   cd Gesture-AI
   ```

2. **Install dependencies**
   ```bash
   pip install flask whisper numpy
   ```

3. **Run the Flask application**
   ```bash
   python app.py
   ```

4. Open your browser and navigate to:  
   👉 `http://localhost:5000`

## 📂 Project Structure

```
Gesture-AI/
├── app.py                    → Flask application
├── word_mappings.json        → Text-to-gesture mapping
├── static/
│   ├── css/style.css         → Styling
│   ├── js/app.js             → Frontend logic
│   ├── videos/               → Sign language gesture videos
│   └── avatar_standing.png / Hello.gif → UI assets
├── templates/index.html      → Web interface template
```

## How Gesture AI Benefits Users

💡 Transforms speech into animated sign language promptly  
🎓 Offers an interactive way to learn basic sign language gestures  
🧏‍♀️ Enhances communication access for the Deaf and Hard-of-Hearing community  
🌐 Available for free, web-based, and user-friendly for everyone  

## Features

🎙️ Converts real-time speech to text using Whisper AI  
👋 Dynamic gesture playback powered by Blender animations       
🖥️ Simple and customizable codebase (Flask + HTML/CSS/JS)          
🗂️ Flexible JSON-based gesture mapping            
🔌 Works offline after setup  

## Contact

🌐 GitHub: [RajeshwariMR](https://github.com/RajeshwariMR)
