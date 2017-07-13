nagios-unity
============

Nagios plugin for monitoring Unity system

``nagios-unity`` is built on top of ``storops``, which interacts with Unity storage via RESTful API. ``nagios-unity`` provides
a easy-to-use command line interface for invocation of nagios servers. ``nagios-unity`` follows the output rules defined
by `Print only one line of text <https://nagios-plugins.org/doc/guidelines.html#AEN33>`_

License
-------

`Apache license version 2 <LICENSE>`_

Installation
------------


From Pypi
^^^^^^^^^

The ``nagios-unity`` can be install via pypi.

.. code-block:: bash

    $ pip install nagios-unity

From source
^^^^^^^^^^^

Alternatively, clone this repo via git and:

.. code-block:: bash

    $ cd nagios-unity
    $ sudo python setup.py install

Once installed, a ``nagios-unity``(on *nux) or ``nagios-unity.exe`` (on Windows) command will be available for use.

Command line usage
------------------

User can invoke the command line ``nagios-unity`` in bash or CMD/PowerShell. To get the help, type ``nagios-unity --help``.

Here is the example:

.. code-block:: bash

    $ nagios-unity --help
    Unity plugin for Nagios.

    Usage:
        nagios-unity [-v] -H <HOST> -u <USERNAME> -p <PASSWORD> <OBJECT> [-w <warning>] [-c <critical>]
        nagios-unity -h | --help
        nagios-unity --version

    Arguments:
        OBJECT  One of below values:
            battery, dae, disk, dpe,
            ethernet_port fan, fc_port,
            io_module, lcc, memory_module,
            pool, power_supply, sas_port,
            sp, ssc, ssd, system

    Options:
        -h --help                         Show this screen.
        -V --version                      Show version.
        -H --host                         Unity IP address.
        -u --username                     Unity User login.
        -p --password                     Unity password.
        -w --warning                      warning threshold.
        -c --critical                     critical threshold.
        -v --verbose                      show verbose logs.

    Examples:
      nagios-unity -H 192.168.1.100 -u admin -p password ssc



Configuration
-------------

.. caution::

    Before proceeding, make sure the nagios and its components are corrected configured.
    It is also suggested to try out the ``nagios-unity`` command line.



- Create a template ``storage-array`` in ``templates.cfg``.

.. code-block:: ini

    # Define a template for switches that we can reuse
    define host{
        name			storage-array	; The name of this host template
        use			generic-host	; Inherit default values from the generic-host template
        hostgroups		storage-arrays; Host groups that Windows servers should be a member of
        check_period		24x7		; By default, switches are monitored round the clock
        check_interval		5		; Switches are checked every 5 minutes
        retry_interval		1		; Schedule host check retries at 1 minute intervals
        max_check_attempts	10		; Check each switch 10 times (max)
        check_command		check-host-alive	; Default command to check if routers are "alive"
        notification_period	24x7		; Send notifications at any time
        notification_interval	30		; Resend notifications every 30 minutes
        notification_options	d,r		; Only send notifications for specific host states
        contact_groups		admins		; Notifications get sent to the admins by default
        register		0		; DONT REGISTER THIS - ITS JUST A TEMPLATE
        }


- Create a dedicated ``storage.cfg`` for storing all storage arrays.

.. code-block:: ini

    $ touch storage.cfg


- Add groups for grouping all storage devices in ``storage.cfg``

.. code-block:: ini

    define hostgroup{
        hostgroup_name  storage-arrays
        alias           External Storage
    }

- Add array for nagios management.

.. code-block:: ini

    define host{
        use         storage-array
        host_name   OB_H1132        ; The name we're giving to this host
        alias       My Nagios Unity ; A longer name associated with the host
        address»    10.245.101.35   ; IP address of the host
    }

- Add command for nagios use.

.. code-block:: ini

    # for unity

    define command{
        command_name    nagios-unity
        command_line    /usr/local/bin/nagios-unity -H <Management IP> -u <User> -p <Password> -v $ARG1$
    }

Note: please replace above credentials for the Unity array.

- Add services for managed arrays.

.. code-block:: ini

    define service{
        use»                generic-service
        host_name           OB_H1132
        service_description Ethernet Ports
        check_command       nagios-unity!ethernet_port
        }

    define service{
        use»                generic-service
        host_name           OB_H1132
        service_description FC Ports
        check_command       nagios-unity!fc_port
        }

    define service{
        use»                generic-service
        host_name           OB_H1132
        service_description SAS Ports
        check_command       nagios-unity!sas_port
        }

- Restart nagios to reflect the changes.

.. code-block:: ini

    $ sudo service nagios restart


Contributions
-------------

Simply fork this repo and send PR for your code change(also tests to cover your change),
remember to give a title and description of your PR. We are willing to enhance this project with you :).



