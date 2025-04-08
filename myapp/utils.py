import fitz  # PyMuPDF
import os
from pdf2image import convert_from_path
from django.conf import settings
from .models import BookPage

def convert_pdf_to_images(book):
    pdf_path = os.path.join(settings.MEDIA_ROOT, str(book.book_file))
    output_folder = os.path.join(settings.MEDIA_ROOT, 'book_pages', str(book.id))

    # Create directory if not exists
    os.makedirs(output_folder, exist_ok=True)

    # Convert PDF to images
    images = convert_from_path(pdf_path, poppler_path=r'C:\Program Files\poppler-24.08.0\Library\bin')  # Update poppler path if needed

    # Save each image as a BookPage
    for i, image in enumerate(images):
        image_path = os.path.join(output_folder, f"page_{i + 1}.jpg")
        image.save(image_path, "JPEG")

        # Save record in BookPage model
        BookPage.objects.create(
            book=book,
            page_number=i + 1,
            image=f"book_pages/{book.id}/page_{i + 1}.jpg"
        )
