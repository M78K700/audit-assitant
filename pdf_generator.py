from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
import os
import tempfile

def create_pdf_report(audit_plan, output_path):
    """Create a professional PDF audit report."""
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        rightMargin=50,
        leftMargin=50,
        topMargin=50,
        bottomMargin=50
    )
    
    # Define styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=20,
        spaceAfter=30,
        alignment=1,  # Center alignment
        fontName='Helvetica-Bold'
    )
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=12,
        spaceBefore=20,
        fontName='Helvetica-Bold'
    )
    subheading_style = ParagraphStyle(
        'CustomSubHeading',
        parent=styles['Heading3'],
        fontSize=12,
        spaceAfter=8,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=8,
        leading=14,
        fontName='Helvetica'
    )
    
    # Create content
    content = []
    
    # Title
    content.append(Paragraph(f"Financial Audit Plan", title_style))
    content.append(Paragraph(f"{audit_plan['company_name']}", title_style))
    content.append(Spacer(1, 30))
    
    # Company Information
    content.append(Paragraph("1. Company Information", heading_style))
    company_data = [
        ["Company Name:", audit_plan['company_name']],
        ["Sector:", audit_plan['sector']],
        ["Audit Period:", audit_plan['audit_period']],
        ["Team Size:", str(audit_plan['team_size'])]
    ]
    company_table = Table(company_data, colWidths=[150, 250])
    company_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey)
    ]))
    content.append(company_table)
    content.append(Spacer(1, 20))
    
    # Audit Objectives
    content.append(Paragraph("2. Audit Objectives", heading_style))
    for objective in audit_plan['objectives']:
        content.append(Paragraph(f"• {objective}", normal_style))
    content.append(Spacer(1, 20))
    
    # Audit Scope
    content.append(Paragraph("3. Audit Scope", heading_style))
    for scope_item in audit_plan['scope']:
        content.append(Paragraph(f"• {scope_item}", normal_style))
    content.append(Spacer(1, 20))
    
    # Risk Assessment
    content.append(Paragraph("4. Risk Assessment", heading_style))
    
    # High Risk Areas
    content.append(Paragraph("High Risk Areas:", subheading_style))
    for risk in audit_plan['risks']['High']:
        content.append(Paragraph(f"• {risk}", normal_style))
    content.append(Spacer(1, 12))
    
    # Medium Risk Areas
    content.append(Paragraph("Medium Risk Areas:", subheading_style))
    for risk in audit_plan['risks']['Medium']:
        content.append(Paragraph(f"• {risk}", normal_style))
    content.append(Spacer(1, 12))
    
    # Low Risk Areas
    content.append(Paragraph("Low Risk Areas:", subheading_style))
    for risk in audit_plan['risks']['Low']:
        content.append(Paragraph(f"• {risk}", normal_style))
    content.append(Spacer(1, 20))
    
    # Resource Allocation
    content.append(Paragraph("5. Resource Allocation", heading_style))
    
    # High Risk Team
    if audit_plan['team_members']['high_risk']:
        content.append(Paragraph("High Risk Team:", subheading_style))
        for member in audit_plan['team_members']['high_risk']:
            content.append(Paragraph(f"• {member}", normal_style))
        content.append(Spacer(1, 12))
    
    # Medium Risk Team
    if audit_plan['team_members']['medium_risk']:
        content.append(Paragraph("Medium Risk Team:", subheading_style))
        for member in audit_plan['team_members']['medium_risk']:
            content.append(Paragraph(f"• {member}", normal_style))
        content.append(Spacer(1, 12))
    
    # Low Risk Team
    if audit_plan['team_members']['low_risk']:
        content.append(Paragraph("Low Risk Team:", subheading_style))
        for member in audit_plan['team_members']['low_risk']:
            content.append(Paragraph(f"• {member}", normal_style))
    
    # Build PDF
    doc.build(content)

def generate_pdf_download(audit_plan):
    """Generate a PDF report and return it as bytes for download."""
    # Create a temporary file
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
    temp_path = temp_file.name
    temp_file.close()
    
    try:
        # Generate the PDF
        create_pdf_report(audit_plan, temp_path)
        
        # Read the generated PDF into bytes
        with open(temp_path, 'rb') as f:
            pdf_bytes = f.read()
        
        return pdf_bytes
    finally:
        # Clean up the temporary file
        try:
            os.unlink(temp_path)
        except:
            pass 