# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots['test_parse_form[parse_form/form1.html] 1'] = {
    'password': '',
    'remember': '1',
    'username': ''
}

snapshots['test_parse_form[parse_form/form2.html] 1'] = {
    'comments': '',
    'email': '',
    'name': '',
    'radio_input': '2',
    'redirect': 'http://www.opera.com',
    'select_field': 'a1',
    'select_multiple': [
        'b',
        'c'
    ]
}
