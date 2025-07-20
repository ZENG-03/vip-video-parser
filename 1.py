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
        # 添加更多设备的 User-Agent 和请求头
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

        # 使用 GET 请求代替 HEAD 请求，某些服务器可能不支持 HEAD
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

        # URL编码
        encoded_url = urllib.parse.quote(video_url)

        # 并发检查所有解析接口
        futures = [executor.submit(check_server_availability, server, encoded_url)
                  for server in PARSE_SERVERS]

        # 收集所有可用的解析URL
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

def start_server(host='0.0.0.0', port=5000):
    """启动Web服务器"""
    try:
        print(f"启动服务器在 http://{host}:{port}")
        print("可以通过以下地址访问：")
        print(f"1. http://localhost:{port}")
        print(f"2. http://127.0.0.1:{port}")
        print("3. 在同一网络的其他设备上，可以通过本机IP地址访问")
        app.run(host=host, port=port, debug=False)
    except Exception as e:
        print(f"启动服务器时发生错误: {e}")

if __name__ == '__main__':
    start_server()
