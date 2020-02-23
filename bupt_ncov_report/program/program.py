__all__ = (
    'Program',
)

import html
import json
import logging
import sys
import traceback
from typing import Mapping, Optional

import requests

from ..constant import *
from ..predef import *
from ..program_utils import *
from ..program.inform import *

logger = logging.getLogger(__name__)


class Program:
    """
    程序的主入口，实现了主要的逻辑。
    使用本类时，直接调用 main 函数即可。
    本类提供状态码。状态码应用于外部代码退出此程序。
    """

    def __init__(
            self,
            program_utils: ProgramUtils,
            session: requests.Session,
            config: Mapping[str, Optional[ConfigValue]],
    ):
        self._prog_util = program_utils
        self._sess = session

        self._check_config(config)
        self._initialize_logger(logger, config.get('BNR_LOG_PATH'))  # type: ignore
        self._conf: Mapping[str, Optional[ConfigValue]] = config
        self._exit_status: int = 0

    def get_exit_status(self) -> int:
        return self._exit_status

    @staticmethod
    def _check_config(config: Mapping[str, Optional[ConfigValue]]) -> None:
        """
        检查程序配置是否正确；如不正确则抛出异常。
        :return: None
        """

        # 检查 BUPT SSO 用户名、密码
        for key in ('BUPT_SSO_USER', 'BUPT_SSO_PASS'):
            if config[key] is None:
                raise ValueError(f'配置 {key} 未设置。缺少此配置，该脚本无法自动登录北邮网站。')

        # 检查 Telegram 的环境变量是否已经设置
        if (config['TG_BOT_TOKEN'] is None) != (config['TG_CHAT_ID'] is None):
            raise ValueError('TG_BOT_TOKEN 和 TG_CHAT_ID 必须同时设置，否则程序无法正确运行。')

    @staticmethod
    def _initialize_logger(logger: logging.Logger, log_file: Optional[str]) -> None:
        """
        初始化传入的 Logger 对象，
        将 INFO 以上的日志输出到屏幕，将所有日志存入文件。
        :param logger: Logger 对象
        :param log_file: 日志文件路径
        :return: None
        """
        logger.setLevel(logging.DEBUG)

        # 将日志输出到控制台
        sh = logging.StreamHandler(sys.stdout)
        sh.setLevel(logging.INFO)
        sh.setFormatter(logging.Formatter('[%(levelname)s] %(message)s'))
        logger.addHandler(sh)

        # 将日志输出到文件
        if log_file:
            fh = logging.FileHandler(log_file, encoding='utf-8')
            fh.setLevel(logging.DEBUG)
            fh.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
            logger.addHandler(fh)

    def do_ncov_report(self) -> str:
        """
        进行信息上报的工作函数，包含本脚本主要逻辑。
        :return: 上报 API 的返回内容。
        """
        # 登录北邮 nCoV 上报网站
        logger.info('登录北邮 nCoV 上报网站')
        login_res = self._sess.post(LOGIN_API, data={
            'username': self._conf['BUPT_SSO_USER'],
            'password': self._conf['BUPT_SSO_PASS'],
        })
        if login_res.status_code != 200:
            logger.debug(f'登录页：\n'
                         f'status code: {login_res.status_code}\n'
                         f'url: {login_res.url}')
            raise RuntimeError('登录 API 返回的 HTTP 状态码不是 200。')

        # 获取上报页面的数据
        report_page_res = self._sess.get(REPORT_PAGE)
        logger.debug(f'报告页：\n'
                     f'status code: {report_page_res.status_code}\n'
                     f'url: {report_page_res.url}')
        if report_page_res.status_code != 200:
            raise RuntimeError('上报页面的 HTTP 状态码不是 200。')
        if report_page_res.url != REPORT_PAGE:
            raise RuntimeError('访问上报页面时被重定向。您的北邮账号和密码可能有误。')
        page_html = report_page_res.text
        if '每日上报' not in page_html:
            raise RuntimeError('上报页面的 HTML 中没有找到「每日上报」，可能已经改版。')

        # 从上报页面中提取 POST 的参数
        post_data = self._prog_util.extract_post_data(page_html)
        logger.debug(f'最终提交参数：{json.dumps(post_data)}')

        # 检查上报参数有没有异常
        if self._conf['STOP_WHEN_SICK']:
            self._prog_util.check_data_sick(post_data)

        # 最终 POST
        report_api_res = self._sess.post(REPORT_API, post_data)
        if report_api_res.status_code != 200:
            raise RuntimeError('上报 API 返回的 HTTP 状态码不是 200。')

        return report_api_res.text

    def main(self) -> str:
        """
        真正的主函数。
        该函数读取程序配置，并尝试调用工作函数；
        该函数随后获取工作函数的返回值或异常内容，通过 Telegram 机器人发送给用户。

        :return: 通过 Telegram 机器人发送的信息
        """
        # 运行工作函数
        logger.info('运行工作函数')
        success = True
        try:
            res = self.do_ncov_report()
        except:
            success = False
            res = traceback.format_exc()

        # 生成消息并打印到控制台
        if success:
            msg = f'[bupt-ncov-report] <b>成功：</b>服务器的返回是：\n\n' \
                  f'<pre>{html.escape(res)}</pre>'
            trans_msg = f'[bupt-ncov-report] 成功：服务器的返回是：\n\n' \
                        f'{res}'
        else:
            msg = f'[bupt-ncov-report] <b>失败：</b>发生如下异常：\n\n' \
                  f'<pre>{html.escape(res)}</pre>'
            trans_msg = f'[bupt-ncov-report] 失败：发生如下异常：\n\n' \
                        f'{res}'
        logger.info(msg)

        if self._conf['TG_BOT_TOKEN'] is not None and self._conf['TG_CHAT_ID'] is not None:
            tg = TG(msg, self._conf, self._sess, logger, success)
            success = tg.send_result()

        if self._conf['QQ_BOT_HOST'] and self._conf['QQ_BOT_TOKEN'] and self._conf['QQ_ID']:
            qq = QQ(trans_msg, self._conf, self._sess, logger, success)
            success = qq.send_result()

        if self._conf['SERVER_CHAN_SC_KEY']:
            wechat = WECHAT(trans_msg, self._conf, self._sess, logger, success)
            success = wechat.send_result()

        if not success:
            self._exit_status = 1

        return msg
