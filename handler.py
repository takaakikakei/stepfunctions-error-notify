from time import sleep
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def time_out(event, context):
    try:
        # タイムアウトを意図的に引き起こす処理
        sleep(30)
        return True
    except Exception as e:
        logger.exception("time_out func {}".format(e))
        raise
