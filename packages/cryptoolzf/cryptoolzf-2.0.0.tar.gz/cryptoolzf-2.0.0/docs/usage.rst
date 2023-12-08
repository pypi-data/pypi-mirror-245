=====
Usage
=====

Read the :doc:`installation` guidelines first!

Even though functions may be part of a subcommand, they are listed "horizontally" here.

Before each function, there is a help output pasted such that the command may be inspected while reading.

The help output describes the exact usage, and the guidelines below help to explain "safe" usage.

create
======

.. code-block:: text

    Usage: cryptoolzf keys create [OPTIONS] [NUMBER_PASSPHRASES]
                                 [NUMBER_KEYS_CREATED]

      This command creates a keypair for a chosen network and encrypts the secret
      with a chosen algorithm combination (designated by the keyword shown in
      options), formats it into a chosen format, and also writes (depending on
      format or choice etc.) it into a file or stdout. Note that the options may
      also be appended at the end, but it is advisable to prepend them before
      commands.

      NUMBER_PASSPHRASES is the number of passphrases used for key creation. We
      demand either 1 passphrase for all keys, or multiple keys, for the SAME
      NUMBER_KEYS_CREATED.

    Options:
      -n, --network [ethereum]  The network to create keys for.
      -a, --algorithm [aesgcm]  The keyword for the set of algorithms which should
                                be used. For example, aesgcm is currently pbdkf2 +
                                aesgcm.
      -f, --format [pem|qr]     The default output format for encrypted data.
      -o, --outfile FILE        The file to print the created data to.
      --header TEXT             The custom header to use for PEM blocks.
      --digest / --no-digest    Before encryption, compute the digest of the
                                private key. Currently only a dummy option. NOTE:
                                Do NOT send this with encrypted text.
      -h, --help                Show this message and exit.

1. As mentioned, first download the program. For serious data, always use a fixed pipx installed version with a suffix, as mentioned.

2. If you are using :code:`create` to actually generate an important private key, disconnect from the internet.

3. Try generating multiple dummy examples based on your settings. For example:

.. code-block:: bash

    cryptoolzf keys create --header TEST # this is equal to cryptoolzf keys create 1 1 --header TEST
    cryptoolzf keys create 2 2 --header TEST
    cryptoolzf keys create --format qr --outfile <specify filepath here>
    cryptoolzf keys create 2 2 --format qr --outfile <specify filepath here>

4. These should generate outputs, either one or multiple PEM blocks in the following format:

.. code-block:: text

    Your Ethereum Public Key:

    0xBa171cc5D6c3813744592422b026b9392FD4FD05

    The encrypted private key block:

    -----BEGIN KEYS-----

    7Tve5fCIpL/ICTCo46pIR46EucPdecIipxhPilSX9b+zc/0VOKLACstf8xtDIlfO
    oQ00nz3H+qZGQP8BohBIwfq1XL4dZEqWh4qrjubsk5bVpkAw06fLLeSNNTQ=

    -----END KEYS-----

5. Or multiple QR codes, such as the following, where the corresponding public key will be printed both to console and to a QR code. Note that the QR code with a smaller amount of squares is your public key, you will also notice this if you simply scan it!

.. image:: resources/sample_public.png

.. note::

    This is a public key, read the note below on info.

.. image:: resources/sample_private.png

.. note::

    This is what a private key looks like, it has noticeably more squares than a private key. When scanned, it also base64 encoded, and doesn't resemble a public key at all.

6. Possibly reboot the machine, then only reconnect to the internet, also possibly remove the files beforehand from your device. It all depends on your threat model.

