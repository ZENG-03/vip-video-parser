# python实现免费看VIP电影 - 优化版
import re
import tkinter as tk
import tkinter.messagebox as msgbox
import webbrowser
import threading

class App:
    # 初始化图形化界面
    def __init__(self, width=1000, height=600):
        self.w = width
        self.h = height
        self.title = '播放视频'
        self.root = tk.Tk(className=self.title)
        self.url = tk.StringVar()
        self.v = tk.IntVar()
        self.v.set(1)

        # 界面布局
        frame_1 = tk.Frame(self.root)
        frame_2 = tk.Frame(self.root)

        group = tk.Label(frame_1, text='播放通道:', padx=10, pady=10)
        tb = tk.Radiobutton(frame_1, text='唯一通道', variable=self.v, value=1, width=10, height=10)
        label = tk.Label(frame_2, text='请输入视频播放地址:')
        entry = tk.Entry(frame_2, textvariable=self.url, highlightcolor='Fuchsia', highlightthickness=1, width=50)
        self.play_button = tk.Button(frame_2, text='播放', font=('楷体', 20), fg='Purple', width=10, height=10, command=self.start_video_play)

        frame_1.pack()
        frame_2.pack()
        group.grid(row=0, column=0)
        tb.grid(row=0, column=1)
        label.grid(row=0, column=0)
        entry.grid(row=0, column=1)
        self.play_button.grid(row=0, column=2, ipadx=10, ipady=10)

    # 启动视频播放线程
    def start_video_play(self):
        video_url = self.url.get()
        if not re.match(r'https?://\w.+', video_url):
            msgbox.showerror(title='错误', message='视频地址无效，请检查....')
            return

        # 显示加载提示
        self.play_button.config(text='加载中...')
        threading.Thread(target=self.video_play, args=(video_url,), daemon=True).start()

    # 解析VIP视频源并打开浏览器播放
    def video_play(self, ip):
        # 多个解析接口
        parse_servers = [
            "https://jx.m3u8.tv/jx/jx.php?url=",
            "https://api.example.com/parse?url=",  # 示例备用解析接口
            "https://parse.another.com/play?url="
        ]

        for server in parse_servers:
            try:
                play_url = f"{server}{ip}"
                webbrowser.open(play_url)
                break
            except Exception as e:
                print(f"尝试解析失败: {server}, 错误: {e}")
        self.play_button.config(text='播放')

    # 运行程序
    def loop(self):
        self.root.mainloop()


if __name__ == '__main__':
    App().loop()
