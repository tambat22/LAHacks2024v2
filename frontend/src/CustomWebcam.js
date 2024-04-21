import React, { useCallback, useState, useEffect, useRef } from 'react';
import Webcam from "react-webcam";
import axios from 'axios';
import ImageUploading from 'react-images-uploading';
import { debounce } from 'lodash';

const CustomWebcam = () => {
  const webcamRef = useRef(null);
  const [imgSrc, setImgSrc] = useState(null);
  const [images, setImages] = useState([]);

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
    })
    .catch(error => {
      console.error('Error uploading image:', error);
    });
  };

  const debouncedSendImage = debounce(sendImageToServer, 300);

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
  }, []);

  useEffect(() => {
    images.forEach(image => {
      debouncedSendImage(image.file);
    });
  }, [images]);

  const onImageChange = (imageList, addUpdateIndex) => {
    setImages(imageList);
  };

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
        {({ onImageUpload, onImageRemoveAll }) => (
          <div className="upload__image-wrapper">
            <button onClick={onImageUpload}>Browse</button>
            {images.map((image, index) => (
              <div key={index} className="image-item">
                <img src={image.data_url} alt="" width="100" />
                <button onClick={onImageRemoveAll}>Remove</button>
              </div>
            ))}
          </div>
        )}
      </ImageUploading>
    </div>
  );
};

export default CustomWebcam;
