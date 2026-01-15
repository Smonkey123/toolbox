import json

# 模拟缩写数据库
ACRONYM_DATABASE = {
    "API": [
        {"acronym": "API", "meaning": "Application Programming Interface", "field": "软件开发"},
        {"acronym": "API", "meaning": "Active Pharmaceutical Ingredient", "field": "医药"}
    ],
    "HTTP": [
        {"acronym": "HTTP", "meaning": "HyperText Transfer Protocol", "field": "网络通信"}
    ],
    "AI": [
        {"acronym": "AI", "meaning": "Artificial Intelligence", "field": "人工智能"},
        {"acronym": "AI", "meaning": "Adobe Illustrator", "field": "设计软件"}
    ]
}


def lookup_acronym(term: str) -> list:
    """查询缩写或术语"""
    term = term.upper()
    results = []

    # 精确匹配
    if term in ACRONYM_DATABASE:
        results.extend(ACRONYM_DATABASE[term])

    # 模糊匹配
    for acronym, meanings in ACRONYM_DATABASE.items():
        if term in acronym or acronym in term:
            results.extend(meanings)

    return results


def load_acronym_database():
    """从文件加载缩写数据库"""
    try:
        with open('data/acronyms.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return ACRONYM_DATABASE