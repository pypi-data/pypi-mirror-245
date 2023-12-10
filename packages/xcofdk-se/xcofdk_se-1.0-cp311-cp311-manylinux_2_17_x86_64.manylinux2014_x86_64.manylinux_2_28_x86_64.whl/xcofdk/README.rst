Project Description
===================

**XCOFDK** is an e\ **X**\ tensible, **C**\ ustomizable and **O**\ bject-oriented **F**\ ramework **D**\ evelopment **K**\ it with the primary
purpose of providing: 

- complete, reliable *life cycle management*, 
- ready-to-use runtime environment for *multithreading*.

XCOFDK is designed by the concept of *high-level abstraction* and implemented to enable rapid development of reliable (embedded) applications  
by providing a software framework composed of *building blocks called* subsystems. Subsystems are defined and designed by focusing on their 
associated, high-level functionality and responsibility represented thru their respective API (*Application Programming Interface*).

Key characteristics of the design of XCOFDK are:

- completely object-oriented,  
- inspired by the design principle KISS, 
- general-purpose composition in terms of a software framework, 
- applicable for multiple programming languages, e.g. Python, C++, Java, 
- applicable for multiple operating systems, e.g Linux, Windows, macOS, 
- highly configurable, thus customizable and extensible,  
- composed of a collection of well-defined subsystems, 
- provides a runtime environment as its major service for execution of tasks, 
- thus enabling multithreading by a clear, manageable API to start/stop/abort tasks, 
- enabling development of event (or message) driven applications,
- support for (aliveness) monitoring of tasks, 
- support for transparant communication subsystem(s), 
- support for full life cycle management, 
- support for well-defined, coordinated shutdown sequence, 
- support for tracking, handling and report of detected failures. 


Installation
=============

`XCOFDK Starter Edition (SE) <https://www.xcofdk.de/install/index.html#xcofdk-starter-edition>`_ is available as the *free-of-charge* 
version of `XCOFDK <https://www.xcofdk.de/>`_ for **Python 3.11, Linux**.

.. note::
  By installing you agree to the terms and conditions of use of the software (see section **Licensing** below).

Install using `pip <https://pypi.org/project/pip/>`_:

.. code-block:: bash

    $> python3.11 -m pip install xcofdk-se


Quick Start
===========

Example below illustrates most simple way to start `XCOFDK <https://www.xcofdk.de/>`_ in Python: 

.. code-block::

   # file: defaultmxu.py

   from xcofdk import fwapi


   def RunQuickStart() -> bool:
       print('Welcome to quick start of XCOFDK.')

       # indicate that main task is finished / stopped by returning 'False'
       return False


   def Main() -> int:
       mxu = fwapi.StartXcoFW(fwStartMXU_=RunQuickStart, bAutoStartMXU_=True)
       res = mxu is not None
       if res:
           res = fwapi.StopXcoFW()
       if not fwapi.JoinXcoFW():
           res = False
       return 0 if res else 1


   if __name__ == "__main__":
       exit(Main())

When executed the output of the program should like this:

.. code-block:: bash

    $> python3.11 -m defaultmxu 
    --------------------------------------------------------------------------------
    -----
    ----- XCOFDK Starter Edition (SE)  -  v1.0
    -----
    ----- NOTE:
    ----- This version of XCOFDK is subject to pre-build limitations with regard
    ----- to both configuration and runtime features.
    --------------------------------------------------------------------------------
    [15:43:06.062 XWNG] No MainXcoUnit instance passed to, will create a default one serving as main xcounit.
    [15:43:06.146 KPI] Done initial (resource) loading: 0.273
    [15:43:06.147 KPI] Framework is up and running: 0.081
    [15:43:06.147 INF] Started framework.
    [15:43:06.149 INF] Starting main xcounit defaultMainXU...
    Welcome to quick start of XCOFDK.
    [15:43:06.154 INF][XTd_501001] Execution of main xcounit defaultMainXU done after successful start.
    [15:43:06.155 INF][XTd_501001] Got request to stop framework.
    [15:43:06.155 KPI][XTd_501001] Starting coordinated shutdown...
    [15:43:06.155 INF][XTd_501001] Got request to join framework.
    [15:43:06.156 INF][XTd_501001] Waiting for framework to complete shutdown sequence...
    [15:43:06.222 KPI] Finished coordinated shutdown.
    [15:43:06.255 KPI] Framework active tracking duration: 0.163
    --------------------------------------------------------------------------------
    Fatals(0), Errors(0), Warnings(0), Infos(6)
    Total processing time: 0.472
    --------------------------------------------------------------------------------
    
    
    --------------------------------------------------------------------------------
    ----- Resulted LC status : SUCCESS
    -----  LcState[0x3500] : LcStopped , TMgrStopped , FwMainStopped , MainXcoUnitStopped
    -----
    --------------------------------------------------------------------------------
    $>


.. _ref_sec_license: Licensing

Licensing
=========

Use of `XCOFDK Starter Edition (SE) <https://www.xcofdk.de/install/index.html#xcofdk-starter-edition>`_ is subject to 
the terms and conditions of the software. For more information refert to the 
`XCOFDK Starter Edition (SE) Licensing page <https://www.xcofdk.de/install/index.html#ref-subsec-install-xcofdkpy-se-licensing>`_.


Links
=====

- Documentation: `<https://www.xcofdk.de/>`_
