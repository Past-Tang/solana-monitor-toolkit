# 导入requests库用于HTTP请求
import requests
# 导入datetime模块用于时间处理
import datetime

def log_print(text):
    """带时间戳的日志打印函数"""
    # 获取当前时间并格式化
    nowtime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # 打印带时间戳的日志信息
    print(f"[{nowtime}]: {text}")

def fetch_data(url, headers):
    """
    从指定URL获取数据
    :param url: 请求的URL
    :param headers: 请求头信息
    :return: 返回解析后的数据
    """
    try:
        # 发送GET请求
        response = requests.get(url, headers=headers)
        # 检查HTTP错误
        response.raise_for_status()
        # 解析并返回数据
        return response.json()['data']["rank"]
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"Request error occurred: {req_err}")
    except KeyError as key_err:
        print(f"Key error: {key_err}")
    return []

def get_recent_active_wallets(data):
    """
    获取最近活跃的钱包地址
    :param data: 原始数据
    :return: 最近24小时内活跃的钱包地址列表
    """
    try:
        # 筛选最近24小时内活跃的钱包地址
        recent_active_wallets = [
            item['wallet_address']
            for item in data
            if item['last_active'] >= datetime.datetime.now().timestamp() - (1 * 24 * 60 * 60)
        ]
        return recent_active_wallets
    except KeyError as key_err:
        print(f"Key error in processing data: {key_err}")
    return []

def smart_updata():
    """更新聪明钱包地址列表"""
    # 设置请求头
    headers = {'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +)'}
    
    # 获取第一组聪明钱包数据
    url1 = 'https://gmgn.ai/defi/quotation/v1/rank/sol/wallets/7d?tag=smart_degen&orderby=pnl_7d&direction=desc'
    data1 = fetch_data(url1, headers)
    recent_active_wallets1 = get_recent_active_wallets(data1)
    
    # 获取第二组聪明钱包数据
    url2 = 'https://gmgn.ai/defi/quotation/v1/rank/sol/wallets/7d?tag=pump_smart&orderby=pnl_7d&direction=desc'
    data2 = fetch_data(url2, headers)
    recent_active_wallets2 = get_recent_active_wallets(data2)
    
    # 合并两组数据并去重
    combined_recent_active_wallets = list(set(recent_active_wallets1 + recent_active_wallets2))
    
    # 将结果写入文件
    with open('../data/smart_wallets.txt', 'w', encoding='utf-8') as file:
        for item in combined_recent_active_wallets:
            file.write(item + '\n')
    
    # 记录日志
    log_print(f"成功更新{len(combined_recent_active_wallets)}个聪明钱包地址。")

if __name__ == '__main__':
    # 主程序入口
    smart_updata()
