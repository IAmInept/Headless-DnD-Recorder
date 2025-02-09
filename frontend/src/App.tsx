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
      <div>
        <button disabled={isRecording === recordingState.Recording} onClick={() => {SetRecording(1); fetch("/api/on")}}>Start Recording</button>
        <button disabled={isRecording === recordingState.Standby} onClick={() => {SetRecording(0); fetch("/api/off")}} >Stop Recording</button> 
      </div>
    </>
  )
}

export default App
