import json
from datetime import datetime

# 模拟序列号数据库
SERIAL_DATABASE = {
    "SN123456789": {
        "name": "iPhone 15 Pro",
        "model": "A3102",
        "manufacture_date": "2024-01-15",
        "warranty_status": "在保"
    },
    "SN987654321": {
        "name": "MacBook Pro",
        "model": "MNXQ3",
        "manufacture_date": "2023-11-20",
        "warranty_status": "已过保"
    }
}

def lookup_serial(serial_number: str) -> dict:
    """查询序列号信息"""
    return SERIAL_DATABASE.get(serial_number.upper())

def load_serial_database():
    """从文件加载序列号数据库"""
    try:
        with open('data/serials.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return SERIAL_DATABASE