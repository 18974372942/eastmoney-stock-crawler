import pandas as pd
import numpy as np
from typing import Dict, Any

class StockAnalyzer:
    def __init__(self, config, data):
        self.config = config
        self.data = data.copy()  # 复制数据，避免修改原始数据
        self._preprocess_data()
    
    def _preprocess_data(self):
        """数据预处理"""
        # 将日期列转换为datetime类型
        self.data['日期'] = pd.to_datetime(self.data['日期'])
        
        # 按日期排序
        self.data = self.data.sort_values('日期')
        
        # 计算每日涨跌幅
        self.data['涨跌幅(%)'] = self.data['收盘价'].pct_change() * 100
        
        # 计算移动平均线
        self.data['MA5'] = self.data['收盘价'].rolling(window=5).mean()  # 5日均线
        self.data['MA10'] = self.data['收盘价'].rolling(window=10).mean()  # 10日均线
        self.data['MA20'] = self.data['收盘价'].rolling(window=20).mean()  # 20日均线
        
        # 计算波动率
        self.data['波动率(%)'] = self.data['收盘价'].rolling(window=20).std() * 100
        
        # 计算成交量变化率
        self.data['成交量变化率(%)'] = self.data['成交量'].pct_change() * 100
    
    def analyze(self) -> Dict[str, Any]:
        """执行数据分析"""
        results = {}
        
        # 1. 基本统计信息
        results['基本统计信息'] = self._get_basic_statistics()
        
        # 2. 趋势分析
        results['趋势分析'] = self._get_trend_analysis()
        
        # 3. 波动性分析
        results['波动性分析'] = self._get_volatility_analysis()
        
        # 4. 成交量分析
        results['成交量分析'] = self._get_volume_analysis()
        
        # 5. 价格区间分析
        results['价格区间分析'] = self._get_price_range_analysis()
        
        # 6. 技术指标分析
        results['技术指标分析'] = self._get_technical_indicator_analysis()
        
        return results
    
    def _get_basic_statistics(self) -> Dict[str, Any]:
        """获取基本统计信息"""
        close_prices = self.data['收盘价']
        return {
            '分析周期': f"{self.data['日期'].min().strftime('%Y-%m-%d')} 至 {self.data['日期'].max().strftime('%Y-%m-%d')}",
            '样本数量': len(self.data),
            '平均收盘价': close_prices.mean(),
            '最高收盘价': close_prices.max(),
            '最低收盘价': close_prices.min(),
            '收盘价标准差': close_prices.std(),
            '最大单日涨幅': self.data['涨跌幅(%)'].max(),
            '最大单日跌幅': self.data['涨跌幅(%)'].min(),
            '平均涨跌幅': self.data['涨跌幅(%)'].mean()
        }
    
    def _get_trend_analysis(self) -> Dict[str, Any]:
        """获取趋势分析结果"""
        latest_price = self.data['收盘价'].iloc[-1]
        ma5 = self.data['MA5'].iloc[-1]
        ma10 = self.data['MA10'].iloc[-1]
        ma20 = self.data['MA20'].iloc[-1]
        
        # 判断短期趋势
        if latest_price > ma5:
            short_term_trend = "上升"
        elif latest_price < ma5:
            short_term_trend = "下降"
        else:
            short_term_trend = "横盘"
        
        # 判断中期趋势
        if ma5 > ma10 and ma10 > ma20:
            medium_term_trend = "上升"
        elif ma5 < ma10 and ma10 < ma20:
            medium_term_trend = "下降"
        else:
            medium_term_trend = "震荡"
        
        return {
            '短期趋势(5日)': short_term_trend,
            '中期趋势(5-10-20日)': medium_term_trend,
            '当前价格与均线': {
                '收盘价': latest_price,
                '5日均线': ma5,
                '10日均线': ma10,
                '20日均线': ma20
            }
        }
    
    def _get_volatility_analysis(self) -> Dict[str, Any]:
        """获取波动性分析结果"""
        latest_volatility = self.data['波动率(%)'].iloc[-1]
        high_volatility_days = len(self.data[self.data['波动率(%)'] > 3])  # 波动率大于3%视为高波动
        low_volatility_days = len(self.data[self.data['波动率(%)'] < 1])  # 波动率小于1%视为低波动
        
        return {
            '当前波动率(20日标准差)': f"{latest_volatility:.2f}%",
            '高波动天数占比': f"{high_volatility_days/len(self.data)*100:.2f}%",
            '低波动天数占比': f"{low_volatility_days/len(self.data)*100:.2f}%",
            '波动率最高值': f"{self.data['波动率(%)'].max():.2f}%",
            '波动率最低值': f"{self.data['波动率(%)'].min():.2f}%"
        }
    
    def _get_volume_analysis(self) -> Dict[str, Any]:
        """获取成交量分析结果"""
        avg_volume = self.data['成交量'].mean()
        high_volume_days = self.data[self.data['成交量'] > avg_volume * 1.5]  # 成交量大于平均1.5倍视为高量
        low_volume_days = self.data[self.data['成交量'] < avg_volume * 0.5]  # 成交量小于平均0.5倍视为低量
        
        return {
            '平均成交量': avg_volume,
            '高成交量天数占比': f"{len(high_volume_days)/len(self.data)*100:.2f}%",
            '低成交量天数占比': f"{len(low_volume_days)/len(self.data)*100:.2f}%",
            '量价关系': self._analyze_volume_price_relationship()
        }
    
    def _analyze_volume_price_relationship(self) -> str:
        """分析量价关系"""
        # 计算收盘价和成交量的相关系数
        corr = self.data['收盘价'].corr(self.data['成交量'])
        
        if corr > 0.7:
            return f"强正相关(相关系数: {corr:.2f})，量价配合良好，趋势可持续性较强"
        elif corr > 0.3:
            return f"弱正相关(相关系数: {corr:.2f})，量价有一定配合，但趋势强度一般"
        elif corr > -0.3:
            return f"弱负相关(相关系数: {corr:.2f})，量价关系不明显，趋势可能较弱"
        else:
            return f"强负相关(相关系数: {corr:.2f})，量价背离，趋势可能即将反转"
    
    def _get_price_range_analysis(self) -> Dict[str, Any]:
        """获取价格区间分析结果"""
        latest_price = self.data['收盘价'].iloc[-1]
        max_price = self.data['最高价'].max()
        min_price = self.data['最低价'].min()
        
        # 计算价格区间
        price_range = max_price - min_price
        upper_range = max_price - latest_price
        lower_range = latest_price - min_price
        
        return {
            '价格区间': f"{min_price:.2f} - {max_price:.2f}",
            '当前价格位置': f"{lower_range/price_range*100:.2f}% (距离最高价: {upper_range:.2f}, 距离最低价: {lower_range:.2f})",
            '近期支撑位': self._calculate_support_level(),
            '近期阻力位': self._calculate_resistance_level()
        }
    
    def _calculate_support_level(self) -> float:
        """计算支撑位"""
        # 简单支撑位计算：取最近20天内的最低价附近的密集成交区
        recent_data = self.data.iloc[-20:]
        min_price = recent_data['最低价'].min()
        
        # 计算价格分布
        price_bins = pd.cut(recent_data['最低价'], bins=10)
        bin_counts = price_bins.value_counts()
        
        # 找到最低价所在区间
        min_bin = None
        for bin_range in bin_counts.index:
            if min_price >= bin_range.left and min_price <= bin_range.right:
                min_bin = bin_range
                break
        
        # 如果找到最低价所在区间且该区间成交量较大，则取该区间的中值作为支撑位
        if min_bin and bin_counts[min_bin] > bin_counts.mean():
            return (min_bin.left + min_bin.right) / 2
        
        return min_price
    
    def _calculate_resistance_level(self) -> float:
        """计算阻力位"""
        # 简单阻力位计算：取最近20天内的最高价附近的密集成交区
        recent_data = self.data.iloc[-20:]
        max_price = recent_data['最高价'].max()
        
        # 计算价格分布
        price_bins = pd.cut(recent_data['最高价'], bins=10)
        bin_counts = price_bins.value_counts()
        
        # 找到最高价所在区间
        max_bin = None
        for bin_range in bin_counts.index:
            if max_price >= bin_range.left and max_price <= bin_range.right:
                max_bin = bin_range
                break
        
        # 如果找到最高价所在区间且该区间成交量较大，则取该区间的中值作为阻力位
        if max_bin and bin_counts[max_bin] > bin_counts.mean():
            return (max_bin.left + max_bin.right) / 2
        
        return max_price
    
    def _get_technical_indicator_analysis(self) -> Dict[str, Any]:
        """获取技术指标分析结果"""
        # 计算RSI指标 (相对强弱指标)
        delta = self.data['收盘价'].diff()
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)
        avg_gain = gain.rolling(window=14).mean()
        avg_loss = loss.rolling(window=14).mean()
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        self.data['RSI'] = rsi
        
        # 计算MACD指标
        exp1 = self.data['收盘价'].ewm(span=12, adjust=False).mean()
        exp2 = self.data['收盘价'].ewm(span=26, adjust=False).mean()
        macd = exp1 - exp2
        signal = macd.ewm(span=9, adjust=False).mean()
        histogram = macd - signal
        self.data['MACD'] = macd
        self.data['Signal'] = signal
        self.data['Histogram'] = histogram
        
        # 获取最新指标值
        latest_rsi = self.data['RSI'].iloc[-1]
        latest_macd = self.data['MACD'].iloc[-1]
        latest_signal = self.data['Signal'].iloc[-1]
        latest_histogram = self.data['Histogram'].iloc[-1]
        
        # 分析指标信号
        rsi_signal = self._analyze_rsi_signal(latest_rsi)
        macd_signal = self._analyze_macd_signal(latest_macd, latest_signal, latest_histogram)
        
        return {
            'RSI(14)': {
                '当前值': f"{latest_rsi:.2f}",
                '信号': rsi_signal
            },
            'MACD(12,26,9)': {
                'MACD值': f"{latest_macd:.2f}",
                '信号线值': f"{latest_signal:.2f}",
                '柱状图值': f"{latest_histogram:.2f}",
                '信号': macd_signal
            }
        }
    
    def _analyze_rsi_signal(self, rsi: float) -> str:
        """分析RSI指标信号"""
        if rsi > 70:
            return "超买，可能面临回调压力"
        elif rsi < 30:
            return "超卖，可能存在反弹机会"
        elif rsi > 50:
            return "强势区域，上升趋势可能延续"
        else:
            return "弱势区域，下降趋势可能延续"
    
    def _analyze_macd_signal(self, macd: float, signal: float, histogram: float) -> str:
        """分析MACD指标信号"""
        if macd > signal and histogram > 0:
            return "MACD线在信号线上方且柱状图为正，多头信号"
        elif macd < signal and histogram < 0:
            return "MACD线在信号线下方且柱状图为负，空头信号"
        elif macd > signal and histogram < 0:
            return "MACD线在信号线上方但柱状图为负，多头力量减弱"
        else:
            return "MACD线在信号线下方但柱状图为正，空头力量减弱"    