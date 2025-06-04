import argparse
from src.crawler import StockCrawler
from src.analyzer import StockAnalyzer
from src.visualizer import StockVisualizer
from src.config import Config

def main():
    # 创建命令行参数解析器
    parser = argparse.ArgumentParser(description='东方财富网股票数据爬取与分析工具')
    parser.add_argument('--stock_code', type=str, default='600519', help='股票代码，默认为贵州茅台(600519)')
    parser.add_argument('--market', type=str, default='sh', choices=['sh', 'sz'], help='股票市场，sh表示沪市，sz表示深市，默认为沪市')
    parser.add_argument('--start_date', type=str, default='20240101', help='开始日期，格式为YYYYMMDD，默认为20240101')
    parser.add_argument('--end_date', type=str, default='20250601', help='结束日期，格式为YYYYMMDD，默认为20250601')
    parser.add_argument('--kline_type', type=str, default='day', choices=['day', 'week', 'month'], help='K线类型，day表示日线，week表示周线，month表示月线，默认为日线')
    parser.add_argument('--output_dir', type=str, default='data', help='数据输出目录，默认为data')
    parser.add_argument('--analysis', action='store_true', help='是否进行数据分析，默认不进行')
    parser.add_argument('--visualization', action='store_true', help='是否进行数据可视化，默认不进行')
    
    # 解析命令行参数
    args = parser.parse_args()
    
    # 配置参数
    config = Config(
        stock_code=args.stock_code,
        market=args.market,
        start_date=args.start_date,
        end_date=args.end_date,
        kline_type=args.kline_type,
        output_dir=args.output_dir
    )
    
    try:
        # 1. 数据爬取
        crawler = StockCrawler(config)
        df = crawler.fetch_stock_data()
        
        if df is not None and not df.empty:
            print(f"成功获取{config.stock_code}的股票数据，共{len(df)}条记录")
            
            # 2. 数据分析（如果需要）
            if args.analysis:
                analyzer = StockAnalyzer(config, df)
                analysis_results = analyzer.analyze()
                print("数据分析完成")
                print(analysis_results)
                
                # 3. 数据可视化（如果需要）
                if args.visualization:
                    visualizer = StockVisualizer(config, df)
                    visualizer.visualize()
                    print("数据可视化完成")
            else:
                print("跳过数据分析步骤")
        else:
            print("未获取到有效股票数据，程序退出")
            
    except Exception as e:
        print(f"程序运行出错: {e}")

if __name__ == "__main__":
    main()    