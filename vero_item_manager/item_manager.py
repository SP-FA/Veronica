import os
import pickle

from vero_item_manager import ItemOperationError
from vero_item_manager.item_base import ItemBase
from vero_item_manager.item_manager_enum import ItemState
from vero_visualizer.text_visualizer import TextVisualizer


class ItemManager:
    """实现物品管理的各种增删改查操作

    Attributes:
        DATA_PATH (str): 数据保存路径
        SINGLE_INSTANCE (ItemManager): 对象单例

        _itemList (List[ItemBase]): 存放 Item 的列表
    """
    __createKey = object()

    DATA_PATH = os.path.dirname(__file__) + "/item_data/data.pkl"
    SINGLE_INSTANCE = None

    def __init__(self, key):
        """私有构造方法，不可在外部调用
        """
        assert (key == ItemManager.__createKey), "ItemManager objects must be created using ItemManager.get_manager"
        self.load_data()

    @staticmethod
    def get_manager():
        if ItemManager.SINGLE_INSTANCE is None:
            ItemManager.SINGLE_INSTANCE = ItemManager(ItemManager.__createKey)
        return ItemManager.SINGLE_INSTANCE

    def add_item(self, itemName, itemFeat, savePlace, itemNum=1, itemDesc="", imgPath=""):
        self._itemList.append(ItemBase(itemName, itemNum, itemFeat, itemDesc, savePlace, imgPath))
        self.save_data()

    def del_item(self, delItem=None, idx=None):
        if delItem is not None:
            self._itemList.remove(delItem)
        elif idx is not None:
            del self._itemList[idx]
        self.save_data()

    # def change_item(self):
    #     ...

    def search_item(self, searchStr):
        itemSimDict = {}
        for item in self._itemList:
            sim = item.matches_search_criteria(searchStr)
            if sim == -1: continue
            itemSimDict[item] = sim

        sortedItemSimDict = dict(sorted(itemSimDict.items(), key=lambda x: x[1], reverse=True))
        return list(sortedItemSimDict.keys())

    def show_item(self, idx=None):
        """展示 item 信息

        Args:
            idx: 如果为 None，则返回所有 item 的简略信息，如果不为 None，则返回某个 item 的详细信息
        """
        if idx is not None:
            if idx >= len(self._itemList): return [""]
            return [str(self._itemList[idx])]
        return [item.get_brief_info() for item in self._itemList]

    def check_in_item(self, item=None, idx=None):
        if item is not None:
            self._itemList[self._itemList.index(item)].check_in()
        elif idx is not None:
            self._itemList[idx].check_in()
        self.save_data()

    def check_out_item(self, item=None, idx=None):
        if item is not None:
            self._itemList[self._itemList.index(item)].check_out()
        elif idx is not None:
            self._itemList[idx].check_out()
        self.save_data()

    def check_item_state(self, item=None, idx=None):
        if item is not None:
            return self._itemList[self._itemList.index(item)].state
        if idx is not None:
            return self._itemList[idx].state

    def save_data(self):
        with open(ItemManager.DATA_PATH, "wb") as f:
            dumped = pickle.dumps(self._itemList)
            f.write(dumped)

    def load_data(self):
        try:
            with open(ItemManager.DATA_PATH, "rb") as f:
                dumped = f.read()
                self._itemList = pickle.loads(dumped)
        except FileNotFoundError:
            self._itemList = []


