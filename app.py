from flask import Flask, render_template, request, jsonify
import qrcode
import io
import base64
import requests

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    qr_data = ''
    if request.method == 'POST':
        phone_number = request.form['phone_number']
        login_response = requests.post(
            'https://yinruijianshen.com/yrjs/wechat/sviphy/login',
            data={
                'sj': phone_number,
                'loginType': 'huiyuan',
                'mdStr': 'yrjs_md_tf',
                'md': 'yrjs_md_tf'
            },
            headers={
                'Content-Type': 'application/x-www-form-urlencoded',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090b19)XWEB/11253'
            }
        )
        login_data = login_response.json().get('data', {})
        uid = login_data.get('id')
        if uid:
            qr_response = requests.post(
                'https://yinruijianshen.com/yrjs/wechat/msg/getUserQrmText',
                data={'uid': uid, 'md': 'yrjs_md_tf'},
                headers={
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090b19)XWEB/11253'
                }
            )
            qr_data = qr_response.json().get('data', '')
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_H,
                box_size=10,
                border=4,
            )
            qr.add_data(qr_data)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            buffered = io.BytesIO()
            img.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
            return render_template('index.html', phone_number=phone_number, qr_data=img_str)
        else:
            return 'Failed to get data'
    return render_template('index.html', phone_number='', qr_data='')

if __name__ == '__main__':
    app.run(debug=True)
