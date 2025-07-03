import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [videoUrl, setVideoUrl] = useState('');
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');
  const [downloadLink, setDownloadLink] = useState('');
  const [thumbnailUrl, setThumbnailUrl] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [downloadProgress, setDownloadProgress] = useState('0%');

  const handleDownload = async () => {
    setMessage('');
    setError('');
    setDownloadLink('');
    setThumbnailUrl(''); // Clear thumbnail on new download attempt
    setIsLoading(true);
    setDownloadProgress('0%'); // Reset progress on new download attempt

    try {
      const response = await fetch('http://localhost:5000/download', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url: videoUrl }),
      });

      const data = await response.json();

      if (response.ok) {
        setMessage(data.message);
        setDownloadLink(`http://localhost:5000/downloaded_files/${data.file_path}`);
        setThumbnailUrl(data.thumbnail_url);
      } else {
        setError(data.error);
      }
    } catch (err) {
      setError('Failed to connect to the backend server.');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    let intervalId;
    if (isLoading) {
      intervalId = setInterval(async () => {
        try {
          const response = await fetch('http://localhost:5000/progress');
          const data = await response.json();
          if (data.progress) {
            setDownloadProgress(data.progress);
          }
        } catch (err) {
          console.error('Error fetching progress:', err);
        }
      }, 1000); // Poll every 1 second
    } else {
      clearInterval(intervalId);
    }
    return () => clearInterval(intervalId);
  }, [isLoading]);

  return (
    <div className="App">
      <header className="App-header">
        <h1>Facebook Video Downloader</h1>
        <div className="input-container">
          <input
            type="text"
            placeholder="Enter Facebook video URL"
            value={videoUrl}
            onChange={(e) => setVideoUrl(e.target.value)}
          />
          <button onClick={handleDownload} disabled={isLoading}>{isLoading ? 'Downloading...' : 'Download'}</button>
        </div>
        {isLoading && <p className="loading-message">Downloading... {downloadProgress}</p>}
        {message && !isLoading && <p className="success-message">{message}</p>}
        {error && !isLoading && <p className="error-message">{error}</p>}
        {downloadLink && (
          <>
            {thumbnailUrl && <img src={thumbnailUrl} alt="Video Thumbnail" className="video-thumbnail" />}
            <a href={downloadLink} download className="download-link">
              Click here to download your video
            </a>
          </>
        )}
      </header>
    </div>
  );
}

export default App;
