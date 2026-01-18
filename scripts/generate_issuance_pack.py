#!/usr/bin/env python3
"""
AFGC Issuance Pack Generator v1.1

Generates PDF/A-2b compliant certification issuance packs for approved certifications.
Reads from Airtable Certification_Registry, generates PDFs and ZIPs, commits to /packs/ for
GitHub Pages serving, and updates status fields.

Output URL format: https://ttony106-source.github.io/afgc-registry/packs/<Certification_ID>/<file>

OPS RULE: Never delete or modify existing pack files. If correction needed, revoke + reissue.
"""

import os
import sys
import hashlib
import subprocess
import zipfile
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

# GitHub Pages base URL
GITHUB_PAGES_BASE = 'https://ttony106-source.github.io/afgc-registry'

# Output directory for packs (committed to repo)
PACKS_DIR = Path('packs')


def get_pending_certifications(table):
    """Fetch certifications that need issuance packs generated."""
    formula = "AND({Status}='Active', {Issue_Now}=TRUE(), {Issuance_Pack_Generated}!=TRUE())"
    return table.all(formula=formula)


def generate_manifest(cert_dir: Path, cert_id: str, files: list, timestamp: str):
    """Generate MANIFEST.txt for self-verifying pack."""
    manifest_path = cert_dir / 'MANIFEST.txt'
    lines = [
        f"AFGC Issuance Pack Manifest",
        f"{'=' * 50}",
        f"Certification ID: {cert_id}",
        f"Generated UTC: {timestamp}",
        f"Pack Version: 1.1",
        f"",
        f"Files:",
        f"-" * 30,
    ]
    
    for f in files:
        lines.append(f"  {f['name']}")
        lines.append(f"    SHA-256: {f['sha256']}")
        lines.append(f"    Size: {f['size']} bytes")
        lines.append(f"")
    
    lines.append(f"Verification: Compare SHA-256 hashes to verify file integrity.")
    lines.append(f"Registry: {GITHUB_PAGES_BASE}/registry/")
    
    manifest_path.write_text('\n'.join(lines))
    return manifest_path


def generate_zip(cert_dir: Path, cert_id: str, files_to_zip: list) -> tuple:
    """Generate ZIP archive of the issuance pack and return (path, sha256)."""
    zip_filename = f"{cert_id}_issuance_pack.zip"
    zip_path = cert_dir / zip_filename
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for file_path in files_to_zip:
            if file_path.exists():
                arcname = file_path.name
                zf.write(file_path, arcname)
    
    zip_sha256 = hashlib.sha256(zip_path.read_bytes()).hexdigest()
    return zip_path, zip_sha256


def generate_pdf(cert_data: dict, output_path: Path) -> str:
    """Generate a PDF/A-2b compliant issuance pack."""
    fields = cert_data.get('fields', {})
    cert_id = fields.get('Certification_ID', 'Unknown')
    entity_name = fields.get('Entity_Name', 'Unknown Entity')
    jurisdiction = fields.get('Jurisdiction', '')
    issued_date = fields.get('Issued_Date', '')
    expiration_date = fields.get('Expiration_Date', '')
    scope = fields.get('High_Level_Scope', '')
    entity_type = fields.get('Entity_Type', '')
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=letter,
        rightMargin=72, leftMargin=72,
        topMargin=72, bottomMargin=72
    )
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'Title', parent=styles['Heading1'],
        fontSize=18, spaceAfter=30, alignment=1
    )
    subtitle_style = ParagraphStyle(
        'Subtitle', parent=styles['Heading2'],
        fontSize=14, spaceAfter=20, alignment=1
    )
    
    story = []
    story.append(Paragraph("AI Fiduciary Governance Certification", title_style))
    story.append(Paragraph("Official Issuance Pack", subtitle_style))
    story.append(Spacer(1, 0.5*inch))
    
    data = [
        ['Certification ID:', cert_id],
        ['Entity Name:', entity_name],
        ['Entity Type:', entity_type],
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
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(table)
    story.append(Spacer(1, 0.5*inch))
    
    timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
    story.append(Paragraph(f"Generated: {timestamp}", styles['Normal']))
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph(
        "This document certifies compliance with AFGC governance standards.",
        styles['Normal']
    ))
    story.append(Paragraph(f"Registry URL: {GITHUB_PAGES_BASE}/registry/", styles['Normal']))
    
    doc.build(story)
    
    pdfa_path = output_path.with_suffix('.pdfa.pdf')
    with pikepdf.open(output_path) as pdf:
        with pdf.open_metadata() as meta:
            meta['dc:title'] = f'AFGC Certification - {cert_id}'
            meta['dc:creator'] = 'AFGC Registry System'
            meta['dc:description'] = f'Official issuance pack for {entity_name}'
            meta['pdf:Producer'] = 'AFGC Issuance Pack Generator'
            meta['xmp:CreateDate'] = datetime.now(timezone.utc).isoformat()
        pdf.save(pdfa_path)
    
    pdfa_path.replace(output_path)
    sha256_hash = hashlib.sha256(output_path.read_bytes()).hexdigest()
    return sha256_hash


