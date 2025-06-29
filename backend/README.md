# Fatigue Monitoring System

This project is a fatigue monitoring system that utilizes FastAPI for the backend and PyQt5 for the frontend. The system is designed to detect signs of fatigue through image recognition, leveraging a pre-trained model.

## Project Structure

The project is organized into two main directories: `backend` and `frontend`.

### Backend

- **app.py**: Entry point for the backend application. It sets up the FastAPI server and routes.
- **models/detector.py**: Contains the `Detector` class responsible for loading the model and performing image recognition.
- **routes/api.py**: Defines the API routes that handle requests from the frontend and return recognition results.
- **utils/image_processing.py**: Includes utility functions for image processing, such as reading and preprocessing images.
- **data.yaml**: Configuration file that contains the model's recognition categories and paths.
- **requirements.txt**: Lists the Python dependencies required for the backend.

### Frontend

- **main.py**: Entry point for the frontend application. It initializes the main window and starts the PyQt5 application.
- **ui/main_window.py**: Defines the layout of the main window, including buttons and the camera/results area.
- **widgets/camera_widget.py**: Implements the camera widget that displays the camera feed.
- **widgets/table_widget.py**: Implements the results table widget that shows recognition results, including ID, category, position, confidence, and captured images.
- **widgets/button_panel.py**: Implements the button panel widget with functionalities to open images, start recognition, clear history, and exit the application.
- **resources/icons**: Directory for storing icon resources used in the project.
- **utils/api_client.py**: Contains utility functions for interacting with the backend API, sending requests, and processing responses.

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd fatigue_monitor_system
   ```

2. Install the required dependencies:
   ```
   pip install -r backend/requirements.txt
   ```

## Usage

1. Start the backend server:
   ```
   python backend/app.py
   ```

2. Run the frontend application:
   ```
   python frontend/main.py
   ```

3. Use the buttons on the left side of the interface to interact with the system:
   - Open an image
   - Open the camera
   - Start recognition
   - Clear history
   - Exit the system

## License

This project is licensed under the MIT License.