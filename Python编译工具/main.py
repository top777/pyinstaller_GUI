import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import subprocess
import os

class PyInstallerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title('Python编译工具')
        self.root.geometry('630x500')
        
        # 变量
        self.py_file = tk.StringVar()
        self.icon_file = tk.StringVar()
        self.no_console = tk.BooleanVar()
        self.app_name = tk.StringVar()
        self.author = tk.StringVar()
        self.version = tk.StringVar()
        self.email = tk.StringVar()

        # 布局
        self.create_widgets()

    def create_widgets(self):
        row = 0
        # 选择py文件
        tk.Label(self.root, text='选择Python脚本:').grid(row=row, column=0, sticky='e', padx=5, pady=5)
        tk.Entry(self.root, textvariable=self.py_file, width=40).grid(row=row, column=1, padx=5)
        tk.Button(self.root, text='浏览', command=self.browse_py).grid(row=row, column=2, padx=5)
        row += 1
        # 是否无console
        tk.Checkbutton(self.root, text='无控制台窗口（适合GUI程序）', variable=self.no_console).grid(row=row, column=1, sticky='w', pady=5)
        row += 1
        # 选择icon
        tk.Label(self.root, text='选择图标(.ico):').grid(row=row, column=0, sticky='e', padx=5, pady=5)
        tk.Entry(self.root, textvariable=self.icon_file, width=40).grid(row=row, column=1, padx=5)
        tk.Button(self.root, text='浏览', command=self.browse_icon).grid(row=row, column=2, padx=5)
        row += 1
        # 软件名称
        tk.Label(self.root, text='软件名称:').grid(row=row, column=0, sticky='e', padx=5, pady=5)
        tk.Entry(self.root, textvariable=self.app_name, width=40).grid(row=row, column=1, padx=5)
        row += 1
        # 开发者
        tk.Label(self.root, text='开发者:').grid(row=row, column=0, sticky='e', padx=5, pady=5)
        tk.Entry(self.root, textvariable=self.author, width=40).grid(row=row, column=1, padx=5)
        row += 1
        # 版本号
        tk.Label(self.root, text='版本号:').grid(row=row, column=0, sticky='e', padx=5, pady=5)
        tk.Entry(self.root, textvariable=self.version, width=40).grid(row=row, column=1, padx=5)
        row += 1
        # 邮箱
        tk.Label(self.root, text='联系邮箱:').grid(row=row, column=0, sticky='e', padx=5, pady=5)
        tk.Entry(self.root, textvariable=self.email, width=40).grid(row=row, column=1, padx=5)
        row += 1
        # 打包按钮
        tk.Button(self.root, text='开始打包', command=self.start_pack).grid(row=row, column=1, pady=10)
        row += 1
        # 日志输出
        tk.Label(self.root, text='日志输出:').grid(row=row, column=0, sticky='ne', padx=5, pady=5)
        self.log_text = scrolledtext.ScrolledText(self.root, width=70, height=12, state='disabled')
        self.log_text.grid(row=row, column=1, columnspan=2, padx=5, pady=5)

    def browse_py(self):
        file = filedialog.askopenfilename(filetypes=[('Python文件', '*.py')])
        if file:
            self.py_file.set(file)

    def browse_icon(self):
        file = filedialog.askopenfilename(filetypes=[('ICO文件', '*.ico')])
        if file:
            self.icon_file.set(file)

    def start_pack(self):
        py_path = self.py_file.get()
        if not py_path or not os.path.isfile(py_path):
            messagebox.showerror('错误', '请选择有效的Python脚本文件！')
            return
        # 先显示"打包中，请稍等...."
        self.log_text.config(state='normal')
        self.log_text.delete(1.0, tk.END)
        self.log('打包中，请稍等...')
        self.log_text.config(state='disabled')
        # 组装pyinstaller命令
        cmd = ['pyinstaller', '--noconfirm', '--clean']
        if self.no_console.get():
            cmd.append('--windowed')
        else:
            cmd.append('--console')
        if self.icon_file.get():
            cmd += ['--icon', self.icon_file.get()]
        # 如果没有icon参数，则不加--icon，让pyinstaller用默认图标
        # 处理元信息
        if self.app_name.get():
            cmd += ['--name', self.app_name.get()]
        if self.version.get():
            cmd += ['--version-file', self.create_version_file()]
        cmd.append(py_path)
        self.log('打包命令: ' + ' '.join(cmd))
        self.run_command(cmd)

    def create_version_file(self):
        # 生成标准的VSVersionInfo RC格式内容
        version = self.version.get() or '1.0.0.0'
        # 版本号格式转换 1.2.3 -> 1,2,3,0
        version_tuple = tuple((version + '.0.0.0').split('.')[:4])
        version_tuple = ','.join(version_tuple)
        author = self.author.get() or ''
        app_name = self.app_name.get() or ''
        email = self.email.get() or ''
        filename = os.path.basename(self.py_file.get()).replace('.py', '.exe')
        version_info = f"""
# UTF-8
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=({version_tuple}),
    prodvers=({version_tuple}),
    mask=0x3f,
    flags=0x0,
    OS=0x4,
    fileType=0x1,
    subtype=0x0,
    date=(0,0)
    ),
  kids=[
    StringFileInfo([
      StringTable(
        '040904B0',
        [StringStruct('CompanyName', '{author}'),
        StringStruct('FileDescription', '{app_name}'),
        StringStruct('FileVersion', '{version}'),
        StringStruct('InternalName', '{app_name}'),
        StringStruct('LegalCopyright', 'Copyright (c) {author}'),
        StringStruct('OriginalFilename', '{filename}'),
        StringStruct('ProductName', '{app_name}'),
        StringStruct('ProductVersion', '{version}'),
        StringStruct('Comments', 'Contact: {email}')])
      ]),
    VarFileInfo([VarStruct('Translation', [1033, 1200])])
  ]
)
"""
        version_path = os.path.join(os.path.dirname(self.py_file.get()), 'version.txt')
        with open(version_path, 'w', encoding='utf-8') as f:
            f.write(version_info)
        return version_path

    def run_command(self, cmd):
        try:
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            self.log_text.config(state='normal')
            self.log_text.delete(1.0, tk.END)
            for line in process.stdout:
                self.log(line)
            process.wait()
            if process.returncode == 0:
                self.log('打包完成！')
            else:
                self.log('打包失败，请检查日志。')
            self.log_text.config(state='disabled')
        except Exception as e:
            self.log(f'运行出错: {e}')

    def log(self, msg):
        self.log_text.config(state='normal')
        self.log_text.insert(tk.END, msg if msg.endswith('\n') else msg + '\n')
        self.log_text.see(tk.END)
        self.log_text.config(state='disabled')

def main():
    root = tk.Tk()
    app = PyInstallerGUI(root)
    root.mainloop()

if __name__ == '__main__':
    main() 