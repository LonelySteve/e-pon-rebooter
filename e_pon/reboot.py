import requests, re, time, sys

re_session_key = re.compile(r"var sessionKey='(\d+)'")
s = requests.session()
s.cookies.set('language', 'cn')  # 语言默认中文，这应该没啥影响


def _login(username, password):
    """
    登录光猫
    :param username: 终端配置账户用户名
    :param password: 终端配置账户密码
    :return: None
    """
    s.cookies.set('username', username)
    s.cookies.set('password', password)

    r = s.get('http://192.168.1.1/main.html?from=loginpage')
    r.raise_for_status()


def reboot(username, password):
    """
    重启光猫
    :param username: 终端配置账户用户名
    :param password: 终端配置账户密码
    :return: 光猫重启操作是否执行成功
    """
    _login(username, password)
    r = s.get('http://192.168.1.1/mng_resetrouter.html')
    r.raise_for_status()
    result = re_session_key.search(r.text)
    if not result:
        raise Exception('登录失败！')
    session_key = result.group(1)
    reboot_url = 'http://192.168.1.1/mng_rebootinfo%s.cgi' % s.cookies['language'].upper()
    r2 = s.get(reboot_url, params={'sessionKey': session_key})
    r2.raise_for_status()
    return 'setTimeout("reboot()", 60000);' in r2.text  # 这里只是个简单的判断，可能并不准确


def reboot_and_wait(username, password, check_func=None, timeout=100):
    """
    重启光猫并等待光猫重启完成，这需要一个检查函数来确定光猫是否重启完成，如果检查光猫重启状态时间超时，则将抛出TimeoutError异常
    :param username: 终端配置账户用户名
    :param password: 终端配置账户密码
    :param check_func: 光猫重启完成检查函数，它不接受任何参数，由返回值来决定光猫是否重启成功 (默认值是 None，即使用内置的检查函数)
    :param timeout: 超时时间，等待100秒后开始计算(默认值是 100，单位为秒，必须为整数)
    :return: 是否执行成功
    """

    if reboot(username, password):
        time.sleep(100)  # 重启过程大概需要两分钟，这里设置为100秒延迟
        if not check_func:
            def def_check_func():
                r = requests.get('https://www.baidu.com')
                r.raise_for_status()
                return True

            check_func = def_check_func
        # 循环检测验证是否成功
        for _ in range(timeout):
            try:
                if not check_func():
                    raise Exception("验证失败！")
            except Exception:
                # 验证失败
                pass
            else:
                break
            time.sleep(1)
        else:
            raise TimeoutError()
        return True
    return False


if __name__ == '__main__':
    _, uname, pwd, *_ = sys.argv
    print(reboot(uname, pwd))
