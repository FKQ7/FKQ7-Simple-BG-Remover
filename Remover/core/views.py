from django.shortcuts import render
from django.http import JsonResponse
from PIL import Image
from io import BytesIO
from rembg import remove
import base64
from .models import ImageUpload

def main(request):
    # Retrieve or create ImageUpload object
    image_upload, created = ImageUpload.objects.get_or_create(pk=1)

    # Increment upload count if image is uploaded
    if request.method == 'POST' and request.FILES.get('image'):
        uploaded_image = request.FILES['image']
        input_image = Image.open(uploaded_image)
        output_image = remove(input_image)
        buffered_output = BytesIO()
        output_image.save(buffered_output, format="PNG")
        encoded_output = base64.b64encode(buffered_output.getvalue()).decode('utf-8')
        html_content = f'<h2>Processed Image</h2><img src="data:image/png;base64,{encoded_output}" />'
        
        # Update upload count
        image_upload.upload_count += 1
        image_upload.save()
    else:
        html_content = None
    
    # Track visitor count using session
    visitor_count = request.session.get('visitor_count', 0)
    request.session['visitor_count'] = visitor_count + 1

    return render(request, 'index.html', {'html_content': html_content, 'upload_count': image_upload.upload_count, 'visitor_count': request.session['visitor_count']})
