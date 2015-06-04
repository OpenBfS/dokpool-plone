# -*- coding: utf-8 -*-

class ReadOnlyException(Exception):
    """Raised when a field or extension that has been set read-only is
    illegally set."""
