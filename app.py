import base64
from flask import Flask, request, render_template, send_file
from PIL import Image
from io import BytesIO

from function import get_text_from_image_gpt_vision, get_text_from_image_gpt_vision_with_position, process_image_with_pesel_blur

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def upload_and_process():
    if request.method == 'POST':
        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            img = Image.open(uploaded_file)

            # Convert the original image to base64
            buffered = BytesIO()
            img.save(buffered, format="PNG")
            original_img_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')

            # Call the function that requires base64-encoded image
            words = get_text_from_image_gpt_vision(original_img_base64)
            output = words['choices'][0]['message']['content']
            output = output.replace("`", "")
            output = output.replace("json", "")

            import pdb; pdb.set_trace()
            blurred_image = process_image_with_pesel_blur(img)            
        
            # Save the image to a BytesIO object.
            img_io = BytesIO()
            blurred_image.save(img_io, 'PNG')
            img_io.seek(0)

            # Send the image as an attachment for download
            return send_file(img_io, as_attachment=True, download_name=f'{uploaded_file.filename}-processed.png', mimetype='image/png')
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)