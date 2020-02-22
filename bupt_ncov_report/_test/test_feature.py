import json
import os
import tempfile
import unittest
from typing import Any, Dict, List, MutableMapping, NamedTuple, Optional, Tuple

from bupt_ncov_report import *

LOGIN_PAGE_URL = r'https://app.bupt.edu.cn/uc/wap/login'
LOGIN_API_RESP = r'''{"e":0,"m":"操作成功","d":{}}'''
LOGIN_API_FAILED_RESP = r'''{"e":0,"m":"ユーザーまたはパスワードは正しくありません。","d":{}}'''
REPORT_API_RESP = r'''{"e":1,"m":"今天已经填报了","d":{}, "f": "bupt_ncov_report-FeatureTest"}'''
REPORT_PAGE_HTML = r'''
<!DOCTYPE html>
<html lang="zh-CN">

<head>
<title>每日上报</title>
</head>

<body class="">

<script type="text/javascript">
  var def = {"address": "abc", "area": "", "bztcyy": "1", "city": "", "created": "1141141919", "created_uid": "0", "date": "20770101", "fjsj": "0", "fxyy": "", "geo_api_info": "ghi", "glksrq": "", "gllx": "", "gwszdd": "", "id": "114514", "jcbhlx": "", "jcbhrq": "", "jchbryfs": "", "jcjg": "", "jcjgqr": "0", "jcqzrq": "", "jcwhryfs": "", "jhfjhbcc": "", "jhfjjtgj": "", "jhfjrq": "", "jhfjsftjhb": "0", "jhfjsftjwh": "0", "jrdqjcqk": [], "jrdqtlqk": [], "jrsfqzfy": "", "jrsfqzys": "", "province": "def", "qksm": "", "remark": "", "sfcxtz": "0", "sfcxzysx": "0", "sfcyglq": "0", "sfjcbh": "0", "sfjchbry": "0", "sfjcqz": "", "sfjcwhry": "0", "sfsfbh": "0", "sftjhb": "0", "sftjwh": "0", "sfyqjzgc": "", "sfyyjc": "0", "sfzx": "0", "szgj": "", "tw": "3", "uid": "1919", "xjzd": "\u5317\u4eac"};
  var vm = new Vue({
    el: '.form-detail2',
    data: {
      realname: '田所浩二',
      number: '2020114514',
      date: '2020-02-08',
      info: $.extend({ ismoved: 0 }, def),
      oldInfo: {"address": "123", "area": "1", "bztcyy": "1", "city": ""},
      tipMsg: '',
      ajaxLock: false,
      showFxyy: false,
      hasFlag: '1',
    }
  });

</script>
</body>

</html>
'''

POST_DATA_NORMAL = {
    'address': 'abc',
    'area': '',
    'bztcyy': '1',
    'city': '',
    'created': '1141141919',
    'created_uid': '0',
    'date': '20770101',
    'fjsj': '0',
    'fxyy': '',
    'geo_api_info': 'ghi',
    'glksrq': '',
    'gllx': '',
    'gwszdd': '',
    'id': '114514',
    'jcbhlx': '',
    'jcbhrq': '',
    'jchbryfs': '',
    'jcjg': '',
    'jcjgqr': '0',
    'jcqzrq': '',
    'jcwhryfs': '',
    'jhfjhbcc': '',
    'jhfjjtgj': '',
    'jhfjrq': '',
    'jhfjsftjhb': '0',
    'jhfjsftjwh': '0',
    'jrdqjcqk': [],
    'jrdqtlqk': [],
    'jrsfqzfy': '',
    'jrsfqzys': '',
    'province': 'def',
    'qksm': '',
    'remark': '',
    'sfcxtz': '0',
    'sfcxzysx': '0',
    'sfcyglq': '0',
    'sfjcbh': '0',
    'sfjchbry': '0',
    'sfjcqz': '',
    'sfjcwhry': '0',
    'sfsfbh': '0',
    'sftjhb': '0',
    'sftjwh': '0',
    'sfyqjzgc': '',
    'sfyyjc': '0',
    'sfzx': '0',
    'szgj': '',
    'tw': '3',
    'uid': '1919',
    'xjzd': '北京',
}

