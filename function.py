import pytesseract
import datetime
from PIL import Image, ImageFilter, ImageDraw
import base64
import requests

# OpenAI API Key
api_key = "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"

def validate_pesel(pesel):
    """Returns True if PESEL is valid, False otherwise"""
    if len(pesel) != 11:
        return False

    # Checksum validation
    
    # check if pesel is a number
    if not pesel.isdigit():
        return False
    
    weights = [1, 3, 7, 9, 1, 3, 7, 9, 1, 3, 1]
    checksum = sum(int(pesel[i]) * weights[i] for i in range(11)) % 10
    if checksum != 0:
        return False

    # Date of bith validation
    year = int(pesel[0:2])
    month = int(pesel[2:4])
    day = int(pesel[4:6])

    if month > 80:
        year += 1800
        month -= 80
    elif month > 60:
        year += 2200
        month -= 60
    elif month > 40:
        year += 2100
        month -= 40
    elif month > 20:
        year += 2000
        month -= 20
    else:
        year += 1900

    try:
        birth_date = datetime.date(year, month, day)
    except ValueError:
        return False

    # Serial number validation
    serial_number = int(pesel[6:9])
    if serial_number == 0:
        return False

    return True


def blur_text_regions(image, text_regions):
    # Create a copy of the input image to work on
    blurred_image = image.copy()
    
    # Apply a Gaussian blur to the specified text regions
    for region in text_regions:
        x, y, w, h = region
        text_area = image.crop((x, y, x + w, y + h))
        blurred_text_area = text_area.filter(ImageFilter.GaussianBlur(radius=10))
        blurred_image.paste(blurred_text_area, (x, y))

    return blurred_image


def process_image_with_pesel_blur(image):
    # Find and store the text regions that match the PESEL pattern
    pesel_regions = []
    # Use pytesseract to get the bounding box of the text
    data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
    for index, data_text in enumerate(data['text']):
        if validate_pesel(data_text):
            x, y, w, h = data['left'][index], data['top'][index], data['width'][index], data['height'][index]
            pesel_regions.append((x, y, w, h))
    
    # Blur the PESEL regions in the image
    blurred_image = blur_text_regions(image, pesel_regions)
    
    return blurred_image


def get_text_from_image_gpt_vision(base64_image):

    headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
    }

    payload = {
    "model": "gpt-4-vision-preview",
    "messages": [
        {
        "role": "user",
        "content": [
            {
            "type": "text",
            "text": """
            Return me all the words from the image. Your response must  be in valid JSON format.
            
            Example:
            {
                'words': [
                    'Hello', 
                    'Word', 
                    '79920432', 
                    '0204412344', 
                    '1234567890',
                ]
            }
            """
            },
            {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image}"
            }
            }
        ]
        }
    ],
    "max_tokens": 300
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    return response.json()

def get_text_from_image_gpt_vision_with_position(base64_image):

    headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
    }

    payload = {
    "model": "gpt-4-vision-preview",
    "messages": [
        {
        "role": "user",
        "content": [
            {
            "type": "text",
            "text": """
            Return me all the words from the image and its coresponding position on image. Your response must  be in valid JSON format.
            
            Example:
            {
                words: {
                    'Hello': {'x': 100, 'y': 200, 'w': 50, 'h': 50} 
                    'Word': {'x': 300, 'y': 230, 'w': 140, 'h': 350}, 
                    '79920432': {'x': 140, 'y': 650, 'w': 150, 'h': 150}, 
                    '0204412344' {'x': 500, 'y': 500, 'w': 450, 'h': 50}, 
                    '1234567890' {'x': 200, 'y': 700, 'w': 350, 'h': 250},
                }
            }
            """
            },
            {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image}"
            }
            }
        ]
        }
    ],
    "max_tokens": 300
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    return response.json()

import cv2
import numpy as np
import tensorflow as tf

def load_image(image_path):
    # Load and preprocess the image as before
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = cv2.resize(image, (128, 32))
    image = np.expand_dims(image, axis=-1)
    image = np.expand_dims(image, axis=0)
    return image

def load_trained_model(model_path):
    # Load the trained model
    return tf.keras.models.load_model(model_path)

def decode_prediction(prediction, vocab):
    # Decode the prediction as before
    decoded = tf.keras.backend.ctc_decode(prediction, input_length=np.ones(prediction.shape[0])*prediction.shape[1])[0][0]
    out = tf.keras.backend.get_value(decoded)
    text = ''.join([vocab[x] for x in out[0]])  # Convert to string
    return text

# Load your image
image_path = '/Users/wlodeksowa/Code/workationinit_blog/public/survey.png'
image = load_image(image_path)

# Load your trained model
model_path = '/models/model.h5'
model = load_trained_model(model_path)

# Define your vocabulary
vocab = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"

# Make a prediction
prediction = model.predict(image)
text = decode_prediction(prediction, vocab)

print("Recognized text:", text)
