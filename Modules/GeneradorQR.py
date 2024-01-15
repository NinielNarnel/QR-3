import qrcode
from io import BytesIO

def generate_qr_code(substance, data):
    # Use substance attributes as needed
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=4,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    # Convert the QR code image to bytes
    buffer = BytesIO()
    img.save(buffer)
    qr_code_bytes = buffer.getvalue()

    return qr_code_bytes
