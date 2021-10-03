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