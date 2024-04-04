# Image Color Analyzer

This is a Python Flask application that allows users to upload images and analyze the dominant colors in the image using KMeans clustering algorithm. The application uses Flask framework for web development, Bootstrap for styling, and PIL (Python Imaging Library) for image processing.

## Features
- Allows users to upload images.
- Analyzes the dominant colors in the uploaded image.
- Displays the dominant colors and their occurrences as a JSON response.
- Provides a simple web interface for users to interact with.

## Installation
1. Clone the repository:
    ```bash
   git clone https://github.com/jakubswi/Image-Colour-Palette-Generator.git
    cd image-color-analyzer

2. Install the required dependencies:
    ```bash
   pip install -r requirements.txt

## Usage
1. Run the Flask application:
   ```bash
   python app.py

2. Open your web browser and go to `http://localhost:5000` to access the application.

3. Upload an image using the provided form.

4. Click the "Upload" button to analyze the dominant colors in the image.

5. The application will display the dominant colors and their occurrences as a JSON response.

## Configuration
- The Flask application uses a secret key for CSRF protection. You can modify the `SECRET_KEY` in the `app.py` file.
- Uploaded images are stored in the `uploads` directory. You can change the upload destination by modifying the `UPLOADED_PHOTOS_DEST` variable in the `app.py` file.

## Dependencies
- Flask
- Flask-Bootstrap
- Flask-Uploads
- Flask-WTF
- NumPy
- Pillow
- scikit-learn (sklearn)

## Contributing
Contributions are welcome! If you find any issues or have suggestions for improvements, please feel free to open an issue or create a pull request.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
