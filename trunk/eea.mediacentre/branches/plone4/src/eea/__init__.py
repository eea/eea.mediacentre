""" Declare this a namespace package if pkg_resources is available.
"""
try:
    import pkg_resources
    pkg_resources.declare_namespace('eea')
except ImportError:
    pass
