from fincookie.api import set_dev, get_cookies, get_logs, get_loads, cookie_format, headers_format, proxy_format
from importlib.metadata import version as __version__
from fincookie.api import __latest_version__

__version__ = __version__(__name__)
if sum([int(v) * 100 ** i for i, v in enumerate(__version__.split('.')[::-1])]) < sum([int(v) * 100 ** i for i, v in enumerate(__latest_version__.split('.')[::-1])]):
    print(f'Warning: Your fincookie version is outdated. Please upgrade to {__latest_version__}')
