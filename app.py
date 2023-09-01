from flask import send_file
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from flask import Flask, render_template, request
import requests
import os
import base64

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    image_data = []
    loaded_count = 0  # ตัวนับจำนวนรูปภาพที่โหลดสำเร็จ

    if request.method == 'POST':
        book_id = request.form.get('base_url')
        base_url = f"https://readonline.ebookstou.org/flipbook/{book_id}/files/mobile"

        i = 1
        while True:
            url = f"{base_url}/{i}.jpg"
            response = requests.get(url)
            if response.status_code == 200:
                encoded = base64.b64encode(response.content).decode("utf-8")
                image_data.append(encoded)
                loaded_count += 1
                i += 1  # เพิ่มค่าตัวนับ
            else:
                break  # ไม่สามารถโหลดภาพต่อได้

    return render_template('index.html', image_data=image_data, loaded_count=loaded_count)


@app.route('/download_pdf', methods=['GET'])
def download_pdf():
    image_data = []  # ยังไม่ได้โหลดรูปภาพ คุณต้องรวมโค้ดสำหรับโหลดรูปภาพที่นี่

    # สร้าง PDF
    pdf_file_path = "/path/to/save/pdf.pdf"  # กำหนดที่เก็บไฟล์ PDF
    c = canvas.Canvas(pdf_file_path, pagesize=letter)
    for i, img_base64 in enumerate(image_data):
        # แปลงรูปภาพจาก base64 เป็น binary
        img_binary = base64.b64decode(img_base64)

        # สร้าง PDF ด้วย reportlab (ตัวอย่างนี้เป็นแค่โค้ดที่ง่าย)
        c.drawImage(img_binary, 100, 750, width=500, height=500)
        c.showPage()

    c.save()

    return send_file(pdf_file_path, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=False)
