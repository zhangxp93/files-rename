# Git 忽略规则说明

## PyCharm / IntelliJ IDEA 文件

### 完全忽略 .idea 目录（推荐）
当前配置采用完全忽略 `.idea/` 目录的方式，这是最简单和安全的做法。

```gitignore
.idea/
```

### 被忽略的 PyCharm 文件类型

#### 1. 工作区和用户特定文件
- `workspace.xml` - 工作区布局和窗口状态
- `tasks.xml` - 任务配置
- `usage.statistics.xml` - 使用统计
- `dictionaries/` - 用户词典
- `shelf/` - 搁置的更改

#### 2. 数据源和数据库
- `dataSources/` - 数据源配置
- `dataSources.ids` - 数据源ID
- `dataSources.local.xml` - 本地数据源
- `sqlDataSources.xml` - SQL数据源

#### 3. UI和界面
- `uiDesigner.xml` - UI设计器配置
- `dynamic.xml` - 动态配置
- `dbnavigator.xml` - 数据库导航器

#### 4. 构建和依赖
- `gradle.xml` - Gradle配置
- `libraries/` - 库配置

#### 5. 插件相关
- `mongoSettings.xml` - MongoDB插件
- `sonarlint/` - SonarLint插件
- `httpRequests/` - HTTP客户端请求

#### 6. 缓存文件
- `caches/` - 各种缓存文件

### 项目文件类型
- `*.iml` - IntelliJ模块文件
- `*.iws` - IntelliJ工作区文件
- `*.ipr` - IntelliJ项目文件

## 其他开发工具

### Visual Studio Code
```gitignore
.vscode/
*.code-workspace
```

### 系统文件
```gitignore
# Windows
Thumbs.db
Desktop.ini
*.tmp

# macOS
.DS_Store
.Spotlight-V100
.Trashes

# Linux
*~
```

## Python 特定文件

### 编译和缓存
```gitignore
__pycache__/
*.py[cod]
*.so
*.egg
*.egg-info/
```

### 虚拟环境
```gitignore
venv/
env/
ENV/
venv_python/
```

### 打包文件
```gitignore
build/
dist/
*.spec
```

## 项目特定忽略

### 备份文件
```gitignore
*.bak
*.backup
*.old
backup_*/
```

### 日志和临时文件
```gitignore
*.log
*.tmp
*.temp
logs/
```

### 测试和覆盖率
```gitignore
.coverage
.pytest_cache/
htmlcov/
```

## 最佳实践

### 1. 团队协作
- 忽略所有用户特定的IDE配置
- 保留项目级别的配置（如果需要）
- 使用全局gitignore处理通用文件

### 2. 安全考虑
- 忽略包含敏感信息的配置文件
- 不提交数据库连接信息
- 排除API密钥和凭据

### 3. 性能优化
- 忽略大型构建产物
- 排除缓存文件
- 不跟踪临时文件

## 检查忽略状态

### 查看被忽略的文件
```bash
git status --ignored
```

### 强制添加被忽略的文件
```bash
git add -f <filename>
```

### 检查文件是否被忽略
```bash
git check-ignore <filename>
```

## 注意事项

1. **现有文件**: 如果文件已经被Git跟踪，添加到.gitignore不会自动忽略它们
2. **删除跟踪**: 需要先从Git中删除文件，然后添加到.gitignore
3. **全局忽略**: 可以设置全局gitignore处理通用文件类型

### 删除已跟踪的文件
```bash
# 从Git中删除但保留本地文件
git rm --cached <filename>

# 删除整个目录
git rm -r --cached <directory>
```
