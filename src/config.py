class Config:
    def __init__(self, stock_code, market, start_date, end_date, kline_type, output_dir):
        self.stock_code = stock_code
        self.market = market
        self.start_date = start_date
        self.end_date = end_date
        self.kline_type = kline_type
        self.output_dir = output_dir
    
    def __str__(self):
        return (f"配置信息:\n"
                f"  股票代码: {self.stock_code}\n"
                f"  市场: {self.market}\n"
                f"  开始日期: {self.start_date}\n"
                f"  结束日期: {self.end_date}\n"
                f"  K线类型: {self.kline_type}\n"
                f"  输出目录: {self.output_dir}")    