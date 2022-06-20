# -*- coding: utf-8 -*-

from typing import List
from mcdreforged.api.utils.serializer import Serializable

class Configuration(Serializable):
    text_src: List[str] = []
    schedule: Dict = {
        "method": "interval",  # interval or cron
        "value": 15  # interval(min)
    }

