import React, { useEffect, useState } from 'react';

function App() {
  const [transcript, setTranscript] = useState('');
  const [isSpeechDetected, setIsSpeechDetected] = useState(false);
  const [summary, setSummary] = useState('');
  const [speechTimestamps, setSpeechTimestamps] = useState([]);
  const [recognition, setRecognition] = useState(null);
  const [isStopButtonClicked, setIsStopButtonClicked] = useState(false);

  const appendTranscriptWithTimestamp = (newTranscript) => {
    const currentTime = new Date().toLocaleTimeString();
    const newSpeech = `${currentTime}: ${newTranscript}`;
    setTranscript((prevTranscript) => prevTranscript + '\n' + newSpeech);
    setSpeechTimestamps((prevTimestamps) => [...prevTimestamps, newSpeech]);
    setIsSpeechDetected(true);
  };

  const startSpeechRecognition = () => {
    const recognitionInstance = new window.webkitSpeechRecognition();
    recognitionInstance.continuous = true;

    recognitionInstance.onresult = function (event) {
      const newTranscript = event.results[event.results.length - 1][0].transcript;
      appendTranscriptWithTimestamp(newTranscript);
    };

    recognitionInstance.onstart = function () {
      setIsSpeechDetected(true);
      setIsStopButtonClicked(false);
      console.log('start');
    };

    recognitionInstance.onend = function () {
      setIsSpeechDetected(false);
      console.log('end');
      if (isStopButtonClicked) {
        // Stop button was clicked, start summarization
        startSummarization();
      }
    };

    recognitionInstance.start();
    setRecognition(recognitionInstance);
  };

  const stopSpeechRecognition = () => {
    if (recognition) {
      recognition.stop();
      setIsStopButtonClicked(true);
      // Start summarization immediately when the "Stop Speech" button is clicked
      startSummarization();
    }
  };

  const eraseTranscription = () => {
    setTranscript('');
    setSummary('');
    setIsSpeechDetected(false);
    setSpeechTimestamps([]);
  };

  const startSummarization = () => {
    if (!isSpeechDetected) {
      // Split the transcript into individual messages based on line breaks
      const messages = transcript.split('\n');

      // Filter out empty messages and timestamps
      const filteredMessages = messages.filter((message) => message.trim() !== '');

      // Join the filtered messages to create a single text for summarization
      const summarizedText = filteredMessages.join('\n');

      if (summarizedText) {
        fetch('http://localhost:8080/summarize', {
          method: 'POST',
          body: JSON.stringify({ transcript: summarizedText }),
          headers: {
            'Content-Type': 'application/json',
          },
        })
          .then((response) => {
            if (!response.ok) {
              throw new Error('Network response was not ok');
            }
            return response.json();
          })
          .then((data) => {
            const newSummary = data.summary;
            setSummary(newSummary);
          })
          .catch((error) => {
            console.error('Error:', error);
          });
      }
    }
    setIsSpeechDetected(false);
  };

  useEffect(() => {
    if (transcript !== '' && !isSpeechDetected) {
      startSummarization();
    }
  }, [transcript, isSpeechDetected]);

  return (
    <div className="App">
      <h1>Audio-to-Agreement (change title later)</h1>

      {/* Step 1: user uploads an audio file */}
      <form method="post" encType="multipart/form-data">
        <input type="file" name="file" accept=".mp3, .wav, .ogg" hidden />
        <input type="submit" value="Transcribe" hidden />
      </form>

      {/* Step 2: display transcribed text */}
      <button onClick={startSpeechRecognition}>Start Speech</button>
      <button onClick={stopSpeechRecognition}>Stop Speech</button>
      <button onClick={eraseTranscription}>Erase</button>
      {transcript === '' ? (
        <div id="transcription">say something</div>
      ) : (
        <div id="speechTranscriptContainer">
          <div id="transcription">
            <h2>Transcribed Text:</h2>
            {/* <p>{transcript}</p> */}
          </div>
        </div>
      )}

      {/* Display speech timestamps */}
      <div id="speechTimestamps">
        {speechTimestamps.map((timestamp, index) => (
          <p key={index}>{timestamp}</p>
        ))}
      </div>

      {/* Step 3: display the summary */}
      <div id="summaryContainer">
        <h2>Summary:</h2>
        <div id="summary">{summary}</div>
      </div>

      {/* Step 4: generate agreements */}
      <h2>Generated Agreements:</h2>
      <p>Note: maybe generate 3 agreement templates to choose from (?)</p>
      <ul>
        <li>Agreement 1</li>
        <li>Agreement 2</li>
        <li>Agreement 3</li>
        {/* additional agreements will be listed here */}
      </ul>

      {/* Step 5: user feedback and modification using audio file upload */}
      <h2>Review and Modify Agreements:</h2>
      <form action="/modify" method="POST" encType="multipart/form-data">
        <input type="file" name="audio_feedback" accept=".mp3, .wav, .ogg" />
        <input type="submit" value="Upload Audio Feedback" />
      </form>

      {/* Step 6: ai suggestions */}
      <h2>AI Suggestions:</h2>
      <p>AI-generated suggestions based on user feedback will display here</p>

      {/* Step 7: finalise & download agreements */}
      <a href="/download">Download Customized Agreements</a>

      {/* Future features - will leave it here for now and check off later */}
      <h2>Future Features:</h2>
      <ul className="future-features">
        <li>Live translation</li>
        <li>Read agreements aloud</li>
        <li>Auto-sign certain documents</li>
        <li>Remove signatures</li>
        <li>Manage document collections</li>
      </ul>
    </div>
  );
}

export default App;
