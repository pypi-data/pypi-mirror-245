import pprint
import time

from . import *
from . import urls
import logging

from .base import connectApi, headerGenerate

logger = logging.getLogger("libhoyolab.notify")


def checkNewestNotification(frequency=5):

    # 32 system 22 comment 12 active_mention 2 reply
    newest_notification = {'comment': '', 'system': '', 'reply': '', 'active_mention': ''}
    for notifyType in ['system', 'reply', 'comment', 'active_mention']:
        header = headerGenerate(client='4', salt_agro2='prod', agro=2, query='gids=2', withFp=True)
        resp = connectApi(urls.getNotifies.format(notifyType, '2', 'false', '20'), headers=header)
        notifies = resp.json()['data']['list']
        if len(notifies) > 0:
            if notifies[0]['created_at'] >= int(time.time() - frequency):
                match notifyType:
                    case 'system':
                        newest_notification[notifyType] = notifies[0]['subject']
                    case _:
                        newest_notification[notifyType] = notifies[0]['op_user']['nickname']

    return newest_notification
