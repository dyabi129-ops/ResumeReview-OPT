"""
PDF Exporter - fixed version using cell width calculation
"""
from fpdf import FPDF

def export_resume_as_pdf(resume_text: str) -> bytes:
    pdf = FPDF(format='A4')
    pdf.add_page()
    pdf.set_left_margin(20)
    pdf.set_right_margin(20)
    pdf.set_top_margin(20)
    pdf.set_auto_page_break(auto=True, margin=20)

    usable_w = 210 - 20 - 20  # A4 width minus margins = 170mm

    # Sanitize unicode characters Helvetica can't render
    resume_text = resume_text.replace("•", "-").replace("\u2022", "-").replace("\u2013", "-").replace("\u2014", "--").replace("\u2018", "'").replace("\u2019", "'").replace("\u201c", '"').replace("\u201d", '"')

    lines = resume_text.split("\n")
    for line in lines:
        line = line.strip()
        if not line:
            pdf.ln(3)
            continue

        is_header = (line.isupper() and 3 < len(line) < 60) or \
                    (line.endswith(":") and len(line) < 50 and line[0].isupper())

        if is_header:
            pdf.ln(3)
            pdf.set_font("Helvetica", style="B", size=11)
            pdf.set_text_color(0, 0, 0)
            pdf.multi_cell(usable_w, 7, line)
            pdf.set_draw_color(100, 100, 100)
            pdf.set_line_width(0.3)
            pdf.line(20, pdf.get_y(), 190, pdf.get_y())
            pdf.ln(2)
        elif line.startswith(("•", "-", "*")):
            pdf.set_font("Helvetica", size=10)
            pdf.set_text_color(40, 40, 40)
            clean = line.lstrip("•-* ").strip()
            pdf.set_x(25)
            pdf.multi_cell(usable_w - 5, 5.5, "- " + clean)
        else:
            pdf.set_font("Helvetica", size=10)
            pdf.set_text_color(40, 40, 40)
            pdf.multi_cell(usable_w, 5.5, line)

    return bytes(pdf.output())
