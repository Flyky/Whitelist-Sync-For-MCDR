# -*- coding: utf-8 -*-

import os 
from mcdreforged.api.all import *
from whitelist_sync.config import Configuration

Prefix = '!!wls'
CONFIG_FILE = 'WhitelistSync.json'
config: Configuration


def register_command(server: PluginServerInterface):
    pass


def on_load(server: PluginServerInterface, old):
    global config
    config = server.load_config_simple(CONFIG_FILE, target_class=Configuration)
    server.register_help_message(Prefix, {
        'en_us': 'sync whitelist with online text file',
        'zh_cn': '同步白名单文件'
    })
    register_command(server)
    