This is the entire :code:`create` process, but you should also at least :code:`reveal` once to check whether everything worked properly! You could also reboot your machine before doing this to see whether that has any impact (98% chance that it doesn't).

This is described next.

reveal
======

.. code-block:: text

    Usage: cryptoolzf keys reveal [OPTIONS] [NUMBER_PASSPHRASES] FILEPATHS...

      This command is used to decrypt the encrypted format you have received, as
      output of the `create` command into some file or stdout. This format must be
      pasted into preferably ONE file and then given as input to the command, with
      the right options, according to how you encrypted your data.

      NOTE that for QR codes, the QR code must be scanned by the user and only the
      "plaintext" cyphertext should be pasted into a file, see the docs for more.

      NUMBER_PASSPHRASES is the number of passphrases which will be SEQUENTIALLY
      used to decrypt the inputted key data which is read from files. FILEPATHS
      are the paths to the files which contain the key data.

    Options:
      -n, --network [ethereum]  The network the keys belong to.
      -a, --algorithm [aesgcm]  The keyword for the set of algorithms which the
                                data is encrypted with.
      -f, --format [pem|qr]     Format of the formatted input cyphertext. In
                                future will be automatic.  [required]
      -o, --outfile FILE        The file to print the decrypted data to.
      --digest / --no-digest    Verify private key digest during decryption.
                                Currently a dummy option.
      -h, --help                Show this message and exit.

1. If not testing, disconnect from the internet, airgap the device, the plaintext secret key will be either printed to file or console now.

2. Take any dummy examples you generated and know the passphrases for, then (following the above samples):

3. For PEM blocks, paste **either** the entire paste data (preferred), or just the following part, BUT DON'T MODIFY THE FORMAT, including NEWLINES, INDENTATION:

.. code-block:: text

    -----BEGIN KEYS-----

    7Tve5fCIpL/ICTCo46pIR46EucPdecIipxhPilSX9b+zc/0VOKLACstf8xtDIlfO
    oQ00nz3H+qZGQP8BohBIwfq1XL4dZEqWh4qrjubsk5bVpkAw06fLLeSNNTQ=

    -----END KEYS-----

4. For QR codes, scan it, then copy the data into a text file sequentially, noting that the '=' endings are IMPORTANT (the following is not from the sample):

.. code-block:: text

    Nx2IA2tsu/Xzl07kmkJKdGr3Qz9JTcvv/Fp4nAf42/+CFGxuNAws5KN71FLt+Iw5dHdDIioeIKPiLa0Dl/Ss86vlRdyQeoktaeD44nf3jZPIF+GaOXM5vwcWkBk=
    lRzkK4S9qR8KjyXo9ygxehGhDcGPz4CGZgcrIbqt9vVB5VuCzoNYcVkvTm/bcLfDIordhfo6DH8Q8ge35Mujygv93ks6YFzyOx9Z07+lhrre8sCwpffdGTJfW6w=

5. The format must be specified for the reveal command, it won't automatically detect it:

.. code-block:: bash

    cryptoolzf keys reveal 1 <path to file with data> -f pem # will print to stdout
    cryptoolzf keys reveal 2 <path to file with data> -f qr # 2 for the "2 2" case
    cryptoolzf keys reveal 1 <path to file with data> -o <path to file you want pk written to> -f qr
    cryptoolzf keys reveal 2 <path to file with data> -o <path to file you want pk written to> -f pem

6. The password for the above sample qrcode is "test" (you can just save it), it should print (or save) the following:

.. code-block:: text

    The decrypted private key (note it down!):

    cdb9054628d8b1886d19a5f4d8ba3833409ca36c817a602ea8b09fa1cc8fd743

8. If you enter the private key into some wallet, you should notice that the public address of the sample corresponds to 0xBcC4A7A98cE8808d1a607FA8d89aA222b4558CaC, the same thing you would get when scanning the public key QR.

9. If not testing, keep the device disconnected and save the key somewhere, either onto a USB, or into a KeepassXC database, a software wallet... Secure erase (data shredding) (or just erase) the plaintext data from the device.

10.  If not testing, reboot.

tl;dr be careful

primes
======

.. code-block:: bash

    cryptoolzf primes -b 512 -r 0
    # 13407807929942597099574024998205846127479365820592393377723561443721764030073546976801874298166903427690031858186486050853753882811946569946433649006083527
    cryptoolzf primes --least -b 400 -r 9
    # 2582249878086908589655919172003011874329705792829223512830659356540647622016841194629645353280137831435903171972747490109
    cryptoolzf primes --mersenne -b 13
    # 8191
    cryptoolzf primes --mersenne -r 13
    # 531137992816767098689588206552468627329593117727031923199444138200403559860852242739162502265229285668889329486246501015346579337652707239409519978766587351943831270835393219031728127

crypto
======

:code:`crypto` is a subpackage and as such can be imported into python code you're writing, for now, only an example, this is enough though because the way the library is used is quite simple:

.. code-block:: python

    from cryptoolzf.crypto import SecretBytes
    from cryptoolzf.crypto.circuits import EncryptPBDKF2_AESGCM, DecryptPBDKF2_AESGCM

    ecirc = EncryptPBDKF2_AESGCM(
        pbdkf2_passphrase=SecretBytes("Some passphrase.".encode('ascii')),
        aesgcm_plaintext=SecretBytes("Secret text.".encode('ascii'))
    )

    outs = ecirc()
    print(outs)

    dcirc = DecryptPBDKF2_AESGCM(
        pbdkf2_passphrase=SecretBytes("Some passphrase.".encode('ascii')),
        aesgcm_cyphertext=outs.aesgcm_cyphertext
    )

    print(dcirc().aesgcm_plaintext.get_secret_value())
