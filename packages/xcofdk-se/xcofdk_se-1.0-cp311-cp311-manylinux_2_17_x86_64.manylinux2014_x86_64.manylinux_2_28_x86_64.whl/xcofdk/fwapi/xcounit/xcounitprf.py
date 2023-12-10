# #!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# File   : xcounitprf.py
# Author : Farzad Safa (farzad.safa@xcofdk.de)
#
# Copyright (C) 2023 Farzad Safa
# All rights reserved.
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# Import libs / modules
# ------------------------------------------------------------------------------
from xcofdk._xcofw.fwCFG import _C055


# ------------------------------------------------------------------------------
# Interface
# ------------------------------------------------------------------------------
class XcoUnitProfile(_C055):
    """
    This class represents an application task’s profile defined as a container of all properties which
    specify the runtime configuration of a task instance.
    """

    __slots__ = []

    def __init__(self):
        """
        Constructor of class XcoUnitProfile with respective default values of all properties of the instance to be created.

        Sample code snippet to print out default values:

        >>> from xcofdk.fwapi.xcounit import XcoUnitProfile
        >>> from xcofdk.fwapi.xcounit import xlogif
        >>>
        >>> #...
        >>> xuPrf = XcoUnitProfile()
        >>> xlogif.XLogInfo(f'xuPrf: {xuPrf}')
        >>>
        >>> # outuput will look like as shown below:
        >>> #  [11:13:29.075 XINF] xuPrf:  XcoUnit profile :
        >>> #        aliasName                      : None
        >>> #        isMainXcoUnit                  : False
        >>> #        isPrivilegedXcoUnit            : False
        >>> #        isSetupDisabled                : False
        >>> #        isTeardownDisabled             : False
        >>> #        isInternalQueueEnabled         : False
        >>> #        isExternalQueueEnabled         : False
        >>> #        isExternalQueueBlocking        : False
        >>> #        isSyncExecutionRequired        : False
        >>> #        cyclicRunPauseTimespanMS       : 100
        >>> #        cyclicMaxProcessingTimespanMS  : 50
        """
        _C055.__init__(self)

    def __str__(self):
        """
        Returns:
        The string representation of this instance, see also default values in c-tor.
        """
        return _C055.__str__(self)

    @staticmethod
    def GetDefaultCyclicRunPauseTimespanMS():
        """
        Returns:
        Default cyclic run pause timespan [ms].
        """
        return _C055._F0049()

    @staticmethod
    def GetDefaultCyclicMaxProcessingTimespanMS():
        """
        Returns:
        Default cyclic timespan [ms] assumed as maximum processing time.
        """
        return _C055._F0011()

    @property
    def isValid(self) -> bool:
        """
        Returns:
        Getter property to return True if the instance is considered valid and well-configured, False otherwise.
        """
        return self._p1568

    @property
    def isFrozen(self) -> bool:
        """
        Returns:
        Getter property to return True if the instance has been made read-only, False otherwise.

        Note:
        A frozen task profile will refuse to make any change to its current configuration via any of
        its setter properties.
        """
        return self._p1542

    @property
    def isMainXcoUnit(self) -> bool:
        """
        Returns:
        Getter property to return True if this profile’s associated task is the singleton of MainXcoUnit,
        False otherwise.
        """
        return self._p1065

    @property
    def isPrivilegedXcoUnit(self) -> bool:
        """
        Returns:
        Getter property to return True if this profile’s associated task is configured to be given special priveleges,
        False otherwise.
        """
        return self._p0492

    @isPrivilegedXcoUnit.setter
    def isPrivilegedXcoUnit(self, bPrivilegedXcoUnit_ : bool):
        """
        Setter property used to enable a task instance to be assigned special priveleges.

        Parameters:
        bPrivilegedXcoUnit_  : If True this profile’s associated task instance will be configured to be given special priveleges.
        """
        self._p0492 = bool(bPrivilegedXcoUnit_)

    # @property
    # def isAutoStartEnabled(self) -> bool:
    #     return self._isAutoStartEnabled
    #
    # @isAutoStartEnabled.setter
    # def isAutoStartEnabled(self, bAutoStart_ : bool):
    #     self._isAutoStartEnabled = bool(bAutoStart_)

    @property
    def isSetupDisabled(self) -> bool:
        """
        Returns:
        Getter property to return True if this profile’s associated task is configured to skip execution of Setup phase,
        False otherwise.
        """
        return self._p0842

    @isSetupDisabled.setter
    def isSetupDisabled(self, bSkipSetup_ : bool):
        """
        Setter property used to make a task instance is configured to skip Setup phase.

        Parameters:
        bSkipSetup_  : If True this profile’s associated task instance will be configured to skip execution of Setup phase.
        """
        self._p0842 = bool(bSkipSetup_)

    @property
    def isTeardownDisabled(self) -> bool:
        """
        Returns:
        Getter property to return True if this profile’s associated task is configured to skip execution of Teardown phase,
        False otherwise.
        """
        return self._p0560

    @isTeardownDisabled.setter
    def isTeardownDisabled(self, bSkipTeardown_ : bool):
        """
        Setter property used to make a task instance is configured to skip Teardown phase.

        Parameters:
        bSkipTeardown_  : If True this profile’s associated task instance will be configured to skip execution of
                          Teardown phase.
        """
        self._p0560 = bool(bSkipTeardown_)

    @property
    def isInternalQueueEnabled(self) -> bool:
        """
        Returns:
        Getter property to return True if this profile’s associated task is configured to have an internal queue,
        False otherwise.
        """
        return self._p0318

    @isInternalQueueEnabled.setter
    def isInternalQueueEnabled(self, bInternaQueue_ : bool):
        """
        Setter property used to make a task instance is configured to be assigned an internal queue when created.

        Parameters:
        bInternaQueue_  : If True this profile’s associated task instance will be configured to be assigned an
                          internal queue when created.
        """
        self._p0318 = bool(bInternaQueue_)

    @property
    def isExternalQueueEnabled(self) -> bool:
        """
        Returns:
        Getter property to return True if this profile’s associated task is configured to have an external queue,
        False otherwise.
        """
        return self._p0319

    @isExternalQueueEnabled.setter
    def isExternalQueueEnabled(self, bExternaQueue_ : bool):
        """
        Setter property used to make a task instance is configured to be assigned an external queue when created.

        Parameters:
        bExternaQueue_  : If True this profile’s associated task instance will be configured to be assigned an
                          external queue when created.
        """
        self._p0319 = bool(bExternaQueue_)

    @property
    def isExternalQueueBlocking(self) -> bool:
        """
        Returns:
        Getter property to return True if this profile’s associated task is configured to have a blocking external queue,
        False otherwise.
        """
        return self._p0276

    @isExternalQueueBlocking.setter
    def isExternalQueueBlocking(self, bBlockingExtQqueue_ : bool):
        """
        Setter property used to make a task instance is configured to be assigned a blocking external queue when created.

        Parameters:
        bBlockingExtQqueue_  : If True this profile’s associated task instance will be configured to be assigned a
                               blocking external queue when created.
        """
        self._p0276 = bool(bBlockingExtQqueue_)

    @property
    def isSyncExecutionRequired(self) -> bool:
        """
        Returns:
        Getter property to return True if this profile’s associated task is configured to be a synchronous task,
        False otherwise.
        """
        return self._p0277

    @isSyncExecutionRequired.setter
    def isSyncExecutionRequired(self, bSyncExecRequired_ : bool):
        """
        Setter property used to make a task instance is configured to be a synchronous one.

        Parameters:
        bSyncExecRequired_  : If True this profile’s associated task instance will be configured to be a synchronous task.
        """
        self._p0277 = bool(bSyncExecRequired_)

    @property
    def isSingleCycleRunPhase(self) -> bool:
        """
        Returns:
        Getter property to return True if cyclicRunPauseTimespanMS equals to 0, False otherwise.
        """
        return self._p0377

    @property
    def aliasName(self) -> str:
        """
        Returns:
        Getter property to return the alias name of this profile’s associated task.
        """
        return self._p1464

    @aliasName.setter
    def aliasName(self, aliasName_ : str):
        """
        Setter property used to specify the alias name used for this profile’s associated task.

        Parameters:
        aliasName_  : alias name to be used for this profile’s associated task.
        """
        self._p1464 = aliasName_

    @property
    def cyclicRunPauseTimespanMS(self) -> int:
        """
        Returns:
        Getter property to return the cyclic timespan [ms] of this profile’s associated task before next cycle
        (if any) of its Run phase, i.e. XcoUnit.RunXcoUnit(), is executed.
        """
        return self._p0223

    @cyclicRunPauseTimespanMS.setter
    def cyclicRunPauseTimespanMS(self, cyclicRunPauseTimespan_ : [int, float]):
        """
        Setter property used to specify the cyclic timespan [ms] of this profile’s associated task before next cycle
        (if any) of its Run phase, i.e. XcoUnit.RunXcoUnit(), is executed.

        Except for priviledged, synchronous task instances, the value passed to must be positive.
        For priviledged, synchronous task instances, however, 0 may also be specified making associated task’s Run phase
        a single-cycle loop. In other words, XcoUnit.RunXcoUnit() of that task will be executed only once.

        Parameters:
        cyclicRunPauseTimespan_  : value as the cyclic timespan [ms]. If specified as decimal point value [sec],
                                   it will be converted to an integer value [ms] accordingly.
        """
        self._p0223 = cyclicRunPauseTimespan_

    @property
    def cyclicMaxProcessingTimespanMS(self) -> int:
        """
        Returns:
        Getter property to return the accepted maximum processing timespan [ms] of this profile’s associated task whenever
        a single cycle of its Run phase, i.e. XcoUnit.RunXcoUnit(), is executed.

        Note:
        Unless the “strict timing” feature of the runtime environment is not enabled, this property is used to submit an appropriate
        warning message only whenever the expiration of the specified maximum timespan is detected by the framework.
        """
        return self._p0102

    @cyclicMaxProcessingTimespanMS.setter
    def cyclicMaxProcessingTimespanMS(self, cyclicMaxProcTimespan_ : [int, float]):
        """
        Setter property used to specify the accepted maximum processing timespan [ms] of this profile’s associated task whenever
        a single cycle of its Run phase, i.e. XcoUnit.RunXcoUnit(), is executed.

        Parameters:
        cyclicMaxProcTimespan_  : non-negative value as the accepted maximum processing timespan [ms]. If specified as decimal
                                  point value [sec], it will be converted to an integer value [ms] accordingly.
        """
        self._p0102 = cyclicMaxProcTimespan_

    def CloneProfile(self):
        """
        Creates copy instance of this task profile.

        Returns:
        A new instance of XcoUnitProfile with exactly same configuration as this instance except for the property isMainXcoUnit
        which always set to False.
        """
        return _C055._F1679(self)

    def _AssignProfile(self, rhs_):
        """
        Protected method designed for inernal purposes of this class.

        Returns:
        rhs_  : task profile whose configuration shall be copied to this instance except for the property isMainXcoUnit which
                remains unchanged.
        """
        return _C055._AssignProfile(self, rhs_)
#END class XcoUnitProfile
