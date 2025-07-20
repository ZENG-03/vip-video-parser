"""# watch_vip_move.py - 增强版（支持清晰度选择 + VLC 播放）
import os
import sys
import urllib.parse

# ✅ 第一步：先设置 VLC 路径
vlc_path = r'F:\PYTHON  ZUOYE\HAOWAN DAIMA\1Python抓取VIP电影免费看\vlc-3.0.0'

# 添加路径到环境变量
os.environ['PATH'] = vlc_path + ';' + os.environ['PATH']
os.add_dll_directory(vlc_path)

# ✅ 第二步：再导入 vlc 模块
import re
import tkinter as tk
import tkinter.messagebox as msgbox
import threading
import vlc  # 现在可以正确加载了


class App:
    def __init__(self, width=1000, height=600):
        self.w = width
        self.h = height
        self.title = 'VIP视频播放器'
        self.root = tk.Tk(className=self.title)
        self.url = tk.StringVar()
        self.quality_var = tk.StringVar(value="高清")

        # VLC播放器初始化
        try:
            self.instance = vlc.Instance()
            self.player = self.instance.media_player_new()
            print("VLC播放器初始化成功")
        except Exception as e:
            print(f"VLC播放器初始化失败: {e}")
            msgbox.showerror("错误", f"VLC播放器初始化失败: {e}")
            sys.exit(1)

        # 界面布局
        frame_1 = tk.Frame(self.root)
        frame_2 = tk.Frame(self.root)

        label_url = tk.Label(frame_1, text='请输入视频播放地址:')
        entry_url = tk.Entry(frame_1, textvariable=self.url, highlightcolor='Fuchsia', highlightthickness=1, width=50)

        label_quality = tk.Label(frame_2, text='请选择清晰度:')
        quality_menu = tk.OptionMenu(frame_2, self.quality_var, "标清", "高清", "超清")

        self.play_button = tk.Button(frame_2, text='播放', font=('楷体', 20), fg='Purple', width=10, command=self.start_video_play)

        frame_1.pack(pady=20)
        frame_2.pack(pady=20)

        label_url.grid(row=0, column=0)
        entry_url.grid(row=0, column=1)
        label_quality.grid(row=1, column=0)
        quality_menu.grid(row=1, column=1)
        self.play_button.grid(row=1, column=2, ipadx=10, ipady=10)

    def start_video_play(self):
        video_url = self.url.get()
        if not re.match(r'https?://\w.+', video_url):
            msgbox.showerror(title='错误', message='视频地址无效，请检查....')
            return

        selected_quality = self.quality_var.get()
        self.play_button.config(text='加载中...')

        threading.Thread(target=self.video_play, args=(video_url, selected_quality), daemon=True).start()

    def video_play(self, ip, quality):
        # 多个解析接口
        parse_servers = [
            "https://jx.m3u8.tv/jx/jx.php?url=",
            "https://www.flvplay.org/jiexi/?url=",
            "https://www.8090g.cn/url.php?url=",
            "https://jx.m3u8.tv/jx/m3u8play.php?url="
        ]

        # server = parse_servers.get(quality, parse_servers["高清"])
        for server in parse_servers:
            try:
                # URL 编码
                play_url = f"{server}{urllib.parse.quote_plus(ip)}"
                print(f"尝试播放: {play_url}")  # 打印播放链接
                media = self.instance.media_new(play_url)
                self.player.set_media(media)
                self.player.play()
                print("视频开始播放")  # 打印播放开始信息
                break  # 成功播放后退出循环
            except Exception as e:
                msgbox.showerror("播放失败", f"无法播放该视频: {e}")
                print(f"播放失败: {e}")  # 打印详细错误信息
            finally:
                self.play_button.config(text='播放')

    def loop(self):
        self.root.mainloop()


if __name__ == '__main__':
    app = App()
    app.loop()
    """