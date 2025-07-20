from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__, template_folder='../templates')
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/parse', methods=['POST'])
def parse_video():
    data = request.get_json()
    url = data.get('url')
    # 这里添加你的视频解析逻辑
    return jsonify({"success": True, "url": url})

if __name__ == '__main__':
    app.run()
