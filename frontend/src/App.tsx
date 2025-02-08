import { useEffect, useState } from 'react'
import './App.css'

function App() {
  const [isRecording, SetRecording] = useState(0)

  useEffect(() => {
    if (isRecording == 1) {
      fetch('/api/on', {
        method: "GET"
      })

    } else {
      fetch('/api/off', {
        method: "GET"
      })
    }
  }, [isRecording]
)

  return (
    <>
      <button onClick={() => SetRecording(1)}>Click Me</button>
      <button onClick={() => SetRecording(0)}>Dont Click Me!</button>
    </>
  )
}print

export default App
