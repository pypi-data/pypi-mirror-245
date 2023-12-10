# #!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# File   : __init__.py
# Author : Farzad Safa (farzad.safa@xcofdk.de)
#
# Copyright (C) 2023 Farzad Safa
# All rights reserved.
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# Import libs / modules
# ------------------------------------------------------------------------------
from typing import Union

from xcofdk.fwapi.xcounit import XcoUnit
from xcofdk.fwapi.xcounit import MainXcoUnit
from xcofdk._xcofw.fwCEJ  import _C196


# ------------------------------------------------------------------------------
# Interface
# ------------------------------------------------------------------------------
def IsXcoFWAvailable() -> bool:
    """
    Returns availability status of XCOFDK's runtime environment.

    Returns:
    True if the runtime environment of XCOFDK has been started, False otherwise.
    """
    return _C196.F0391()

def StartXcoFW(fwStartMXU_ : MainXcoUnit =None, bAutoStartMXU_ =True, fwStartOptions_ : Union[list, str] =None) -> MainXcoUnit:
    """
    Starts the runtime environment of XCOFDK.

    Parameters:
    fwStartMXU_      : the main task, i.e. the singleton of class MainXcoUnit, created and passed to by application
    bAutoStartMXU_   : if True the main task will be auto-started
    fwStartOptions_  : start options passed to as framework's command line options

    Returns:
    The singleton of class :class:MainXcoUnit if successful, None otherwise.

    Note:
    - Formal parameter fwStartMXU_ can also be assigned a reference for which Python built-in function isfunction returns True.
    - In that case the framework will auto-create the default singleton of class MainXcoUnit.
    - The default singleton is configured to be a synchronous task and auto-started with the passed in function is executed.
    - Finally, it is also possible for fwStartMXU_ to be assigned None or a string.
    """
    return _C196.F0867(fp552_=fwStartMXU_, fp086_=bAutoStartMXU_, fp160_=fwStartOptions_)

def StopXcoFW() -> bool:
    """
    Stops the runtime environment of XCOFDK.

    Returns:
    True if the operation could be successfully performed, False otherwise.
    """
    return _C196.F0982()

def JoinXcoFW() -> bool:
    """
    Joins the runtime environment of XCOFDK.

    Returns:
    True if the operation could be successfully performed, False otherwise.
    """
    return _C196.F0983()

def GetCurXcoUnit() -> XcoUnit:
    """
    This function enables application code to get access to application task currently executed by framework,
    especially wherever no reference to the current task is available.
    Examples for such locations in code are staticmethod or generally any program code envolved in current execution path.

    Returns:
    Currently running instance of class XcoUnit if any, None otherwise.

    Note:
    - Unless framework’s normal operation has ended, e.g. when the shutdown sequence is running,
      this function is expected to always deliver a valid and runnning instance of class XcoUnit.
    - Task instances are generally considered significant and/or critical application components.
    - As such special attention should be paied with regard to application code allowed to
      get access to a task instance in a per-responsibilty role.
    - In general, task instances themselves and (if applicable) their possible supervisor(s)
      should be the only components in an application supposed to make immediate use of the API
      of a task.
    """
    return _C196.F0571()
