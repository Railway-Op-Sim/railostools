import typing
import dataclasses


@dataclasses.dataclass
class Coordinate:
    X: int
    Y: int

    def __getitem__(self, index) -> typing.Tuple[int, int]:
        if index < 0 or index > 1:
            raise ValueError("Index must be 0, 1")
        return self.X if index == 0 else self.Y

    def __str__(self) -> str:
        _sign_x = "N" if self.X < 0 else ""
        _sign_y = "N" if self.Y < 0 else ""
        return f"{_sign_x}{abs(self.X)}-{_sign_y}{abs(self.Y)}"
