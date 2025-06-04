import requests
import pandas as pd
import time
from fake_useragent import UserAgent
import os
from typing import Optional

class StockCrawler:
    def __init__(self, config):
        self.config = config
        self.ua = UserAgent()
        self.headers = {
            'User-Agent': self.ua.random,
            'Referer': 'https://quote.eastmoney.com/'
        }
        self.url = 'https://push2his.eastmoney.com/api/qt/stock/kline/get'
        
        # 创建输出目录
        if not os.path.exists(config.output_dir):
            os.makedirs(config.output_dir)
    
    def _get_market_prefix(self) -> str:
        """根据市场类型获取前缀"""
        return '1' if self.config.market == 'sh' else '0'
    
    def _get_kline_type_code(self) -> str:
        """根据K线类型获取代码"""
        kline_types = {'day': '101', 'week': '102', 'month': '103'}
        return kline_types.get(self.config.kline_type, '101')
    
    def fetch_stock_data(self) -> Optional[pd.DataFrame]:
        """获取股票数据"""
        # 构建请求参数
        params = {
            'secid': f"{self._get_market_prefix()}.{self.config.stock_code}",
            'ut': 'fa5fd1943c7b386f172d6893dbfba10b',
            'fields1': 'f1,f2,f3,f4,f5,f6',
            'fields2': 'f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61',
            'klt': self._get_kline_type_code(),
            'fqt': '0',
            'beg': self.config.start_date,
            'end': self.config.end_date,
            'lmt': '1000',
            'skip': '0'
        }
        
        try:
            print(f"开始请求{self.config.stock_code}的股票数据...")
            # 发送请求
            response = requests.get(self.url, params=params, headers=self.headers, timeout=10)
            response.raise_for_status()  # 检查请求是否成功
            
            # 解析JSON数据
            data = response.json()
            
            # 提取K线数据
            if 'data' in data and 'klines' in data['data']:
                klines = data['data']['klines']
                # 拆分K线数据
                stock_data = []
                for kline in klines:
                    items = kline.split(',')
                    stock_data.append({
                        '日期': items[0],
                        '开盘价': float(items[1]),
                        '收盘价': float(items[2]),
                        '最高价': float(items[3]),
                        '最低价': float(items[4]),
                        '成交量': float(items[5]),
                        '成交额': float(items[6]) if len(items) > 6 else 0
                    })
                
                # 转换为DataFrame
                df = pd.DataFrame(stock_data)
                
                # 保存为CSV文件
                file_path = os.path.join(self.config.output_dir, 
                                        f"{self.config.stock_code}_{self.config.kline_type}_data.csv")
                df.to_csv(file_path, index=False, encoding='utf-8-sig')
                print(f"数据爬取成功，已保存至{file_path}")
                
                return df
            else:
                print("数据获取失败，未找到K线数据！")
                print(data)
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"请求异常: {e}")
            return None
        except KeyError as ke:
            print(f"数据解析异常，缺少关键字段: {ke}")
            return None
        except Exception as e:
            print(f"发生错误: {e}")
            return None    