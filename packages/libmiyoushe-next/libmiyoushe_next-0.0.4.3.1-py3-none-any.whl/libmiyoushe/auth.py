import logging
import time

import webview

from . import *
from . import urls, base, configs

logger = logging.getLogger('libhoyolab.auth')

loginPageDestroyed_user = False

cookies = ''

page = """<!DOCTYPE html>
<html lang=zh>

<head>
<meta charset=UTF-8>
<title>Login</title>
<style>
button {
    height: 50px;
    width: 150px;
    border: none;
    margin: 0 auto;
    border-radius: 20px;
}

* {
    text-align: center;
}
</style>
<script>
function afterShowLoginPage() {
    pywebview.api.tologin().then(function(flag) {
        if(flag['flag']) {
            document.getElementsByClassName('login_user')[0].setAttribute("style", "display: none");
            document.getElementsByClassName('end')[0].setAttribute("style", "display: block");
        } else {
            alert("尝试显示窗口失败，请关闭该窗口后再试");
        }
    })
}

function afterLoginSuccess_user() {
    let status = confirm("是否登录完毕？");
    if(status) {
        document.getElementsByClassName('end')[0].setAttribute('disabled', '');
        pywebview.api.getcookies_user().then(function(flag) {
            console.log(flag['flag']);
            if(flag['flag']) {
                document.getElementsByClassName('end')[0].setAttribute("style", "display: none");
                document.getElementsByClassName('step')[0].setAttribute("style", "display: none");
                document.getElementsByClassName('ableToClose')[0].setAttribute("style", "display: block");
            } else {
                alert('尝试获取登录参数错误，请重新登录！');
                document.getElementsByClassName('end')[0].removeAttribute('disabled');
                document.getElementsByClassName('end')[0].setAttribute("style", "display:none ");document.getElementsByClassName('login_user')[0].setAttribute("style ","display: block ");
            }
        })
    }
}
</script>

<body>
    <p>
        <button class=login_user onclick=afterShowLoginPage() style=display:block>登录通行证</button>
    </p>
    <p>
        <button class=end onclick=afterLoginSuccess_user() style=display:none>完成</button>
    </p>
    <h1 class=ableToClose style=display:none>现在可以关闭该页面了</h1>
    <p class=step style="margin:0 auto">步骤：在打开通行证页面后,登录通行证</p>
</body>
</html>"""


def login(*args):
    """
    通过login_ticket获取其他需要的登录cookie信息
    :param args: login_ticket
    :return: bool 执行状态 True => 成功，False => 失败
    """
    try:
        for login_ticket in args:
            resp = session.get(urls.Cookie_url.format(login_ticket))
            data = resp.json()
            if "成功" in data["data"]["msg"]:
                stuid = ltuid = account_id = data["data"]["cookie_info"]["account_id"]
                cookie_token = data['data']["cookie_info"]['cookie_token']
                resp = session.get(url=urls.Cookie_url2.format(login_ticket, stuid))  # 获取stoken
                data = resp.json()
                stoken_v1 = data["data"]["list"][0]["token"]
                ltoken = data["data"]["list"][1]["token"]
                header = {'Cookie': f'stoken={stoken_v1};stuid={stuid}',
                          'DS': base.DS2(salt='prod'),
                          'x-rpc-app_id': 'bll8iq97cem8',
                          'x-rpc-game_biz': 'bbs_cn'}
                resp = session.post(urls.Cookie_url4, headers=header)
                data = resp.json()
                stoken_v2 = data['data']['token']['token']
                mid = data['data']['user_info']['mid']
                account = {
                    "login_ticket": login_ticket,
                    "stuid": stuid,
                    "stoken": [stoken_v1, stoken_v2],
                    "ltoken": ltoken,
                    "ltuid": ltuid,
                    'cookie_token': cookie_token,
                    'mid': mid,
                    'account_id': account_id
                }
                configs.writeAccount(stuid, account)
                set_current_user(account_id)
            else:
                continue
        return True
    except Exception as e:
        print(type(e), e)
        return False


def logout(uid: str = 'all'):
    """
    通过清空已记录的登录信息实现退出登录
    """
    configs.clearAccount(uid)


def reLogin(uid: str = 'all'):
    """
    刷新登录状态
    :return: bool 执行状态 True => 成功，False => 失败
    """

    def inner_reLogin(inner_uid):
        account = configs.readAccount('dict', inner_uid)
        if account['isLogin']:
            login_ticket = account['login_ticket']
            return login(login_ticket)

    exist_user_list = getExistUser()
    if uid == 'all':
        for uid in exist_user_list:
            inner_reLogin(uid)
    elif uid == 'current':
        inner_reLogin(get_current_user())
    elif uid in exist_user_list:
        inner_reLogin(uid)


def createLoginMmt():
    resp_mmt = session.get(urls.mmt.format(int(time.time() * 1000))).json()
    return resp_mmt['data']['mmt_data']


