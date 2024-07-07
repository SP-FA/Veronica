import time

from vero_item_manager import ItemOperationError
from vero_item_manager.item_manager_enum import ItemState, ThresholdWeight
from vero_visualizer.text_visualizer import TextVisualizer


class ItemBase:
    """保存物品信息的基类

    Attributes:
        FIND_THRESHOLD (float): 查找到该 item 所需要达到的相似度阈值

        _itemName (str): 物品名称
        _itemNum  (str): 物品数量
        _itemFeat (str): 物品特征（简略描述）
        _itemDesc (str): 物品描述
        _savePlace (str): 物品存放位置
        _state (int): 物品状态
        _checkOutTime (Time): 取出日期
        _checkInTime (Time): 存放日期
        _imgPath (str): 物品图片存放路径
    """

    FIND_THRESHOLD = 0.6

    def __init__(self, itemName, itemNum, itemFeat, itemDesc, savePlace, imgPath):
        self._itemName = itemName
        self._itemNum  = itemNum
        self._itemFeat = itemFeat
        self._itemDesc = itemDesc
        self._savePlace = savePlace
        self._imgPath = imgPath

        self._state = ItemState.STORE
        self._checkInTime = time.asctime(time.localtime(time.time()))
        self._checkOutTime = None

        self._visual = TextVisualizer(maxLineLength=40, beforeLine="| ", afterLine=" |")

    @property
    def time(self):
        if self._state == ItemState.STORE:       return self._checkInTime
        elif self._state == ItemState.NOT_STORE: return self._checkOutTime

    @property
    def state(self):
        return self._state

    def check_out(self):
        if self._state == ItemState.STORE:
            self._state = ItemState.NOT_STORE
        else:
            raise ItemOperationError("Can not change state to NOT_STORE, because the item is not in the state STORE")

    def check_in(self):
        if self._state == ItemState.NOT_STORE:
            self._state = ItemState.STORE
        else:
            raise ItemOperationError("Can not change state to STORE, because the item is not in the state NOT_STORE")

    def matches_search_criteria(self, searchStr):
        """计算搜索内容和 item 的相似度

        Args:
            searchStr (str): 搜索内容

        Returns:
            float: 相似度，如果返回 -1 说明没有达到阈值，该 item 不是要搜索的物品
        """

        def longest_common_subsequence(str2):
            """计算最大公共子序列

            Args:
                str2 (str): item 字符串

            Returns:
                int: 最大公共子序列长度
            """
            len1 = len(searchStr)
            len2 = len(str2)

            if len1 * len2 == 0: return 0

            pre = 0
            cur = 1
            dp = [[0] * (len2 + 1) for _ in range(2)]

            for i in range(1, len1 + 1):
                for j in range(1, len2 + 1):
                    if searchStr[i - 1] == str2[j - 1]:
                        dp[cur][j] = dp[pre][j - 1] + 1
                    else:
                        dp[cur][j] = max([dp[pre][j], dp[cur][j - 1]])
                pre = 0 if pre else 1
                cur = 0 if cur else 1
            return dp[pre][len2]

        nameSim = longest_common_subsequence(self._itemName) / len(searchStr)
        featSim = longest_common_subsequence(self._itemFeat) / len(searchStr)
        descSim = longest_common_subsequence(self._itemDesc) / len(searchStr)

        if nameSim * ThresholdWeight.NAME.value > ItemBase.FIND_THRESHOLD: return nameSim
        if featSim * ThresholdWeight.FEAT.value > ItemBase.FIND_THRESHOLD: return featSim / ThresholdWeight.FEAT.value
        if descSim * ThresholdWeight.DESC.value > ItemBase.FIND_THRESHOLD: return descSim / ThresholdWeight.NAME.value
        return -1

    def get_brief_info(self):
        return (
            f"|{self._itemName}|{self._itemFeat}|{self._state}|"
        )

    def __str__(self):
        return (
            f"\n{self._visual.headLine}"
            f"{self._visual(f'Item Name: {self._itemName}')}"
            f"{self._visual.splitLine}"
            f"{self._visual(f'Item Number: {self._itemNum}')}"
            f"{self._visual(f'Feature: {self._itemFeat}')}"
            f"{self._visual.blankLine}"
            f"{self._visual(f'Description: {self._itemDesc}')}"
            f"{self._visual.blankLine}"
            f"{self._visual(f'Save Place: {self._savePlace}')}"
            f"{self._visual(f'State: {self._state}')}"
            f"{self._visual(f'Time: {self.time}')}"
            f"{self._visual.headLine}"
        )

    def __hash__(self):
        return hash(self.__str__())

