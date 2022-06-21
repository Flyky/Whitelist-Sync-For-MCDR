# -*- coding: utf-8 -*-

from typing import List, Dict, Any
from mcdreforged.api.utils.serializer import Serializable

class Configuration(Serializable):
    text_src: List[str] = []
    schedule: Dict[str, Any] = {
        "method": "interval",  # interval or cron
        "value": 15  # interval(min)
    }

