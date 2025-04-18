#ifndef __ROS_COMMON_HXX__
#define __ROS_COMMON_HXX__

#include <iostream>
#include <cmath>
#include <regex>
#include <format>
#include <string>

#include "railostools/exceptions.hxx"

namespace RailOSTools {

std::string strip(const std::string& s);
std::vector<std::string> strip_svector(const std::vector<std::string>& s);

class Coordinate {
  private:
    const int x_;
    const int y_;
    std::pair<int, int> parse_int_pair_(const std::string& coord_str);
  public:
    Coordinate(int x, int y): x_(x), y_(y) {}
    Coordinate(const std::pair<int, int>& coord_pair) : x_(coord_pair.first), y_(coord_pair.second) {}
    Coordinate(const std::string& coord_str) : Coordinate(parse_int_pair_(coord_str)) {}
    int X() const { return x_; }
    int Y() const { return y_; }
    int abs() const { return std::sqrt(x_ * x_ + y_ * y_); }
    friend std::ostream& operator<<(std::ostream& o, const Coordinate& coord) { 
      if(coord.X() < 0) o << "N";
      o << std::abs(coord.X());
      if(coord.Y() < 0) o << "N";
      o << std::abs(coord.Y());
      return o;
    }
    Coordinate operator+(const Coordinate& other) const;
    Coordinate operator-(const Coordinate& second) const;
    bool operator==(const Coordinate& other) const;
    bool operator!=(const Coordinate& other) const;
};

enum class Level1Mode {
  BackMode = 0,
  TrackMode = 1,
  PrefDirMode = 2,
  OperMode = 3,
  RestartSessionOperMode = 4,
  TimetableMode = 5
};


enum class Level2OperMode {
    NoOperMode = 0,
    Operating = 1,
    PreStart = 2,
    Paused = 3
};


enum class TrackType {
    Simple = 0,
    Crossover = 1,
    Points = 2,
    Buffers = 3,
    Bridge = 4,
    SignalPost = 5,
    Continuation = 6,
    Platform = 7,
    GapJump = 8,
    FootCrossing = 9,
    Unused = 10,
    Concourse = 11,
    Parapet = 12,
    NamedNonStationLocation = 13,
    Erase = 14,
    LevelCrossing = 15
};

enum class LevelCrossingState {
    RAISED = 0,
    LOWERED = 1,
    IN_MOTION = 2
};

enum class SignalAspect {
    RED = 0,
    YELLOW = 1,
    DOUBLE_YELLOW = 2,
    GREEN = 3
};

enum class Elements {
    Horizontal = 1,
    Vertical = 2,
    Up_Right = 3,
    Up_Left = 4,
    Down_Right = 5,
    Down_Left = 6,
    Junction_Right_Up_RightAngle = 7,
    Junction_Left_Up_RightAngle = 8,
    Junction_Right_Down_RightAngle = 9,
    Junction_Left_Down_RightAngle = 10,
    Junction_Up_Left_RightAngle = 11,
    Junction_Up_Right_RightAngle = 12,
    Junction_Down_Left_RightAngle = 13,
    Junction_Down_Right_RightAngle = 14,
    Crossing_Horizontal_Vertical = 15,
    Crossing_DiagonalUp_DiagonalDown = 16,
    DiagonalUp = 18,
    DiagonalDown = 19,
    DiagonalUp_Right = 20,
    Right_DiagonalDown = 21,
    DiagonalDown_Right = 22,
    Right_DiagonalUp = 23,
    Up_DiagonalUp = 24,
    Up_DiagonalRight = 25,
    Down_DiagonalRight = 26,
    Down_DiagonalLeft = 27,
    Junction_Right_Up_45Angle = 28,
    Junction_Left_Up_45Angle = 29,
    Junction_Right_Down_45Angle = 30,
    Junction_Left_Down_45Angle = 31,
    Junction_Up_Left_45Angle = 32,
    Junction_Up_Right_45Angle = 33,
    Junction_Down_Left_45Angle = 34,
    Junction_Down_Right_45Angle = 35,
    Junction_DiagonalDown_Up_45Angle = 36,
    Junction_DiagonalUp_Up_45Angle = 37,
    Junction_DiagonalUp_Down_45Angle = 38,
    Junction_DiagonalDown_Down_45Angle = 39,
    Junction_DiagonalDown_Left_45Angle = 40,
    Junction_DiagonalUp_Right_45Angle = 41,
    Junction_DiagonalUp_Left_45Angle = 42,
    Junction_DiagonalDown_Right_45Angle = 43,
    Crossing_DiagonalDown_Vertical = 44,
    Crossing_DiagonalUp_Vertical = 45,
    Crossing_DiagonalUp_Horizontal = 46,
    Crossing_DiagonalDown_Horizontal = 47,
    Vertical_Over_Horizontal = 48,
    Horizontal_Over_Vertical = 49,
    DiagonalUp_Over_Right_Down = 50,
    DiagonalDown_Over_Right_Up = 51,
    Vertical_Over_DiagonalDown = 52,
    Vertical_Over_DiagonalUp = 53,
    DiagonalUp_Over_Vertical = 54,
    DiagonalDown_Over_Vertical = 55,
    Horizontal_Over_DiagonalUp = 56,
    Horizontal_Over_DiagonalDown = 57,
    DiagonalDown_Over_Horizontal = 58,
    DiagonalUp_Over_Horizontal = 59,
    TrackEnd_Left = 60,
    TrackEnd_Right = 61,
    TrackEnd_Down = 62,
    TrackEnd_Up = 63,
    TrackEnd_Up_Left = 64,
    TrackEnd_Up_Right = 65,
    TrackEnd_Down_Left = 66,
    TrackEnd_Down_Right = 67,
    Signal_Right = 68,
    Signal_Left = 69,
    Signal_Up = 70,
    Signal_Down = 71,
    Signal_Up_Left = 72,
    Signal_Up_Right = 73,
    Signal_Down_Left = 74,
    Signal_Down_Right = 75,
    Platform_Up = 76,
    Platform_Down = 77,
    Platform_Left = 78,
    Platform_Right = 79,
    Exit_Left = 80,
    Exit_Right = 81,
    Exit_Down = 82,
    Exit_Up = 83,
    Exit_Up_Left = 84,
    Exit_Up_Right = 85,
    Exit_Down_Left = 86,
    Exit_Down_Right = 87,
    Connection_Left = 88,
    Connection_Right = 89,
    Connection_Down = 90,
    Connection_Up = 91,
    Connection_Up_Left = 92,
    Connection_Up_Right = 93,
    Connection_Down_Left = 94,
    Connection_Down_Right = 95,
    Concourse = 96,
    Bridge_End_Up_Right_Wing_Down = 97,
    Bridge_End_Up_Left_Wing_Down = 98,
    Bridge_End_Down_Right_Wing_Up = 99,
    Bridge_End_Down_Left_Wing_Up = 100,
    Bridge_End_Down_Left_Wing_Right = 101,
    Bridge_End_Down_Right_Wing_Left = 102,
    Bridge_End_Up_Left_Wing_Right = 103,
    Bridge_End_Up_Right_Wing_Right = 104,
    Bridge_Center_Diagonal_Down = 105,
    Bridge_Center_Diagonal_Up = 106,
    Bridge_Wing_Down_Wing_Right = 107,
    Bridge_Wing_Down_Wing_Left = 108,
    Bridge_Wing_Up_Wing_Right = 109,
    Bridge_Wing_Up_Wing_Left = 110,
    Bridge_End_Right_Wing_Down_Left = 111,
    Bridge_End_Left_Wing_Down_Right = 112,
    Bridge_End_Right_Wing_Up_Left = 113,
    Bridge_End_Left_Wing_Up_Right = 114,
    Bridge_End_Down_Wing_Up_Right = 115,
    Bridge_End_Down_Wing_Up_Left = 116,
    Bridge_End_Up_Wing_Down_Right = 117,
    Bridge_End_Up_Wing_Down_Left = 118,
    Bridge_Center_Vertical = 120,
    Bridge_Wing_Up_Right_Down_Right = 121,
    Bridge_Wing_Down_Left_Down_Right = 122,
    Bridge_Wing_Up_Left_Up_Right = 123,
    Bridge_Wing_Up_Left_Down_Left = 124,
    Arrow_Horizontal_Left = 125,
    Arrow_Horizontal_Right = 126,
    Arrow_Vertical_Up = 127,
    Arrow_Vertical_Down = 128,
    Bridge_Vertical = 129,
    Bridge_Horizontal = 130,
    Non_Station_Location = 131,
    Junction_UpLeft_UpRight = 132,
    Junction_RightUp_RightDown_45Angle = 133,
    Junction_DownLeft_DownRight_45Angle = 134,
    Junction_LeftUp_LeftDown = 135,
    Junction_Left_45Angle_Up_45Angle = 136,
    Junction_Right_45Angle_Up_45Angle = 137,
    Junction_Right_45Angle_Down_45Angle = 138,
    Junction_Left_45Angle_Down_45Angle = 139,
    Arrow_Up_Right = 140,
    Arrow_Up_Left = 141,
    Arrow_Down_Left = 142,
    Arrow_Down_Right = 143,
    Level_Crossing = 144,
    Underpass_Vertical = 145,
    Underpass_Horizontal = 146
};
};

#endif
