"""Convert DOCX scrolls into signed PDF documents."""

import os
import glob
import datetime
import argparse
from fpdf import FPDF
from docx import Document
from dotenv import load_dotenv

load_dotenv()
SCROLL_DIR = os.getenv("FLAMEVAULT_PATH")

if not SCROLL_DIR:
    raise EnvironmentError(
        "Required environment variable FLAMEVAULT_PATH is missing."
    )

parser = argparse.ArgumentParser(
    description="Generate PDFs from DOCX files found in FLAMEVAULT_PATH"
)
parser.add_argument(
    "--out",
    dest="output_dir",
    default=SCROLL_DIR,
    help="Directory to write generated PDFs",
)
args = parser.parse_args()

os.makedirs(args.output_dir, exist_ok=True)

for docx_file in glob.glob(f"{SCROLL_DIR}/*.docx"):
    """Convert each DOCX file to a PDF with a timestamp footer."""

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
    basename = os.path.splitext(os.path.basename(docx_file))[0]
    output_pdf = os.path.join(args.output_dir, f"{basename}.pdf")
    pdf.output(output_pdf)
