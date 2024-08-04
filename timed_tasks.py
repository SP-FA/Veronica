from utils.configure_util import ConfLoader
from vero_auto_sign.get_params import get_user_params
from vero_auto_sign.sign_request import sign_process

if __name__ == "__main__":
    path = "./conf.yaml"
    params = ConfLoader(path)

    # auto sign task
    users = ["SPFA"]
    for user in users:
        signCfgPath = f"./vero_auto_sign/cfgs/{user}.cfg"
        get_user_params(f"./vero_auto_sign/cfgs/{user}.cfg", "./vero_auto_sign/public_key.pem")
        sign_process(user, signCfgPath, params)
