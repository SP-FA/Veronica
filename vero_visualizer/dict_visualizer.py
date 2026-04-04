from typing import Union


class DictVisualizer:
    """实现字典可视化，把字典看作一个 table，key 是 column name 每一行填一个 dict，支持 List[Dict]
    """
    def __init__(self):
        pass

    def __call__(self, dicts: Union[list[dict], dict]) -> str:
        if isinstance(dicts, dict):
            dicts = [dicts]
        
        # 获取所有的 keys 作为表头
        headers = set()
        for d in dicts:
            headers.update(d.keys())
        headers = sorted(headers)

        # 构建表格字符串
        table_str  = "--" + "---".join(["-" * len(header) for header in headers]) + "--\n"
        table_str += "| " + " | ".join(headers) + " |\n"
        table_str += "|-" + "-|-".join(["-" * len(header) for header in headers]) + "-|\n"
        
        for d in dicts:
            row = []
            for header in headers:
                row.append(str(d.get(header, "")))
            table_str += "| " + " | ".join(row) + " |\n"
        
        return table_str
