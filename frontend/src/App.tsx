import { useState } from 'react'
import './App.css'

enum recordingState {
  Standby = 0,
  Recording = 1
}

function App() {
  const [isRecording, SetRecording] = useState(0)
  return (
    <>
      <h1>Foundry VTT Recorder</h1>
      <div id='btn_container'>
        <button id="btn_srtRecording" disabled={isRecording === recordingState.Recording} onClick={() => {SetRecording(1); fetch("/api/on")}}>Start Recording</button>
        <button id="btn_stpRecordingdarkgreen"disabled={isRecording === recordingState.Standby} onClick={() => {SetRecording(0); fetch("/api/off")}} >Stop Recording</button> 
      </div>
    </>
  )
}

export default App
