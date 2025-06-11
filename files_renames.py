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
        self.find_var = tk.StringVar(value="1_PN_refpow5_SMPL0916_I_+85")
        self.replace_var = tk.StringVar(value="1_PN_refpow5_SMPL0916_I_+25")
        self.backup_var = tk.BooleanVar(value=True)  # 默认启用备份
        
        self.create_widgets()
        self.center_window()
        
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

        execute_btn = tk.Button(button_frame, text="执行重命名",
                               command=self.execute_rename,
                               bg='#27ae60', fg='white', **btn_style)
        execute_btn.pack(side="left", padx=(0, 10))

        clear_btn = tk.Button(button_frame, text="清空结果",
                             command=self.clear_results,
                             bg='#95a5a6', fg='white', **btn_style)
        clear_btn.pack(side="left")
        
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
        """添加结果文本"""
        self.result_text.insert(tk.END, text)
        self.result_text.see(tk.END)
        self.root.update_idletasks()
        
    def clear_results(self):
        """清空结果"""
        self.result_text.delete(1.0, tk.END)
        self.status_var.set("已清空结果")

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
        """执行重命名"""
        if not self.validate_inputs():
            return
            
        # 确认对话框
        result = messagebox.askyesnocancel(
            "确认操作", 
            "确定要执行文件重命名操作吗？\n\n⚠️ 此操作不可撤销！\n\n建议先点击'预览更改'查看效果。"
        )
        
        if not result:
            return
            
        folder_path = self.folder_var.get()
        find_text = self.find_var.get()
        replace_text = self.replace_var.get()
        enable_backup = self.backup_var.get()

        self.add_result("=" * 60 + "\n")
        self.add_result("🚀 开始执行重命名\n")
        self.add_result("=" * 60 + "\n")

        # 创建备份文件夹（如果启用备份）
        backup_folder = None
        if enable_backup:
            self.add_result("📁 创建备份文件夹...\n")
            backup_folder = self.create_backup_folder(folder_path)
            if backup_folder:
                self.add_result(f"✅ 备份文件夹已创建: {os.path.basename(backup_folder)}\n")
            else:
                self.add_result("❌ 备份文件夹创建失败，继续执行重命名（不备份）\n")

        success_count = 0
        error_count = 0
        backup_count = 0
        
        try:
            for filename in os.listdir(folder_path):
                file_path = os.path.join(folder_path, filename)
                if os.path.isfile(file_path) and find_text in filename:
                    new_filename = filename.replace(find_text, replace_text)
                    old_file = os.path.join(folder_path, filename)
                    new_file = os.path.join(folder_path, new_filename)
                    
                    try:
                        # 检查新文件是否已存在
                        if os.path.exists(new_file):
                            self.add_result(f"⚠️  跳过: {filename} (目标文件已存在)\n")
                            error_count += 1
                            continue

                        # 备份原文件（如果启用备份）
                        backup_success = True
                        if enable_backup and backup_folder:
                            backup_success = self.backup_file(old_file, backup_folder)
                            if backup_success:
                                backup_count += 1
                                self.add_result(f"💾 已备份: {filename}\n")
                            else:
                                # 备份失败，询问是否继续
                                continue_rename = messagebox.askyesno(
                                    "备份失败",
                                    f"文件 {filename} 备份失败！\n\n是否继续重命名此文件？"
                                )
                                if not continue_rename:
                                    self.add_result(f"⏭️  跳过: {filename} (用户选择不重命名)\n")
                                    error_count += 1
                                    continue

                        os.rename(old_file, new_file)
                        self.add_result(f"✅ 重命名成功: {filename}\n    -> {new_filename}\n")
                        success_count += 1

                    except Exception as e:
                        self.add_result(f"❌ 重命名失败: {filename}\n    错误: {str(e)}\n")
                        error_count += 1
                        
        except Exception as e:
            messagebox.showerror("处理错误", f"处理文件夹时出错:\n{str(e)}")
            return
            
        self.add_result("=" * 60 + "\n")
        self.add_result("🎉 重命名操作完成！\n")
        self.add_result(f"✅ 重命名成功: {success_count} 个文件\n")
        self.add_result(f"❌ 重命名失败: {error_count} 个文件\n")
        if enable_backup:
            self.add_result(f"💾 文件备份: {backup_count} 个文件\n")
            if backup_folder and backup_count > 0:
                self.add_result(f"📁 备份位置: {backup_folder}\n")
        self.add_result("=" * 60 + "\n\n")

        status_msg = f"重命名完成 - 成功: {success_count}, 失败: {error_count}"
        if enable_backup:
            status_msg += f", 备份: {backup_count}"
        self.status_var.set(status_msg)

        if success_count > 0:
            result_msg = f"文件重命名完成！\n\n✅ 重命名成功: {success_count} 个文件\n❌ 重命名失败: {error_count} 个文件"
            if enable_backup and backup_count > 0:
                result_msg += f"\n💾 文件备份: {backup_count} 个文件"
            messagebox.showinfo("操作完成", result_msg)


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
        if messagebox.askokcancel("退出", "确定要退出文件重命名工具吗？"):
            root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()


if __name__ == "__main__":
    main()