REPORT_PAGE_HTML_OF_SICK_PEOPLE = r'''
<!DOCTYPE html>
<html lang="zh-CN">

<head>
<title>每日上报</title>
</head>

<body class="">

<script type="text/javascript">
  var def = {"address": "abc", "area": "", "bztcyy": "1", "city": "", "created": "1141141919", "created_uid": "0", "date": "20770101", "fjsj": "0", "fxyy": "", "geo_api_info": "ghi", "glksrq": "", "gllx": "", "gwszdd": "", "id": "114514", "jcbhlx": "", "jcbhrq": "", "jchbryfs": "", "jcjg": "", "jcjgqr": "0", "jcqzrq": "", "jcwhryfs": "", "jhfjhbcc": "", "jhfjjtgj": "", "jhfjrq": "", "jhfjsftjhb": "0", "jhfjsftjwh": "0", "jrdqjcqk": [], "jrdqtlqk": [], "jrsfqzfy": "", "jrsfqzys": "", "province": "def", "qksm": "", "remark": "", "sfcxtz": "0", "sfcxzysx": "0", "sfcyglq": "0", "sfjcbh": "1", "sfjchbry": "0", "sfjcqz": "", "sfjcwhry": "0", "sfsfbh": "0", "sftjhb": "0", "sftjwh": "0", "sfyqjzgc": "", "sfyyjc": "0", "sfzx": "0", "szgj": "", "tw": "3", "uid": "1919", "xjzd": "\u5317\u4eac"};
  var vm = new Vue({
    el: '.form-detail2',
    data: {
      realname: '田所浩二',
      number: '2020114514',
      date: '2020-02-08',
      info: $.extend({ ismoved: 0 }, def),
      oldInfo: {"address": "123", "area": "1", "bztcyy": "1", "city": ""},
      tipMsg: '',
      ajaxLock: false,
      showFxyy: false,
      hasFlag: '1',
    }
  });

</script>
</body>

</html>
'''

LOGIN_PAGE_HTML = r'''
<!DOCTYPE html>
<html lang="zh-CN">

<head>
  <title>登录</title>
</head>

<body class="">

  <div id="app" v-cloak>
    <div class="content">
      <div><i class="icon iconfont icon-touxiang"></i>
        <input type="text" :placeholder="'请输入'+setting.account_copy" v-model="username" autocomplete="off" />
      </div>
      <div><i class="icon iconfont icon-mima" style=""></i>
        <input type="password" :placeholder="'请输入'+setting.password_copy" v-model="password" autocomplete="off" />
      </div>
    </div>
    <div class="btn" @click='login()'>登 录</div>
    <div class="footer" v-if="setting.login_remarks != undefined && setting.login_remarks != ''">
      <h2><span></span>注意事项<span></span></h2>
      <p v-html="setting.login_remarks"></p>
    </div>
    <div class="foot">
      <p>版权所有&copy;{{setting.copyright}}</p>
    </div>
  </div>
</body>

</html>
'''

TG_API_RESP = r'''{"ok": true}'''


class RequestHistory(NamedTuple):
    """
    Session 的 mock 类支持「调用历史」功能。

    本类用于存放 session mock 类的 get、post 方法被调用时传入的参数。
    以下类成员与 requests 的 html 方法的参数一一对应；请查阅 requests 文档。
    除以下参数以外的参数会被忽略，不会存入本类中。
    """

    action: str
    url: str
    data: Optional[Dict[str, Any]]
    json: Optional[Dict[str, Any]]


class MockResponse(NamedTuple):
    """
    模拟 requests 中调用 get、set 所返回的 Response 对象。
    关于属性的作用，请参照 requests 的文档。
    """

    status_code: int
    text: str
    url: str

    def json(self) -> Dict[str, Any]:
        """
        将 text 属性当作 json 格式解析，转换为 dict。
        :return: dict
        """
        return json.loads(self.text)


class MockWhenWrapper:
    """
    为了实现 mock.when(...).respond(...) 语法，该类实现了 respond 方法。
    在调用 session mock 类的 when 方法时会返回本类实例。
    本类与 MockRequestsSession 强依赖。
    """

    def __init__(
            self,
            resp: MutableMapping[Tuple[str, str], MockResponse],
            url: str,
            action: str,
    ):
        """
        传入实现 mock 功能所必要的参数。
        :param resp: MockRequestsSession 中的 _resp 对象
        :param url: 用户在 when 中指定的 url
        :param action: 用户在 when 中指定的 action
        """
        self._resp = resp
        self._url = url
        self._action = action

    def respond(self, status_code: int = 200, text: str = '', url: Optional[str] = None):
        if url is None:
            url = self._url

        self._resp[self._action, self._url] = MockResponse(status_code, text, url)


