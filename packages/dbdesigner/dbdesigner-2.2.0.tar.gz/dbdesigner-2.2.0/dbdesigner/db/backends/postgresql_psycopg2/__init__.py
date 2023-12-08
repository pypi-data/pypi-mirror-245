import warnings

from dbdesigner.utils.deprecation import RemovedInDjango30Warning

warnings.warn(
    "The dbdesigner.db.backends.postgresql_psycopg2 module is deprecated in "
    "favor of dbdesigner.db.backends.postgresql.",
    RemovedInDjango30Warning, stacklevel=2
)
