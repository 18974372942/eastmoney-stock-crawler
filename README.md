# 东方财富网股票数据爬取与分析项目

## 项目概述
本项目是一个基于Python的股票数据爬取与分析工具，可从东方财富网获取股票历史数据，进行数据清洗、分析和可视化，并生成详细的分析报告。该项目采用模块化设计，结构清晰，易于扩展。

## 功能特点
- 支持爬取东方财富网股票历史K线数据（日线、周线、月线）
- 提供数据清洗功能，处理缺失值、异常值等
- 进行多维度数据分析，包括趋势分析、波动性分析、成交量分析等
- 提供多种可视化图表，直观展示股票走势
- 自动生成HTML格式的分析报告，包含图表和分析建议

## 安装与使用

### 安装依赖pip install -r requirements.txt
### 使用方法
1. 直接运行主程序（默认爬取贵州茅台数据）python main.py
2. 使用命令行参数指定爬取的股票和范围python main.py --stock_code 601318 --market sh --start_date 20230101 --end_date 20250601 --kline_type day --analysis --visualization
### 命令行参数说明
- `--stock_code`: 股票代码，默认为600519（贵州茅台）
- `--market`: 股票市场，sh表示沪市，sz表示深市，默认为沪市
- `--start_date`: 开始日期，格式为YYYYMMDD，默认为20240101
- `--end_date`: 结束日期，格式为YYYYMMDD，默认为20250601
- `--kline_type`: K线类型，day表示日线，week表示周线，month表示月线，默认为日线
- `--output_dir`: 数据输出目录，默认为data
- `--analysis`: 是否进行数据分析，默认不进行
- `--visualization`: 是否进行数据可视化，默认不进行

## 项目结构eastmoney-stock-crawler/
├── main.py                   # 项目主入口
├── src/                      # 源代码目录
│   ├── crawler.py            # 数据爬取模块
│   ├── analyzer.py           # 数据分析模块
│   ├── visualizer.py         # 数据可视化模块
│   ├── config.py             # 配置类
│   ├── report_generator.py   # 报告生成模块
│   └── __init__.py           # 包初始化文件
├── data/                     # 数据输出目录（自动生成）
│   ├── visualizations/       # 可视化图表（自动生成）
│   └── reports/              # 分析报告（自动生成）
├── requirements.txt          # 依赖包清单
└── README.md                 # 项目说明文档
## 注意事项
1. 爬取数据时请遵守东方财富网的`robots.txt`协议，避免频繁请求导致IP被封
2. 由于网站结构可能会变化，如遇爬取失败，请检查并更新爬取代码
3. 本项目仅供学习交流使用，不构成投资建议

## 贡献
欢迎提交Issue和Pull Request来改进项目！    