class MockRequestsSession:
    """
    该类用于模拟 requests 的 Session 类。

    该类的 API 设计模仿了著名 Java mocking 库 Mockito，允许用户用 mock.when(...).respond(...)
    的方式来表示「当访问某 url 时，返回的 Response 对象内容是……」。
    """

    def __init__(self):
        """初始化私有属性"""
        self._resp: MutableMapping[Tuple[str, str], MockResponse] = {}
        self._history: List[RequestHistory] = []

    def history(self) -> List[RequestHistory]:
        """返回该类被调用的历史"""
        return self._history.copy()

    def find_history(self, url) -> List[RequestHistory]:
        """
        查找访问该 URL 的调用历史。
        :param url: URL
        :return 调用历史列表；当没有调用历史时，返回空列表
        """
        return [x for x in self._history if x.url == url]

    def last_request(self) -> RequestHistory:
        """
        返回该类被最后一次调用的历史。
        当没被调用过时，抛出异常。
        :return: 调用历史
        """
        if len(self._history) == 0:
            raise ValueError('No any history')

        return self._history[-1]

    def get(self, url, *args, **kwargs):
        """模拟的 get 方法。该方法会记录调用历史。"""
        self._history.append(RequestHistory('get', url, None, None))

        resp = self._resp.get(('get', url))
        if resp is None:
            raise RuntimeError(f'UrlNotFoundError: when try to get {url}')

        return resp

    def post(self, url, data=None, json=None, *args, **kwargs):
        """模拟的 post 方法。该方法会记录调用历史。"""
        self._history.append(RequestHistory('post', url, data, json))

        resp = self._resp.get(('post', url))
        if resp is None:
            raise RuntimeError(f'UrlNotFoundError: when try to post to {url}')

        return resp

    def when(self, action: str, url: str) -> MockWhenWrapper:
        """
        用于注册调用 get/post 时的返回值。
        :param action: 字符串，只能为 get 或 post；若 action 为 post，则 get 此 url 时不会返回该值
        :param url: get/post 的 URL（精确匹配，大小写敏感）
        :return: MockWhenWrapper
        """
        action = action.lower()
        assert action == 'post' or action == 'get'

        return MockWhenWrapper(
            resp=self._resp,
            url=url,
            action=action
        )


def correctly_login_tester(self: unittest.TestCase, session: MockRequestsSession) -> None:
    """测试：断言正确提交登录请求"""

    login_history = session.find_history(LOGIN_API)
    self.assertEqual(len(login_history), 1)
    login_history = login_history[0]

    self.assertEqual(login_history.data, {
        'username': '2020114514',
        'password': '114514',
    })


def visited_url_tester(self: unittest.TestCase, session: MockRequestsSession, url: str) -> None:
    """
    测试用例的工具函数：断言访问了指定的 url。
    :param self: 测试类实例
    :param session: MockRequestsSession
    :param url: URL
    :return: None
    """

    history = session.find_history(url)
    self.assertEqual(len(history), 1)


def not_visit_url_tester(self: unittest.TestCase, session: MockRequestsSession, url: str) -> None:
    """
    测试用例的工具函数：断言没有访问指定的 url。
    :param self: 测试类实例
    :param session: MockRequestsSession
    :param url: URL
    :return: None
    """

    history = session.find_history(url)
    self.assertEqual(history, [])


def correctly_post_report_data_tester(self: unittest.TestCase, session: MockRequestsSession) -> None:
    """测试：断言上报 API 提交内容正确"""

    report_history = session.find_history(REPORT_API)
    self.assertEqual(len(report_history), 1)
    report_history = report_history[0]

    self.assertEqual(report_history.data, POST_DATA_NORMAL)


def log_written_tester(self: unittest.TestCase, log_path: str, written_text: str) -> None:
    """
    测试：断言写了日志
    :param log_path: 日志文件路径
    :param written_text: 在日志里能找到的内容
    :return: None
    """
    # 如果日志文件中有 REPORT_API_RESP 的内容，那整个程序运行一定成功了。
    with open(log_path, 'r', encoding='utf-8') as f:
        text = f.read()

    self.assertIn(written_text, text)


def generate_config(self: unittest.TestCase, stop_when_sick: bool) -> Dict[str, Any]:
    """
    生成 config。会返回完美 config。
    会调用 tempfile 以生成临时日志文件。其中的 BNR_LOG_PATH 是合法的日志地址。

    :param self: 测试类的实例。
    :param stop_when_sick: STOP_WHEN_SICK 配置。
    :return: 完美配置，用于传入 bupt_ncov_report.Program
    """
    log_fd, log_path = tempfile.mkstemp(suffix='.log')
    os.close(log_fd)

    config = {
        'BUPT_SSO_USER': '2020114514',
        'BUPT_SSO_PASS': '114514',
        'TG_BOT_TOKEN': '114514:abcdef',
        'TG_CHAT_ID': '1145141919810',
        'BNR_LOG_PATH': log_path,
        'STOP_WHEN_SICK': stop_when_sick,
    }

    return config


