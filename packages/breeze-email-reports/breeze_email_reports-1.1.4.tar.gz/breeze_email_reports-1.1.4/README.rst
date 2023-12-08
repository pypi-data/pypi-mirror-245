====================
Breeze Email Reports
====================
The Breeze Church Management System (CHMS) is used by many churches to manage
their operations. Breeze has modules to support (not necessarily a complete list):

* A database of church members, with flexibility on data to keep on members
* Tracking giving, including pledges, and preparing giving statements
* Creating events, with volunteer management and attendance tracking
* Online giving
* Emails and texts to members
* Online forms

Breeze also has a network REST Application Programming Interface (API) that provides remote applications access
to a church's Breeze data. While the interface is pretty obtuse, the API
makes it possible to retrieve and update a church's data outside of
Breeze's normal web interface. The command-line
utilities in this package do not update any data, but they can be used to
email periodic reports on Breeze.

The current release contains one utility: ``email_profile_report``,
which can be used
to periodically email a report to selected recipients detailing changes
in a church's member database between runs. Other utilities may be added in future releases.

Using these facilities takes a fair amount of configuration to provide
the credentials needed to access the Breeze API and to allow
sending emails. Both of these are implemented in dependent packages,
but to make it easier for users some basic detail is included in the documentation.

See DOCUMENTATION_ for details on use how to set up and use these reports.

.. _DOCUMENTATION: https://github.com/dawillcox/breeze_email_reports/blob/main/DOCUMENTATION.rst
