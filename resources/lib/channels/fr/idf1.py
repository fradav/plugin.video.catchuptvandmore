# -*- coding: utf-8 -*-
"""
    Catch-up TV & More
    Copyright (C) 2019  SylvainCecchetto

    This file is part of Catch-up TV & More.

    Catch-up TV & More is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    Catch-up TV & More is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along
    with Catch-up TV & More; if not, write to the Free Software Foundation,
    Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
"""

# The unicode_literals import only has
# an effect on Python 2.
# It makes string literals as unicode like in Python 3
from __future__ import unicode_literals

from codequick import Route, Resolver, Listitem, utils, Script

from resources.lib.labels import LABELS
from resources.lib import web_utils
from resources.lib.listitem_utils import item_post_treatment

import json
import re
import urlquick
'''
TODO Add Replay
'''

URL_ROOT = 'http://www.idf1.fr'

# LIVE :
URL_LIVE = URL_ROOT + '/live'
# Get Id
JSON_LIVE = 'https://json.dacast.com/b/%s/%s/%s'
# Id in 3 part
JSON_LIVE_TOKEN = 'https://services.dacast.com/token/i/b/%s/%s/%s'

# Id in 3 part


def live_entry(plugin, item_id, **kwargs):
    return get_live_url(plugin, item_id, item_id.upper())


@Resolver.register
def get_live_url(plugin, item_id, video_id, **kwargs):

    resp = urlquick.get(URL_LIVE, max_age=-1)
    list_id_values = re.compile(r'player.js\" id=\"(.*?)\"').findall(
        resp.text)[0].split('_')

    resp2 = urlquick.get(
        JSON_LIVE % (list_id_values[0], list_id_values[1], list_id_values[2]),
        max_age=-1)
    live_json_parser = json.loads(resp2.text)

    # json with token
    resp3 = urlquick.get(
        JSON_LIVE_TOKEN % (list_id_values[0], list_id_values[1],
                           list_id_values[2]),
        max_age=-1)
    token_json_parser = json.loads(resp3.text)

    return live_json_parser["hls"] + token_json_parser["token"]