class getLoginTicketBySms:
    @staticmethod
    def createSms(phone, mmt, geetest_data=None):
        if geetest_data is None:
            geetest_data = {}
        datas = {
            'action_type': 'login',
            'mmt_key': mmt,
            'mobile': phone,
            't': str(int(time.time() * 1000))
        }
        if geetest_data:
            match geetest_data['version']:
                case 'none':
                    pass
                case 'gt3':
                    datas['geetest_challenge'] = geetest_data['geetest_challenge']
                    datas['geetest_validate'] = geetest_data['geetest_validate']
                    datas['geetest_seccode'] = geetest_data['geetest_seccode']
                case 'gt4':
                    if geetest_data['geetest_v4_data'] is dict:
                        datas['geetest_v4_data'] = json.dumps(geetest_data['geetest_v4_data'])
                    else:
                        datas['geetest_v4_data'] = geetest_data['geetest_v4_data']
        raw_resp = session.post(urls.send_sms, data=datas)
        resp_login = raw_resp.json()
        return resp_login

    @staticmethod
    def verifySms(phone, code):
        datas = {
            'source': 'user.mihoyo.com',
            'mobile_captcha': code,
            'mobile': phone,
            't': str(int(time.time() * 1000))
        }
        raw_resp = session.post(urls.login_sms, data=datas)
        resp_login = raw_resp.json()
        if resp_login['data']['msg'] == '成功':
            return {'msg': resp_login['data']['msg'], 'token': resp_login['data']['account_info']['weblogin_token']}
        else:
            return {'msg': resp_login['data']['msg'], 'token': ''}


def getLoginTicketByPassword(username: str, password: str, mmt: str, pwd_crypto=True, geetest_data=None):
    """
    使用用户名密码获取login_ticket
    :param pwd_crypto:是否加密密码
    :param geetest_data: 极验人机验证返回信息（需要转换成JSON文本）
    :param mmt: 人机验证token
    :param username: 米哈游通行证 - 账号
    :param password: 米哈游通行证 - 密码
    :return: dict 'msg' => 执行返回信息，'token' => login_ticket(失败返回空字符串)
    """
    if geetest_data is None:
        geetest_data = {}
    datas = {
        'account': username,
        'password': base.encrypt(password) if pwd_crypto else password,
        'is_crypto': str(pwd_crypto).lower(),
        'mmt_key': mmt,
        'source': 'user.mihoyo.com',
        't': str(int(time.time() * 1000))
    }
    if geetest_data:
        match geetest_data['version']:
            case 'none':
                pass
            case 'gt3':
                datas['geetest_challenge'] = geetest_data['geetest_challenge']
                datas['geetest_validate'] = geetest_data['geetest_validate']
                datas['geetest_seccode'] = geetest_data['geetest_seccode']
            case 'gt4':
                if geetest_data['geetest_v4_data'] is dict:
                    datas['geetest_v4_data'] = json.dumps(geetest_data['geetest_v4_data'])
                else:
                    datas['geetest_v4_data'] = geetest_data['geetest_v4_data']
    raw_resp = session.post(urls.login_pwd, data=datas)
    resp_login = raw_resp.json()
    if resp_login['data']['msg'] == '成功':
        return {'msg': resp_login['data']['msg'], 'token': resp_login['data']['account_info']['weblogin_token']}
    else:
        return {'msg': resp_login['data']['msg'], 'token': ''}


def loginByWeb(gui_page: str = page, open_webview=True):
    """
    利用pywebview处理用户登录事件并利用获取到的login_ticket完成登录
    :param open_webview: 是否启动webview界面
    :param gui_page: 自定义登录gui界面
    """
    global cookies

    class apis:
        def tologin(self):
            global loginPageDestroyed_user
            if not loginPageDestroyed_user:
                loginAccount_user.show()
                return {'flag': True}
            else:
                main.create_confirmation_dialog(title="错误", message="尝试打开米游社时出错，请稍后重试")
                main.destroy()
                return {'flag': False}

        def getcookies_user(self):
            global loginPageDestroyed_user, cookies
            loginAccount_user.hide()
            cookies = dict(
                list(map(lambda l: l.split("="), loginAccount_user.evaluate_js("document.cookie").split("; "))))
            loginAccount_user.confirm_close = False
            main.confirm_close = False
            flag = login(cookies.get('login_ticket', ''))
            if flag:
                loginAccount_user.destroy()
                loginPageDestroyed_user = True
            return {'flag': flag}

    api = apis()
    loginAccount_user = webview.create_window(title="!!!完成登录操作前请勿关闭该窗口!!!",
                                              url="https://user.mihoyo.com", hidden=True,
                                              confirm_close=True, height=900, width=900)
    main = webview.create_window(js_api=api, on_top=True, x=10, y=10, title='!!!完成登录操作前请勿关闭该窗口!!!',
                                 html=gui_page, minimized=False, confirm_close=True, resizable=False, height=175,
                                 width=650)

    if open_webview:
        webview.start()


class GeetestVerification:
    @staticmethod
    def createVerification():
        resp = session.get(url=urls.createVerification, headers=base.headerGenerate(client='2'))
        return resp.json()['data']

    @staticmethod
    def verifyVerification(geetest_json):
        if geetest_json is str:
            geetest_json = json.loads(geetest_json)
        resp = session.post(url=urls.verifyVerification, headers=base.headerGenerate(client='2'), json=geetest_json)
        return resp.json()
