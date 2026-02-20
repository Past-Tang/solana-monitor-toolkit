import re

def format_price(price):
    """
    格式化价格显示，特别处理极小数值
    :param price: 输入价格，可以是字符串或数字
    :return: 格式化后的价格字符串
    """
    # 如果price是字符串，转换为浮点数
    if isinstance(price, str):
        price = float(price)

    # 将数值转换为字符串，保留足够多的小数位
    price_str = f"{price:.20f}".rstrip('0')

    # 使用正则表达式找到小数点后第一个非零数字的位置
    match = re.search(r'0*([1-9])', price_str.split('.')[1])
    if match:
        index = match.start(1)
    
    # 处理极小数值（小于0.01）的特殊格式化
    if price < 0.01 and index > 2:
        # 使用科学计数法简化显示
        return f"0.0{{{index - 1}}}{price_str.split('.')[1][index]}"
    
    # 处理普通小数
    elif '.' in price_str:
        integer_part, fractional_part = price_str.split('.')
        
        # 处理末尾有多个0的情况
        if fractional_part and '0' in fractional_part:
            # 找到小数点后最后一个零的位置
            last_zero_index = len(fractional_part) - len(fractional_part.rstrip('0'))
            if last_zero_index > 1:
                # 使用简化表示法
                return f"{integer_part}.0{{{len(fractional_part) - last_zero_index - 1}}}{fractional_part[last_zero_index:]}"
        
        # 默认保留两位小数
        return f"{price:.2f}"
    
    # 处理整数情况
    else:
        # 默认保留两位小数
        return f"{price:.2f}"
