import re

import fitz  # PyMuPDF
from .boxes_linkedin import column_boxes

def extract_text_from_pdf(pdf_path):
    """
    Extracts plain text content from a PDF document using PyMuPDF.

    Args:
        pdf_path (str): Path to the PDF file.

    Returns:
        str: Extracted text from the PDF.
    """
    doc = fitz.open(pdf_path)
    text = "Nom"

    for page in doc:
        bboxes = column_boxes(page, footer_margin=50, no_image_text=True)
        for rect in bboxes:
            text += page.get_text(clip=rect, sort=True)
        text += "-" * 20 + "\n"

    return text


def convert_linkedin_pdf_to_txt(
        pdf_path,
        output_txt_path="./formatted_resume.txt"
):
    """
    Converts a LinkedIn resume in PDF format to formatted text.

    Args:
        pdf_path (str): Path to the LinkedIn resume PDF.
        output_txt_path (str, optional): Output path for
        the formatted text file.
        Default is "./formatted_resume.txt".
    """
    # Extract text from PDF using PyMuPDF
    pdf_text = extract_text_from_pdf(pdf_path)

    # Create a dictionary to map section headers to their corresponding content
    sections = {
        "Nom": "Coordonnées",
        "Coordonnées": "Principales compétences",
        "Principales compétences": "Résumé",
        "Résumé": "Expérience",
        "Expérience": "Formation",
        "Formation": "Compétences Clés",
        "Compétences Clés": "Pour plus de détails \
        sur mon parcours et mes réalisations,\
         je vous invite à consulter mon site web :",
        "Pour plus de détails sur mon parcours et mes réalisations, \
        je vous invite à consulter mon site web :": ""
        # Assuming the last section continues until the end of the document
    }

    # Write the formatted content to a text file
    with open(output_txt_path, "w", encoding="utf-8") as txt_file:
        for section, next_section in sections.items():
            pattern = re.compile(
                re.escape(section) + r"(.*?)" + re.escape(next_section),
                re.DOTALL
            )
            match = pattern.search(pdf_text)
            if match:
                section_content = match.group(1).strip()

                # Print section and content (for debugging)
                # print(f'Section: {section}\nContent: {section_content}')

                # Write the formatted content to a text file
                txt_file.write(f"**{section}**\n\n{section_content}\n\n")


# Example usage:
# convert_linkedin_pdf_to_txt("path/to/linkedin_resume.pdf")
