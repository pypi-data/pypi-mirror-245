=======
History
=======

2.1.0 (2023-12-07)
------------------

* Actually fix by adding reqs in `setup.cfg` `install_requires`.


2.0.0 (2023-12-07)
------------------

* Fork by mtugan
* Fix `requirements.txt` not being included.

1.3.2 (2023-02-06)
------------------

* Fix data files in `cryptoolzf/resources` not being included.

1.3.0 (2023-02-06)
------------------

* `prime` command.
* Fix all instances of that write-to-file bug.
* Some style formatting.

1.2.1 (2023-02-03)
------------------

* Bugfix on main command because of a file object
* Don't print "No digest created!", we might not plan digest, need to analyze utility first.

1.2.0 (2023-02-02)
------------------

* Users couldn't use 1 passphrase to decrypt entire text file if so encrypted.
* QR format now also prints public key to QR. See Usage.

1.1.0 (2023-02-02)
------------------

* Fix ugly abstractions in tools.keys and replace with something better.

1.0.2 (2023-02-01)
------------------

* Minor config fixups.

1.0.1 (2023-01-30)
------------------

* First release on PyPI.
