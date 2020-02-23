__all__ = ['TG', 'QQ', 'WECHAT']

from ..constant import TIMEOUT_SECOND


class Inform(object):
    """
    处理通知
    """
    def __init__(self, msg, conf, session, logger, success):
        self._msg = msg
        self._conf = conf
        self._sess = session
        self.logger = logger
        self._success = success

    def send_result(self):
        pass


class TG(Inform):
    def __init__(self, msg, conf, session, logger, success):
        super().__init__(msg, conf, session, logger, success)

    def send_result(self):
        # 如果用户指定了 Telegram 相关信息，就把消息通过 Telegram 发送给用户
        self.logger.info('将运行结果通过 Telegram 机器人发送。')
        try:
            tg_res_raw = self._sess.post(
                f'https://api.telegram.org/bot{self._conf["TG_BOT_TOKEN"]}/sendMessage',
                json={
                    'chat_id': self._conf['TG_CHAT_ID'],
                    'text': self._msg,
                    'parse_mode': 'HTML',
                },
                timeout=TIMEOUT_SECOND
            )

            tg_res = tg_res_raw.json()
            if 'ok' not in tg_res:
                raise ValueError('Telegram API 的返回值很奇怪。')
            if not tg_res['ok']:
                raise ValueError(f'Telegram API 调用失败，可能您的 Token 或 chat id 配置有误。'
                                 f'API 的返回是：\n{tg_res}')

        except:
            # 将 Telegram 机器人的错误也打印下来
            self.logger.error('调用 Telegram API 时发生错误。', exc_info=True)
            self._success = False

        return self._success


class QQ(Inform):
    def __init__(self, msg, conf, session, logger, success):
        super().__init__(msg, conf, session, logger, success)

    def send_result(self):
        self.logger.info('将运行结果通过 QQ 机器人发送。')
        try:
            qq_res_raw = self._sess.get(
                (f'http://{self._conf["QQ_BOT_HOST"]}/' +
                 f'send_private_msg?' +
                 f'access_token={self._conf["QQ_BOT_TOKEN"]}&' +
                 f'user_id={self._conf["QQ_ID"]}' +
                 f'&message={self._msg}'),
                timeout=TIMEOUT_SECOND
            )

            qq_res = qq_res_raw.json()
            if 'status' not in qq_res:
                raise ValueError('QQ bot API 的返回值很奇怪。')
            if qq_res_raw.status_code == 403:
                raise ValueError('QQ bot API 调用失败，您的 Token 可能配置有误。')
            if qq_res['status'] != 'ok':
                raise ValueError(f'QQ bot API 调用失败，可能您的 Token 或 qq id 配置有误。'
                                 f'API 的返回是：\n{qq_res}')

        except :
            # 将 Telegram 机器人的错误也打印下来
            self.logger.error('调用 QQ bot API 时发生错误。', exc_info=True)
            self._success = False

        return self._success


class WECHAT(Inform):
    def __init__(self, msg, conf, session, logger, success):
        super().__init__(msg, conf, session, logger, success)

    def send_result(self):
        self.logger.info('将运行结果通过 ServerChan 发送到微信。')
        try:
            sc_res_raw = self._sess.post(
                (f'https://sc.ftqq.com/' +
                 f'{self._conf["SC_KEY"]}.send?' +
                 f'text=疫情防控通填报结果&' +
                 f'desp={self._msg}'),
                timeout=TIMEOUT_SECOND
            )

            sc_res = sc_res_raw.json()
            if 'errmsg' not in sc_res:
                raise ValueError('ServerChan API 的返回值很奇怪。')
            if sc_res['errmsg'] != 'success':
                raise ValueError(f'ServerChan API 调用失败，可能您的 Token 配置有误。'
                                 f'API 的返回是：\n{sc_res}')

        except:
            # 将 Telegram 机器人的错误也打印下来
            self.logger.error('调用 ServerChan API 时发生错误。', exc_info=True)
            self._success = False

        return self._success
