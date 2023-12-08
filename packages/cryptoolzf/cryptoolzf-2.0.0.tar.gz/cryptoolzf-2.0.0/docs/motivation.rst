.. highlight:: shell

==========
Motivation
==========

keys
^^^^

What
----

You want to secure your money on Ethereum by using a multisig type scheme, the first option (the not obvious one) you have:

* `Shamir Secret Sharing`_: you split the original private key into multiple encrypted files and send them out to people. You need to recover a threshold amount of files you've created when you've split the file, the file is then reconstructed. This is a GOOD scheme with which you can backup your hardware wallet.
        * Some hardware wallets support this natively, for example, `Trezor has a Shamir backup feature`_.
        * There is also `this python library`_ which supports threshold based Shamir Secret Sharing.

.. _`Shamir Secret Sharing`: https://en.wikipedia.org/wiki/Shamir%27s_Secret_Sharing
.. _`Trezor has a Shamir backup feature`: https://trezor.io/learn/a/what-is-shamir-backup
.. _`This python library`: https://github.com/jesseduffield/horcrux

The problem
-----------

Many non-Trezor owners will not be comfortable with private key plaintext data being loaded into memory on their device (please read the next chapter on what the purpose of this tool is to understand why we are making this claim), and even with a Trezor, or any hardware wallet with support SSS for that matter, many people will not be comfortable splitting up their original seed into something which isn't an electrical device. Also, notice that Trezor's implementation is intended as a *backup* feature.

Furthermore, owners might like their funds to be much more readily available by using multisig wallets on the network, which is possible with SSS, but with a higher overhead, in the sense of repeated collecting of shares for one wallet, where the multisig itself already has a threshold.

We are noting, that this idea mainly revolves around personal fund storage.

The solution
------------

Read carefully:

Instead of splitting one key up into multiple shares, or making a multisig and splitting K keys of N multisig assigned "owner" public keys up into multiple shares, for example 5 shares with a 3 threshold, which would give 5 * K shares,

we offer the possibility for K out of N multisig keys to instead be passphrase encrypted, but not split, such that they can be transmitted to other parties, and easily retrieved.

These keys can be used for backups and for usage of the multisig (note that the following is not a USAGE guide, for USAGE see USAGE):

        1. Make a 2/3 multisig, 2 hardware wallets (1 key with you, 1 at a safe location or with someone from your family), 1 extra owner.
        2. Generate an ethereum keypair in QR format (you receive the public key in console output...).
        3. (Optionally) Generate another 99 QR codes as dummies, with a different password every ... 11 codes, as an example.
        4. Pack the encrypted keyfile(s) into some format, zip it as an example, and send it to someone you trust, or upload it somewhere safe.

.. warning::

        Obviously, you are only going to send the encrypted (private!) keyfiles and not the public keys to owners, this is for the reason such that the owners cannot discover your multisig address and thus the amount of funds you've stored!

        5. Set the extra owner to the valid public key (the one corresponding to the correct QR code).
        6. Each time you want to trade, decode the QR into a private key (disconnect from the internet obviously, see USAGE!!!!!), enter into a wallet app.
        7. Execute transactions necessary.
        8. Replace the QR owner with a new one.
        9.  Repeat 2-5.

Furthermore, you can imagine, if you trust the people involved (!!!!), and if you have insured proper device security (because with 2/4, a hacker could steal funds if they can decrypt all keys), then you could make the move of actually distributing more encrypted keyfiles than your personal "safe safe" number.

For example, a 2 out of 4 multisig where another QR code is printed out and glued to a non-suspicious location, and so on.

Features
--------

Now:

* Generate and symmetrically encrypt a number of private keys with either one passphrase or multiple.
* The public key is stated together with the encrypted private key at generation.
* Output is in format which you can easily send-and-forget and decrypt later on when needed again. QR code available too!

Planned:

* Steganography - embed your data into an image or other kind of file
* BLAKE2b private key message digests for-your-eyes-only (!! because message digests of plaintext could possibly compromise cyphertext integrity, and you don't want to share that you've created one) for private key integrity checks (tl;dr verify you decrypted the intended cyphertext and someone isn't trying to check whether they can guess your password).