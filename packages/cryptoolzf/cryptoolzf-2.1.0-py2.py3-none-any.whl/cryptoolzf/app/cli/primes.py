from typing import List, Union

import click

from cryptoolzf.crypto.constants import Primes, PRIMES_MERSENNE, PRIMES_LEAST_POW_TWO

from .cryptoolzf import cryptoolzf, help

_primes_help_text = "Get a prime number according to arguments \
passed to options. Currently only returns primes close to powers of two \
and mersenne primes, and it also doesn't do probabilistic checks, it \
instead just reads the data from included files."


@click.command(help=_primes_help_text)
@click.option(
    "--least",
    "prime",
    flag_value="least",
    required=False,
    default=True,
    help="Primes of the form 2^n - k. This is the default.      n ∈ ([8,400],512), 0 <= k < (n != 512 ? 10 : 1)",
)
@click.option(
    "--mersenne",
    "prime",
    flag_value="mersenne",
    required=False,
    help="Primes of the form 2^p - 1, where p is prime.          2 <= p < 20000",
)
@click.option(
    "--check/--no-check",
    type=bool,
    required=False,
    default=False,
    help="Just print all the possible values for the components of the selected prime type \
(such as n, k, p). Ignores --bits and --rank.",
)
@click.option(
    "-b",
    "--bits",
    nargs=1,
    type=int,
    required=False,
    default=None,
    help="Supply the number of bits, meaning which power to raise 2 to.",
)
@click.option(
    "-r",
    "--rank",
    nargs=1,
    type=int,
    required=False,
    default=-1,
    help="Supply the rank meaning either the index of the mersenne prime if 8 is at 0, or \
the index of the k value for the least 2^n - k prime.",
)
def primes(prime, check, bits, rank):
    missing = lambda prime: f"primes :: no arguments supplied for --{prime}"
    both = (
        lambda prime, first, second: f"primes :: --{prime} requires both --{first} and --{second}"
    )
    takes_one = (
        lambda prime, first, second: f"primes :: --{prime} takes only one of --{first}, --{second}"
    )

    try:
        if prime == "mersenne":
            if check:
                click.echo(PRIMES_MERSENNE)
            elif bits and 0 <= rank:
                click.echo(takes_one(prime, "bits", "rank"))
            elif bits:
                click.echo(Primes.get_mersenne(bits))
            elif 0 <= rank:
                click.echo(Primes.get_mersenne_by_rank(rank))
            else:
                click.echo(missing(prime))
                exit(1)
        elif prime == "least":
            if check:
                click.echo(PRIMES_LEAST_POW_TWO)
            elif bits and 0 <= rank:
                click.echo(Primes.get_least_near_pow_two(bits, rank))
            elif bits or 0 <= rank:
                click.echo(both(prime, "bits", "rank"))
            else:
                click.echo(missing(prime))
                exit(1)
    except Exception as e:
        print(e)
        exit(1)


cryptoolzf.add_command(primes)
