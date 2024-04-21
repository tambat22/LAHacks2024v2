import React, { useState, useEffect, useRef } from "react";

const TextToSpeech = ({ text }) => {
  const [isPaused, setIsPaused] = useState(false);
  const synth = useRef(window.speechSynthesis);
  const utterance = useRef(null);

  useEffect(() => {
    // Setting up the new utterance every time text changes
    utterance.current = new SpeechSynthesisUtterance(text);
    utterance.current.onend = () => {
      console.log("Finished in speaking");
      setIsPaused(false); // Reset pause state when speech ends
    };

    // Speak the text immediately when it is updated
    if (text) {
      synth.current.speak(utterance.current);
    }

    // Clean up on component unmount or text change
    return () => {
      synth.current.cancel();
    };
  }, [text]); // Dependency on 'text' means this effect runs whenever text changes

  const handlePlay = () => {
    if (isPaused) {
      synth.current.resume();
      setIsPaused(false);
    }
  };

  const handlePause = () => {
    if (!synth.current.paused && synth.current.speaking) {
      synth.current.pause();
      setIsPaused(true);
    }
  };

  const handleStop = () => {
    synth.current.cancel();
    setIsPaused(false);
  };

  return (
    <div>
      {/* The Play button now only resumes paused speech */}
      <button onClick={handlePlay} disabled={!isPaused}>
        {isPaused ? "Resume" : "Play"}
      </button>
      <button
        onClick={handlePause}
        disabled={!synth.current.speaking || isPaused}
      >
        Pause
      </button>
      <button
        onClick={handleStop}
        disabled={!synth.current.speaking && !isPaused}
      >
        Stop
      </button>
    </div>
  );
};

export default TextToSpeech;
