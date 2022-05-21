import enum


class Level1Mode(enum.Enum):
    BaseMode = 0
    TrackMode = 1
    PrefDirMode = 2
    OperMode = 3
    RestartSessionOperMode = 4
    TimetableMode = 5


class Level2OperMode(enum.Enum):
    NoOperMode = 0
    Operating = 1
    PreStart = 2
    Paused = 3


class TrackType(enum.Enum):
    Crossover = 0
    Points = 1
    Buffers = 2
    Bridge = 3
    SignalPost = 4
    Continuation = 5
    Platform = 6
    GapJump = 7
    FootCrossing = 8
    Unused = 9
    Concourse = 10
    Parapet = 11
    NamedNonStationLocation = 11
    Erase = 12
    LevelCrossing = 13


class Elements(enum.Enum):
    Horizontal = 1
    Vertical = 2
    Up_Right = 3
    Up_Left = 4
    Down_Right = 5
    Down_Left = 6
    Junction_Right_Up_RightAngle = 7
    Junction_Left_Up_RightAngle = 8
    Junction_Right_Down_RightAngle = 9
    Junction_Left_Down_RightAngle = 10
    Junction_Up_Left_RightAngle = 11
    Junction_Up_Right_RightAngle = 12
    Junction_Down_Left_RightAngle = 13
    Junction_Down_Right_RightAngle = 14
    Crossing_Horizontal_Vertical = 15
    Crossing_DiagonalUp_DiagonalDown = 16
    DiagonalUp = 18
    DiagonalDown = 19
    DiagonalUp_Right = 20
    Right_DiagonalDown = 21
    DiagonalDown_Right = 22
    Right_DiagonalUp = 23
    Up_DiagonalUp = 24
    Up_DiagonalRight = 25
    Down_DiagonalRight = 26
    Down_DiagonalLeft = 27
