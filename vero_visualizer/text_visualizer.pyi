from typing import List

class TextVisualizer:
    def __init__(self, maxLineLength: int, beforeLine: str, afterLine: str):
        self.maxLineLength = maxLineLength
        self.beforeLine = beforeLine
        self.afterLine = afterLine
    def __call__(self, text: str) -> str: ...
    @property
    def splitLine(self) -> str: ...
    @property
    def blankLine(self) -> str: ...
    @property
    def headLine(self) -> str: ...
    def _sep_section(self, section: str) -> List[str]: ...
    def _fill_line(self, line: str) -> str: ...
    def _get_word(self, section: str, index: int) -> (str, int, int): ...
    def _cal_strlen(self, sentence: str) -> float: ...
    def _is_Chinese(self, char: str) -> bool: ...


class ItemManageSystem:
    def __init__(self):
        self._manager = None
        self._visual = None

    def show_main_UI(self) -> str: ...
