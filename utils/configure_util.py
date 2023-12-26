import yaml


# def wt_yaml(title, msg=None, imgPaths=None, filePaths=None, timer=TIMER_OFF, mailbox=""):
#     path = os.getcwd() + "/" + title + ".yaml"
#     with open(path, 'w', encoding='utf-8') as f:
#         dct = {"title": title}
#         if msg is not None: dct.update({"message": msg})
#         if imgPaths is not None: dct.update({"imgPaths": imgPaths})
#         if filePaths is not None: dct.update({"filePaths": filePaths})
#         if timer != 0 and timer != 1: timer = 0
#         dct.update({"timer": timer})
#
#         if mailbox != "": dct.update({"mailbox": mailbox})
#
#         yaml.dump(dct, stream=f, allow_unicode=True)
#
#
# def ch_yaml(path, dct, node):
#     config = rd_yaml(path)
#     config[node] = dct
#     with open(path, 'w', encoding='utf-8') as f:
#         yaml.dump(config, stream=f, allow_unicode=True)
#
#
# def ad_yaml(path, dct, node):
#     config = rd_yaml(path)
#     config[node].extend([dct])
#     with open(path, 'w', encoding='utf-8') as f:
#         yaml.dump(config, stream=f, allow_unicode=True)


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

    def _save(self, path):
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

