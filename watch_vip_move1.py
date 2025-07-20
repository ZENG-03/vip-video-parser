# 简化版VIP视频播放器 - 高速版
import tkinter as tk
import tkinter.messagebox as msgbox
import webbrowser
import urllib.parse
import threading
import concurrent.futures
import requests
from concurrent.futures import ThreadPoolExecutor

class App:
    def __init__(self):
        print("正在初始化程序...")
        self.root = tk.Tk()
        self.root.title('VIP视频解析播放器 - 高速版')
        self.root.geometry('800x400')

        # 增加并发数量到8
        self.executor = ThreadPoolExecutor(max_workers=8)

        # 确保超时时间足够
        self.timeout = 3

        # 界面布局
        frame = tk.Frame(self.root)
        frame.pack(expand=True, fill='both', padx=20, pady=20)

        tk.Label(frame, text="请输入视频地址：", font=('微软雅黑', 12)).pack(pady=10)
        self.url_entry = tk.Entry(frame, width=50, font=('微软雅黑', 10))
        self.url_entry.pack(pady=10)

        self.status_label = tk.Label(frame, text="", fg="gray", font=('微软雅黑', 10))
        self.status_label.pack(pady=5)

        self.play_button = tk.Button(
            frame,
            text="开始播放",
            command=self.start_play_video,
            font=('黑体', 12),
            bg='purple',
            fg='white',
            width=15,
            height=1
        )
        self.play_button.pack(pady=20)

        print("初始化完成")

    def update_status(self, message, color="gray"):
        self.status_label.config(text=message, fg=color)
        self.root.update()

    def check_url(self, server, url):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
            }
            response = requests.head(f"{server}{url}", timeout=self.timeout, headers=headers, allow_redirects=True)
            if response.status_code == 200:
                return server
        except:
            pass
        return None

    def start_play_video(self):
        self.play_button.config(state='disabled')
        threading.Thread(target=self.play_video, daemon=True).start()

    def play_video(self):
        try:
            url = self.url_entry.get().strip()
            if not url:
                msgbox.showwarning("警告", "请输入视频地址！")
                return

            if not url.startswith(('http://', 'https://')):
                msgbox.showwarning("警告", "请输入正确的视频地址！")
                return

            # 更新解析接口列表，以智能解析接口为主
            servers = [
                "https://api.lhh.la/vip/?url=",            # 智能解析接口
                "https://jx.777jiexi.com/player/?url=",    # 稳定智能接口
                "https://api.jhdyw.vip/?url=",             # 解析专线接口
                "https://jx.7c7c.vip/jx/?url=",            # 全网解析接口
                "https://jx.iztyy.com/svip/?url=",         # 高清解析接口
                "https://jx.parwix.com:4433/player/?url=", # 智能云解析
                "https://jx.playerjy.com/?url=",           # 稳定解析接口
                "https://j.zz22x.com/jx/?url="             # 备用智能接口
            ]

            self.update_status("正在检测最快的解析接口...", "blue")
            encoded_url = urllib.parse.quote(url)

            # 并发检测所有接口
            futures = [self.executor.submit(self.check_url, server, encoded_url) for server in servers]

            for future in concurrent.futures.as_completed(futures):
                server = future.result()
                if server:
                    play_url = f"{server}{encoded_url}"
                    self.update_status(f"已找到最快接口，正在打开...", "green")
                    webbrowser.open(play_url)
                    print(f"使用接口: {play_url}")
                    return

            self.update_status("暂时无法找到可用的解析接口，请稍后重试", "red")
            msgbox.showerror("错误", "当前没有可用的解析接口，请稍后重试")

        except Exception as e:
            self.update_status(f"发生错误: {str(e)}", "red")
            msgbox.showerror("错误", f"播放失败: {str(e)}")

        finally:
            self.play_button.config(state='normal')

    def loop(self):
        self.root.mainloop()

if __name__ == '__main__':
    try:
        print("程序开始运行...")
        app = App()
        print("启动主循环...")
        app.loop()
    except Exception as e:
        print(f"发生错误: {e}")
        input("按回车键退出...")
