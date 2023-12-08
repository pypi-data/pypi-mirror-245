# -*- coding: utf-8 -*-
from src.utils import HOST


class RedPacketConfig(object):
    def __init__(self, red_packet_switch=True, heartbeat=True, smart_mode=True, threshold=0.5, adventure_mode=True,
                 timeout=7, rate=3, rps_limit=100):
        self.red_packet_switch = red_packet_switch
        self.heartbeat = heartbeat
        self.smart_mode = smart_mode
        self.threshold = threshold
        self.adventure_mode = adventure_mode
        self.timeout = timeout
        self.rate = rate
        self.rps_limit = rps_limit


class AuthConfig(object):
    def __init__(self, username='', password='', mfa_code='', key=''):
        self.username = username
        self.password = password
        self.mfa_code = mfa_code
        self.key = key
        self.accounts: list[tuple[str, ...]] = []

    def add_account(self, username='', password=''):
        self.accounts.append((username, password))


class ChatConfig(object):
    def __init__(self, blacklist=[], kw_blacklist=['你点的歌来了'], repeat_mode_switch=False, frequency=5, soliloquize_switch=False,
                 soliloquize_frequency=20, sentences=[], answer_mode: bool = False, fish_ball: str = '凌 捞鱼丸',
                 chat_user_color: str | None = None, chat_content_color: str | None = None):
        self.repeat_mode_switch = repeat_mode_switch
        self.frequency = frequency
        self.soliloquize_switch = soliloquize_switch
        self.soliloquize_frequency = soliloquize_frequency
        self.sentences = ['你们好！', '牵着我的手，闭着眼睛走你也不会迷路。',
                          '吃饭了没有?', '💗 爱你哟！'] + sentences
        self.blacklist = blacklist
        self.kw_blacklist = kw_blacklist
        self.answer_mode = answer_mode
        self.fish_ball = fish_ball
        self.chat_user_color = chat_user_color
        self.chat_content_color = chat_content_color


class Config(object):
    def __init__(self, auth: AuthConfig = None, redpacket: RedPacketConfig = None, chat: ChatConfig = None, cfg_path: str = None, host: str = 'https://fishpi.cn'):
        self.auth_config = auth
        self.redpacket_config = redpacket
        self.chat_config = chat
        self.cfg_path = cfg_path
        self.host = host


class CliOptions(object):
    def __init__(self, username: str = '', password: str = '', code: str = '', file_path: str = None, host: str = None):
        self.username = username
        self.password = password
        self.code = code
        self.file_path = file_path
        self.host = host


def init_defualt_config() -> Config:
    return Config(AuthConfig(), RedPacketConfig(), ChatConfig(), None, HOST)


GLOBAL_CONFIG = Config()
