#!python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# File   : run_xcogen.py
# Author : Farzad Safa (farzad.safa@xcofdk.de)
#
# Copyright (C) 2023 Farzad Safa
# All rights reserved.
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# Import libs / modules
# ------------------------------------------------------------------------------
#TODO: IMPL_DOC  -  'run_xcogen.py': output redirecting is not working this way  !!
#  from xcofdk._xcofw.fwadmin.fwadmindefs import _FwAdapterConfig
#  if _FwAdapterConfig._IsRunXcoGenRedirectionEnabled():
#     _FwAdapterConfig._RedirectPyLogging()

from xcofdk._xcofwa.fwFHK import _C108

if not _C108._F0171():
    _C108._F0640()

from xcofdk._xcofw.fwDGI import _C160


# ------------------------------------------------------------------------------
# Interface
# ------------------------------------------------------------------------------
def RunXCoGen():
    return _C160._F1063()


# ------------------------------------------------------------------------------
# Execution
# ------------------------------------------------------------------------------
if __name__ == '__main__':
    RunXCoGen()
