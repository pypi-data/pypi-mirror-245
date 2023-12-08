from typing import Callable
from cryptoolzf.utils import get_resource

# FORMAT: { 'n': ['k'] }
# PRIME: 2**n - k
PRIMES_LEAST_POW_TWO = get_resource("primes_least_pow_two.json")

# FORMAT: [p]
# PRIME: 2**p - 1
PRIMES_MERSENNE = [
    2,
    3,
    5,
    7,
    13,
    17,
    19,
    31,
    61,
    89,
    107,
    127,
    521,
    607,
    1279,
    2203,
    2281,
    3217,
    4253,
    4423,
    9689,
    9941,
    11213,
    19937,
]


class Primes:
    @staticmethod
    def get_least_near_pow_two(bitnum: int, rank: int):
        """Supports 8-400 and 512 bits, currently."""
        power = str(bitnum)
        ks = PRIMES_LEAST_POW_TWO.get(power)
        if ks:
            if rank < len(ks):
                return 2**bitnum - int(ks[rank])
            else:
                raise ValueError(
                    f"Primes.get_least_near_pow_two: in 2^{power} - k_i, i<={rank} not supported."
                )
        else:
            raise ValueError(f"Primes.get_least_near_pow_two: 2^{power} not supported.")

    @staticmethod
    def get_mersenne_by_rank(rank: int):
        if rank < len(PRIMES_MERSENNE):
            return Primes.get_mersenne(PRIMES_MERSENNE[rank])
        else:
            raise ValueError(
                f"Primes.get_mersenne_by_rank: rank <= {rank} not supported."
            )

    @staticmethod
    def get_mersenne(bitnum: int):
        """Primes below 20k bits supported."""
        if bitnum in PRIMES_MERSENNE:
            return 2**bitnum - 1
        else:
            raise ValueError(
                f"Primes.get_mersenne: 2^{bitnum} - 1 is not prime or not supported."
            )
