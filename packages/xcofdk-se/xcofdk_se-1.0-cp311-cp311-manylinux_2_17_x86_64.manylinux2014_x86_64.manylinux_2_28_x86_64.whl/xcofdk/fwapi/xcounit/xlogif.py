# #!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# File   : xlogif.py
# Author : Farzad Safa (farzad.safa@xcofdk.de)
#
# Copyright (C) 2023 Farzad Safa
# All rights reserved.
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# Import libs / modules
# ------------------------------------------------------------------------------
from xcofdk._xcofw import fwCFI


# ------------------------------------------------------------------------------
# Interface - xcounit logging API
# ------------------------------------------------------------------------------
def XIsDieModeEnabled() -> bool:
    """
    Returns:
    True if application’s die-mode is enabled for the life cycle in hand, False otherwise.
    """
    return fwCFI._F0638()

def XIsExceptionModeEnabled():
    """
    Returns:
    True if application’s exception-mode is enabled for the life cycle in hand, False otherwise.
    """
    return fwCFI._F0278()

def XLogTrace(xlogMsg_ : str):
    """
    Puts out a trace message.

    Parameters:
    xlogMsg_  : trace message to be submitted
    """
    fwCFI._F1466(xlogMsg_)

def XLogDebug(xlogMsg_ : str):
    """
    Puts out a debug message.

    Parameters:
    xlogMsg_  : debug message to be submitted
    """
    fwCFI._F1467(xlogMsg_)

def XLogInfo(xlogMsg_ : str):
    """
    Puts out an info message.

    Parameters:
    xlogMsg_  : info message to be submitted
    """
    fwCFI._F1543(xlogMsg_)

def XLogWarning(xlogMsg_ : str):
    """
    Puts out a warning message.

    Parameters:
    xlogMsg_  : warning message to be submitted
    """
    fwCFI._F1248(xlogMsg_)

def XLogError(xlogMsg_ : str):
    """
    Submitts a user error message.

    Parameters:
    xlogMsg_  : user error message to be submitted
    """
    fwCFI._F1468(xlogMsg_)

def XLogErrorEC(xlogMsg_ : str, xlogErrorCode_ : int =None):
    """
    Submitts a user error message with a given error code.

    Parameters:
    xlogMsg_        : user error message to be submitted
    xlogErrorCode_  : error code of the user error message to be submitted
    """
    fwCFI._F1249(xlogMsg_, xlogErrorCode_)

def XLogFatal(xlogMsg_ : str):
    """
    Submitts a fatal error message.

    Parameters:
    xlogMsg_  : fatal error message to be submitted
    """
    fwCFI._F1469(xlogMsg_)

def XLogFatalEC(xlogMsg_ : str, xlogErrorCode_ : int =None):
    """
    Submitts a fatal error message with a given error code.

    Parameters:
    xlogMsg_        : fatal error message to be submitted
    xlogErrorCode_  : error code of the fatal error message to be submitted
    """
    fwCFI._F1250(xlogMsg_, xlogErrorCode_)


# ------------------------------------------------------------------------------
# Interface - xcounit current error API
# ------------------------------------------------------------------------------
def XIsErrorFree() -> bool:
    """
    Returns:
    True if no user/fatal error has been detected for currently running application task, False otherwise.
    """
    return fwCFI._F1163()

def XIsFatalErrorFree() -> bool:
    """
    Returns:
    True if no fatal error has been detected for currently running application task, False otherwise.
    """
    return fwCFI._F0639()

def XGetCurrentError():
    """
    Returns:
    if any the error instance of currently running application task, None otherwise.
    """
    return fwCFI._F0726()

def XClearCurrentError() -> bool:
    """
    If applicable it clears the error instance of currently running application task making it effectvely error free.

    Returns:
    True if clear operation could be performed successfully, False otherwise.
    """
    return fwCFI._F0561()

def XSetError(xsetMsg_ : str):
    """
    If applicable it sets/replaces the error instance of currently running application task by the user error passed to.

    Parameters:
    xsetMsg_  : user error message to be set

    Note:
    The operation will fail if there is some error already.
    """
    fwCFI._F1470(xsetMsg_)

def XSetErrorEC(xsetMsg_ : str, xsetErrorCode_ : int =None):
    """
    If applicable it sets/replaces the error instance of currently running application task by the user error passed to.

    Parameters:
    xsetMsg_        : user error message to be set
    xsetErrorCode_  : error code of the user error to be set

    Note:
    The operation will fail if there is some error already.
    """
    fwCFI._F1251(xsetMsg_, xsetErrorCode_)

def XSetFatalError(xsetMsg_ : str):
    """
    If applicable it sets/replaces the error instance of currently running application task by the fatal error passed to.

    Parameters:
    xsetMsg_  : fatal error message to be set

    Note:
    The operation will fail if there is some error already.
    """
    fwCFI._F0951(xsetMsg_)

def XSetFatalErrorEC(xsetMsg_ : str, xsetErrorCode_ : int =None):
    """
    If applicable it sets/replaces the error instance of currently running application task by the fatal error passed to.

    Parameters:
    xsetMsg_        : user error message to be set
    xsetErrorCode_  : error code of the fatal error to be set

    Note:
    The operation will fail if there is some error already.
    """
    fwCFI._F0727(xsetMsg_, xsetErrorCode_)
