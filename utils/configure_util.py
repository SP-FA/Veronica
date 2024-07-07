import yaml


class ConfLoader:
    """用于加载配置文件，并进行交互

    Attributes:
        params (Dict): 报存配置文件的参数
    """
    def __init__(self, path):
        self.params = self._read(path)

    @staticmethod
    def _read(path):
        with open(path, 'r', encoding='utf-8') as f:
            dct = yaml.load(f.read(), Loader=yaml.FullLoader)
        return dct

    def save(self, path):
        with open(path, 'w', encoding='utf-8') as f:
            yaml.dump(self.params, stream=f, allow_unicode=True)

    def add(self, **kwargs):
        for k, v in kwargs.items():
            self.params[k] = v

    def __str__(self):
        info = ""
        for k, v in self.params.items():
            info = info + f"[PARAM] {k}: {v}\n"
        return info

    def __getitem__(self, key):
        return self.params[key]
