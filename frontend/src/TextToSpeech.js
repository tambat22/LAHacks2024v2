import React, { useState, useEffect, useRef } from "react";

const TextToSpeech = ({ text }) => {
  const [isPaused, setIsPaused] = useState(false);
  const synth = useRef(window.speechSynthesis);
  const utterance = useRef(null);

  useEffect(() => {
    utterance.current = new SpeechSynthesisUtterance(text);
    utterance.current.onend = () => {
      console.log("Finished in speaking");
    };

    // Clean up on component unmount or text change
    return () => {
      synth.current.cancel();
    };
  }, [text]);

  const handlePlay = () => {
    if (isPaused) {
      synth.current.resume();
    } else {
      synth.current.speak(utterance.current);
    }

    setIsPaused(false);
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
      <button onClick={handlePlay}>{isPaused ? "Resume" : "Play"}</button>
      <button onClick={handlePause}>Pause</button>
      <button onClick={handleStop}>Stop</button>
    </div>
  );
};

export default TextToSpeech;
