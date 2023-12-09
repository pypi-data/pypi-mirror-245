from ..response import get, post


def login_pw(username, password):
    "使用账号密码登录GC平台并获取信息"
    # 获取token
    url = "https://www.gamecreator.com.cn/index.php/apis/user/passwordlogin"
    json = {"username": username, "password": password}
    data = post(url, json)
    if data["code"] == 20000:
        # 获取信息
        url = "https://www.gamecreator.com.cn/index.php/apis/user/getuserinfo"
        token = data["data"]["token"]
        data = login_token(token)
    return data


def login_token(token):
    "使用token登录GC平台并获取信息"
    url = "https://www.gamecreator.com.cn/index.php/apis/user/getuserinfo"
    headers = {"Token": token}
    return get(url, headers)
