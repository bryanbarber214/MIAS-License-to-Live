"""
QR Code Generator Module
License to Live: MIAS - Python/Streamlit Version
Generates emergency access QR codes for patients
CORRECTED: Uses correct page name for Streamlit Cloud
"""

import qrcode
import io
import secrets
from PIL import Image, ImageDraw, ImageFont
import base64

def generate_emergency_token() -> str:
    """
    Generate a secure random token for emergency access
    Returns a 32-character alphanumeric token
    """
    return secrets.token_urlsafe(32)


def create_emergency_qr_code(patient_id: int, emergency_token: str, base_url: str = "https://bryanbarber214.github.io/MIAS-License-to-Live/emergency_access.html") -> Image:
    """
    Create QR code for emergency medical access
    
    Args:
        patient_id: Patient's database ID
        emergency_token: Unique emergency access token
        base_url: Base URL of the application
        
    Returns:
        PIL Image object containing the QR code
    """
    # Create emergency access URL - CORRECTED to match page name
    emergency_url = f"{base_url}?token={emergency_token}"
    
    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,  # High error correction
        box_size=10,
        border=4,
    )
    
    qr.add_data(emergency_url)
    qr.make(fit=True)
    
    # Create image
    qr_image = qr.make_image(fill_color="black", back_color="white")
    
    return qr_image


def create_printable_qr_card(patient_data: dict, qr_image: Image, emergency_token: str) -> Image:
    """
    Create a printable card with QR code and patient information
    
    Args:
        patient_data: Dictionary with patient information
        qr_image: PIL Image of QR code
        emergency_token: Emergency access token
        
    Returns:
        PIL Image of printable card
    """
    # Card dimensions (3.5" x 2" at 300 DPI = 1050 x 600 pixels)
    card_width = 1050
    card_height = 600
    
    # Create white background
    card = Image.new('RGB', (card_width, card_height), 'white')
    draw = ImageDraw.Draw(card)
    
    # Add red border
    border_width = 10
    draw.rectangle(
        [(0, 0), (card_width-1, card_height-1)], 
        outline='#e74c3c', 
        width=border_width
    )
    
    # Resize QR code to fit card
    qr_size = 350
    qr_image_resized = qr_image.resize((qr_size, qr_size))
    
    # Paste QR code on left side
    qr_x = 50
    qr_y = (card_height - qr_size) // 2
    card.paste(qr_image_resized, (qr_x, qr_y))
    
    # Add text on right side
    text_x = qr_x + qr_size + 40
    text_y = 80
    
    # Title
    draw.text(
        (text_x, text_y),
        "🚨 EMERGENCY",
        fill='#e74c3c',
        font=None  # Use default font
    )
    
    text_y += 40
    draw.text(
        (text_x, text_y),
        "MEDICAL ACCESS",
        fill='#e74c3c',
        font=None
    )
    
    # Patient info
    text_y += 60
    draw.text(
        (text_x, text_y),
        f"Patient: {patient_data.get('first_name', '')} {patient_data.get('last_name', '')}",
        fill='black',
        font=None
    )
    
    text_y += 35
    blood_type = patient_data.get('blood_type', 'Unknown')
    draw.text(
        (text_x, text_y),
        f"Blood Type: {blood_type}",
        fill='black',
        font=None
    )
    
    text_y += 35
    draw.text(
        (text_x, text_y),
        f"DOB: {patient_data.get('date_of_birth', '')}",
        fill='black',
        font=None
    )
    
    # Instructions
    text_y += 60
    draw.text(
        (text_x, text_y),
        "Scan for emergency",
        fill='#666666',
        font=None
    )
    
    text_y += 30
    draw.text(
        (text_x, text_y),
        "medical information",
        fill='#666666',
        font=None
    )
    
    # Token (small text at bottom)
    draw.text(
        (50, card_height - 40),
        f"Code: {emergency_token[:16]}...",
        fill='#999999',
        font=None
    )
    
    return card


def image_to_base64(image: Image) -> str:
    """
    Convert PIL Image to base64 string for display in Streamlit
    
    Args:
        image: PIL Image object
        
    Returns:
        Base64 encoded string
    """
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return img_str


def image_to_bytes(image: Image) -> bytes:
    """
    Convert PIL Image to bytes for download
    
    Args:
        image: PIL Image object
        
    Returns:
        Bytes of the image
    """
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    return buffered.getvalue()

