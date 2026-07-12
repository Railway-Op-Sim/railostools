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
    Crailossover,
    Points,
    Buffers,
    Bridge,
    SignalPost,
    Continuation,
    Platform,
    GapJump,
    FootCrailossing,
    Unused,
    Concourse,
    Parapet,
    NamedNonStationLocation,
    Erase,
    LevelCrailossing,
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
    CrailossingHorizontalVertical,
    CrailossingDiagonalUpDiagonalDown,
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
