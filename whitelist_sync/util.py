# -*- coding: utf-8 -*-

from mcdreforged.plugin.server_interface import PluginServerInterface
from mcdreforged.api.rtext import *
from typing import List


def parse_whitelist_str(raw: str) -> List:
    '''
    vanilla: 'There are 3 whitelisted players: a1, q2, e3'
    '''
    splitraw = raw.split(': ')
    return splitraw[1].split(', ') if len(splitraw) == 2 else []


def get_whitelist():
    server_inst = PluginServerInterface.get_instance()
    command = 'whitelist list'
    wl_str = ''
    if server_inst.is_rcon_running():
        wl_str = server_inst.rcon_query(command)
    else:
        pass
    return parse_whitelist_str(wl_str)

def msg_of_update_detail(_dict: Dict):
    if not _dict:
        return ''
    if _dict.get('remove', None):
        _remove = RText(f'移除id: {_dict["remove"]}\n')
    if _dict.get('append', None):
        _append = RText(f'新增id: {_dict["append"]}')
    return RTextList(
        _remove, _append
    )