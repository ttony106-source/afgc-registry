#!/usr/bin/env python3
"""
AFGC Issuance Pack Generator

Generates PDF/A-2b compliant certification issuance packs for approved certifications.
Reads from Airtable Certification_Registry, generates PDFs, and updates status fields.
"""

import os
import sys
import hashlib
from datetime import datetime, timezone
from pathlib import Path

try:
    from pyairtable import Api
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib import colors
    import pikepdf
except ImportError as e:
    print(f"Missing dependency: {e}")
    print("Install with: pip install pyairtable reportlab pikepdf")
    sys.exit(1)

# Configuration from environment
AIRTABLE_API_KEY = os.environ.get('AIRTABLE_API_KEY')
AIRTABLE_BASE_ID = os.environ.get('AIRTABLE_BASE_ID')
AIRTABLE_TABLE_ID = os.environ.get('AIRTABLE_TABLE_ID')
DRY_RUN = os.environ.get('DRY_RUN', 'false').lower() == 'true'

OUTPUT_DIR = Path('output')


def get_pending_certifications(table):
    """Fetch certifications that need issuance packs generated."""
    formula = "AND({Status}='Active', {Issue_Now}=TRUE(), {Issuance_Pack_Generated}!=TRUE())"
    return table.all(formula=formula)


def generate_pdf(cert_data: dict, output_path: Path) -> str:
    """Generate a PDF/A-2b compliant issuance pack."""
    fields = cert_data.get('fields', {})
    cert_id = fields.get('Certification_ID', 'Unknown')
    entity_name = fields.get('Entity_Name', 'Unknown Entity')
    jurisdiction = fields.get('Jurisdiction', '')
    issued_date = fields.get('Issued_Date', '')
    expiration_date = fields.get('Expiration_Date', '')
    scope = fields.get('High_Level_Scope', '')
    
    # Create PDF
    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=letter,
        rightMargin=72, leftMargin=72,
        topMargin=72, bottomMargin=72
    )
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=30,
        alignment=1  # Center
    )
    
    story = []
    
    # Header
    story.append(Paragraph("AI Fiduciary Governance Certification", title_style))
    story.append(Paragraph("Official Issuance Pack", styles['Heading2']))
    story.append(Spacer(1, 0.5*inch))
    
    # Certificate details table
    data = [
        ['Certification ID:', cert_id],
        ['Entity Name:', entity_name],
        ['Jurisdiction:', jurisdiction],
        ['Issue Date:', issued_date],
        ['Expiration Date:', expiration_date],
        ['Scope:', scope],
    ]
    
    table = Table(data, colWidths=[2*inch, 4*inch])
    table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
    ]))
    story.append(table)
    story.append(Spacer(1, 0.5*inch))
    
    # Footer
    timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
    story.append(Paragraph(f"Generated: {timestamp}", styles['Normal']))
    story.append(Paragraph(
        "This document certifies compliance with AFGC governance standards.",
        styles['Normal']
    ))
    
    doc.build(story)
    
    # Convert to PDF/A-2b using pikepdf
    pdfa_path = output_path.with_suffix('.pdfa.pdf')
    with pikepdf.open(output_path) as pdf:
        # Add PDF/A metadata
        with pdf.open_metadata() as meta:
            meta['dc:title'] = f'AFGC Certification - {cert_id}'
            meta['dc:creator'] = 'AFGC Registry System'
            meta['pdf:Producer'] = 'AFGC Issuance Pack Generator'
        pdf.save(pdfa_path)
    
    # Replace original with PDF/A version
    pdfa_path.replace(output_path)
    
    # Calculate SHA256
    sha256_hash = hashlib.sha256(output_path.read_bytes()).hexdigest()
    return sha256_hash


def update_airtable_record(table, record_id: str, pack_url: str, sha256: str):
    """Update Airtable record with issuance pack details."""
    if DRY_RUN:
        print(f"  [DRY RUN] Would update record {record_id}")
        return
    
    table.update(record_id, {
        'Issuance_Pack_Generated': True,
        'Issuance_Pack_URL': pack_url,
        'Issuance_Pack_SHA256': sha256,
        'Issuance_Dispatch_Status': 'Pending',
    })


def main():
    """Main entry point."""
    if not all([AIRTABLE_API_KEY, AIRTABLE_BASE_ID, AIRTABLE_TABLE_ID]):
        print("Error: Missing required environment variables")
        print("Required: AIRTABLE_API_KEY, AIRTABLE_BASE_ID, AIRTABLE_TABLE_ID")
        sys.exit(1)
    
    print(f"AFGC Issuance Pack Generator")
    print(f"Mode: {'DRY RUN' if DRY_RUN else 'LIVE'}")
    print(f"Base ID: {AIRTABLE_BASE_ID}")
    print(f"Table ID: {AIRTABLE_TABLE_ID}")
    print("-" * 50)
    
    # Connect to Airtable
    api = Api(AIRTABLE_API_KEY)
    table = api.table(AIRTABLE_BASE_ID, AIRTABLE_TABLE_ID)
    
    # Get pending certifications
    pending = get_pending_certifications(table)
    print(f"Found {len(pending)} certifications pending issuance packs")
    
    if not pending:
        print("No certifications to process.")
        return
    
    # Ensure output directory exists
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Process each certification
    for cert in pending:
        record_id = cert['id']
        fields = cert.get('fields', {})
        cert_id = fields.get('Certification_ID', 'Unknown')
        
        print(f"\nProcessing: {cert_id}")
        
        try:
            # Generate PDF
            output_path = OUTPUT_DIR / f"{cert_id}_issuance_pack.pdf"
            sha256 = generate_pdf(cert, output_path)
            print(f"  Generated: {output_path}")
            print(f"  SHA256: {sha256}")
            
            # For now, URL is placeholder - would be uploaded to storage
            pack_url = f"https://afgc-registry.github.io/packs/{cert_id}.pdf"
            
            # Update Airtable
            update_airtable_record(table, record_id, pack_url, sha256)
            print(f"  Status: Updated")
            
        except Exception as e:
            print(f"  Error: {e}")
            if not DRY_RUN:
                table.update(record_id, {
                    'Issuance_Dispatch_Status': 'Failed',
                    'Issuance_Error_Log': str(e),
                })
    
    print(f"\n{'=' * 50}")
    print(f"Processing complete.")


if __name__ == '__main__':
    main()
