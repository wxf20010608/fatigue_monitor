# Fatigue Monitoring System Frontend

This project is a fatigue monitoring system that utilizes FastAPI for the backend and PyQt5 for the frontend. The system is designed to detect signs of fatigue through image recognition and provides a user-friendly interface for interaction.

## Project Structure

- **frontend/**
  - **main.py**: Entry point for the frontend application, initializes the main window and starts the application.
  - **ui/**
    - **main_window.py**: Defines the layout of the main window, including the button panel and display areas.
  - **widgets/**
    - **camera_widget.py**: Displays the camera feed.
    - **table_widget.py**: Shows the results of the recognition, including ID, category, recognition position, confidence, and captured images.
    - **button_panel.py**: Contains buttons for opening images, starting recognition, clearing history, and exiting the application.
  - **resources/**
    - **icons/**: Contains icon resources used in the application.
  - **utils/**
    - **api_client.py**: Handles communication with the backend API, sending requests and processing responses.

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd fatigue_monitor_system
   ```

2. Install the required dependencies:
   ```
   pip install -r ../backend/requirements.txt
   ```

## Usage

1. Start the backend server:
   ```
   cd backend
   uvicorn app:app --reload
   ```

2. Run the frontend application:
   ```
   cd ../frontend
   python main.py
   ```

3. Use the buttons on the left side of the interface to interact with the system:
   - **Open Image**: Load an image for recognition.
   - **Open Camera**: Start the camera feed.
   - **Start Recognition**: Begin the fatigue detection process using the loaded image or camera feed.
   - **Clear History**: Reset the results table.
   - **Exit System**: Close the application.

## Acknowledgments

This project leverages FastAPI for efficient backend development and PyQt5 for a responsive user interface. Special thanks to the contributors and libraries that made this project possible.