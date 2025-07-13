# analyzer/file_reporter.py

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit
import os

def generate_pdf_report(results, output_path="data/match_report.pdf"):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4
    y = height - 40
    max_width = width - 80  # Margins
    line_height = 14

    def draw_wrapped(text, font="Helvetica", size=10, y_offset=0):
        nonlocal y
        c.setFont(font, size)
        wrapped = simpleSplit(text, font, size, max_width)
        for line in wrapped:
            if y < 60:
                c.showPage()
                y = height - 40
                c.setFont(font, size)
            c.drawString(40, y, line)
            y -= line_height
        y -= y_offset

    c.setFont("Helvetica-Bold", 16)
    c.drawString(40, y, "🔐 LeakTrace-AI++ File Similarity Report")
    y -= 30

    for result in results:
        if y < 100:
            c.showPage()
            y = height - 40

        leaked_file = os.path.basename(result.get('leaked', 'Unknown'))
        matched_file = result.get('matched', 'No match found')
        matched_file_name = os.path.basename(matched_file) if matched_file != 'No match found' else matched_file

        draw_wrapped(f"📁 Leaked File: {leaked_file}", font="Helvetica-Bold", size=12)
        draw_wrapped(f"✅ Matched With: {matched_file_name}")
        draw_wrapped(f"📊 Similarity Score: {result.get('score', 'N/A')}%")

        snippet = result.get('text', 'No text found').replace("\n", " ").strip()
        snippet_preview = snippet[:500] + "..." if len(snippet) > 500 else snippet
        draw_wrapped(f"📝 Text Snippet: {snippet_preview}", y_offset=10)

        if "error" in result:
            c.setFillColorRGB(1, 0, 0)
            draw_wrapped(f"⚠️ Error: {result['error']}")
            c.setFillColorRGB(0, 0, 0)

        c.line(40, y, width - 40, y)
        y -= 20

    c.save()
    return output_path
