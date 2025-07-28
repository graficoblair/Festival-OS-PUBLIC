#!/usr/bin/env python3
import os

import qrcode
class QRCodeGenerator:

    DEBUG_STATEMENTS_ON = False

    def __init__(self, data):
        self.data = data

    def generate(self):
        qr = qrcode.QRCode(
            version=2,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(self.data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        img.save("QR_code.png")

        #TODO currentDir = os.path.dirname(os.path.abspath(__file__))
        #TODO imagePath = os.path.join(currentDir, 'QR_CODE.png')
        imagePath = os.path.abspath("QR_code.png")

        imgURI = f"file://{imagePath}" # 'https://maps.lib.utexas.edu/maps/historical/newark_nj_1922.jpg' 'https://drive.google.com/file/d/1mqIKAF13UkoVmjosC6bCc_c06DR_qXSC'
        if QRCodeGenerator.DEBUG_STATEMENTS_ON: print(f"Corner 1: {corner1} & Corner 2: {corner2} using img: {imgURI}")
        print(imgURI)
        return imagePath

if __name__ == "__main__":
    pass
