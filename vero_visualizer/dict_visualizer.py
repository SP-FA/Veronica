class DictVisualizer:
    """实现字典可视化，把字典看作一个 table，key 是 column name 每一行填一个 dict，支持 List[Dict]
    """
    def __init__(self, beforeLine, afterLine, *args, **kwargs):
        """
        Args:
            beforeLine (str):
            afterLine (str):
            *args (Tuple): 可以通过提供一个 Tuple 来告诉 visualizer 有哪些 key
            **kwargs (Dict): 可以通过提供一个 Dict 来告诉 visualizer 有哪些 key
        """

