import os
from docx import Document
from docx.shared import Inches
from reportlab.pdfgen import canvas
from PIL import Image
from datetime import datetime

def create_word_document(folder_path, output_docx, title, author, conclusion):
    document = Document()

    # Add Header
    header = document.sections[0].header
    paragraph = header.paragraphs[0]
    run = paragraph.add_run()
    run.add_text("Header Text Here")
    paragraph.alignment = 1  # Center alignment

    # Add Title
    title_paragraph = document.add_heading(title, level=1)
    title_paragraph.alignment = 1  # Center alignment

    # Add Author and Date
    author_date = f"Author: {author} | Date: {datetime.now().strftime('%Y-%m-%d')}"
    document.add_paragraph(author_date)

    # Get a list of all image files in the specified folder
    image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

    for image_file in image_files:
        # Add a paragraph with the image name
        document.add_paragraph(f"Image: {image_file}")

        # Add the image to the document
        image_path = os.path.join(folder_path, image_file)
        document.add_picture(image_path, width=Inches(4))  # Adjust width as needed

        # Add a newline between images
        document.add_paragraph()

    # Add Conclusion
    document.add_heading("Conclusion", level=2)
    document.add_paragraph(conclusion)

    # Add Footer
    footer = document.sections[0].footer
    paragraph = footer.paragraphs[0]
    run = paragraph.add_run()
    run.add_text("Footer Text Here")
    paragraph.alignment = 1  # Center alignment

    # Save the document
    document.save(output_docx)
    print("Successfully saved the document")

#-----------------------------------

from reportlab.pdfgen import canvas
from PIL import Image
import os
def images_to_pdf(image_folder, pdf_path, title, copyright_notice):
    image_paths  = [os.path.join(image_folder, f) for f in os.listdir(image_folder) if f.lower().endswith((".png", ".jpg", ".jpeg"))]

    if not image_paths:
        print("No image files found.")
        return
    # Find the maximum width and height among all images
    max_width, max_height = max(Image.open(image_path).size for image_path in image_paths)
    c = canvas.Canvas(pdf_path, pagesize=(max_width, max_height))
    for idx, image_path in enumerate(image_paths):
        img = Image.open(image_path)
        img_width, img_height = img.size
        # Calculate the scaling factor to fit the image into the PDF
        scale_factor = min(max_width / img_width, max_height / img_height)
        # Calculate the position to center the image on the page
        x_position = (max_width - img_width * scale_factor) / 2
        y_position = (max_height - img_height * scale_factor) / 2
        # Draw the scaled image on the PDF
        c.drawInlineImage(image_path, x_position, y_position, img_width * scale_factor, img_height * scale_factor)
        # Add title in the center
        c.setFont("Helvetica", 16)
        c.drawCentredString(max_width / 2, max_height - 30, title)
        # Add copyright notice in the left corner
        c.setFont("Helvetica", 8)
        c.drawString(10, 10, copyright_notice)
        c.showPage()
    c.save()
    print("Successfully to Save the document")
# Example usage

