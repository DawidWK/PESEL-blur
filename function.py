import pytesseract
import datetime
from PIL import Image, ImageFilter, ImageDraw
from openai import OpenAI
import json


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


def validate_pesel_by_openai(pesel):
    client = OpenAI()

    completion = client.chat.completions.create(
    model="gpt-3.5-turbo-1106",
    messages=[
        {
        "role": "system", 
        "content": """
            Jesteś asystentem który ma za zadanie wykrywać czy podany wyraz jest daną wrażliwą np PESEL'em albo numerem dowodu.

            Odpowiedź w formacie JSON:
            {
            is_sensitive_data: true;
            data: "pesel"
            }
            """
        },
        {"role": "user", "content": f"${pesel}"}
    ],
    response_format={ "type": "json_object" }
    )

    output = json.loads(completion.choices[0].message.content)
    import pdb; pdb.set_trace()
    return output.get('is_sensitive_data', False)


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


def process_image_with_pesel_blur(image, validate_with_openai=False):
    # Find and store the text regions that match the PESEL pattern
    pesel_regions = []
    # Use pytesseract to get the bounding box of the text
    data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
    for index, data_text in enumerate(data['text']):
        if data_text == '':
            continue
        
        if validate_with_openai:
            is_pesel = validate_pesel_by_openai(data_text)
        else:
            is_pesel = validate_pesel(data_text)
        if is_pesel:
            x, y, w, h = data['left'][index], data['top'][index], data['width'][index], data['height'][index]
            pesel_regions.append((x, y, w, h))
    
    # Blur the PESEL regions in the image
    blurred_image = blur_text_regions(image, pesel_regions)
    
    return blurred_image