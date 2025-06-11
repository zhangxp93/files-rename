#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
优化版文件重命名工具 - 减少依赖，优化打包大小
使用Python内置的tkinter库，无额外依赖
"""

import os
import tkinter as tk
from tkinter import filedialog, messagebox
import sys
import shutil
from datetime import datetime
import threading
import queue


class OptimizedFileRenamer:
    def __init__(self, root):
        self.root = root
        self.root.title("文件重命名工具 v1.0")
        self.root.geometry("700x650")
        self.root.resizable(True, True)
        
        # 设置窗口图标（使用默认）
        try:
            self.root.iconbitmap(default='')
        except:
            pass
        
        # 变量
        self.folder_var = tk.StringVar()
        self.find_var = tk.StringVar(value="85C")
        self.replace_var = tk.StringVar(value="25C")
        self.backup_var = tk.BooleanVar(value=True)  # 默认启用备份

        # 线程管理
        self.is_processing = False
        self.current_thread = None
        self.message_queue = queue.Queue()
        
        self.create_widgets()
        self.center_window()

        # 启动消息处理
        self.process_queue()
        
    def center_window(self):
        """窗口居中显示"""
        self.root.update_idletasks()
        width = 700
        height = 650
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def create_widgets(self):
        """创建界面组件"""
        # 主框架
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill="both", expand=True, padx=15, pady=15)

        # 标题
        title_label = tk.Label(main_frame, text="文件重命名工具",
                              font=("Microsoft YaHei", 18, "bold"),
                              bg='#f0f0f0', fg='#2c3e50')
        title_label.pack(pady=(0, 20))

        # 文件夹选择区域
        folder_frame = tk.LabelFrame(main_frame, text=" 选择文件夹 ",
                                    font=("Microsoft YaHei", 10, "bold"),
                                    bg='#f0f0f0', fg='#34495e', padx=10, pady=10)
        folder_frame.pack(fill="x", pady=(0, 15))
        
        folder_entry_frame = tk.Frame(folder_frame, bg='#f0f0f0')
        folder_entry_frame.pack(fill="x")

        self.folder_entry = tk.Entry(folder_entry_frame, textvariable=self.folder_var,
                                    font=("Consolas", 10), state="readonly",
                                    bg='white', relief="sunken", bd=1)
        self.folder_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))

        browse_btn = tk.Button(folder_entry_frame, text="浏览文件夹",
                              command=self.browse_folder,
                              font=("Microsoft YaHei", 9),
                              bg='#3498db', fg='white', relief="flat",
                              padx=15, pady=5, cursor='hand2')
        browse_btn.pack(side="right")
        
        # 文本替换设置区域
        replace_frame = tk.LabelFrame(main_frame, text=" 替换设置 ",
                                     font=("Microsoft YaHei", 10, "bold"),
                                     bg='#f0f0f0', fg='#34495e', padx=10, pady=10)
        replace_frame.pack(fill="x", pady=(0, 15))

        # 查找文本
        find_label = tk.Label(replace_frame, text="查找文本:",
                             font=("Microsoft YaHei", 9), bg='#f0f0f0')
        find_label.pack(anchor="w")

        find_entry = tk.Entry(replace_frame, textvariable=self.find_var,
                             font=("Consolas", 10), bg='white', relief="sunken", bd=1)
        find_entry.pack(fill="x", pady=(5, 10))

        # 替换文本
        replace_label = tk.Label(replace_frame, text="替换为:",
                                font=("Microsoft YaHei", 9), bg='#f0f0f0')
        replace_label.pack(anchor="w")

        replace_entry = tk.Entry(replace_frame, textvariable=self.replace_var,
                                font=("Consolas", 10), bg='white', relief="sunken", bd=1)
        replace_entry.pack(fill="x", pady=(5, 0))

        # 备份选项区域
        backup_frame = tk.LabelFrame(main_frame, text=" 安全选项 ",
                                    font=("Microsoft YaHei", 10, "bold"),
                                    bg='#f0f0f0', fg='#34495e', padx=10, pady=10)
        backup_frame.pack(fill="x", pady=(15, 15))

        backup_checkbox = tk.Checkbutton(backup_frame, text="重命名前创建文件备份（推荐）",
                                        variable=self.backup_var,
                                        font=("Microsoft YaHei", 9), bg='#f0f0f0',
                                        fg='#2c3e50', activebackground='#f0f0f0')
        backup_checkbox.pack(anchor="w")

        backup_info = tk.Label(backup_frame, text="💡 备份文件将保存在目标文件夹的 backup_[时间戳] 子文件夹中",
                              font=("Microsoft YaHei", 8), bg='#f0f0f0', fg='#7f8c8d')
        backup_info.pack(anchor="w", pady=(5, 0))

        # 按钮区域
        button_frame = tk.Frame(main_frame, bg='#f0f0f0')
        button_frame.pack(fill="x", pady=(15, 0))

        # 按钮样式
        btn_style = {
            'font': ("Microsoft YaHei", 10, "bold"),
            'relief': "flat",
            'padx': 20,
            'pady': 8,
            'cursor': 'hand2'
        }

        preview_btn = tk.Button(button_frame, text="预览更改",
                               command=self.preview_changes,
                               bg='#f39c12', fg='white', **btn_style)
        preview_btn.pack(side="left", padx=(0, 10))

        self.execute_btn = tk.Button(button_frame, text="执行重命名",
                                    command=self.execute_rename,
                                    bg='#27ae60', fg='white', **btn_style)
        self.execute_btn.pack(side="left", padx=(0, 10))

        self.cancel_btn = tk.Button(button_frame, text="取消操作",
                                   command=self.cancel_operation,
                                   bg='#e74c3c', fg='white', **btn_style,
                                   state="disabled")
        self.cancel_btn.pack(side="left", padx=(0, 10))

        clear_btn = tk.Button(button_frame, text="清空结果",
                             command=self.clear_results,
                             bg='#95a5a6', fg='white', **btn_style)
        clear_btn.pack(side="left")

        # 进度条区域
        progress_frame = tk.Frame(main_frame, bg='#f0f0f0')
        progress_frame.pack(fill="x", pady=(10, 0))

        self.progress_var = tk.StringVar(value="")
        self.progress_label = tk.Label(progress_frame, textvariable=self.progress_var,
                                      font=("Microsoft YaHei", 9), bg='#f0f0f0', fg='#2c3e50')
        self.progress_label.pack(anchor="w")

        # 结果显示区域
        result_frame = tk.LabelFrame(main_frame, text=" 操作结果 ",
                                    font=("Microsoft YaHei", 10, "bold"),
                                    bg='#f0f0f0', fg='#34495e', padx=10, pady=10)
        result_frame.pack(fill="both", expand=True, pady=(15, 0))

        # 创建文本框和滚动条
        text_frame = tk.Frame(result_frame, bg='#f0f0f0')
        text_frame.pack(fill="both", expand=True)

        self.result_text = tk.Text(text_frame, font=("Consolas", 9),
                                  wrap="word", bg='white', fg='#2c3e50',
                                  relief="sunken", bd=1, height=30)

        scrollbar = tk.Scrollbar(text_frame, orient="vertical",
                                command=self.result_text.yview)
        self.result_text.configure(yscrollcommand=scrollbar.set)

        self.result_text.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # 状态栏
        self.status_var = tk.StringVar(value="就绪 - 请选择文件夹并设置替换规则")
        status_bar = tk.Label(main_frame, textvariable=self.status_var,
                             relief="sunken", anchor="w",
                             font=("Microsoft YaHei", 8), bg='#ecf0f1', fg='#7f8c8d')
        status_bar.pack(fill="x", pady=(10, 0))
        
    def browse_folder(self):
        """浏览文件夹"""
        folder = filedialog.askdirectory(title="选择要处理的文件夹")
        if folder:
            self.folder_var.set(folder)
            self.add_result(f"✓ 已选择文件夹: {folder}\n\n")
            self.status_var.set(f"已选择文件夹: {os.path.basename(folder)}")
            
    def add_result(self, text):
        """添加结果文本（线程安全）"""
        if threading.current_thread() == threading.main_thread():
            # 主线程直接更新
            self.result_text.insert(tk.END, text)
            self.result_text.see(tk.END)
            self.root.update_idletasks()
        else:
            # 工作线程通过队列发送消息
            self.message_queue.put(('add_result', text))

    def add_result_direct(self, text):
        """直接添加结果文本（仅主线程调用）"""
        self.result_text.insert(tk.END, text)
        self.result_text.see(tk.END)
        self.root.update_idletasks()

    def clear_results(self):
        """清空结果"""
        self.result_text.delete(1.0, tk.END)
        self.status_var.set("已清空结果")
        self.progress_var.set("")

    def process_queue(self):
        """处理消息队列"""
        try:
            while True:
                message_type, data = self.message_queue.get_nowait()
                if message_type == 'add_result':
                    self.add_result_direct(data)
                elif message_type == 'set_status':
                    self.status_var.set(data)
                elif message_type == 'set_progress':
                    self.progress_var.set(data)
                elif message_type == 'operation_complete':
                    self.operation_complete(data)
                elif message_type == 'enable_buttons':
                    self.set_buttons_state(True)
        except queue.Empty:
            pass

        # 每100ms检查一次队列
        self.root.after(100, self.process_queue)

    def set_buttons_state(self, enabled):
        """设置按钮状态"""
        if enabled:
            self.execute_btn.config(state="normal")
            self.cancel_btn.config(state="disabled")
            self.is_processing = False
        else:
            self.execute_btn.config(state="disabled")
            self.cancel_btn.config(state="normal")
            self.is_processing = True

    def cancel_operation(self):
        """取消当前操作"""
        if self.current_thread and self.current_thread.is_alive():
            self.is_processing = False
            self.add_result("\n⚠️ 用户取消操作...\n")
            self.status_var.set("操作已取消")
            self.progress_var.set("")
            self.set_buttons_state(True)

    def create_backup_folder(self, folder_path):
        """创建备份文件夹"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_folder = os.path.join(folder_path, f"backup_{timestamp}")

        try:
            os.makedirs(backup_folder, exist_ok=True)
            return backup_folder
        except Exception as e:
            self.add_result(f"❌ 创建备份文件夹失败: {str(e)}\n")
            return None

    def backup_file(self, file_path, backup_folder):
        """备份单个文件"""
        try:
            filename = os.path.basename(file_path)
            backup_path = os.path.join(backup_folder, filename)
            shutil.copy2(file_path, backup_path)
            return True
        except Exception as e:
            self.add_result(f"❌ 备份文件失败 {filename}: {str(e)}\n")
            return False

    def validate_inputs(self):
        """验证输入"""
        if not self.folder_var.get():
            messagebox.showerror("输入错误", "请先选择一个文件夹！")
            return False
            
        if not os.path.exists(self.folder_var.get()):
            messagebox.showerror("路径错误", "选择的文件夹不存在！")
            return False
            
        if not self.find_var.get().strip():
            messagebox.showerror("输入错误", "请输入要查找的文本！")
            return False
            
        return True
        
    def preview_changes(self):
        """预览更改"""
        if not self.validate_inputs():
            return
            
        folder_path = self.folder_var.get()
        find_text = self.find_var.get()
        replace_text = self.replace_var.get()
        
        self.add_result("=" * 60 + "\n")
        self.add_result("🔍 预览更改\n")
        self.add_result("=" * 60 + "\n")
        
        found_files = []
        
        try:
            for filename in os.listdir(folder_path):
                if os.path.isfile(os.path.join(folder_path, filename)) and find_text in filename:
                    new_filename = filename.replace(find_text, replace_text)
                    found_files.append((filename, new_filename))
                    self.add_result(f"📄 原文件名: {filename}\n")
                    self.add_result(f"📝 新文件名: {new_filename}\n")
                    self.add_result("-" * 40 + "\n")
                    
            if found_files:
                self.add_result(f"\n📊 总共找到 {len(found_files)} 个文件需要重命名。\n\n")
                self.status_var.set(f"找到 {len(found_files)} 个文件可以重命名")
            else:
                self.add_result("❌ 没有找到包含指定文本的文件。\n\n")
                self.status_var.set("没有找到匹配的文件")
                
        except Exception as e:
            messagebox.showerror("读取错误", f"读取文件夹时出错:\n{str(e)}")
            
    def execute_rename(self):
        """执行重命名（主线程）"""
        if self.is_processing:
            messagebox.showwarning("操作进行中", "当前有操作正在进行，请等待完成或取消后再试。")
            return

        if not self.validate_inputs():
            return

        # 确认对话框
        result = messagebox.askyesnocancel(
            "确认操作",
            "确定要执行文件重命名操作吗？\n\n⚠️ 此操作不可撤销！\n\n建议先点击'预览更改'查看效果。"
        )

        if not result:
            return

        # 设置按钮状态
        self.set_buttons_state(False)

        # 获取参数
        folder_path = self.folder_var.get()
        find_text = self.find_var.get()
        replace_text = self.replace_var.get()
        enable_backup = self.backup_var.get()

        # 在工作线程中执行重命名
        self.current_thread = threading.Thread(
            target=self._execute_rename_worker,
            args=(folder_path, find_text, replace_text, enable_backup),
            daemon=True
        )
        self.current_thread.start()

    def _execute_rename_worker(self, folder_path, find_text, replace_text, enable_backup):
        """执行重命名（工作线程）"""
        try:
            self.message_queue.put(('add_result', "=" * 60 + "\n"))
            self.message_queue.put(('add_result', "🚀 开始执行重命名\n"))
            self.message_queue.put(('add_result', "=" * 60 + "\n"))
            self.message_queue.put(('set_status', "正在执行重命名操作..."))

            # 创建备份文件夹（如果启用备份）
            backup_folder = None
            if enable_backup:
                self.message_queue.put(('add_result', "📁 创建备份文件夹...\n"))
                backup_folder = self.create_backup_folder(folder_path)
                if backup_folder:
                    self.message_queue.put(('add_result', f"✅ 备份文件夹已创建: {os.path.basename(backup_folder)}\n"))
                else:
                    self.message_queue.put(('add_result', "❌ 备份文件夹创建失败，继续执行重命名（不备份）\n"))

            # 获取所有需要处理的文件
            files_to_process = []
            for filename in os.listdir(folder_path):
                if not self.is_processing:  # 检查是否被取消
                    break
                file_path = os.path.join(folder_path, filename)
                if os.path.isfile(file_path) and find_text in filename:
                    new_filename = filename.replace(find_text, replace_text)
                    files_to_process.append((filename, new_filename))

            if not self.is_processing:
                self.message_queue.put(('add_result', "\n⚠️ 操作已取消\n"))
                self.message_queue.put(('enable_buttons', None))
                return

            total_files = len(files_to_process)
            if total_files == 0:
                self.message_queue.put(('add_result', "❌ 没有找到需要重命名的文件\n"))
                self.message_queue.put(('enable_buttons', None))
                return

            success_count = 0
            error_count = 0
            backup_count = 0

            for i, (filename, new_filename) in enumerate(files_to_process):
                if not self.is_processing:  # 检查是否被取消
                    break

                # 更新进度
                progress = f"正在处理: {i+1}/{total_files} - {filename}"
                self.message_queue.put(('set_progress', progress))

                old_file = os.path.join(folder_path, filename)
                new_file = os.path.join(folder_path, new_filename)

                try:
                    # 检查新文件是否已存在
                    if os.path.exists(new_file):
                        self.message_queue.put(('add_result', f"⚠️  跳过: {filename} (目标文件已存在)\n"))
                        error_count += 1
                        continue

                    # 备份原文件（如果启用备份）
                    if enable_backup and backup_folder:
                        if self.backup_file(old_file, backup_folder):
                            backup_count += 1
                            self.message_queue.put(('add_result', f"💾 已备份: {filename}\n"))

                    # 执行重命名
                    os.rename(old_file, new_file)
                    self.message_queue.put(('add_result', f"✅ 重命名成功: {filename}\n    -> {new_filename}\n"))
                    success_count += 1

                except Exception as e:
                    self.message_queue.put(('add_result', f"❌ 重命名失败: {filename}\n    错误: {str(e)}\n"))
                    error_count += 1

            # 操作完成
            result_data = {
                'success_count': success_count,
                'error_count': error_count,
                'backup_count': backup_count,
                'backup_folder': backup_folder,
                'enable_backup': enable_backup,
                'cancelled': not self.is_processing
            }
            self.message_queue.put(('operation_complete', result_data))

        except Exception as e:
            self.message_queue.put(('add_result', f"❌ 处理过程中发生错误: {str(e)}\n"))
            self.message_queue.put(('enable_buttons', None))

    def operation_complete(self, result_data):
        """操作完成处理（主线程）"""
        success_count = result_data['success_count']
        error_count = result_data['error_count']
        backup_count = result_data['backup_count']
        backup_folder = result_data['backup_folder']
        enable_backup = result_data['enable_backup']
        cancelled = result_data['cancelled']

        if cancelled:
            self.add_result_direct("\n⚠️ 操作已取消\n")
            self.status_var.set("操作已取消")
        else:
            self.add_result_direct("=" * 60 + "\n")
            self.add_result_direct("🎉 重命名操作完成！\n")
            self.add_result_direct(f"✅ 重命名成功: {success_count} 个文件\n")
            self.add_result_direct(f"❌ 重命名失败: {error_count} 个文件\n")
            if enable_backup:
                self.add_result_direct(f"💾 文件备份: {backup_count} 个文件\n")
                if backup_folder and backup_count > 0:
                    self.add_result_direct(f"📁 备份位置: {backup_folder}\n")
            self.add_result_direct("=" * 60 + "\n\n")

            status_msg = f"重命名完成 - 成功: {success_count}, 失败: {error_count}"
            if enable_backup:
                status_msg += f", 备份: {backup_count}"
            self.status_var.set(status_msg)

            if success_count > 0:
                result_msg = f"文件重命名完成！\n\n✅ 重命名成功: {success_count} 个文件\n❌ 重命名失败: {error_count} 个文件"
                if enable_backup and backup_count > 0:
                    result_msg += f"\n💾 文件备份: {backup_count} 个文件"
                messagebox.showinfo("操作完成", result_msg)

        self.progress_var.set("")
        self.set_buttons_state(True)


def main():
    """主函数"""
    root = tk.Tk()
    
    # 设置应用程序图标和属性
    try:
        # Windows下设置任务栏图标
        if sys.platform.startswith('win'):
            import ctypes
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('FileRenamer.1.0')
    except:
        pass
    
    app = OptimizedFileRenamer(root)
    
    # 设置关闭事件
    def on_closing():
        if app.is_processing:
            if messagebox.askyesno("退出确认", "当前有操作正在进行，确定要退出吗？\n\n退出将取消当前操作。"):
                app.is_processing = False  # 取消当前操作
                root.destroy()
        else:
            if messagebox.askokcancel("退出", "确定要退出文件重命名工具吗？"):
                root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()


if __name__ == "__main__":
    main()
