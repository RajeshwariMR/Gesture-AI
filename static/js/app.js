let isRecording = false;

function startSpeechRecognition() {
    if (isRecording) return;
    isRecording = true;

    let outputText = document.getElementById("outputText");
    outputText.innerText = "Listening... 🎤";

    fetch('/speech_to_text', { method: 'POST' })
    .then(response => response.json())
    .then(data => {
        outputText.innerText = "Recognized Text: " + data.text;
        document.getElementById("textInput").value = data.text; // Auto-fill text input
        isRecording = false;
    })
    .catch(error => {
        console.error("Error:", error);
        isRecording = false;
    });
}

function processText() {
    let text = document.getElementById("textInput").value;
    fetch('/process_text', {
        method: 'POST',
        body: new URLSearchParams({ 'text': text }),
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
    })
    .then(response => response.json())
    .then(data => {
        playVideosSequentially(data.videos);
    });
}
function playVideosSequentially(videoList) {
    let videoElement = document.getElementById("gestureVideo");
    let index = 0;

    function playNextVideo() {
        if (index < videoList.length) {
            let videoPath = videoList[index];
            videoElement.src = videoPath;
            videoElement.load();

            videoElement.oncanplay = () => {
                videoElement.play().then(() => {
                    videoElement.style.opacity = "1"; // Ensure video is fully visible
                    index++;
                    videoElement.onended = playNextVideo;
                }).catch(error => console.error("Error playing video:", error));
            };

            videoElement.style.opacity = "0"; // Hide before loading new video
        }
    }

    if (videoList.length > 0) {
        playNextVideo();
    }
}
