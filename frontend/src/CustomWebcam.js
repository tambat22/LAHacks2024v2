import React, { useCallback, useState, useRef } from 'react';
import Webcam from "react-webcam";
import axios from 'axios';

const CustomWebcam = () => {
  const webcamRef = useRef(null);
  const [imgSrc, setImgSrc] = useState(null);
  const capture = useCallback((gi) => {
    const imageSrc = webcamRef.current.getScreenshot();
    setImgSrc(imageSrc);
  }, [webcamRef]);

  const sendImageToServer = () => {
    if (!imgSrc) {
      alert("No image captured.");
      return;
    }

    // Convert Base64 image to a file object
    const blob = fetch(imgSrc).then(res => res.blob()).then(blob => {
      const file = new File([blob], "filename.jpeg", { type: "image/jpeg" });

      const formData = new FormData();
      formData.append("file", file);

      axios.post('http://127.0.0.1:5000/upload/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      .then(response => {
        console.log('Image uploaded successfully:', response.data);
      })
      .catch(error => {
        console.error('Error uploading image:', error);
      });
    });
  };

  return (
    <div className="container">
      {imgSrc ? (
        <img src={imgSrc} alt="Captured" />
      ) : (
        <Webcam
          audio={false}
          height={600}
          width={600}
          ref={webcamRef}
          screenshotFormat="image/jpeg"
        />
      )}
      <div className="btn-container">
        <button onClick={capture}>Capture photo</button>
        <button onClick={sendImageToServer}>Send to Server</button>
      </div>
    </div>
  );
};

export default CustomWebcam;