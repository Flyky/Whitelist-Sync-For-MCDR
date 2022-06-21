# -*- coding: utf-8 -*-

import os 
from mcdreforged.api.all import *
from whitelist_sync.config import Configuration
from whitelist_sync.online_text import ListForComparison
from whitelist_sync.util import get_whitelist

Prefix = '!!wls'
CONFIG_FILE = 'WhitelistSync.json'
config: Configuration
listc: ListForComparison


def print_help_message(source: CommandSource):
    msg = RTextList(
        RText('--------- Whitelist Sync §r---------\n'),
        RText('一个与在线文本文件同步白名单的MCDR插件\n'),
        RText('§a『命令说明』§r\n'),
        RText(Prefix, RColor.gray).c(RAction.suggest_command, Prefix).h('点击写入聊天栏'),RText(' | 显示帮助信息\n'),
        RText(f'{Prefix} update', RColor.gray).c(RAction.suggest_command, f'{Prefix} update').h('点击写入聊天栏'),RText(' | 立即更新一次白名单\n'),
        RText(f'{Prefix} ls', RColor.gray).c(RAction.suggest_command, f'{Prefix} ls').h('点击写入聊天栏'),RText(' | 显示当前白名单\n')
    )
    source.reply(msg)


def print_whitelist(source: CommandSource):
    source.reply(f'§e[WhitelistSync] 以下为当前白名单({len(listc.whitelist)}): \n{listc.whitelist}')


def pull_and_sync(source: CommandSource):
    global listc
    listc.update_onlinelist()
    sync(source)

@new_thread('whitelist_sync')
def sync(source: CommandSource):
    global listc
    update_result = listc.compare_lists()
    source.get_server().logger.info(update_result)
    if update_result:
        rml = update_result.get('remove', [])
        apl = update_result.get('append', [])
        for id in rml:
            source.get_server().execute(f'whitelist remove {id}')
        for id in apl:
            source.get_server().execute(f'whitelist add {id}')
        listc.set_whitelist(get_whitelist())
        source.reply('§e[WhitelistSync] 同步白名单')
    else:
        source.reply('§e[WhitelistSync] 白名单无更新')


def register_command(server: PluginServerInterface):
    '''
    !!wls   #display help_msg
    !!wls update  # update whitelist by now
    !!wls ls  # list whitelist
    '''
    def required_errmsg(src: CommandSource, id: int):
        if id == 1:
            src.reply('§c* 该命令仅供玩家使用')
        elif id == 2:
            src.reply('§c* 抱歉，您没有权限使用该命令')
    
    server.register_command(
        Literal(Prefix).runs(print_help_message).
        then(
            Literal('ls').requires(lambda src: src.has_permission_higher_than(0)).
            on_error(RequirementNotMet, lambda src: required_errmsg(src, 2)).
            runs(print_whitelist)
        ).
        then(
            Literal('update').requires(lambda src: src.has_permission_higher_than(1)).
            on_error(RequirementNotMet, lambda src: required_errmsg(src, 2)).
            runs(pull_and_sync)
        )
    )


def on_load(server: PluginServerInterface, old):
    global config, listc
    config = server.load_config_simple(CONFIG_FILE, target_class=Configuration)
    server.register_help_message(Prefix, {
        'en_us': 'sync whitelist with online text file',
        'zh_cn': '同步白名单文件'
    })
    register_command(server)

    if server.is_server_startup():
        whitelist = get_whitelist()
        listc = ListForComparison(config.text_src, whitelist)
        sync(server.get_plugin_command_source())
    

def on_server_startup(server: PluginServerInterface):
    global listc
    whitelist = get_whitelist()
    listc = ListForComparison(config.text_src, whitelist)
    sync(server.get_plugin_command_source())
