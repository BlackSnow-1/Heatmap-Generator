import argparse
from typing import List


class HTMLGenerator:

    # 接受一个 xlsx 文件路径生成
    def __init__(self, items: str):

        if not isinstance(items, str):
            raise TypeError("items must be a string")



        self.items = items

    def generate_html(self):



        return
    