import warnings
from glue.utils.error import GlueDeprecationWarning
warnings.warn('Importing from glue.viewers.profile.qt is deprecated, use glue_qt.viewers.profile instead', GlueDeprecationWarning)
from glue_qt.viewers.profile import *  # noqa
