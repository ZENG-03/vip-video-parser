from flask import Flask, render_template, request, jsonify
import requests
import urllib.parse
from concurrent.futures import ThreadPoolExecutor
import logging
import ssl
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 创建线程池
executor = ThreadPoolExecutor(max_workers=8)

# 禁用SSL警告
ssl._create_default_https_context = ssl._create_unverified_context

# 解析接口列表
PARSE_SERVERS = [
    "https://api.lhh.la/vip/?url=",            # 智能解析接口
    "https://jx.777jiexi.com/player/?url=",    # 稳定智能接口
    "https://api.jhdyw.vip/?url=",             # 解析专线接口
    "https://jx.7c7c.vip/jx/?url=",           # 全网解析接口
    "https://jx.iztyy.com/svip/?url=",         # 高清解析接口
    "https://jx.parwix.com:4433/player/?url=", # 智能云解析
    "https://jx.playerjy.com/?url=",           # 稳定解析接口
    "https://j.zz22x.com/jx/?url="             # 备用智能接口
]

def check_server_availability(server_url, video_url):
    """检查解析服务器是否可用"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': '*/*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Connection': 'keep-alive',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache'
        }

        url = f"{server_url}{video_url}"
        response = requests.get(url, timeout=2.0, headers=headers, allow_redirects=True, verify=False)

        if response.status_code == 200:
            return url
    except Exception as e:
        logger.debug(f"Server {server_url} check failed: {str(e)}")
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/parse', methods=['POST'])
def parse_video():
    try:
        data = request.get_json()
        video_url = data.get('url', '').strip()

        if not video_url:
            return jsonify({'error': '请输入视频地址'}), 400

        if not video_url.startswith(('http://', 'https://')):
            return jsonify({'error': '请输入正确的视频地址'}), 400

        encoded_url = urllib.parse.quote(video_url)

        futures = [executor.submit(check_server_availability, server, encoded_url)
                  for server in PARSE_SERVERS]

        parse_urls = []
        for future in futures:
            result = future.result()
            if result:
                parse_urls.append(result)

        if not parse_urls:
            return jsonify({'error': '当前没有可用的解析接口'}), 503

        return jsonify({
            'status': 'success',
            'parse_urls': parse_urls
        })

    except Exception as e:
        logger.error(f"Parse error: {str(e)}")
        return jsonify({'error': str(e)}), 500

# 为PythonAnywhere适配的启动代码
if __name__ == '__main__':
    # 本地调试时使用
    app.run(debug=False)

# 为云平台准备的WSGI入口
application = app
