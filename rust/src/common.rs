#[derive(Debug, PartialEq, Eq, Hash)]
pub enum Level1Mode {
    BaseMode,
    TrackMode,
    PrefDirMode,
    OperMode,
    RestartSessionOperMode,
    TimetableMode,
}

#[derive(Debug, PartialEq, Eq, Hash)]
pub enum Level2OperMode {
    NoOperMode,
    Operating,
    PreStart,
    Paused,
}

#[derive(Debug, PartialEq, Eq, Hash)]
pub enum TrackType {
    Simple,
    Crossover,
    Points,
    Buffers,
    Bridge,
    SignalPost,
    Continuation,
    Platform,
    GapJump,
    FootCrossing,
    Unused,
    Concourse,
    Parapet,
    NamedNonStationLocation,
    Erase,
    LevelCrossing,
}

#[derive(Debug, PartialEq, Eq, Hash)]
pub enum Elements {
    Horizontal,
    Vertical,
    UpRight,
    UpLeft,
    DownRight,
    DownLeft,
    JunctionRightUpRightAngle,
    JunctionLeftUpRightAngle,
    JunctionRightDownRightAngle,
    JunctionLeftDownRightAngle,
    JunctionUpLeftRightAngle,
    JunctionUpRightRightAngle,
    JunctionDownLeftRightAngle,
    JunctionDownRightRightAngle,
    CrossingHorizontalVertical,
    CrossingDiagonalUpDiagonalDown,
    DiagonalUp,
    DiagonalDown,
    DiagonalUpRight,
    RightDiagonalDown,
    DiagonalDownRight,
    RightDiagonalUp,
    UpDiagonalUp,
    UpDiagonalRight,
    DownDiagonalRight,
    DownDiagonalLeft,
}
