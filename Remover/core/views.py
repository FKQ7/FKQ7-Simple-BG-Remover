from django.shortcuts import render
from PIL import Image
from io import BytesIO
from rembg import remove
import base64

def main(request):
    html_content = None  
    
    if request.method == 'POST' and request.FILES.get('image'):
        # get the uploaded image
        uploaded_image = request.FILES['image']
        
        # load the image
        input_image = Image.open(uploaded_image)
        
        # Remove the background
        output_image = remove(input_image)
        
        # Convert the processed image to a base64-encoded string
        buffered_output = BytesIO()
        output_image.save(buffered_output, format="PNG")
        encoded_output = base64.b64encode(buffered_output.getvalue()).decode('utf-8')
        
        # Embed the base64-encoded image in HTML
        html_content = f'<h2>Processed Image</h2><img src="data:image/png;base64,{encoded_output}" />'
        
    # Else
    return render(request, 'index.html', {'html_content': html_content})
