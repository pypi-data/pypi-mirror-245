from ..core import _core  # need to pull in dependent base-types
from ._ui import shyft_with_stm

if shyft_with_stm:
    from ._ui import qt_version as UiQtVersion, export as _ui_export, ItemDataProperty, LayoutInfo, LayoutClient, LayoutServer  # from ._ui import *

from shyft.energy_market.core import ModelInfo
import json
from shiboken2 import getCppPointer as _getCppPointer
from PySide2 import __version__ as PySideVersion
from PySide2.QtCore import __version__ as PySideQtVersion, qVersion as _get_pyside_qt_runtime_version
from PySide2.QtWidgets import QWidget

__doc__ = _ui.__doc__
__version__ = _ui.__version__

QtVersion = _get_pyside_qt_runtime_version()


def print_versions():
    print(f"Shyft ui python module version {__version__} built with Qt version {UiQtVersion}")  # Shyft version and Qt version used to compile _ui.pyd
    print(f"PySide2 version {PySideVersion} built with Qt version {PySideQtVersion}")  # PySide2 version and Qt version used to compile PySide2
    print(f"Qt version {QtVersion}")  # Qt version of runtime libraries currently used


def export(window: QWidget) -> str:
    """
    Export the window/QWidget layout to a json suitable for the front end framework.
    Note that the routine harvest the essential properties recursively starting at the top level.
    Ref. to the shyft/python/test_suites/energy_market/ui directory for examples.

    Parameters
    ----------
    window: QWidget
       A QWidget containing the layout and components to be converted to a json string

    Returns
    -------
       A json formatted string that contains the essential information harvested from the QWidget
    """
    ptr = _getCppPointer(window)
    return _ui_export(ptr[0])


def export_print(window: QWidget, pretty: bool = False, indent: int = 2):
    """
    Same as `export`, but using json loads and dumps to provide a pretty readable version.


    Parameters
    ----------
    window: QWidget
       A QWidget containing the layout and components to be converted to a json string
    pretty: bool
       If true then pretty format
    indent: int
       The indent used to format th json

    Returns
    -------
       A json pretty formatted string that contains the essential information harvested from the QWidget
    """
    cfg = export(window)
    if pretty:
        print(json.dumps(json.loads(cfg), indent=indent))
    else:
        print(cfg)


__all__ = [
    'print_versions', 'QtVersion', 'PySideVersion', 'PySideQtVersion', 'UiQtVersion',
    'export', 'export_print', 'ItemDataProperty',
    'LayoutInfo', 'LayoutServer', 'LayoutClient', 'shyft_with_stm'
]
