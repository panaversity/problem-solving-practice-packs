# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "Pillow>=10.0",
#   "reportlab>=4.0",
# ]
# ///
"""
Generate Pack 2 v2 receipts: 5 paper-photo JPGs, 5 email PDFs, 5 app PNGs.

All data is fake-but-plausible. Two planted outliers ($340 hotel folio,
$180 phone bill) so "flag unusual purchases" has a clear correct answer.
Spread across Sep + Oct 2024, ~6 categories.
"""
from __future__ import annotations

import os
import random
from datetime import date
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

OUT = Path(__file__).parent / "receipts"
PHOTOS = OUT / "photos"
PDFS = OUT / "pdfs"
SCREENS = OUT / "screenshots"
for d in (PHOTOS, PDFS, SCREENS):
    d.mkdir(parents=True, exist_ok=True)


# ---------- font helpers ----------
def _font(size: int, mono: bool = False, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates_mono = [
        "/System/Library/Fonts/Menlo.ttc",
        "/System/Library/Fonts/Courier New.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
    ]
    candidates_sans = [
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    candidates_bold = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "/System/Library/Fonts/HelveticaNeue.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    ]
    pool = candidates_mono if mono else (candidates_bold if bold else candidates_sans)
    for p in pool:
        if Path(p).exists():
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                continue
    return ImageFont.load_default()


# ---------- JPGs: phone photos of paper receipts ----------
def make_paper_receipt(
    path: Path,
    merchant: str,
    address: str,
    when: str,
    lines: list[tuple[str, float]],
    subtotal: float,
    tax: float,
    total: float,
    *,
    payment: str = "VISA ****4521",
) -> None:
    W, H = 720, 1040
    bg = Image.new("RGB", (W, H), color=(247, 244, 235))  # slight cream
    draw = ImageDraw.Draw(bg)

    f_head = _font(36, mono=True, bold=True)
    f_mid = _font(22, mono=True)
    f_sm = _font(20, mono=True)

    y = 60
    draw.text((W // 2 - draw.textlength(merchant, font=f_head) // 2, y), merchant, fill="black", font=f_head)
    y += 56
    for line in address.split("\n"):
        draw.text((W // 2 - draw.textlength(line, font=f_sm) // 2, y), line, fill="black", font=f_sm)
        y += 28
    y += 12
    draw.text((W // 2 - draw.textlength(when, font=f_mid) // 2, y), when, fill="black", font=f_mid)
    y += 40
    draw.line([(40, y), (W - 40, y)], fill="black", width=2)
    y += 16

    for label, amount in lines:
        draw.text((60, y), label, fill="black", font=f_sm)
        amt_str = f"${amount:>7.2f}"
        draw.text((W - 60 - draw.textlength(amt_str, font=f_sm), y), amt_str, fill="black", font=f_sm)
        y += 28

    y += 12
    draw.line([(40, y), (W - 40, y)], fill="black", width=1)
    y += 14
    for label, amount in (("Subtotal", subtotal), ("Tax", tax)):
        draw.text((60, y), label, fill="black", font=f_sm)
        amt_str = f"${amount:>7.2f}"
        draw.text((W - 60 - draw.textlength(amt_str, font=f_sm), y), amt_str, fill="black", font=f_sm)
        y += 28
    y += 6
    draw.line([(40, y), (W - 40, y)], fill="black", width=2)
    y += 16
    draw.text((60, y), "TOTAL", fill="black", font=_font(28, mono=True, bold=True))
    tot_str = f"${total:.2f}"
    draw.text((W - 60 - draw.textlength(tot_str, font=_font(28, mono=True, bold=True)), y), tot_str, fill="black", font=_font(28, mono=True, bold=True))
    y += 60

    draw.text((60, y), f"Paid: {payment}", fill="black", font=f_sm)
    y += 28
    draw.text((60, y), "Thank you for your business.", fill="black", font=f_sm)

    # subtle paper noise
    random.seed(hash(str(path)) & 0xFFFFFFFF)
    for _ in range(2400):
        x = random.randint(0, W - 1)
        yy = random.randint(0, H - 1)
        v = random.randint(220, 245)
        bg.putpixel((x, yy), (v, v, v - 10))

    # slight rotation to look like a phone photo
    rotated = bg.rotate(random.uniform(-0.7, 0.7), resample=Image.BICUBIC, fillcolor=(40, 40, 50))
    rotated.save(path, "JPEG", quality=82)


# ---------- PDFs: clean email receipts ----------
def make_pdf_receipt(
    path: Path,
    brand: str,
    brand_color: str,
    title: str,
    when: str,
    confirmation: str,
    rows: list[tuple[str, str]],
    total: float,
) -> None:
    c = canvas.Canvas(str(path), pagesize=letter)
    w, h = letter

    # brand band
    c.setFillColor(HexColor(brand_color))
    c.rect(0, h - 0.9 * inch, w, 0.9 * inch, fill=1, stroke=0)
    c.setFillColor(HexColor("#FFFFFF"))
    c.setFont("Helvetica-Bold", 22)
    c.drawString(0.6 * inch, h - 0.55 * inch, brand)

    c.setFillColor(HexColor("#222222"))
    c.setFont("Helvetica-Bold", 18)
    c.drawString(0.6 * inch, h - 1.4 * inch, title)
    c.setFont("Helvetica", 11)
    c.drawString(0.6 * inch, h - 1.7 * inch, f"Date: {when}")
    c.drawString(0.6 * inch, h - 1.9 * inch, f"Confirmation: {confirmation}")

    # body rows
    y = h - 2.4 * inch
    c.setFont("Helvetica-Bold", 11)
    c.drawString(0.6 * inch, y, "Item")
    c.drawRightString(w - 0.6 * inch, y, "Amount")
    y -= 0.18 * inch
    c.setStrokeColor(HexColor("#CCCCCC"))
    c.line(0.6 * inch, y, w - 0.6 * inch, y)
    y -= 0.22 * inch
    c.setFont("Helvetica", 11)
    for label, amount in rows:
        c.drawString(0.6 * inch, y, label)
        c.drawRightString(w - 0.6 * inch, y, amount)
        y -= 0.22 * inch

    y -= 0.18 * inch
    c.line(0.6 * inch, y, w - 0.6 * inch, y)
    y -= 0.28 * inch
    c.setFont("Helvetica-Bold", 14)
    c.drawString(0.6 * inch, y, "Total")
    c.drawRightString(w - 0.6 * inch, y, f"${total:.2f}")

    # footer
    c.setFont("Helvetica", 9)
    c.setFillColor(HexColor("#777777"))
    c.drawString(0.6 * inch, 0.6 * inch, f"This is an automated receipt from {brand}. Please retain for your records.")

    c.showPage()
    c.save()


# ---------- PNGs: phone-app screenshot style ----------
def make_screenshot(
    path: Path,
    app: str,
    theme_bg: str,
    accent: str,
    headline: str,
    sub_lines: list[str],
    amount: float,
    when: str,
    *,
    light_text: bool = True,
) -> None:
    W, H = 750, 1334  # iPhone 8 pt
    bg = Image.new("RGB", (W, H), color=theme_bg)
    draw = ImageDraw.Draw(bg)

    # status bar
    draw.rectangle([(0, 0), (W, 90)], fill=theme_bg)
    text_color = (255, 255, 255) if light_text else (20, 20, 20)
    draw.text((40, 36), "9:41", fill=text_color, font=_font(24, bold=True))
    draw.text((W - 90, 36), "100%", fill=text_color, font=_font(20))

    # app title bar
    f_app = _font(28, bold=True)
    draw.text((W // 2 - draw.textlength(app, font=f_app) // 2, 130), app, fill=text_color, font=f_app)

    # big checkmark circle
    cx, cy, r = W // 2, 340, 90
    draw.ellipse([(cx - r, cy - r), (cx + r, cy + r)], outline=accent, width=8)
    # check
    draw.line([(cx - 36, cy + 4), (cx - 8, cy + 36)], fill=accent, width=10)
    draw.line([(cx - 8, cy + 36), (cx + 44, cy - 32)], fill=accent, width=10)

    # headline
    f_h1 = _font(38, bold=True)
    draw.text((W // 2 - draw.textlength(headline, font=f_h1) // 2, 470), headline, fill=text_color, font=f_h1)

    # amount
    amt_str = f"${amount:.2f}"
    f_amt = _font(80, bold=True)
    draw.text((W // 2 - draw.textlength(amt_str, font=f_amt) // 2, 540), amt_str, fill=text_color, font=f_amt)

    # sub lines
    y = 680
    f_sub = _font(22)
    for line in sub_lines:
        draw.text((W // 2 - draw.textlength(line, font=f_sub) // 2, y), line, fill=text_color, font=f_sub)
        y += 38

    # bottom card with date
    card_y = H - 240
    draw.rounded_rectangle([(40, card_y), (W - 40, H - 80)], radius=20, fill=(255, 255, 255) if light_text else (240, 240, 240))
    f_card = _font(22, bold=True)
    f_card_sm = _font(20)
    draw.text((70, card_y + 30), "Date", fill=(20, 20, 20), font=f_card)
    draw.text((W - 70 - draw.textlength(when, font=f_card_sm), card_y + 32), when, fill=(20, 20, 20), font=f_card_sm)

    bg.save(path, "PNG", optimize=True)


# ---------- the 15 receipts ----------
def build_photos() -> None:
    make_paper_receipt(
        PHOTOS / "grocery-fresh-mart-2024-09-04.jpg",
        merchant="FRESH MART #214",
        address="1840 Hawthorne Blvd\nPortland OR 97214",
        when="09/04/2024  14:22",
        lines=[
            ("Organic Bananas", 3.18),
            ("Whole Milk 1gal", 4.49),
            ("Sourdough Loaf", 5.99),
            ("Pasture Eggs Dz", 7.29),
            ("Spinach 5oz", 3.79),
            ("Olive Oil 500ml", 11.49),
            ("Salmon Fillet", 14.62),
            ("Bell Peppers x3", 4.17),
        ],
        subtotal=55.02,
        tax=0.00,
        total=55.02,
        payment="VISA ****4521",
    )
    make_paper_receipt(
        PHOTOS / "gas-shell-2024-09-12.jpg",
        merchant="SHELL #5527",
        address="2200 NE Sandy Blvd\nPortland OR 97232",
        when="09/12/2024  07:48",
        lines=[
            ("Regular 11.842 gal", 51.31),
            ("Cooler bottle water", 2.49),
        ],
        subtotal=53.80,
        tax=0.00,
        total=53.80,
        payment="VISA ****4521",
    )
    make_paper_receipt(
        PHOTOS / "coffee-blue-bottle-2024-09-19.jpg",
        merchant="BLUE BOTTLE COFFEE",
        address="3401 SE Division St\nPortland OR 97202",
        when="09/19/2024  08:34",
        lines=[
            ("Cortado", 5.25),
            ("Almond croissant", 5.50),
        ],
        subtotal=10.75,
        tax=0.97,
        total=11.72,
        payment="APPLE PAY",
    )
    make_paper_receipt(
        PHOTOS / "restaurant-pho-saigon-2024-10-08.jpg",
        merchant="PHO SAIGON",
        address="412 NW 21st Ave\nPortland OR 97209",
        when="10/08/2024  19:12",
        lines=[
            ("Pho Tai (lg)", 16.95),
            ("Pho Ga (md)", 13.95),
            ("Spring rolls (2)", 8.50),
            ("Vietnamese coffee x2", 9.00),
        ],
        subtotal=48.40,
        tax=4.36,
        total=52.76,
        payment="VISA ****4521",
    )
    make_paper_receipt(
        PHOTOS / "pharmacy-cvs-2024-10-22.jpg",
        merchant="CVS PHARMACY #4712",
        address="950 SW Morrison St\nPortland OR 97205",
        when="10/22/2024  17:55",
        lines=[
            ("Generic ibuprofen 200mg", 8.99),
            ("Multivitamin 100ct", 14.49),
            ("Toothpaste", 5.79),
            ("Bandage assortment", 6.49),
        ],
        subtotal=35.76,
        tax=0.00,
        total=35.76,
        payment="VISA ****4521",
    )


def build_pdfs() -> None:
    make_pdf_receipt(
        PDFS / "uber-2024-09-15.pdf",
        brand="Uber",
        brand_color="#000000",
        title="Receipt for your trip",
        when="September 15, 2024 — 11:42 PM",
        confirmation="UBER-09F12C7A",
        rows=[
            ("Trip fare", "$18.40"),
            ("Booking fee", "$2.75"),
            ("Tip", "$3.00"),
        ],
        total=24.15,
    )
    make_pdf_receipt(
        PDFS / "amazon-2024-09-28.pdf",
        brand="amazon",
        brand_color="#232F3E",
        title="Your Amazon.com order",
        when="September 28, 2024",
        confirmation="112-7820934-4452209",
        rows=[
            ("Anker USB-C charger 65W", "$32.99"),
            ("Cat6 ethernet cable, 10ft (2-pack)", "$12.49"),
            ("Shipping & handling", "$0.00"),
        ],
        total=45.48,
    )
    make_pdf_receipt(
        PDFS / "electric-utility-2024-10-01.pdf",
        brand="Pacific Power",
        brand_color="#0E5C8C",
        title="Monthly electric bill",
        when="Billing period: Aug 28 — Sep 27, 2024",
        confirmation="Acct 4429-8810-22",
        rows=[
            ("Electricity usage 612 kWh", "$78.40"),
            ("Distribution charge", "$14.20"),
            ("State taxes & fees", "$6.18"),
        ],
        total=98.78,
    )
    make_pdf_receipt(
        PDFS / "netflix-2024-10-05.pdf",
        brand="NETFLIX",
        brand_color="#E50914",
        title="Subscription renewal",
        when="October 5, 2024",
        confirmation="NF-RNW-281109",
        rows=[
            ("Standard plan, monthly", "$15.49"),
        ],
        total=15.49,
    )
    # planted outlier #1: hotel folio
    make_pdf_receipt(
        PDFS / "hotel-folio-marriott-2024-10-18.pdf",
        brand="Marriott Bonvoy",
        brand_color="#A00031",
        title="Guest folio — Marriott Downtown Seattle",
        when="Check-in Oct 17 — Check-out Oct 18, 2024",
        confirmation="MR-77418302",
        rows=[
            ("Room (1 night)", "$289.00"),
            ("Occupancy tax", "$32.40"),
            ("Resort fee", "$18.00"),
            ("Parking", "$45.00"),
        ],
        total=384.40,
    )


def build_screenshots() -> None:
    make_screenshot(
        SCREENS / "apple-pay-2024-09-09.png",
        app="Wallet",
        theme_bg="#0F1116",
        accent="#34C759",
        headline="Paid Trader Joe's",
        sub_lines=["with Apple Pay", "VISA ****4521"],
        amount=42.18,
        when="Sep 9, 2024",
        light_text=True,
    )
    make_screenshot(
        SCREENS / "stripe-receipt-2024-09-23.png",
        app="Stripe",
        theme_bg="#FFFFFF",
        accent="#635BFF",
        headline="Paid Calmly Therapy",
        sub_lines=["Monthly subscription", "Confirmation 5xKn-RT88"],
        amount=22.00,
        when="Sep 23, 2024",
        light_text=False,
    )
    make_screenshot(
        SCREENS / "app-store-2024-10-03.png",
        app="App Store",
        theme_bg="#000000",
        accent="#0A84FF",
        headline="Purchase complete",
        sub_lines=["Notability — Pro upgrade", "Annual subscription"],
        amount=14.99,
        when="Oct 3, 2024",
        light_text=True,
    )
    make_screenshot(
        SCREENS / "venmo-2024-10-14.png",
        app="Venmo",
        theme_bg="#008CFF",
        accent="#FFFFFF",
        headline="Paid Alex Chen",
        sub_lines=["Rent share — October", "Confirmation V-9P210"],
        amount=68.50,
        when="Oct 14, 2024",
        light_text=True,
    )
    # planted outlier #2: phone bill
    make_screenshot(
        SCREENS / "transit-clipper-2024-10-25.png",
        app="Verizon",
        theme_bg="#CD040B",
        accent="#FFFFFF",
        headline="Phone bill paid",
        sub_lines=["Auto-pay successful", "Acct *****821"],
        amount=182.40,
        when="Oct 25, 2024",
        light_text=True,
    )


def main() -> None:
    build_photos()
    build_pdfs()
    build_screenshots()
    files = sorted(OUT.rglob("*"))
    files = [f for f in files if f.is_file()]
    print(f"Generated {len(files)} receipt files:")
    for f in files:
        size = f.stat().st_size
        print(f"  {size:>8} B  {f.relative_to(OUT)}")


if __name__ == "__main__":
    main()