class ItemManageSystem:
    """item manager 的系统 UI 和交互
    TODO: 目前只能实现控制台交互，后续添加其他交互方式，可以进行选择

    Attributes:
        _manager: item manager 单例
        _visual: 可视化对象
    """
    def __init__(self):
        self._manager = ItemManager.get_manager()
        self._visual = TextVisualizer(maxLineLength=80, beforeLine="| ", afterLine=" |")

    def show_main_UI(self):
        return (
            f"{self._visual.headLine}"
            f"{self._visual('Item Manager')}"
            f"{self._visual.splitLine}"
            f"{self._visual('Choose Option:')}"
            f"{self._visual('[1] Show all items')}"
            f"{self._visual('[2] Search item')}"
            f"{self._visual('[3] Add item')}"
            f"{self._visual('[4] Delete item')}"
            f"{self._visual('[5] Change item information')}"
            f"{self._visual.headLine}"
        )

    def show_items(self):
        """展示所有 item 的简略信息
        TODO: 开发自动打印 table 的模块，用 table 打印这些信息
        """
        briefInfo = self._manager.show_item()
        listedInfo = [f"{self._visual(f'[{k}] {info}')}" for k, info in enumerate(briefInfo)]
        listedInfo = "".join(listedInfo)
        return (
            f"{self._visual.headLine}"
            f"{listedInfo}"
            f"{self._visual.blankLine}"
            f"{self._visual('You can check specific item detail by inputting item id.')}"
            f"{self._visual('Exit [q]')}"
            f"{self._visual.headLine}"
        )

    def show_item_detail(self, idx):
        """展示某个 item 的详细信息"""
        return self._manager.show_item(idx)[0]

    def add_item_UI(self):
        itemName = input("Please input the item name: ")
        itemNum = input("Please input the count of the item: ")
        itemFeat = input("Please input the item feature: ")
        itemDesc = input("Please describe the item in detail: ")
        savePlace = input("Please input the save place: ")
        self._manager.add_item(itemName, itemFeat, savePlace, itemNum, itemDesc)

    def del_item_UI(self, searchStr=None):
        """展示所有 item 的简略信息，并选择哪个 item 要删除
        TODO: 开发自动打印 table 的模块，用 table 打印这些信息

        Args:
            searchStr (str): 如果不为 None 则按照提供的字符串搜索
        """
        if searchStr is None:
            briefInfo = self._manager.show_item()
            listedInfo = [f"{self._visual(f'[{k}] {info}')}" for k, info in enumerate(briefInfo)]
        else:
            itemList = self._manager.search_item(searchStr)
            listedInfo = [f"{self._visual(f'[{k}] {item.get_brief_info()}')}" for k, item in enumerate(itemList)]
        listedInfo = "".join(listedInfo)
        print(
            f"{self._visual.headLine}"
            f"{listedInfo}"
            f"{self._visual.blankLine}"
            f"{self._visual('You can delete an item by inputting item id.')}"
            f"{self._visual('Exit [q]')}"
            f"{self._visual.headLine}"
        )
        while True:
            opt = input("Input: ")
            if opt == "q": return
            try:
                opt = int(opt)
                if searchStr is None:
                    print(self._manager.show_item(idx=opt)[0])
                else:
                    print(itemList[opt])
                print(
                    f"{self._visual.headLine}"
                    f"{self._visual('Confirm the deletion')}"
                    f"{self._visual.splitLine}"
                    f"{self._visual('Confirm [e]')}"
                    f"{self._visual('Cancel [q]')}"
                    f"{self._visual.headLine}"
                )
                confirm = input("Input: ")
                if confirm == "q": return
                elif confirm == "e":
                    if searchStr is None:
                        self._manager.del_item(idx=opt)
                    else:
                        self._manager.del_item(delItem=itemList[opt])
                    return
                else:
                    raise ValueError
            except (ValueError, IndexError):
                print("Invalid option!")

    # def change_item_UI(self):
    #     ...

    def check_out_UI(self, searchStr):
        if searchStr is None:
            briefInfo = self._manager.show_item()
            listedInfo = [f"{self._visual(f'[{k}] {info}')}" for k, info in enumerate(briefInfo)]
        else:
            itemList = self._manager.search_item(searchStr)
            listedInfo = [f"{self._visual(f'[{k}] {item.get_brief_info()}')}" for k, item in enumerate(itemList)]
        listedInfo = "".join(listedInfo)
        print(
            f"{self._visual.headLine}"
            f"{listedInfo}"
            f"{self._visual.blankLine}"
            f"{self._visual('You can check out an item by inputting item id.')}"
            f"{self._visual('Exit [q]')}"
            f"{self._visual.headLine}"
        )
        while True:
            opt = input("Input: ")
            if opt == "q": return
            try:
                opt = int(opt)
                if searchStr is None and self._manager.check_item_state(idx=opt) is ItemState.STORE:
                    print(self._manager.show_item(idx=opt)[0])
                elif searchStr is not None and self._manager.check_item_state(item=itemList[opt]) is ItemState.STORE:
                    print(itemList[opt])
                else:
                    raise ItemOperationError("")
                print(
                    f"{self._visual.headLine}"
                    f"{self._visual('Confirm to check out')}"
                    f"{self._visual.splitLine}"
                    f"{self._visual('Confirm [e]')}"
                    f"{self._visual('Cancel [q]')}"
                    f"{self._visual.headLine}"
                )
                confirm = input("Input: ")
                if confirm == "q":
                    return
                elif confirm == "e":
                    if searchStr is None:
                        self._manager.check_out_item(idx=opt)
                    else:
                        self._manager.check_out_item(item=itemList[opt])
                    return
                else:
                    raise ValueError
            except (ValueError, IndexError):
                print("Invalid option!")
            except ItemOperationError:
                print("This item is already checked out")

    def check_in_UI(self, searchStr=None):
        if searchStr is None:
            briefInfo = self._manager.show_item()
            listedInfo = [f"{self._visual(f'[{k}] {info}')}" for k, info in enumerate(briefInfo)]
        else:
            itemList = self._manager.search_item(searchStr)
            listedInfo = [f"{self._visual(f'[{k}] {item.get_brief_info()}')}" for k, item in enumerate(itemList)]
        listedInfo = "".join(listedInfo)
        print(
            f"{self._visual.headLine}"
            f"{listedInfo}"
            f"{self._visual.blankLine}"
            f"{self._visual('You can check in an item by inputting item id.')}"
            f"{self._visual('Exit [q]')}"
            f"{self._visual.headLine}"
        )
        while True:
            opt = input("Input: ")
            if opt == "q": return
            try:
                opt = int(opt)
                if searchStr is None and self._manager.check_item_state(idx=opt) is ItemState.NOT_STORE:
                    print(self._manager.show_item(idx=opt)[0])
                elif searchStr is not None and self._manager.check_item_state(item=itemList[opt]) is ItemState.NOT_STORE:
                    print(itemList[opt])
                else:
                    raise ItemOperationError("")
                print(
                    f"{self._visual.headLine}"
                    f"{self._visual('Confirm to check in')}"
                    f"{self._visual.splitLine}"
                    f"{self._visual('Confirm [e]')}"
                    f"{self._visual('Cancel [q]')}"
                    f"{self._visual.headLine}"
                )
                confirm = input("Input: ")
                if confirm == "q":
                    return
                elif confirm == "e":
                    if searchStr is None:
                        self._manager.check_in_item(idx=opt)
                    else:
                        self._manager.check_in_item(item=itemList[opt])
                    return
                else:
                    raise ValueError
            except (ValueError, IndexError):
                print("Invalid option!")
            except ItemOperationError:
                print("This item is already checked in")


if __name__ == "__main__":
    # test del item
    # system = ItemManageSystem()
    # system.del_item_UI("item")
    # print(system.show_items())

    # test add item
    # system = ItemManageSystem()
    # print(system.show_items())
    # system.add_item_UI()
    # print(system.show_items())

    # test check out / in item
    system = ItemManageSystem()
    print(system.show_items())
    system.check_in_UI("item 2")
    print(system.show_items())
