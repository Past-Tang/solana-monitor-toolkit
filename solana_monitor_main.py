# 导入操作系统模块，用于文件路径处理等系统操作
import os  # 操作系统相关的功能，如文件路径处理
# 导入线程模块，用于实现多线程并发
import threading  # 线程管理模块
# 导入队列模块，用于线程间安全的数据传递
import queue  # 线程安全的队列实现
# 导入时间模块，用于时间计算和延时操作
import time  # 时间相关的功能，如延时和睡眠
# 导入线程池模块，用于高效管理多个并发任务
from concurrent.futures import ThreadPoolExecutor, as_completed  # 线程池管理
# 从钱包监控模块导入数据获取函数
from run.solana_transaction_monitor import fetch_data  # 导入钱包数据获取函数
# 从Telegram机器人模块导入BOT类
from utils.solana_telegram_bot import BOT  # 导入Telegram机器人实例化方法
# 导入日期时间模块，用于时间计算和格式化
from datetime import datetime, timedelta, timezone
# 导入价格格式化工具
from utils import solana_price_formatter as format_price
# 初始化Telegram机器人实例，用于发送通知
Tgbot = BOT()


# 定义项目根目录路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def get_wallets():
    """从Smart_wallets.txt文件中读取钱包地址"""
    # 使用with语句确保文件正确打开和关闭
    with open(os.path.join(BASE_DIR, 'data', 'smart_wallets.txt'), 'r') as file:
        # 读取所有行，去除每行首尾空白字符后存储为列表并返回
        wallets = [line.strip() for line in file.readlines()]
    return wallets


# 定义函数：负责获取指定钱包的数据并放入队列
def fetch_wallet_data(wallet, data_queue):
    try:
        # 调用fetch_data函数获取钱包数据
        data = fetch_data(wallet)
        # 将获取的数据放入队列
        data_queue.put(data)
    except Exception as e:
        print(f"Error fetching data for wallet {wallet}: {e}")


# 定义函数：负责从队列中取出数据并发送至Telegram
def send_messages(data_queue, sent_messages):
    while True:
        if not data_queue.empty():
            data = data_queue.get()
            data_str = str(data)  # 将数据转换为字符串形式以便于哈希和存储
            #直接控制信息
            dt_object = datetime.fromtimestamp(data['timestamp'], tz=timezone.utc)
            current_time = datetime.now(timezone.utc)
            one_hour_ago = current_time - timedelta(hours=0.2)
            if dt_object > one_hour_ago:
                if data_str not in sent_messages:
                    if data['smart_len'] > 3 and data['smart_len']:  # 聪明钱这么少别凑热闹

                        Tgbot.send_message(Buyprice=round(data["buy_amount"], 3),BuyallU=format_price.format_price(data["token_price"]),tokenname=data["token_symbol"],tokencode=data["token_address"],mytime=time.strftime('%Y年%m月%d日 %H时%M分%S秒',time.localtime(data["timestamp"])),zhuwnag=data["chain"],hour=data["hour_buy"],opentime='Null',num=data["smart_len"],)

                sent_messages.add(data_str)
                time.sleep(3.5)
            else:
                print("监听......")
        else:
            # 队列为空时，等待一段时间再检查
            time.sleep(5)


# 主函数
def main():
    # 获取钱包列表
    wallets = get_wallets()
    # 初始化数据队列
    data_queue = queue.Queue()
    # 初始化已发送消息集合
    sent_messages = set()

    # 启动一个后台线程用于发送消息
    threading.Thread(target=send_messages, args=(data_queue, sent_messages), daemon=True).start()

    # 使用线程池管理数据采集线程，最大并发数为20
    with ThreadPoolExecutor(max_workers=20) as executor:
        while True:
            futures = []

            # 为每个钱包启动一个线程来抓取数据
            for wallet in wallets:
                futures.append(executor.submit(fetch_wallet_data, wallet, data_queue))

            # 等待所有线程执行完成
            for future in as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    print(f"Error: {e}")

            # 在一轮监控后等待一段时间再开始下一轮
            time.sleep(5)


# 程序入口点
if __name__ == "__main__":
    main()
