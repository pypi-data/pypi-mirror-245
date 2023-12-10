# #!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# File   : xcouniterr.py
# Author : Farzad Safa (farzad.safa@xcofdk.de)
#
# Copyright (C) 2023 Farzad Safa
# All rights reserved.
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# Import libs / modules
# ------------------------------------------------------------------------------
from xcofdk._xcofw.fwCEP import _C090
from xcofdk._xcofw.fwDEI import _C028


# ------------------------------------------------------------------------------
# Interface
# ------------------------------------------------------------------------------
class XcoUnitError:
    """
    Instances of this class represent current error of a task, i.e. an instance of class XcoUnit.
    """
    __slots__ = ['__xue']

    def __init__(self, xcounitErr_ : _C090):
        """
        Constructor of this class.
        """
        self.__xue = xcounitErr_

    def __str__(self):
        """
        Returns:
        The string representation of this instance.
        """
        return _C090.__str__(self.__xue)

    @property
    def isFatalError(self) -> bool:
        """
        Returns:
        Getter property to return True if this instance is a fatal error, False otherwise.
        """
        return self.__xue._p1161

    @property
    def isDieError(self) -> bool:
        """
        Returns:
        Getter property to return True if this instance is a fatal error with application’s die-mode of
        error handling subsystem is enabled too, False otherwise.
        """
        return self.__xue._p1357

    @property
    def uniqueID(self) -> int:
        """
        Returns:
        Getter property to return the unique ID of this instance.
        """
        return self.__xue._p1492

    @property
    def message(self) -> str:
        """
        Returns:
        Getter property to return the message of this instance.
        """
        return self.__xue._p1609

    @property
    def errorCode(self) -> int:
        """
        Returns:
        Getter property to return the error code of this instance if any, None otherwise.
        """
        return self.__xue._p1458
#END class XcoUnitError


class XcoUnitException(_C028):
    """
    Instances of this class represent exceptions raised to inform currently running task, i.e. an instance of
    class XcoUnit.RunXcoUnit(), about a failure, i.e. fatal error, via exception handling mechanism of the host
    system (if available and enabled).
    """

    def __init__(self, xcounitXcp_ : _C028):
        """
        Constructor of this class.
        """
        _C028.__init__(self, fp619_=xcounitXcp_)

    def __str__(self):
        """
        Returns:
        The string representation of this instance.
        """
        return _C028.__str__(self)

    @property
    def isDieException(self):
        """
        Returns:

        Getter property to return True if this exception is raised while application’s die-mode of error handling subsystem
        is enabled too, False otherwise.
        """
        return self._p0946

    @property
    def uniqueID(self) -> int:
        """
        Returns:
        Getter property to return the unique ID of this instance.
        """
        return self._p1492

    @property
    def message(self) -> str:
        """
        Returns:
        Getter property to return the message of this instance.
        """
        return self._p1609

    @property
    def errorCode(self) -> int:
        """
        Returns:
        Getter property to return the error code of this instance if any, None otherwise.
        """
        return self._p1458

    @property
    def callstack(self) -> str:
        """
        Returns:
        Getter property to return the callstack of this instance if any, None otherwise.
        """
        return self._p1430

    @property
    def traceback(self) -> str:
        """
        Returns:
        Getter property to return the traceback of this instance if any, None otherwise.
        """
        return self._p1456
#END class XcoUnitException
