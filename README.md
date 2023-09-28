

# Flask Application

This is a Flask application that blur pesel from provided image

## Prerequisites

Before running this application, you'll need the following installed on your system:

- Python 3.x
- pip (Python package manager)

## Setup

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/DawidWK/PESEL-blur.git
   ```

2. Navigate to the project directory:

   ```bash
   cd PESEL-blur
   ```

3. Create a virtual environment (recommended) to isolate project dependencies:

   ```bash
   python -m venv venv
   ```

4. Activate the virtual environment:

   - On Windows:

     ```bash
     venv\Scripts\activate
     ```

   - On macOS and Linux:

     ```bash
     source venv/bin/activate
     ```

5. Install the project dependencies from `requirements.txt`:

   ```bash
   pip install -r requirements.txt
   ```

## Tesseract Installation

This application uses Tesseract for text recognition. To install Tesseract:

### Windows

1. Download the Tesseract installer from the following link:

   [Tesseract Installer for Windows](https://github.com/UB-Mannheim/tesseract/wiki)

2. Run the installer and follow the installation instructions.

### macOS

```bash
brew install tesseract
```

### Linux (Ubuntu/Debian)

```bash
sudo apt-get install tesseract-ocr
```

### Verify Tesseract Installation

After installing Tesseract, verify the installation by running the following command:

```bash
tesseract --version
```

## Running the Application

To run the Flask application:

```bash
python app.py
```

The application will start, and you can access it in your web browser at `http://localhost:8000`.
