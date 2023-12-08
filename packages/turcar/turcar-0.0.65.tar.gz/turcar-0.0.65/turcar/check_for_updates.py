import re
import sys
import subprocess
import tkinter as tk
import os
import shutil
import threading


class CheackUpdates:
    def __init__(self):
        self.os_type = sys.platform
        self.root = tk.Tk()
        self.url = f"https://pypi.org/pypi/turcar/json"

    def is_windows(self):
        return self.os_type.startswith('win')

    def is_linux(self):
        return self.os_type.startswith('linux')

    def is_mac(self):
        return self.os_type.startswith('darwin')

    def close(self):
        self.root.destroy()

    # 检查版本
    def cheack_version(self, version):
        self.root.title('新版本更新')
        self.root.resizable(False, False)
        self.root.geometry("300x200")  # 设置弹框大小
        popup_label = tk.Label(self.root, text="发现新版本，是否立即更新？", font=("Arial", 16))
        popup_label.pack(pady=20)

        self.update_text = tk.StringVar()
        self.update_text.set("更新")
        self.popup_button_update = tk.Button(self.root, textvariable=self.update_text,
                                             command=lambda: self.update_bash('/home/turcar/test/turcar-update.bash',
                                                                              version))
        self.popup_button_update.pack(pady=10)

        popup_button_not_update = tk.Button(self.root, text="不更新", command=self.close)
        popup_button_not_update.pack(pady=10)
        self.root.geometry(
            "500x200+{}+{}".format(int(self.root.winfo_screenwidth() / 2 - 250),
                                   int(self.root.winfo_screenheight() / 2 - 100)))  # 根据窗口大小调整位置
        self.root.mainloop()

    def update_text_fun(self):
        self.update_text.set('正在拼命更新中，更新完毕自动重启，然后就能使用心爱的turcar啦')

    # 更新脚本中的版本号
    def update_bash(self, filename, new_version):
        # from turcar import workbench
        # bench = workbench.Workbench()
        # return bench._on_close()
        # 丢给多线程是因为直接写不更新，因为bash给他阻塞了，但是好像并没有什么作用
        threading.Thread(target=self.update_text_fun).start()

        """
        更新脚本中的版本号

        Args:
            filename: 要更新的脚本文件名
            new_version: 新的版本号，格式为 x.x.x
        """
        if os.path.exists(filename):
            pass
        else:
            # 使用示例
            source_file = "turcar-update.bash"
            destination_file = "/home/turcar/test/turcar-update.bash"
            copy_file(source_file, destination_file)

        # 使用正则表达式匹配并替换版本号
        with open(filename, 'r') as file:
            content = file.read()
            new_content = re.sub(r'(VERSION=)\d+\.\d+\.\d+', r'\g<1>' + new_version, content)

        # 将更新后的内容写回脚本文件
        with open(filename, 'w') as file:
            file.write(new_content)

        # 指定版本更新

        # thread = threading.Thread(target=execute_bash_command, args=(list(filename), ))
        #
        # # 开始线程
        # thread.start()
        #
        # # 等待线程完成
        # thread.join()
        self.popup_button_update.config(state=tk.DISABLED)
        self.update_text.set("更新中...")
        self.root.update()

        execute_bash_command(filename)

        # 显示更新完成的提示消息，关闭窗口
        self.update_text.set("更新完成")
        self.root.after(2000, self.close)  # 2秒后关闭窗口
        self.root.destroy()



def copy_file(source_file, destination_file):
    try:
        shutil.copy(source_file, destination_file)
        print("文件复制成功！")
    except FileNotFoundError:
        print("找不到源文件，请检查路径是否正确。")


# 执行 Bash 命令
def execute_bash_command(command):
    result = subprocess.run(command)
    return True

    # 输出命令执行结果
    # print("命令输出：")
    # print(result.stdout)
    # print()
    #
    # # 输出命令的退出状态码
    # print("退出状态码：", result.returncode)
