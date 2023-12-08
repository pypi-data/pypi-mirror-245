from typing import List, Optional

from pydantic import BaseModel


class Poly(BaseModel):
    order: int
    prime: bool
    finite: bool
    modulo: Optional[int]
    constants: List[int]

    def eval_at(point: int):
        accum = 0
        for coeff in reversed(self.constants):
            accum *= point
            accum += coeff
            accum %= modulo
        return accum
