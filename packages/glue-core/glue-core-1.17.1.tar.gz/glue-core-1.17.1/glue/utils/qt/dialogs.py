import warnings
from glue.utils.error import GlueDeprecationWarning
warnings.warn('Importing from glue.utils.qt.dialogs is deprecated, use glue_qt.utils.dialogs instead', GlueDeprecationWarning)
from glue_qt.utils.dialogs import *  # noqa
