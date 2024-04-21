import React, { useCallback, useState, useEffect, useRef } from 'react';
import Webcam from "react-webcam";
import axios from 'axios';
import ImageUploading from 'react-images-uploading';
import { debounce } from 'lodash';
import TextToSpeech from './TextToSpeech';

const CustomWebcam = () => {
  const webcamRef = useRef(null);
  const [imgSrc, setImgSrc] = useState(null);
  const [images, setImages] = useState([]);
  const [responseText, setResponseText] = useState('');

  // Debounced function to send image to server
  const sendImageToServer = useCallback(debounce((imageFile) => {
    const formData = new FormData();
    formData.append("file", imageFile);

    axios.post('http://localhost:5000/upload/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
    })
    .then(response => {
      console.log("response from server", response.data);
      const responseText = response.data["description"]; // Assume 'text' is the key in the response data containing the text
      const is_dangerous = response.data["is_dangerous"];
      console.log('Image uploaded successfully:', responseText);
      setResponseText(responseText); // Update the state to trigger TextToSpeech
    })
    .catch(error => {
      console.error('Error uploading image:', error);
      setResponseText("Failed to upload image."); // Set error message for TTS
    });
  }, 300), []); // Empty dependency array ensures the function is not recreated on each render

  const captureAndSend = useCallback(() => {
    if (webcamRef.current) {
      const imageSrc = webcamRef.current.getScreenshot();
      setImgSrc(imageSrc);
      if (imageSrc) {
        fetch(imageSrc)
          .then(res => res.blob())
          .then(blob => {
            const file = new File([blob], "webcam.jpeg", { type: "image/jpeg" });
            sendImageToServer(file);
          });
      }
    }
  }, [sendImageToServer]);

  useEffect(() => {
    images.forEach(image => {
      sendImageToServer(image.file);
    });
  }, [images, sendImageToServer]);

  const onImageChange = (imageList, addUpdateIndex) => {
    setImages(imageList);
  };

  return (
    <div className="container">
      <Webcam
        audio={false}
        height={600}
        width={600}
        mirrored={false}
        ref={webcamRef}
        screenshotFormat="image/jpeg"
      />
      {imgSrc && <img src={imgSrc} alt="Captured" style={{ width: "100%" }} />}
      <div className="btn-container">
        <button onClick={captureAndSend}>Capture and Send Photo</button>
      </div>
      <ImageUploading
        multiple={false}
        value={images}
        onChange={onImageChange}
        maxNumber={1}
        dataURLKey="data_url"
      >
        {({ onImageUpload }) => (
          <button onClick={onImageUpload}>Browse</button>
        )}
      </ImageUploading>
      <TextToSpeech text={responseText} />
    </div>
  );
};

export default CustomWebcam;
