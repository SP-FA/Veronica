# Veronica

啊啊啊啊啊啊啊搞不完啦！！！！

这是一个远程服务器监控程序，用于对我的多个设备进行自主管理、提供便捷服务

## 组件

- vero_auto_sign: 米家游戏自动签到，支持原神、崩铁、绝区零
- vero_chat: LLMs 对话
- vero_email: 自动收发 email
- 微信聊天机器人
- vero_item_manager: 物品管理系统
- vero_process_supervisor: 进程监控
- vero_visualizer: 格式化字符串工具

## 快速使用

### 环境配置

```commandline
pip install -r requirements.txt
```

各组件使用样例见 `./samples/`

[//]: # (### 文件)

[//]: # ()
[//]: # (找到 `VeroProc.py`，将此文件复制到需要使用的项目中去。)

[//]: # ()
[//]: # (_未来可能考虑使用 pip 直接安装必要的文件_)

[//]: # ()
[//]: # (### 包的导入和调用)

[//]: # ()
[//]: # (```python)

[//]: # (from VeroProc import SetProcess)

[//]: # (```)

[//]: # ()
[//]: # (通过以下代码可以进行基础配置，自定义发送邮件的内容，附件（图片或文件），并且可以选择是否定时发送：)

[//]: # ()
[//]: # (```python)

[//]: # (proc = SetProcess&#40;"test"&#41;)

[//]: # (msg = "this is a test message")

[//]: # (imgPaths = [{"name": "testPic1", "path": "test1.png"}, {"name": "testPic2", "path": "test2.JPEG"}])

[//]: # (filePaths = [{"name": "testFil", "path": "testFil.txt"}])

[//]: # (mailbox = "****@**.com")

[//]: # (proc.configer&#40;msg, imgPaths, filePaths, timer=1, mailbox=mailbox&#41;)

[//]: # (```)

[//]: # ()
[//]: # (`timer` 参数表示是否启用定时发送邮件，1 为启用，0 为不启用)

[//]: # ()
[//]: # (另可以使用如下代码来向邮件中添加训练时的迭代次数，方便定时查看进度：)

[//]: # ()
[//]: # (```python)

[//]: # (for cur_epoch in range&#40;1, total_epoch+1&#41;:)

[//]: # (    ...)

[//]: # (    proc.set_epoch&#40;cur_epoch, total_epoch&#41;)

[//]: # (    ...)

[//]: # (```)

[//]: # (## 高级使用)

[//]: # ()
[//]: # (可以通过高级用法来使发送的邮件内容更加灵活，以达到动态展示进度的效果。)

[//]: # ()
[//]: # (yaml 配置文件的结构如下：)

[//]: # ()
[//]: # (```)

[//]: # (title: str)

[//]: # (message: str)

[//]: # (imgPaths:)

[//]: # (    - path: str)

[//]: # (      name: str)

[//]: # (filePaths:)

[//]: # (    - path: str)

[//]: # (      name: str)

[//]: # (epoch:)

[//]: # (    now: int)

[//]: # (    total: int)

[//]: # (timer: int 是否启用定时，0 为不启用，1 为启用)

[//]: # (mailbox: str)

[//]: # (```)

[//]: # ()
[//]: # (所有一级 Key（即不包括 `path`, `name`, `now`, `total`）都可以使用 `change_node` 方法进行修改。)

[//]: # (其中 `imgPaths` 和 `filePaths` 是 list 格式，可以使用 `add_node` 方法进行追加。)

[//]: # ()
[//]: # (示例代码如下，这段代码为邮件内添加了一幅图片，并且每次循环计算了一个 loss，将邮件信息修改为这个值：)

[//]: # ()
[//]: # (```python)

[//]: # (loss = 100)

[//]: # (proc.add_node&#40;{"name": "testPic3", "path": "testPic3.JPEG"}, "imgPaths"&#41;)

[//]: # (for i in range&#40;0, 50&#41;:)

[//]: # (    ...)

[//]: # (    proc.change_node&#40;str&#40;loss/&#40;i+1&#41;&#41;, "message"&#41;)

[//]: # (    ...)

[//]: # (```)

[//]: # ()
[//]: # (**注意：由于暂时没有添加验证机制，请谨慎按照以上规定进行修改，以免出现错误。**)

---

项目进度：

- [x] : vero_auto_sign
- [ ] : vero_chat
  - [x] : 支持 ChatGPT
  - [ ] : 判断 ChatGPT 使用的 openai 版本，以及是否使用中转 key
- [ ] : vero_email
  - [x] : 基本功能
  - [ ] : 获取多种类型的 email 附件
- [ ] : vero_wechat
  - [x] : 基本功能
  - [ ] : 封装
- [ ] : vero_item_manager
  - [x] : 基本功能
  - [ ] : 目前只能使用控制台交互，添加其他交互方式
  - [ ] : 使用 table 的形式打印物品信息
- [ ] : vero_process_supervisor
  - [ ] : client
  - [ ] : host
- [ ] : vero_visualizer
  - [x] : text_visualizer
  - [ ] : dict_visualizer
