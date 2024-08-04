## 组件：genshin auto sign

### 使用

1. 配置 `.cfg` 文件，格式为：
    ```
    [mw]
    account =
    password =
    
    [genshin_info]
    uid =
    hdid = e202311201442471
    region = cn_gf01
    dh = hk4e
    
    [starrail_info]
    uid = 
    hdid = e202304121516551
    region = prod_gf_cn
    dh = 
   
    [zzz_info]
    zzz_uid = 
    zzz-hdid = e202406242138391
    zzz-region = prod_gf_cn
    dh = zzz
    
    [credentials]
    
    [params]
    
    [api]
    url = https://api-takumi.mihoyo.com/event/luna/sign
    ```
    - account: 米游社账号
    - password: 米游社密码
    - uid: 原神 / 崩铁 uid
    - dh: 空着不填

2. 运行 get_params.py 文件中的 get_user_params 方法，获取参数
3. 运行 sign_request.py 文件中的 sign_process 方法，签到
