# File Rename Tool

## 🌐 Language / 语言

- [中文](README.md) | [English](#file-rename-tool)

A simple and easy-to-use batch file renaming tool with graphical interface and secure backup functionality.

## 🌟 Features

- 🎯 **Batch Rename** - Support batch find and replace text in filenames
- 🔍 **Preview Function** - Preview all changes before renaming
- 💾 **Auto Backup** - Automatically create file backups before renaming (optional)
- 🖥️ **GUI Interface** - Clean and intuitive user interface
- ⚡ **Lightweight** - Uses only Python built-in libraries, no additional dependencies
- 🛡️ **Safe & Reliable** - Multiple confirmation mechanisms to prevent misoperations
- 🧵 **Multi-threading** - Responsive interface with cancellation support

## 📱 Interface Overview

The program includes the following main areas:
- **Folder Selection** - Choose the folder to process
- **Replace Settings** - Set find and replace text
- **Safety Options** - Choose whether to create backups
- **Action Buttons** - Preview changes, execute rename, cancel operation, clear results
- **Progress Display** - Real-time processing progress
- **Results Display** - Show detailed operation logs

## 📋 Requirements

- Python 3.6 or higher
- tkinter (Python standard library, usually pre-installed)

## 🚀 Usage

### Method 1: Run Python Script Directly
```bash
python src/files_renames.py
```

### Method 2: Use Packaged Executable
1. Download `dist/文件重命名工具_v2.1_updated.exe`
2. Double-click to run, no Python environment required
3. Compatible with all Windows systems (Win7/8/10/11)

### Method 3: Build Executable Yourself
If you want to build the program yourself:
```bash
# Method 1: Use root directory quick build script
build.bat

# Method 2: Enter build directory and use dedicated script
cd build
一键打包.bat

# Method 3: Manual build
pip install pyinstaller
pyinstaller --onefile --windowed --name="FileRenameTool_v2.1" --distpath="dist" "src/files_renames.py"
```

## 📖 Usage Steps

1. **Select Folder** - Click "Browse Folder" to select the folder containing files to rename
2. **Set Replace Rules** - Enter the text to find in "Find Text" and the replacement text in "Replace With"
3. **Confirm Backup Option** - Recommend keeping "Create file backup before renaming" option enabled
4. **Preview Changes** - Click "Preview Changes" to see the renaming operations to be performed
5. **Execute Rename** - After confirmation, click "Execute Rename"
6. **Cancel Operation** - If needed, click "Cancel Operation" button to interrupt

## 💡 Example

Suppose you have the following files:
```
test_file_85C.txt
data_file_85C.csv
config_file_85C.json
```

**Settings:**
- Find Text: `85C`
- Replace With: `25C`

**Result:**
```
test_file_25C.txt
data_file_25C.csv
config_file_25C.json
```

## 🛡️ Safety Features

### Auto Backup
- Program creates `backup_[timestamp]` folder in target directory
- Automatically copies original files to backup folder before renaming
- Timestamp format: `YYYYMMDD_HHMMSS`

### Safety Checks
- Checks if target file already exists before renaming
- Asks user whether to continue if backup fails
- Multiple confirmation dialogs to prevent misoperations
- Support canceling ongoing operations at any time

## 📁 File Structure

```
files-rename/
├── src/                      # Source code directory
│   └── files_renames.py     # Main program file
├── build/                    # Build scripts directory
│   ├── 一键打包.bat         # Simple build script (recommended)
│   ├── 高级打包工具.bat     # Advanced build script
│   ├── 打包工具.bat         # Original build script
│   ├── 文件重命名工具.spec  # PyInstaller config file
│   └── version_info.txt      # Version info file
├── docs/                     # Documentation directory
│   ├── README_打包说明.md   # Build instructions
│   ├── Git忽略规则说明.md   # Git ignore rules
│   └── 开发说明.md          # Development guide
├── dist/                     # Build output directory
│   └── 文件重命名工具_v2.1_updated.exe  # Executable file
├── venv_python/              # Virtual environment directory
├── README.md                 # Main project documentation (Chinese/English)
├── README_EN.md              # English documentation
├── LICENSE                   # MIT License
├── .gitignore               # Git ignore file
├── requirements.txt          # Dependencies file
└── build.bat                 # Quick build script
```

## 🔧 Development Info

- **Language**: Python 3
- **GUI Framework**: tkinter
- **License**: MIT License

## 🤝 Contributing

Welcome to submit Issues and Pull Requests to improve this project.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📝 Changelog

### v2.1
- Added multi-threading support
- Optimized interface responsiveness
- Added operation cancellation
- Real-time progress display
- Increased interface size (800px height)
- Updated default values (85C → 25C)

### v2.0
- Added auto backup feature
- Improved user interface
- Enhanced error handling
- Added detailed documentation

### v1.0
- Basic batch rename functionality
- Graphical user interface
- Preview feature
- Detailed operation logs

## ❓ FAQ

**Q: What file types does the program support?**
A: Supports all file types, the program only modifies filenames, not file contents.

**Q: Will backup files take up a lot of space?**
A: The backup feature copies original files, please ensure sufficient disk space.

**Q: How to restore renamed files?**
A: If backup is enabled, you can restore original files from the `backup_[timestamp]` folder.

**Q: Does the program support regular expressions?**
A: The current version uses simple text replacement and does not support regular expressions.

**Q: Can I cancel an ongoing operation?**
A: Yes, click the "Cancel Operation" button to safely interrupt the current operation.

**Q: Why does the interface freeze when processing many files?**
A: This issue has been resolved in v2.1 with multi-threading support. The interface now remains responsive during operations.

---

## 🌟 Screenshots

*Note: Add screenshots here if available*

## 🔗 Related Links

- [Chinese Documentation](README.md)
- [Build Instructions](docs/README_打包说明.md)
- [Development Guide](docs/开发说明.md)
- [Git Configuration](docs/Git忽略规则说明.md)

---

**Thank you for using File Rename Tool!** 🎉

If you find this project helpful, please consider giving it a ⭐ star!
