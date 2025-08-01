#!/usr/bin/env python3
import os
import qrcode

class QRCodeGenerator:

    DEBUG_STATEMENTS_ON = False

    def __init__(self, data):
        self.data = data

    def generate(self, filename: str = "QR_code.png"):
        qr = qrcode.QRCode(
            version=2,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(self.data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        img.save(filename)
        imagePath = os.path.abspath(filename)

        return imagePath

if __name__ == "__main__":
    qr = QRCodeGenerator("https://google.com")
    qr.generate("TestQR.png")
