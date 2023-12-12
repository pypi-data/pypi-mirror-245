from dataclasses import dataclass


@dataclass(frozen=True)
class Bet:
    """Each player must make a `Bet` at the beginning of each round."""

    number_of_tricks: int
    confident: bool

    def compute_score(self, actual_result: int) -> int:
        """Return the number of points the player should based on the actual outcome."""
        if actual_result == self.number_of_tricks:
            points = actual_result + 10
            return 2 * points if self.confident else points
        else:
            difference = abs(actual_result - self.number_of_tricks)
            return -8 * difference if self.confident else -1 * difference

    def __str__(self) -> str:
        """Return a string representation, eg `2` or `CONFIDENT 1`"""
        return ("CONFIDENT " if self.confident else "") + str(self.number_of_tricks)
