import unittest

from vero_item_manager.item_base import ItemBase
from vero_item_manager.item_manager import ItemManager, ItemManageSystem


class MyTestCase(unittest.TestCase):
    def test_item(self):
        itemName = "test item"
        itemNum = 2
        itemFeat = "Big, Stupid"
        itemDesc = "The test item is big and stupid"
        savePlace = "In my imagination"
        imgPath = "."
        item = ItemBase(itemName, itemNum, itemFeat, itemDesc, savePlace, imgPath)
        print(item)

    def test_item_add(self):
        itemName = "test item"
        itemNum = 2
        itemFeat = "Big, Stupid"
        itemDesc = "The test item is big and stupid"
        savePlace = "In my imagination"
        imgPath = "."
        itemManager = ItemManager.get_manager()
        itemManager.add_item(itemName, itemFeat, savePlace, itemNum, itemDesc, imgPath)
        itemManager.show_item()

    def test_item_save(self):
        itemName = "test item"
        itemNum = 2
        itemFeat = "Big, Stupid"
        itemDesc = "The test item is big and stupid"
        savePlace = "In my imagination"
        imgPath = "."
        itemManager = ItemManager.get_manager()
        itemManager.add_item(itemName, itemFeat, savePlace, itemNum, itemDesc, imgPath)
        itemManager.save_data()
        itemManager.load_data()
        itemManager.show_item()

    def test_item_search(self):
        itemManager = ItemManager.get_manager()
        itemName = "test item1"
        itemNum = 2
        itemFeat = "Big, Stupid"
        itemDesc = "The test item is big and stupid"
        savePlace = "In my imagination"
        imgPath = "."
        itemManager.add_item(itemName, itemFeat, savePlace, itemNum, itemDesc, imgPath)

        itemName = "test item2"
        itemNum = 1
        itemFeat = "Little, Stupid"
        itemDesc = "The test item is little and stupid"
        savePlace = "In my imagination"
        imgPath = "."
        itemManager.add_item(itemName, itemFeat, savePlace, itemNum, itemDesc, imgPath)

        itemName = "a piece of shit"
        itemNum = 1
        itemFeat = "yue"
        itemDesc = "This item is just a piece of shit"
        savePlace = "In my toilet"
        imgPath = "."
        itemManager.add_item(itemName, itemFeat, savePlace, itemNum, itemDesc, imgPath)

        print(itemManager.show_item())
        lst = itemManager.search_item("a big shit")
        for i in lst:
            print(i)

    def test_item_manage_system(self):
        system = ItemManageSystem()
        print(system.show_main_UI())
        print(system.show_items())
        print(system.show_item_detail(2))
        system.add_item_UI()
        system.show_items()


if __name__ == '__main__':
    unittest.main()
