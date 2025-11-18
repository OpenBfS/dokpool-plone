"""Local Behavior Support for Dokpool.

This package provides the core functionality for object-based (local) behaviors in Dokpool,
which is a key architectural feature that allows the same content type to have different
functionality based on assigned applications.

Key Components:
    - localbehavior.py: Core interfaces and adapters for local behavior support
    - adapter.py: Dynamic behavior enumeration based on assigned applications
    - patches.py: Monkey patches to integrate local behavior support into Plone forms
    - vocabulary.py: Vocabulary factory for available application choices

How Local Behaviors Work:
    Unlike standard Plone where behaviors are assigned to content types, Dokpool allows
    behaviors to be assigned to individual content objects. This enables:

    - DPDocuments to have different fields based on assigned applications (ELAN, REI, etc.)
    - Dynamic form rendering that only shows relevant fields
    - Object-specific functionality without creating multiple content types

    For example, a DPDocument assigned to the 'elan' application will have ELAN-specific
    fields and behaviors, while the same content type assigned to 'rei' will have
    REI-specific functionality.

Integration:
    This package automatically patches Plone's form system during import to enable
    local behavior support throughout the system.
"""

from docpool.base.localbehavior import patches  # noqa: F401
