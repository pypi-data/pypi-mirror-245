# #!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# File   : mainxcounit.py
# Author : Farzad Safa (farzad.safa@xcofdk.de)
#
# Copyright (C) 2023 Farzad Safa
# All rights reserved.
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# Import libs / modules
# ------------------------------------------------------------------------------
from xcofdk.fwapi.xcounit import XcoUnitProfile
from xcofdk.fwapi.xcounit import XcoUnit

from xcofdk._xcofw.fwCEM import _C180
from xcofdk._xcofw.fwCFH import _C068
from xcofdk._xcofw.fwCFG import _C055


# ------------------------------------------------------------------------------
# Interface
# ------------------------------------------------------------------------------
#TODO: DESIGN_DOC -  Defaults of MainXcoUnit's profile  !!
class MainXcoUnit(XcoUnit):
    """
    This class is inherited from class XcoUnit. Its application-wide single instance, i.e. its singleton,
    represents the main task of the application.
    """

    __slots__ = []

    def __init__(self, xcounitPrf_ : XcoUnitProfile =None):
        """
        Constructor of class MainXcoUnit.

        Parameters:
        xcounitPrf_  : a valid task profile to be associated to this instance.
                       If the value passed to resolves to None, then a new task profile will be created and used instead.
                       Otherwise, passed to profile will be cloned and used.
        """
        _xup = xcounitPrf_
        if isinstance(_xup, _C068):
            if _xup.isValid and not _xup.isMainXcoUnit:
                _C055._F0950(_xup, True)
        else:
            _xup = _C068(xcounitPrf_, True)

        if _xup.isValid:
            if xcounitPrf_ is None:
                _xup.isSyncExecutionRequired = False
        XcoUnit.__init__(self, _xup)

    @staticmethod
    def GetMainXcoUnitSingleton():
        """
        Returns:
        The singleton of this class if created already, None otherwise.
        """
        return _C180._F0948()
#END class MainXcoUnit
