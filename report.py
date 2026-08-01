from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import os

def generate_report(result):

    os.makedirs("reports", exist_ok=True)

    pdf_file = "reports/Security_Report.pdf"

    doc = SimpleDocTemplate(pdf_file)

    styles = getSampleStyleSheet()

    story = []

    story.append(Paragraph("<b>Security Log Analysis Report</b>", styles['Title']))

    story.append(Paragraph(f"Total Logs : {result['total_logs']}", styles['Normal']))
    story.append(Paragraph(f"Failed Logins : {result['failed_logins']}", styles['Normal']))
    story.append(Paragraph(f"Admin Access : {result['admin_access']}", styles['Normal']))
    story.append(Paragraph(f"404 Errors : {result['error_404']}", styles['Normal']))
    story.append(Paragraph(f"500 Errors : {result['error_500']}", styles['Normal']))
    story.append(Paragraph(f"Threat Level : {result['threat_level']}", styles['Normal']))

    story.append(Paragraph("<br/><b>Suspicious IP Addresses</b>", styles['Heading2']))

    if result["suspicious_ips"]:
        for ip in result["suspicious_ips"]:
            story.append(Paragraph(ip, styles['Normal']))
    else:
        story.append(Paragraph("No suspicious IPs detected.", styles['Normal']))

    story.append(Paragraph("<br/><b>Recommendations</b>", styles['Heading2']))

    if result["threat_level"] == "High":
        story.append(Paragraph("Immediately investigate suspicious IPs and block malicious traffic.", styles['Normal']))
    elif result["threat_level"] == "Medium":
        story.append(Paragraph("Monitor failed login attempts and review server security.", styles['Normal']))
    else:
        story.append(Paragraph("System appears secure. Continue regular monitoring.", styles['Normal']))

    doc.build(story)

    return pdf_file