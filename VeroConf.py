def wt_yaml(title, msg=None, imgPaths=None, filePaths=None, timer=TIMER_OFF, mailbox=""):
    path = os.getcwd() + "/" + title + ".yaml"
    with open(path, 'w', encoding='utf-8') as f:
        dct = {"title": title}
        if msg is not None: dct.update({"message": msg})
        if imgPaths is not None: dct.update({"imgPaths": imgPaths})
        if filePaths is not None: dct.update({"filePaths": filePaths})
        if timer != 0 and timer != 1: timer = 0
        dct.update({"timer": timer})

        if mailbox != "": dct.update({"mailbox": mailbox})

        yaml.dump(dct, stream=f, allow_unicode=True)


def rd_yaml(path):
    with open(path, 'r', encoding='utf-8') as f:
        dct = yaml.load(f.read(), Loader=yaml.FullLoader)
    return dct


def ch_yaml(path, dct, node):
    config = rd_yaml(path)
    config[node] = dct
    with open(path, 'w', encoding='utf-8') as f:
        yaml.dump(config, stream=f, allow_unicode=True)


def ad_yaml(path, dct, node):
    config = rd_yaml(path)
    config[node].extend([dct])
    with open(path, 'w', encoding='utf-8') as f:
        yaml.dump(config, stream=f, allow_unicode=True)

