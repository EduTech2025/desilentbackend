# views.py
import io
from rembg import remove
from PIL import Image
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework import status
from django.http import FileResponse


class RemoveImageBackground(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):
        image_file = request.FILES.get("image")

        if not image_file:
            return Response({"error": "No image file provided."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Open the uploaded image
            input_image = Image.open(image_file)

            # Convert to RGBA if not already
            if input_image.mode != "RGBA":
                input_image = input_image.convert("RGBA")

            # Remove background
            output_image = remove(input_image)

            # Save result to memory
            buffer = io.BytesIO()
            output_image.save(buffer, format="PNG")
            buffer.seek(0)

            return FileResponse(buffer, content_type="image/png")
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
