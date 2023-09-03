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


if __name__ == '__main__':
    app.run(debug=True)