import os
import time
from telebot import types
import telebot

class BOT:
    """
    Telegram 机器人类，用于发送Solana交易预警信息
    """
    def __init__(self):
        """
        初始化Telegram机器人
        """
        # 注意：实际使用时应将token存储在环境变量中
        BOT_TOKEN = '7219032526:AAEeK4IK03pEG59yBW42T5j_p6xo5N_5JI4'
        self.bot = telebot.TeleBot(BOT_TOKEN)

    def StrText(self, BuyallU, Buyprice, tokenname, tokencode, mytime, zhuwnag, hour, opentime, num):
        """
        生成预警消息文本
        :param BuyallU: 总购买金额
        :param Buyprice: 购买价格
        :param tokenname: 代币名称
        :param tokencode: 合约地址
        :param mytime: 时间描述
        :param zhuwnag: 主网名称
        :param hour: 小时交易量
        :param opentime: 开盘时间
        :param num: 聪明钱数量
        :return: 格式化后的消息文本
        """
        # 获取当前时间并格式化
        time_tuple = time.localtime(time.time())
        formatted_time = time.strftime('%m月%d日%H时%M分%S秒', time_tuple)
        
        # 构建消息模板
        message = f"""
        金狗🧈预警：{mytime}{num}个聪明钱正在买它！💹
        
        主网链名⛓️： {zhuwnag}
        代币名称🪙： {tokenname}
        购买价格💵： {Buyprice} USDT
        购买金额💳： {BuyallU} USDT
        小时交易💰️： {hour} USDT
        开盘时间🕞️︎： {opentime}
        
        合约地址（点击复制）: 
                `{tokencode}`
        
        恭喜发财！🧧🧧🧧
        当前系统时间⌛： {formatted_time}
        """
        return message

    def send_message(self, BuyallU, Buyprice, tokenname, tokencode, mytime, zhuwnag, hour, opentime, num):
        """
        发送预警消息到Telegram频道
        :param BuyallU: 总购买金额
        :param Buyprice: 购买价格
        :param tokenname: 代币名称
        :param tokencode: 合约地址
        :param mytime: 时间描述
        :param zhuwnag: 主网名称
        :param hour: 小时交易量
        :param opentime: 开盘时间
        :param num: 聪明钱数量
        """
        # 生成消息内容
        message = self.StrText(BuyallU, Buyprice, tokenname, tokencode, mytime, zhuwnag, hour, opentime, num)
        
        # 创建内联键盘
        markup = types.InlineKeyboardMarkup()
        kline_button = types.InlineKeyboardButton(
            text='立即查看K线', 
            url=f'https://gmgn.ai/eth/token/{tokencode}?embled=1'
        )
        markup.add(kline_button)
        
        # 发送消息到指定频道
        self.bot.send_message(
            chat_id='-1002243425005',
            text=message,
            reply_markup=markup,
            parse_mode="Markdown"
        )

if __name__ == '__main__':
    # 测试用代码
    bot = BOT()
    # bot.send_message()  # 取消注释以发送测试消息
