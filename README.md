# Font Tools

一个基于 Flask 的在线字体工具，支持字体元数据查看和字体子集化功能。

## 功能特性

- 支持 TTF/OTF 字体文件上传
- 查看字体元数据信息
- 根据指定文字创建字体子集，减小字体文件体积
- 简洁的 Bootstrap 界面

## 技术栈

- Python 3.12
- Flask
- FontTools
- Bootstrap
- Docker

## 快速开始

### 使用 Docker
```bash
# 构建 Docker 镜像
docker build -t font-tools .

# 运行 Docker 容器
docker run -d -p 5000:5000 font-tools
```

### 本地运行
```bash
# 安装依赖
pip install -r requirements.txt

# 运行 Flask 应用
python -m flask run
```

访问 http://localhost:5000 即可使用

## 使用说明

1. 上传字体：支持上传 TTF 或 OTF 格式的字体文件
2. 查看元数据：选择已上传的字体文件，点击"获取元信息"按钮
3. 创建子集：选择字体文件，输入需要保留的文字，点击"生成子集"按钮

## 注意事项

- 上传的字体文件保存在 app/fonts 目录
- 生成的子集字体文件以 "subset_" 为前缀