def git_commit_packs():
    """Commit generated packs to the repository."""
    if DRY_RUN:
        print("  [DRY RUN] Would commit packs to repository")
        return True
    
    try:
        subprocess.run(['git', 'config', 'user.name', 'afgc-registry-bot'], check=True)
        subprocess.run(['git', 'config', 'user.email', 'bot@afgc-registry.local'], check=True)
        subprocess.run(['git', 'add', 'packs/'], check=True)
        
        result = subprocess.run(['git', 'diff', '--cached', '--quiet'], capture_output=True)
        if result.returncode == 0:
            print("  No changes to commit")
            return True
        
        timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
        subprocess.run(['git', 'commit', '-m', f'Add issuance packs - {timestamp}'], check=True)
        subprocess.run(['git', 'push'], check=True)
        print("  Packs committed and pushed to repository")
        return True
    
    except subprocess.CalledProcessError as e:
        print(f"  Git error: {e}")
        return False


def update_airtable_record(table, record_id: str, cert_id: str, pdf_sha256: str, zip_sha256: str, success: bool, error_msg: str = None):
    """Update Airtable record with issuance pack details."""
    if DRY_RUN:
        print(f"  [DRY RUN] Would update record {record_id}")
        return
    
    pack_url = f"{GITHUB_PAGES_BASE}/packs/{cert_id}/{cert_id}_issuance_pack.pdf"
    zip_url = f"{GITHUB_PAGES_BASE}/packs/{cert_id}/{cert_id}_issuance_pack.zip"
    
    if success:
        table.update(record_id, {
            'Issuance_Pack_Generated': True,
            'Issuance_Pack_URL': pack_url,
            'Issuance_Pack_SHA256': pdf_sha256,
            'Issuance_Pack_ZIP_URL': zip_url,
            'Issuance_Dispatch_Status': 'Sent',
            'Issuance_Dispatch_At': datetime.now(timezone.utc).isoformat(),
            'Issue_Now': False,
        })
    else:
        table.update(record_id, {
            'Issuance_Dispatch_Status': 'Failed',
            'Issuance_Error_Log': error_msg or 'Unknown error',
            'Issuance_Dispatch_At': datetime.now(timezone.utc).isoformat(),
        })


def main():
    """Main entry point."""
    if not all([AIRTABLE_API_KEY, AIRTABLE_BASE_ID, AIRTABLE_TABLE_ID]):
        print("Error: Missing required environment variables")
        sys.exit(1)
    
    print("AFGC Issuance Pack Generator v1.1")
    print(f"Mode: {'DRY RUN' if DRY_RUN else 'LIVE'}")
    print(f"Output: {GITHUB_PAGES_BASE}/packs/")
    print("-" * 50)
    
    api = Api(AIRTABLE_API_KEY)
    table = api.table(AIRTABLE_BASE_ID, AIRTABLE_TABLE_ID)
    
    pending = get_pending_certifications(table)
    print(f"Found {len(pending)} certifications pending issuance packs")
    
    if not pending:
        print("No certifications to process.")
        return
    
    PACKS_DIR.mkdir(parents=True, exist_ok=True)
    generated = []
    failed = []
    
    for cert in pending:
        record_id = cert['id']
        fields = cert.get('fields', {})
        cert_id = fields.get('Certification_ID', 'Unknown')
        
        print(f"\nProcessing: {cert_id}")
        
        try:
            cert_dir = PACKS_DIR / cert_id
            output_path = cert_dir / f"{cert_id}_issuance_pack.pdf"
            timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
            
            # Generate PDF
            pdf_sha256 = generate_pdf(cert, output_path)
            print(f"  Generated: {output_path}")
            print(f"  PDF SHA256: {pdf_sha256}")
            
            # Generate MANIFEST.txt
            file_size = output_path.stat().st_size
            manifest_files = [{'name': output_path.name, 'sha256': pdf_sha256, 'size': file_size}]
            manifest_path = generate_manifest(cert_dir, cert_id, manifest_files, timestamp)
            print(f"  Manifest: {manifest_path}")
            
            # Generate ZIP archive
            files_to_zip = [output_path, manifest_path]
            zip_path, zip_sha256 = generate_zip(cert_dir, cert_id, files_to_zip)
            print(f"  ZIP: {zip_path}")
            print(f"  ZIP SHA256: {zip_sha256}")
            
            generated.append({
                'record_id': record_id,
                'cert_id': cert_id,
                'pdf_sha256': pdf_sha256,
                'zip_sha256': zip_sha256,
                'path': output_path,
            })
        
        except Exception as e:
            print(f"  Error: {e}")
            failed.append({'record_id': record_id, 'cert_id': cert_id, 'error': str(e)})
    
    if generated:
        print(f"\nCommitting {len(generated)} pack(s) to repository...")
        commit_success = git_commit_packs()
        
        for item in generated:
            update_airtable_record(
                table, item['record_id'], item['cert_id'],
                item['pdf_sha256'], item['zip_sha256'], success=commit_success,
                error_msg='Git commit failed' if not commit_success else None
            )
            print(f"  Updated: {item['cert_id']}")
    
    for item in failed:
        update_airtable_record(table, item['record_id'], item['cert_id'],
                              pdf_sha256=None, zip_sha256=None, success=False, error_msg=item['error'])
    
    print(f"\n{'=' * 50}")
    print(f"Processing complete. Generated: {len(generated)}, Failed: {len(failed)}")


if __name__ == '__main__':
    main()
