# -*- coding: utf-8 -*-

import requests
from typing import List, Set, Dict

class ListForComparison:
    online_src = -1
    onlinelist = -1
    whitelist = -1

    def __init__(self, online_src: List, whitelist: List):
        self.online_src = online_src
        self.whitelist = set(whitelist)
        self.update_onlinelist()

    def set_online_src(self, new_src: List):
        self.online_src = new_src

    def set_whitelist(self, wl: List):
        self.whitelist = set(wl)

    def update_onlinelist(self):
        raw_list = []
        for url in self.online_src:
            req = requests.get(url).text
            req = req.splitlines()
            raw_list.extend(req)
        
        # 去除'#'开头的文本和空格行
        self.onlinelist = set([id for id in raw_list if not id.startswith('#') and not id.isspace()])

    def compare_lists(self) -> Dict:
        result = {}
        if self.onlinelist == -1 or self.whitelist == -1:
            return {}
        result["remove"] = list(self.whitelist - self.onlinelist)
        result["append"] = list(self.onlinelist - self.whitelist)
        if len(result["remove"]) == 0 and len(result["append"]) == 0:
            return {}
        return result
