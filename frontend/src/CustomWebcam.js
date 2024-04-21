import React, { useCallback, useState, useRef, useEffect } from 'react';
import Webcam from "react-webcam";
import axios from 'axios';
import ImageUploading from 'react-images-uploading';

const CustomWebcam = () => {
  const webcamRef = useRef(null);
  const [imgSrc, setImgSrc] = useState(null);
  const [images, setImages] = useState([]);
  const [isSendingAutomatically, setIsSendingAutomatically] = useState(false);
  const [sendIntervalId, setSendIntervalId] = useState(null);
  const synthRef = useRef(window.speechSynthesis);

  const capture = useCallback(() => {
    if (webcamRef.current) {
      const imageSrc = webcamRef.current.getScreenshot();
      setImgSrc(imageSrc);
      return imageSrc;
    }
  }, []);

  const sendImageToServer = (imageFile) => {
    const formData = new FormData();
    formData.append("file", imageFile);
    axios.post('http://localhost:5000/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
    })
    .then(response => {
      console.log('Image uploaded successfully:', response.data);
      speak(response.data.message);
    })
    .catch(error => {
      console.error('Error uploading image:', error);
    });
  };

  const speak = (text) => {
    if (synthRef.current.speaking) {
      console.log("Speech synthesis in progress, waiting...");
      setTimeout(() => speak(text), 100); // Retry after a short delay
      return;
    }
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.onend = () => {
      console.log("Finished in speaking...");
      handleAutomaticCapture();
    };
    synthRef.current.speak(utterance);
  };

  const handleAutomaticCapture = useCallback(() => {
    if (!synthRef.current.speaking) {
      const imageSrc = capture();
      if (imageSrc) {
        fetch(imageSrc)
          .then(res => res.blob())
          .then(blob => {
            const file = new File([blob], "webcam.jpeg", { type: "image/jpeg" });
            sendImageToServer(file);
          });
      }
    } else {
      console.log("Waiting for speech to finish before capturing next image...");
    }
  }, [capture]);

  const handleSendAutomaticallyToggle = () => {
    setIsSendingAutomatically(!isSendingAutomatically);
    if (!isSendingAutomatically) {
      handleAutomaticCapture(); // Start the first capture immediately
    } else {
      if (sendIntervalId) {
        clearInterval(sendIntervalId);
      }
    }
  };

  useEffect(() => {
    return () => {
      if (sendIntervalId) {
        clearInterval(sendIntervalId);
      }
    };
  }, [sendIntervalId]);

  return (
    <div className="container">
      <Webcam
        audio={false}
        height={600}
        width={600}
        ref={webcamRef}
        screenshotFormat="image/jpeg"
      />
      {imgSrc && <img src={imgSrc} alt="Captured" style={{ width: "100%" }} />}
      <button onClick={handleSendAutomaticallyToggle}>
          {isSendingAutomatically ? 'Stop Automatic Sending' : 'Start Automatic Sending'}
      </button>
      <ImageUploading
        multiple={false}
        value={images}
        onChange={(imageList) => {
          if (imageList.length > 0) {
            sendImageToServer(imageList[0].file);
          }
        }}
        maxNumber={1}
        dataURLKey="data_url"
      >
        {({ onImageUpload }) => (
          <button onClick={onImageUpload}>Browse</button>
        )}
      </ImageUploading>
    </div>
  )
};

export default CustomWebcam;