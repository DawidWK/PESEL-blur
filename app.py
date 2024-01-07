from flask import Flask, request, render_template, send_file
from PIL import Image
from io import BytesIO

from function import process_image_with_pesel_blur

app = Flask(__name__)

VALIDATE_WIGH_OPENAI = False

@app.route('/', methods=['GET', 'POST'])
def upload_and_process():
    if request.method == 'POST':
        uploaded_file = request.files['file']
        
        is_image = uploaded_file.filename != '' and (uploaded_file.filename.endswith('.png') or uploaded_file.filename.endswith('.jpg') or uploaded_file.filename.endswith('.jpeg'))
        
        if is_image:
            img = Image.open(uploaded_file)
            blurred_image = process_image_with_pesel_blur(img, VALIDATE_WIGH_OPENAI)            
        
            # Save the image to a BytesIO object.
            img_io = BytesIO()
            blurred_image.save(img_io, 'PNG')
            img_io.seek(0)

            # Send the image as an attachment for download
            return send_file(img_io, as_attachment=True, download_name=f'{uploaded_file.filename}-processed.png', mimetype='image/png')
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)