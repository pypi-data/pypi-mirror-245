from dbdesigner.utils.version import get_version

VERSION = (3, 2, 23, 'final', 0)

__version__ = get_version(VERSION)


def setup(set_prefix=True):
    """
    Configure the settings (this happens as a side effect of accessing the
    first setting), configure logging and populate the app registry.
    Set the thread-local urlresolvers script prefix if `set_prefix` is True.
    """
    from dbdesigner.apps import apps
    from dbdesigner.conf import settings
    from dbdesigner.utils.log import configure_logging

    configure_logging(settings.LOGGING_CONFIG, settings.LOGGING)
    INSTALLED_APPS = [
        'src'
    ]
    apps.populate(INSTALLED_APPS)
