# Veronica

啊啊啊啊啊啊啊搞不完啦！！！！

这是一个远程服务器监控程序。目前的开发进度为：

可以通过向自己的任务内添加特定的代码片段来实现远程监控任务进度。监控程序会定时 / 在任务结束时发送邮件，
你可以自定义邮件内容，以在任何时间地点获取任务的即时反馈。

## 快速使用

### 环境配置

```commandline
pip install -r requirements.txt
```

### 文件

找到 `VeroProc.py`，将此文件复制到需要使用的项目中去。

_未来可能考虑使用 pip 直接安装必要的文件_

### 包的导入和调用

```python
from VeroProc import SetProcess
```

通过以下代码可以进行基础配置，自定义发送邮件的内容，附件（图片或文件），并且可以选择是否定时发送：

```python
proc = SetProcess("test")
msg = "this is a test message"
imgPaths = [{"name": "testPic1", "path": "test1.png"}, {"name": "testPic2", "path": "test2.JPEG"}]
filePaths = [{"name": "testFil", "path": "testFil.txt"}]
mailbox = "****@**.com"
proc.configer(msg, imgPaths, filePaths, timer=1, mailbox=mailbox)
```

`timer` 参数表示是否启用定时发送邮件，1 为启用，0 为不启用

另可以使用如下代码来向邮件中添加训练时的迭代次数，方便定时查看进度：

```python
for cur_epoch in range(1, total_epoch+1):
    ...
    proc.set_epoch(cur_epoch, total_epoch)
    ...
```

## 高级使用

可以通过高级用法来使发送的邮件内容更加灵活，以达到动态展示进度的效果。

yaml 配置文件的结构如下：

```
title : str
message : str
imgPaths:
    - path : str
      name : str
filePaths:
    - path : str
      name : str
epoch:
    now : int
    total : int
timer: int
mailbox: str
```

所有一级 Key（即不包括 `path`, `name`, `now`, `total`）都可以使用 `change_node` 方法进行修改。
其中 `imgPaths` 和 `filePaths` 是 list 格式，可以使用 `add_node` 方法进行追加。

示例代码如下，这段代码为邮件内添加了一幅图片，并且每次循环计算了一个 loss，将邮件信息修改为这个值：

```python
loss = 100
proc.add_node({"name": "testPic3", "path": "testPic3.JPEG"}, "imgPaths")
for i in range(0, 50):
    ...
    proc.change_node(str(loss/(i+1)), "message")
    ...
```

**注意：由于暂时没有添加验证机制，请谨慎按照以上规定进行修改，以免出现错误。**

test code app

---

项目进度：
1. VeroProc：在需要被监视的代码内导入以被识别、编辑邮件内容
    - 修改进程名称，添加特殊标识符以能被监视。
    - 修改配置文件，包括了所有要通过邮件发送的结果
2. VeroSuper：监视器
    - 遍历进程队列
    - 查看进程状态：
        - 进程仍在运行
            - 如果要求定时发生报告，则发送邮件
        - 不在运行：将结果发送邮件
            - 获取进程工作目录，找到配置文件

todo：
3. 自动化管理任务：
    - 任务列表增删
    - 任务排队执行
    - 查看不同用户提交的任务
4. 远程监控电脑状态：
    - 获取 CPU GPU 占用、温度等参数
        - 在紧急情况下（占用率 100%，温度过高）
        - 手动获取
5. 文件整理：
    - 在 yzc 账户下进行测试
    - 初步开发完成后转到 root 账户进行全局管理
