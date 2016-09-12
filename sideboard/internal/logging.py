from __future__ import unicode_literals, absolute_import
import os
import logging.config

import logging_unterpolation

from sideboard.config import config


def _configure_logging():
    logging_unterpolation.patch_logging()
    fname='/etc/sideboard/logging.cfg'
    if os.path.exists(fname):
        logging.config.fileConfig(fname, disable_existing_loggers=True)
    else:
        # ConfigObj doesn't support interpolation escaping, so we manually work around it here
        formatters = config['formatters'].dict()
        for formatter in formatters.values():
            formatter['format'] = formatter['format'].replace('$$', '%')
            formatter['datefmt'] = formatter['datefmt'].replace('$$', '%') or None
        logging.config.dictConfig({
        'version': 1,
        'root': {
            'level': config['loggers']['root'],
            'handlers': config['handlers'].dict().keys()
        },
        'loggers': {
            name: {'level': level}
            for name, level in config['loggers'].items() if name != 'root'
        },
        'handlers': config['handlers'].dict(),
        'formatters': formatters
    })
