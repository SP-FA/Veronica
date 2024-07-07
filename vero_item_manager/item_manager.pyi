import os
from typing import List
from vero_item_manager.item_base import ItemBase


class ItemManager:
    __createKey = object()

    DATA_PATH = os.path.dirname(__file__) + "/item_data/data.pkl"
    SINGLE_INSTANCE = None

    def __init__(self, key: object):
        self._itemList: List[ItemBase] = []
    @staticmethod
    def get_manager() -> ItemManager: ...
    def add_item(self, itemName: str, itemFeat: str, savePlace: str, itemNum: int, itemDesc: str, imgPath: str): ...
    def del_item(self, delItem: ItemBase=None, idx: int=None): ...
    # def change_item(self): ...
    def search_item(self, searchStr: str): ...
    def show_item(self, idx: int=None) -> List[str]: ...
    def check_in_item(self, item: ItemBase=None, idx: int=None): ...
    def check_out_item(self, item: ItemBase=None, idx: int=None): ...
    def save_data(self): ...
    def load_data(self): ...


class ItemManageSystem:
    def __init__(self):
        self._manager = None
        self._visual = None

    def show_main_UI(self) -> str: ...
    def show_items(self) -> str: ...
    def show_item_detail(self, idx: int) -> str: ...
    def add_item_UI(self): ...
    def del_item_UI(self, searchStr: str=None): ...
    # def change_item_UI(self): ...
    def check_out_UI(self, searchStr: str=None): ...
    def check_in_UI(self, searchStr: str=None): ...
