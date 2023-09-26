import React, { useState } from 'react';

function App() {
  const [transcript, setTranscript] = useState('');

  const startSpeechRecognition = () => {
  };

  const eraseTranscription = () => {
    setTranscript('');
  };

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
      <button onClick={eraseTranscription}>Erase</button>
      {transcript === '' ? (
        <div id="transcription">say something</div>
      ) : (
        <div id="speechTranscriptContainer">
          <div id="transcription">
            <h2>Transcribed Text:</h2>
            <p>{transcript}</p>
          </div>
        </div>
      )}

      {/* Step 3: display the summary */}
      <div id="summaryContainer">
        <h2>Summary:</h2>
        <div id="summary"></div>
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
