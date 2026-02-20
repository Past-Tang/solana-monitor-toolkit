"""
Solana钱包活动监控器 - 通过GMGN API实时获取并分析钱包交易数据
包含代币交易记录查询、智能交易识别、风险指标分析等功能
"""
# 导入requests库用于HTTP请求
import requests
# 从Utils包导入tokensmart模块
from Utils import tokensmart

def fetch_data(address):
    """获取指定钱包地址的交易数据"""
    # 设置请求头，模拟Googlebot访问
    headers = {'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'}
    
    # 发送GET请求获取钱包交易数据
    response = requests.get(
        f'https://gmgn.ai/defi/quotation/v1/wallet_activity/sol?type=buy&wallet={address}&limit=10&cost=10',
        headers=headers
    )
    
    # 初始化结果列表
    result = []
    
    # 遍历返回的交易活动数据
    for data in response.json()['data']['activities']:
        # 构建交易信息字典
        activity_info = {
            'chain': data['chain'],  # 区块链名称
            'token_symbol': data['token']['symbol'],  # 代币符号
            'token_address': data['token']['address'],  # 代币合约地址
            'timestamp': data['timestamp'],  # 交易时间戳
            'buy_amount': data['cost_usd'],  # 购买金额（美元）
            'token_price': data['token']['price'],  # 代币价格
            'smart_len': tokensmart.fetch_data(data['token']['address']),  # 获取聪明钱数据
            'hour_buy': "Null",  # 小时交易量（暂未实现）
        }
        # 将交易信息添加到结果列表
        result.append(activity_info)

    # 返回最新的交易信息
    return result[0]

if __name__ == '__main__':
    # 测试获取指定钱包地址的交易数据
    fetch_data('2vkYVxq7HqrB2dzUH4VQ28wGAzv5c6ySt5uqPss5rGTJ')
