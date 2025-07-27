import os, glob, datetime
from fpdf import FPDF
from docx import Document
from dotenv import load_dotenv

load_dotenv()
SCROLL_DIR = os.getenv("FLAMEVAULT_PATH")

for docx_file in glob.glob(f"{SCROLL_DIR}/*.docx"):
    doc = Document(docx_file)
    text = "\n".join([p.text for p in doc.paragraphs if p.text.strip()])

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, os.path.basename(docx_file), ln=True, align='C')
    pdf.set_font("Arial", size=12)
    for line in text.split("\n"):
        pdf.multi_cell(0, 8, line)
    pdf.set_y(-15)
    pdf.set_font("Arial", "I", 8)
    pdf.cell(0, 10, f"FlameSeal: {datetime.datetime.utcnow().isoformat()}Z", 0, 0, 'C')
    output_pdf = docx_file.replace('.docx', '.pdf')
    pdf.output(output_pdf)
