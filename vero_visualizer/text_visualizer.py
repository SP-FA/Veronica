class TextVisualizer:
    def __init__(self, maxLineLength, afterLine):
        self.maxLineLength = maxLineLength
        self.afterLine = afterLine

    def __call__(self, text):
        """将输入的文本生成为一个可以直接打印的格式化字符串。
        1. text -> 分成多个 sections
        2. section -> 分成多个 words
        3. words -> 多个 word 拼成 line
        4. line 补全

        Args:
            text (str): 输入文本

        Returns:
            str: 格式化后的字符串
        """
        text = text.replace("\r", "")
        sections = text.split("\n")
        visualStrings = []
        for section in sections:
            visualStrings.extend(self._sep_section(section))
            visualStrings.append(self._fill_line(" "))

        return self.afterLine.join(visualStrings)

    def _sep_section(self, section):
        """把一个段落合理的分配为多行，每一行长度不超过 self.maxLineLength，段落后加一行空行

        Args:
            section (str): 一个段落，中英混合的字符串

        Returns:
            List[str]: list 中每个元素表示完整的一行
        """
        lineLst = []
        oneLine = ""
        lineLength = 0

        charIndex = 0
        while charIndex < len(section):
            word, wordLen, index = self._get_word(section, charIndex)
            lineLength += wordLen
            if lineLength > self.maxLineLength:
                lineLst.append(self._fill_line(oneLine))
                lineLength = wordLen
                oneLine = word
            else:
                oneLine = oneLine + word
            charIndex = index
        lineLst.append(self._fill_line(oneLine))
        return lineLst

    def _fill_line(self, line):
        """将不足一行长度的字符串补上空格

        Args:
            line (str): 一个中英混合的字符串

        Returns:
            str: 一个完整的行
        """
        m = self._cal_strlen(line)
        return line + " " * (self.maxLineLength - int(m + 0.75))

    def _get_word(self, section, index):
        """从某个位置开始取出一个单词。如果是汉字，则只取出这一个字。如果是英文字母，则取出一个完整的单词。

        TODO: 对标点符号进行判断，目前如果遇到如 "char(char)" 这种字符串会视为一个单词

        Args:
            section (str): 需要取出一个单词的中英混合字符串
            index (int): 从这个位置开始往后找一个完整的单词，该位置必须是汉字 / 英文字母

        Returns:
            str: 完整的单词
            int: 单词的长度
            int: 单词结束位置
        """
        if section[index] == " ": return " ", 1, index + 1
        word = section[index]
        endIndex = len(section)
        for i in range(index + 1, len(section)):
            curChar = section[i]
            if curChar == " " or self._is_Chinese(curChar):
                endIndex = i
                break
            word = word + curChar
        return word, self._cal_strlen(word), endIndex

    @staticmethod
    def _cal_strlen(sentence):
        """计算一个中英混合字符串的长度

        Args:
            sentence (str): 一个中英混合的字符串

        Returns:
            int: 长度
        """
        length = 0
        for char in sentence:
            if '\u4e00' <= char <= '\u9fff':
                length += 1.71428571
            else:
                length += 1
        return length

    @staticmethod
    def _is_Chinese(char: str):
        if '\u4e00' <= char <= '\u9fff': return True
        return False
