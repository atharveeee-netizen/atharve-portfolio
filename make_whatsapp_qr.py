# -*- coding: utf-8 -*-
"""Generate the branded WhatsApp QR PNG for the popup (assets/img/whatsapp-qr.png).

Encodes the wa.me chat link with HIGH error correction and composites the official
WhatsApp badge (assets/img/whatsapp-badge.png = white clear-zone + green circle + the
official glyph) in the centre. The badge PNGs are produced by rendering the official
WhatsApp SVG in a browser (see _walogo.html) — far cleaner than drawing by hand.

Verified scannable with opencv QRCodeDetector (decodes back to the wa.me link).
"""
import qrcode
from qrcode.constants import ERROR_CORRECT_H
from PIL import Image

WA_URL = "https://wa.me/919983974154"
OUT = "assets/img/whatsapp-qr.png"
BADGE = "assets/img/whatsapp-badge.png"
BOX = 14
BORDER = 3


def main():
    qr = qrcode.QRCode(error_correction=ERROR_CORRECT_H, box_size=BOX, border=BORDER)
    qr.add_data(WA_URL)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#171c1c", back_color="white").convert("RGBA")
    w, h = img.size

    badge = Image.open(BADGE).convert("RGBA")
    bs = int(w * 0.26)
    badge = badge.resize((bs, bs), Image.LANCZOS)
    img.alpha_composite(badge, ((w - bs) // 2, (h - bs) // 2))

    img.save(OUT)
    print("wrote %s (%dx%d), badge %dpx" % (OUT, w, h, bs))


if __name__ == "__main__":
    main()
