# Fatigue Monitoring System

This project is a fatigue monitoring system that utilizes FastAPI for the backend and PyQt5 for the frontend. The system is designed to detect signs of fatigue through image recognition, leveraging a pre-trained model.

## Project Structure

```
fatigue_monitor_system
├── backend
│   ├── app.py                # Entry point for the FastAPI backend application
│   ├── models
│   │   └── detector.py       # Contains the Detector class for image recognition
│   ├── routes
│   │   └── api.py            # Defines API routes for handling requests
│   ├── utils
│   │   └── image_processing.py # Utility functions for image processing
│   ├── data.yaml             # Configuration file for model categories
│   ├── requirements.txt       # Python dependencies for the backend
│   └── README.md              # Documentation for the backend
├── frontend
│   ├── main.py               # Entry point for the PyQt5 frontend application
│   ├── ui
│   │   └── main_window.py     # UI layout definition for the main window
│   ├── widgets
│   │   ├── camera_widget.py   # Widget for displaying camera feed
│   │   ├── table_widget.py     # Widget for displaying recognition results
│   │   └── button_panel.py     # Widget for control buttons
│   ├── resources
│   │   └── icons              # Directory for icon resources
│   ├── utils
│   │   └── api_client.py      # Utility functions for API interaction
│   └── README.md              # Documentation for the frontend
└── README.md                  # Overall project documentation
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd fatigue_monitor_system
   ```

2. Install backend dependencies:
   ```
   cd backend
   pip install -r requirements.txt
   ```

3. Install frontend dependencies (if any):
   ```
   cd frontend
   # Add any frontend-specific installation commands here
   ```

## Usage

1. Start the backend server:
   ```
   cd backend
   uvicorn app:app --reload
   ```

2. Run the frontend application:
   ```
   cd frontend
   python main.py
   ```

3. Use the application to open images or the camera, start recognition, and view results.

## Features

- Image and camera input for fatigue detection
- Real-time recognition with confidence scores
- Historical results display with image snapshots

## License

This project is licensed under the MIT License. See the LICENSE file for details.