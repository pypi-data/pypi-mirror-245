# #!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# File   : xcounit.py
# Author : Farzad Safa (farzad.safa@xcofdk.de)
#
# Copyright (C) 2023 Farzad Safa
# All rights reserved.
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# Import libs / modules
# ------------------------------------------------------------------------------
from xcofdk._xcofw.fwCEM import _C180

from xcofdk.fwapi.xcounit import xlogif
from xcofdk.fwapi.xcounit import XcoUnitError
from xcofdk.fwapi.xcounit import XcoUnitProfile


# ------------------------------------------------------------------------------
# Interface
# ------------------------------------------------------------------------------
class XcoUnit(_C180):
    """"
    Instances of this class represent application tasks to be executed by the framework.
    """

    __slots__ = []

    def __init__(self, xcounitPrf_ : XcoUnitProfile =None):
        """
        Constructor of class XcoUnit.

        Parameters:
        xcounitPrf_  : a valid task profile to be associated to this instance.
                       If the value passed to resolves to None, then a new task profile will be created and used instead.
                       Otherwise, passed to profile will be cloned and used.
        """
        _C180.__init__(self, xcounitPrf_)

    def __str__(self):
        """
        Returns:
        The string representation of this instance.
        """
        return _C180.__str__(self)

    # ------------------------------------------------------------------------------
    # API
    # ------------------------------------------------------------------------------
    @property
    def isAttachedToFW(self) -> bool:
        """
        Returns:
        Getter property to return True if this instance is currently attached to the framework, False otherwise.
        """
        return self._p0846

    @property
    def isDetachedFromFW(self) -> bool:
        """
        Returns:
        Getter property to return True if this instance is already dettached from the framework, False otherwise.
        """
        return not self._p0846

    @property
    def isStarted(self) -> bool:
        """
        Returns:
        Getter property to return True if this instance has been started, False otherwise.
        """
        return self._p1362

    @property
    def isRunning(self) -> bool:
        """
        Returns:
        Getter property to return True if this instance is currently running, False otherwise.
        """
        return self._p1363

    @property
    def isDone(self) -> bool:
        """
        Returns:
        Getter property to return True if this instance has finished its execution, False otherwise.
        """
        return self._p1618

    @property
    def isFailed(self) -> bool:
        """
        Returns:
        Getter property to return True if the execution of this instance has been aborted, False otherwise.
        """
        return self._p1474

    @property
    def isTerminated(self) -> bool:
        """
        Returns:
        Getter property to return True if either isDone or isFailed is True, False otherwise.
        """
        return self.isDone or self.isFailed

    @property
    def isTerminating(self) -> bool:
        """
        Returns:
        Getter property to return True if current transitional state (if any) of this instance will end up with
        isTerminated resolves to True, False otherwise.
        """
        return self.isStopping or self.isAborting

    @property
    def isStopping(self) -> bool:
        """
        Returns:
        Getter property to return True if current transitional state (if any) of this instance will end up with
        isDone resolves to True, False otherwise.
        """
        return self._p1254

    @property
    def isAborting(self) -> bool:
        """
        Returns:
        Getter property to return True if current transitional state (if any) of this instance will end up with
        isFailed resolves to True, False otherwise.
        """
        return self._p1255

    @property
    def isErrorFree(self) -> bool:
        """
        Returns:
        Getter property to return True if no error has been detected which was caused by this instance,
        False otherwise.
        """
        return self.currentError is None

    @property
    def isFatalErrorFree(self) -> bool:
        """
        Returns:
        Getter property to return True if no fatal error has been detected which was caused by this instance,
        False otherwise.
        """
        curErr = self.currentError
        return (curErr is None) or not curErr.isFatalError

    @property
    def xcounitUniqueID(self) -> int:
        """
        Returns:
        Getter property to return the unique ID of this instance.
        """
        return self._p0493

    @property
    def xcounitName(self) -> str:
        """
        Returns:
        Getter property to return the unique name of this instance.
        """
        return self._p0847

    @property
    def xcounitAliasName(self) -> str:
        """
        Returns:
        Getter property to return the alias name of this instance.
        """
        return self._p0722

    @property
    def currentError(self) -> XcoUnitError:
        """
        Returns:
        Getter property to return current error of this instance if any, None otherwise.
        """
        return self._p1158

    @property
    def xcounitProfile(self) -> XcoUnitProfile:
        """
        Returns:
        Getter property to return task profile associated with this instance.
        """
        return self._p0947

    def Start(self) -> bool:
        """
        Request to start this task.

        Returns:
        True if the operation could be performed successfully, False otherwise.
        """
        return _C180._A1300(self)

    def Stop(self) -> bool:
        """
        Request to stop this task.

        Returns:
        True if the operation could be performed successfully, False otherwise.
        """
        return _C180._A1314(self, True)

    def Join(self, maxWaitTime_: [int, float] =None) -> bool:
        """
        Request to join this task with the call blocks until the operation is accomplished.

        Parameters:
        maxWaitTime_  : if not None, maximum wait time (in milliseconds for int values or in seconds for float values)
                        before the operation returns.

        Returns:
        True if the operation could be performed successfully, False otherwise.
        """
        return _C180._A1315(self, maxWaitTime_)

    def DetachFromFW(self):
        """
        Request to detach this task from the framework with it will be stopped (if applicable) thru a call to Stop().
        """
        _C180._F1159(self)

    def ClearCurrentError(self) -> bool:
        """
        Request to clear current error (if any) of this instance.

        Returns:
        True if the operation could be performed successfully, False otherwise.
        """
        return _C180._F0636(self)


    # --------------------------------------------------------------------------
    # API to be overridden by sub-classes
    # --------------------------------------------------------------------------
    def SetUpXcoUnit(self) -> bool:
        """
        Setup phase of this instance (if configured so) executed by the framework when successfully started,
        thus isRunning must resolve to True.

        Returns:
        - True if the execution is considered to be continued, i.e. RunXcoUnit() is supposed to be executed afterward,
          False or None otherwise.
        - If False this task is then considered stopped (or finished).
        - If None this task is then considered aborted (or failed). If so and if possible, then a life cycle failure will
          be submitted accordingly by the framework.

        Note:
        - For a return value other than True isRunning will resolve to False.
        - For return value False either one of isStopping or isDone will resolve to True.
        - For return value None either one of isAborting or isFailed will resolve to True.
        """
        xlogif.XLogWarning('Default impl of the setup phase, nothig to do.')
        return True

    def RunXcoUnit(self) -> bool:
        """
        Cyclic run phase of this instance executed by the framework when successfully started or after successful execution
        of its setup phase, thus isRunning must resolve to True.

        Returns:
        - True if the execution is considered to be continued by the next cycle (if any), False or None otherwise.
        - If False this task is then considered stopped (or finished), TearDownXcoUnit() (if configured) will be
          executed subsequently.
        - If None this task is then considered aborted (or failed). If so and if possible, then a life cycle failure will
          be submitted accordingly by the framework.

        Note:
        - For a return value other than True isRunning will resolve to False.
        - For return value False either one of isStopping or isDone will resolve to True.
        - For return value None either one of isAborting or isFailed will resolve to True.
        """
        xlogif.XLogWarning('Default impl of the run phase, nothig to do.')
        return False

    def TearDownXcoUnit(self) -> bool:
        """
        Teardown phase of this instance (if configured so) executed by the framework when stopped (or finished), thus either
        one of isDone or isStopping must resolve to True.

        Returns:
        - None if the execution is considered aborted (or failed). If so and if possible, then a life cycle failure will
          be submitted accordingly by the framework.
        - True or False otherwise.

        Note:
        - For a return value other than None isDone will resolve to True.
        - For return value None isFailed will resolve to True.
        """
        xlogif.XLogWarning('Default impl of the tear down phase, nothig to do.')
        return False
#END class XcoUnit