def register_respond_to_mock(session: MockRequestsSession, login_success: bool, is_sick: bool) -> None:
    """
    将模拟的 HTML 响应逻辑注册到 session 上。
    :param session: MockRequestsSession
    :param login_success: 登录是否成功；为 False 时将模拟登录失败场景
    :param is_sick: 用户是否生病；为 True 时将模拟带病的上报页面
    :return:
    """
    session.when('POST', LOGIN_API).respond(
        text=LOGIN_API_RESP if login_success else LOGIN_API_FAILED_RESP
    )

    if login_success:
        session.when('GET', REPORT_PAGE).respond(
            text=REPORT_PAGE_HTML_OF_SICK_PEOPLE if is_sick else REPORT_PAGE_HTML
        )
    else:
        session.when('GET', REPORT_PAGE).respond(
            url=LOGIN_PAGE_URL,
            text=LOGIN_PAGE_HTML,
        )

    session.when('POST', REPORT_API).respond(text=REPORT_API_RESP)

    session.when(
        'POST', 'https://api.telegram.org/bot114514:abcdef/sendMessage'
    ).respond(text=TG_API_RESP)


def setup_testCase(self: unittest.TestCase, stop_when_sick: bool, login_success: bool, is_sick: bool) -> None:
    """
    多个 TestCase 的 setUp 函数有公共代码，因此抽取出来。
    :param self: 测试类实例
    :param stop_when_sick: 是否开启 stop_when_sick 功能
    :param login_success: （模拟的）登录是否成功
    :param is_sick: 是否模拟用户数据带病的场景
    :return: None
    """
    self.config = generate_config(self, stop_when_sick=stop_when_sick)

    self.sess = MockRequestsSession()
    register_respond_to_mock(self.sess, login_success=login_success, is_sick=is_sick)

    # 此处类型错误忽略
    self.prog = Program(ProgramUtils(PureUtils()), self.sess, self.config)
    self.prog.main()


class TestFeature_Normal(unittest.TestCase):

    def _expected_behavior(self):
        # 正确提交登录请求
        correctly_login_tester(self, self.sess)

        # 访问了报告页
        visited_url_tester(self, self.sess, REPORT_PAGE)

        # 上报 API 提交内容正确
        correctly_post_report_data_tester(self, self.sess)

        # 访问了 Tg API
        visited_url_tester(self, self.sess, 'https://api.telegram.org/bot114514:abcdef/sendMessage')

        # 日志中有上报 API 的服务器返回
        log_written_tester(self, self.config['BNR_LOG_PATH'], 'bupt_ncov_report-FeatureTest')

        # 状态码为 0
        self.assertEqual(self.prog.get_exit_status(), 0)

    def test_everythingAsUsual(self):
        setup_testCase(self, login_success=True, stop_when_sick=True, is_sick=False)
        self._expected_behavior()


class TestFeature_SickButDoNotStop(unittest.TestCase):

    def _expected_behavior(self):
        # 正确提交登录请求
        correctly_login_tester(self, self.sess)

        # 访问了报告页
        visited_url_tester(self, self.sess, REPORT_PAGE)

        # 访问了上报 API（不检查上报内容）、Tg API
        visited_url_tester(self, self.sess, REPORT_API)
        visited_url_tester(self, self.sess, 'https://api.telegram.org/bot114514:abcdef/sendMessage')

        # 日志中有上报 API 的服务器返回
        log_written_tester(self, self.config['BNR_LOG_PATH'], 'bupt_ncov_report-FeatureTest')

        # 状态码为 0
        self.assertEqual(self.prog.get_exit_status(), 0)

    def test_sickButDoNotStop(self):
        setup_testCase(self, login_success=True, stop_when_sick=False, is_sick=True)
        self._expected_behavior()


class TestFeature_FailWhenRunning(unittest.TestCase):

    def _expected_behavior(self):
        # 正确提交登录请求
        correctly_login_tester(self, self.sess)

        # 访问了报告页
        visited_url_tester(self, self.sess, REPORT_PAGE)

        # 未访问上报 API
        not_visit_url_tester(self, self.sess, REPORT_API)

        # 访问了 Tg API
        visited_url_tester(self, self.sess, 'https://api.telegram.org/bot114514:abcdef/sendMessage')

        # 日志中有 RuntimeError
        log_written_tester(self, self.config['BNR_LOG_PATH'], 'RuntimeError')

        # 状态码不为 0
        self.assertNotEqual(self.prog.get_exit_status(), 0)

    def test_sickData_Stop(self):
        setup_testCase(self, login_success=True, stop_when_sick=True, is_sick=True)
        self._expected_behavior()

    def test_loginFailed_Stop(self):
        setup_testCase(self, login_success=False, stop_when_sick=True, is_sick=False)
        self._expected_behavior()


if __name__ == '__main__':
    unittest.main()
