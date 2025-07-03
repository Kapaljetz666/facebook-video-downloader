# Facebook Video Downloader

This is a simple web application that allows you to download Facebook videos by providing their URL. It consists of a Python Flask backend for handling video downloads and a React.js frontend for the user interface.

## Features

*   Download Facebook videos by URL.
*   Displays video thumbnail before download.
*   Shows real-time download progress (percentage).
*   Downloads the best available video and audio quality, then merges them into an MP4 file.

## Technologies Used

### Backend (Python Flask)

*   **Flask:** A micro web framework for Python.
*   **Flask-CORS:** A Flask extension for handling Cross Origin Resource Sharing (CORS), making cross-origin AJAX possible.
*   **yt-dlp:** A command-line program to download videos from YouTube.com and other video sites (used for Facebook video extraction and download).
*   **FFmpeg:** A complete, cross-platform solution to record, convert and stream audio and video (required by `yt-dlp` for merging video and audio streams).

### Frontend (React.js)

*   **React:** A JavaScript library for building user interfaces.
*   **Create React App:** A comfortable environment for learning React, and is the best way to start building a new single-page application in React.
*   **HTML/CSS:** For structuring and styling the web interface.

## Setup Instructions

Follow these steps to set up and run the Facebook Video Downloader on your local machine.

### Prerequisites

*   **Python 3.x:** Make sure you have Python installed.
*   **Node.js & npm:** Make sure you have Node.js and npm (Node Package Manager) installed.
*   **FFmpeg:** `yt-dlp` requires FFmpeg to merge video and audio streams. Download and install FFmpeg, and ensure it's added to your system's PATH environment variable. You can find instructions [here](https://ffmpeg.org/download.html).

### 1. Clone the Repository (or create the project structure)

If you're starting from scratch, ensure you have the following directory structure:

```
facebook-downloader/
├── backend/
│   ├── app.py
│   └── requirements.txt
└── frontend/
    ├── public/
    ├── src/
    ├── package.json
    └── ... (other React files)
```

### 2. Backend Setup

Navigate to the `backend` directory and install the required Python packages:

```bash
cd facebook-downloader/backend
pip install -r requirements.txt
```

### 3. Frontend Setup

Navigate to the `frontend` directory and install the required Node.js packages:

```bash
cd facebook-downloader/frontend
npm install
```

## Usage

### 1. Start the Backend Server

Open a terminal or command prompt, navigate to the `backend` directory, and run the Flask application:

```bash
cd facebook-downloader/backend
python app.py
```

Leave this terminal open. The backend server will be running on `http://localhost:5000`.

### 2. Start the Frontend Development Server

Open a **new** terminal or command prompt, navigate to the `frontend` directory, and start the React development server:

```bash
cd facebook-downloader/frontend
npm start
```

This will open the application in your default web browser (usually `http://localhost:3000`).

### 3. Download a Video

1.  In your web browser, enter the Facebook video URL into the input field.
2.  Click the "Download" button.
3.  You will see a "Downloading..." message with a percentage progress.
4.  Once the download is complete, a "Request successful" message will appear, along with the video thumbnail and a link to download the video.

Downloaded videos will be saved in the `facebook-downloader/backend/downloads` directory on your server, and then served to your browser for download.

## License

This project is open-source and available under the MIT License. (You can change this to your preferred license.)
