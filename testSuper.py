from processSupervisor import Supervisor
import psutil
import pynvml
from vero_email.py_email import Mail


def runSupervisor():
    super = Supervisor()
    super.supervise()
    ...


if __name__ == "__main__":
    pynvml.nvmlInit()
    handle = pynvml.nvmlDeviceGetHandleByIndex(0)
    gpuTemp = pynvml.nvmlDeviceGetTemperature(handle, 0)
    meminfo = pynvml.nvmlDeviceGetMemoryInfo(handle)
    # print("GPU 显存占用：" + str(meminfo.used/1024**2))
    # print("GPU 温度：" + str(gpuTemp))
    msg = "GPU 显存占用：" + str(meminfo.used/1024**2) + "\n"

    # print("CPU 占用率：" + str(psutil.cpu_percent(1)))
    msg = msg + "CPU 占用率：" + str(psutil.cpu_percent(1)) + "\n"

    # print("内存占用率：" + str(psutil.virtual_memory().percent))
    msg = msg + "内存占用率：" + str(psutil.virtual_memory().percent) + "\n"

    mail_host = 'smtp.qq.com'
    mail_user = '2053232384'
    mail_pass = 'syktappnjddlcadd'
    sender = '2053232384@qq.com'
    # receivers 需要设置，用户提前对用户名绑定邮箱
    receivers = ['2997839760@qq.com']
    title = "test mail"

    email = Mail(mail_host, mail_user, mail_pass)
    email.create_mail(title, sender, receivers)
    email.add_msg(title, msg)
    email.send_all()

    runSupervisor()
