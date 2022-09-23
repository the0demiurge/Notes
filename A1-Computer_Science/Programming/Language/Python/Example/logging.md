# Logging

Configuration of logrotate with g-zip compression. These log files could be viewed by [lnav](../../../../../A3-Unix-Like/Tools/lnav.md) command.


```python
import gzip
import logging
import logging.config
import os
import threading
from logging.handlers import BaseRotatingHandler


def init_log_writer_orig(debug_level=None, log_path=None, show_info=False):
    logging_cfg: dict = {
        'version': 1,
        'disable_existing_loggers': True,
        'formatters': {
            'standard': {
                'format': '%(asctime)s:%(levelname)s:%(name)s:%(message)s'
            },
        },
        'handlers': {
            'errhandler': {
                'level': 'WARNING',
                'formatter': 'standard',
                'class': 'logging.StreamHandler',
                'stream': 'ext://sys.stderr',
            },
        },
        'loggers': {
            '': {
                'handlers': ['errhandler'],
                'level': 'DEBUG',
                'propagate': True,
                'formatter': 'standard',
            },
        }
    }
    if log_path:
        logging_cfg['handlers']['filehandler'] = {
            'level': 'DEBUG',
            'formatter': 'standard',
            'class': 'logging.FileHandler',
            'filename': log_path,
        }
        logging_cfg['loggers']['']['handlers'].append('filehandler')
    if show_info:
        logging_cfg['handlers']['infohandler'] = {
            'level': 'INFO',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
        }
        logging_cfg['loggers']['']['handlers'].append('infohandler')
    if debug_level in ['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'NOTSET', ]:
        logging_cfg['loggers']['']['level'] = debug_level

    logging.config.dictConfig(logging_cfg)
    logging.info(f'LOGGING_CFG: {logging_cfg}')


class CompressedRotationFileHandler(BaseRotatingHandler):
    def __init__(self, filename, mode='a', maxBytes=0, backupCount=0, encoding='utf-8'):
        if maxBytes > 0:
            mode = 'a'
        if not mode.endswith('t'):
            mode += 't'
        BaseRotatingHandler.__init__(self, filename, mode, encoding, delay=True)
        self.maxBytes = maxBytes
        self.backupCount = backupCount
        self.namer = lambda x: f"{x}.gz"
        self.basename = self.baseFilename

    def shouldRollover(self, record):
        self.baseFilename = '.'.join([self.basename, str(os.getpid()), str(threading.current_thread().native_id)])
        if self.stream is None:
            self.stream = self._open()
        if self.maxBytes > 0:
            msg = "%s\n" % self.format(record)
            if not os.path.exists(self.rotation_filename(self.baseFilename)):
                self.close()
                self._open()
                return 0
            if os.path.getsize(self.rotation_filename(self.baseFilename)) + len(msg) >= self.maxBytes:
                return 1
        return 0

    def doRollover(self):
        if self.stream:
            self.stream.close()
            self.stream = None
        if self.backupCount > 0:
            for i in range(self.backupCount - 1, 0, -1):
                sfn = self.rotation_filename("%s.%d" % (self.baseFilename, i))
                dfn = self.rotation_filename("%s.%d" % (self.baseFilename, i + 1))
                if os.path.exists(sfn):
                    if os.path.exists(dfn):
                        os.remove(dfn)
                    os.rename(sfn, dfn)
            dfn = self.rotation_filename(self.baseFilename + ".1")
            if os.path.exists(dfn):
                os.remove(dfn)
            self.rotate(self.rotation_filename(self.baseFilename), dfn)
        if not self.delay:
            self.stream = self._open()

    def _open(self):
        baseDir = os.path.dirname(self.rotation_filename(self.baseFilename))
        os.makedirs(baseDir, exist_ok=True)
        return gzip.open(self.rotation_filename(self.baseFilename), self.mode, encoding=self.encoding)


def init_log_writer(debug_level=None, log_path=None, log_size=15000):
    logging_cfg: dict = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '%(asctime)s:%(levelname)s:%(name)s:%(message)s'
            },
        },
        'handlers': {
            'errhandler': {
                'level': 'WARNING',
                'formatter': 'standard',
                'class': 'logging.StreamHandler',
                'stream': 'ext://sys.stderr',
            },
        },
        'loggers': {
            '': {
                'handlers': ['errhandler'],
                'level': 'DEBUG',
                'propagate': True
            },
        },
        'filters': {
            'main': {
                '()': logging.Filter,
                'name': 'main',
            }
        }
    }
    if log_path:
        logging_cfg['handlers']['filehandler'] = {
            'level': 'DEBUG',
            'formatter': 'standard',
            'class': 'main.utils.log_writer.CompressedRotationFileHandler',
            'maxBytes': int(log_size * 1024 * 1024),
            'backupCount': 2,
            'filename': log_path,
            'mode': 'a',
            'filters': ['main'],
        }
        logging_cfg['loggers']['']['handlers'].append('filehandler')
        os.makedirs(os.path.abspath(os.path.dirname(log_path)), exist_ok=True)
    if debug_level in ['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'NOTSET', ]:
        logging_cfg['loggers']['']['level'] = debug_level
    logging.config.dictConfig(logging_cfg)
    logging.getLogger(__name__).info('LOGGING_CONFIG: {}'.format(logging_cfg))

```
