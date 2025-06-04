import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from typing import Optional

class StockVisualizer:
    def __init__(self, config, data):
        self.config = config
        self.data = data.copy()  # 复制数据，避免修改原始数据
        self._preprocess_data()
        
        # 创建可视化输出目录
        self.vis_dir = os.path.join(config.output_dir, "visualizations")
        if not os.path.exists(self.vis_dir):
            os.makedirs(self.vis_dir)
    
    def _preprocess_data(self):
        """数据预处理"""
        # 将日期列转换为datetime类型
        self.data['日期'] = pd.to_datetime(self.data['日期'])
        
        # 按日期排序
        self.data = self.data.sort_values('日期')
        
        # 计算移动平均线
        self.data['MA5'] = self.data['收盘价'].rolling(window=5).mean()  # 5日均线
        self.data['MA10'] = self.data['收盘价'].rolling(window=10).mean()  # 10日均线
        self.data['MA20'] = self.data['收盘价'].rolling(window=20).mean()  # 20日均线
    
    def visualize(self):
        """执行数据可视化"""
        # 1. 绘制价格走势与均线图
        self._plot_price_and_ma()
        
        # 2. 绘制K线图（简化版）
        self._plot_candlestick_chart()
        
        # 3. 绘制成交量图
        self._plot_volume()
        
        # 4. 绘制价格与成交量关系图
        self._plot_price_volume_relationship()
        
        # 5. 绘制月度收盘价统计
        self._plot_monthly_close_price()
        
        # 6. 绘制涨跌幅分布
        self._plot_price_change_distribution()
        
        print(f"所有可视化图表已保存至{self.vis_dir}目录")
    
    def _plot_price_and_ma(self):
        """绘制价格走势与均线图"""
        plt.figure(figsize=(12, 6))
        
        # 绘制收盘价
        plt.plot(self.data['日期'], self.data['收盘价'], label='收盘价', color='#00A1FF', linewidth=2, zorder=3)
        
        # 绘制均线
        plt.plot(self.data['日期'], self.data['MA5'], label='5日均线', color='#FF7D00', linewidth=1.5, zorder=2)
        plt.plot(self.data['日期'], self.data['MA10'], label='10日均线', color='#E60012', linewidth=1.5, zorder=2)
        plt.plot(self.data['日期'], self.data['MA20'], label='20日均线', color='#00B27A', linewidth=1.5, zorder=2)
        
        plt.title(f"{self.config.stock_code}价格走势与均线图")
        plt.xlabel('日期')
        plt.ylabel('价格(元)')
        plt.xticks(rotation=45, ha='right')
        plt.legend()
        
        # 移除左、右、上三边的边框
        plt.gca().spines['left'].set_visible(False)
        plt.gca().spines['right'].set_visible(False)
        plt.gca().spines['top'].set_visible(False)
        
        # 添加网格横线
        plt.grid(axis='y', linestyle='-', zorder=0)
        
        # 保存图表
        file_path = os.path.join(self.vis_dir, f"{self.config.stock_code}_价格走势与均线图.png")
        plt.tight_layout()
        plt.savefig(file_path, dpi=300)
        plt.close()
    
    def _plot_candlestick_chart(self):
        """绘制K线图（简化版）"""
        # 由于matplotlib的mplfinance需要OHLC格式，这里简化处理
        plt.figure(figsize=(12, 6))
        
        # 绘制上涨和下跌的K线
        up = self.data[self.data['收盘价'] >= self.data['开盘价']]
        down = self.data[self.data['收盘价'] < self.data['开盘价']]
        
        # 绘制上涨K线（绿色）
        plt.bar(up['日期'], up['收盘价'] - up['开盘价'], bottom=up['开盘价'], color='#00B27A', width=0.6)
        plt.bar(up['日期'], up['最高价'] - up['收盘价'], bottom=up['收盘价'], color='#00B27A', width=0.2)
        plt.bar(up['日期'], up['开盘价'] - up['最低价'], bottom=up['最低价'], color='#00B27A', width=0.2)
        
        # 绘制下跌K线（红色）
        plt.bar(down['日期'], down['收盘价'] - down['开盘价'], bottom=down['开盘价'], color='#E60012', width=0.6)
        plt.bar(down['日期'], down['最高价'] - down['开盘价'], bottom=down['开盘价'], color='#E60012', width=0.2)
        plt.bar(down['日期'], down['收盘价'] - down['最低价'], bottom=down['最低价'], color='#E60012', width=0.2)
        
        # 添加均线
        plt.plot(self.data['日期'], self.data['MA5'], label='5日均线', color='#FF7D00', linewidth=1.5, zorder=2)
        plt.plot(self.data['日期'], self.data['MA10'], label='10日均线', color='#0066CC', linewidth=1.5, zorder=2)
        
        plt.title(f"{self.config.stock_code}K线图（简化版）")
        plt.xlabel('日期')
        plt.ylabel('价格(元)')
        plt.xticks(rotation=45, ha='right')
        plt.legend()
        
        # 移除左、右、上三边的边框
        plt.gca().spines['left'].set_visible(False)
        plt.gca().spines['right'].set_visible(False)
        plt.gca().spines['top'].set_visible(False)
        
        # 添加网格横线
        plt.grid(axis='y', linestyle='-', zorder=0)
        
        # 保存图表
        file_path = os.path.join(self.vis_dir, f"{self.config.stock_code}_K线图.png")
        plt.tight_layout()
        plt.savefig(file_path, dpi=300)
        plt.close()
    
    def _plot_volume(self):
        """绘制成交量图"""
        plt.figure(figsize=(12, 4))
        
        # 绘制上涨和下跌的成交量
        up = self.data[self.data['收盘价'] >= self.data['开盘价']]
        down = self.data[self.data['收盘价'] < self.data['开盘价']]
        
        # 绘制上涨成交量（绿色）
        plt.bar(up['日期'], up['成交量'], color='#00B27A', width=0.6, label='上涨成交量')
        
        # 绘制下跌成交量（红色）
        plt.bar(down['日期'], down['成交量'], color='#E60012', width=0.6, label='下跌成交量')
        
        plt.title(f"{self.config.stock_code}成交量图")
        plt.xlabel('日期')
        plt.ylabel('成交量')
        plt.xticks(rotation=45, ha='right')
        plt.legend()
        
        # 移除左、右、上三边的边框
        plt.gca().spines['left'].set_visible(False)
        plt.gca().spines['right'].set_visible(False)
        plt.gca().spines['top'].set_visible(False)
        
        # 添加网格横线
        plt.grid(axis='y', linestyle='-', zorder=0)
        
        # 保存图表
        file_path = os.path.join(self.vis_dir, f"{self.config.stock_code}_成交量图.png")
        plt.tight_layout()
        plt.savefig(file_path, dpi=300)
        plt.close()
    
    def _plot_price_volume_relationship(self):
        """绘制价格与成交量关系图"""
        plt.figure(figsize=(12, 6))
        
        # 创建双Y轴
        ax1 = plt.gca()
        ax2 = ax1.twinx()
        
        # 绘制价格（左Y轴）
        ax1.plot(self.data['日期'], self.data['收盘价'], color='#00A1FF', linewidth=2, label='收盘价')
        ax1.set_ylabel('价格(元)', color='#00A1FF')
        ax1.tick_params(axis='y', labelcolor='#00A1FF')
        
        # 绘制成交量（右Y轴）
        ax2.bar(self.data['日期'], self.data['成交量'], color='gray', alpha=0.3, label='成交量')
        ax2.set_ylabel('成交量', color='gray')
        ax2.tick_params(axis='y', labelcolor='gray')
        
        plt.title(f"{self.config.stock_code}价格与成交量关系")
        plt.xlabel('日期')
        plt.xticks(rotation=45, ha='right')
        
        # 合并图例
        lines1, labels1 = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax2.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
        
        # 移除上边框
        ax1.spines['top'].set_visible(False)
        ax2.spines['top'].set_visible(False)
        
        # 添加网格横线
        ax1.grid(axis='y', linestyle='-', zorder=0)
        
        # 保存图表
        file_path = os.path.join(self.vis_dir, f"{self.config.stock_code}_价格与成交量关系图.png")
        plt.tight_layout()
        plt.savefig(file_path, dpi=300)
        plt.close()
    
    def _plot_monthly_close_price(self):
        """绘制月度收盘价统计"""
        # 提取月份信息
        self.data['月份'] = self.data['日期'].dt.to_period('M')
        
        # 按月份分组计算收盘价均值
        monthly_avg = self.data.groupby('月份')['收盘价'].mean().reset_index()
        monthly_avg['月份'] = monthly_avg['月份'].astype(str)
        
        plt.figure(figsize=(12, 6))
        sns.barplot(x='月份', y='收盘价', data=monthly_avg, palette='Blues_d', zorder=3)
        plt.title(f"{self.config.stock_code}月度收盘价均值")
        plt.xlabel('月份')
        plt.ylabel('平均收盘价(元)')
        plt.xticks(rotation=45, ha='right')
        
        # 移除左、右、上三边的边框
        plt.gca().spines['left'].set_visible(False)
        plt.gca().spines['right'].set_visible(False)
        plt.gca().spines['top'].set_visible(False)
        
        # 添加网格横线
        plt.grid(axis='y', linestyle='-', zorder=0)
        
        # 在柱状图上添加数值标签
        for i, row in monthly_avg.iterrows():
            plt.text(i, row['收盘价'] + 5, f'{row["收盘价"]:.2f}', ha='center', fontsize=9)
        
        # 保存图表
        file_path = os.path.join(self.vis_dir, f"{self.config.stock_code}_月度收盘价统计图.png")
        plt.tight_layout()
        plt.savefig(file_path, dpi=300)
        plt.close()
    
    def _plot_price_change_distribution(self):
        """绘制涨跌幅分布"""
        # 计算每日涨跌幅
        self.data['涨跌幅(%)'] = self.data['收盘价'].pct_change() * 100
        # 移除NaN值
        price_changes = self.data['涨跌幅(%)'].dropna()
        
        plt.figure(figsize=(10, 6))
        sns.histplot(price_changes, kde=True, bins=30, color='#00A1FF', zorder=3)
        plt.title(f"{self.config.stock_code}涨跌幅分布")
        plt.xlabel('涨跌幅(%)')
        plt.ylabel('频数')
        
        # 移除左、右、上三边的边框
        plt.gca().spines['left'].set_visible(False)
        plt.gca().spines['right'].set_visible(False)
        plt.gca().spines['top'].set_visible(False)
        
        # 添加网格横线
        plt.grid(axis='y', linestyle='-', zorder=0)
        
        # 添加统计信息
        plt.axvline(price_changes.mean(), color='r', linestyle='dashed', linewidth=1, label=f'均值: {price_changes.mean():.2f}%')
        plt.axvline(0, color='k', linestyle='dashed', linewidth=1)
        
        plt.legend()
        
        # 保存图表
        file_path = os.path.join(self.vis_dir, f"{self.config.stock_code}_涨跌幅分布图.png")
        plt.tight_layout()
        plt.savefig(file_path, dpi=300)
        plt.close()    