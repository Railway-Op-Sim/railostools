import typing
import railostools.common.enumeration as railos_enums

CONNECTIONS: typing.Dict[
    railos_enums.Elements, typing.Optional[typing.Tuple[int, ...]]
] = {
    railos_enums.Elements.Horizontal: (4, 6),
    railos_enums.Elements.Vertical: (2, 8),
    railos_enums.Elements.Up_Right: (6, 8),
    railos_enums.Elements.Up_Left: (4, 8),
    railos_enums.Elements.Down_Right: (2, 6),
    railos_enums.Elements.Down_Left: (2, 4),
    railos_enums.Elements.Junction_Right_Up_RightAngle: (2, 4, 6),
    railos_enums.Elements.Junction_Left_Up_RightAngle: (2, 4, 6),
    railos_enums.Elements.Junction_Right_Down_RightAngle: (4, 6, 8),
    railos_enums.Elements.Junction_Left_Down_RightAngle: (4, 6, 8),
    railos_enums.Elements.Junction_Up_Left_RightAngle: (2, 4, 8),
    railos_enums.Elements.Junction_Up_Right_RightAngle: (2, 6, 8),
    railos_enums.Elements.Junction_Down_Left_RightAngle: (2, 4, 8),
    railos_enums.Elements.Junction_Down_Right_RightAngle: (2, 6, 8),
    railos_enums.Elements.Crossing_Horizontal_Vertical: (2, 4, 6, 8),
    railos_enums.Elements.Crossing_DiagonalUp_DiagonalDown: (1, 3, 7, 9),
    railos_enums.Elements.DiagonalUp: (3, 7),
    railos_enums.Elements.DiagonalDown: (1, 9),
    railos_enums.Elements.DiagonalUp_Right: (6, 7),
    railos_enums.Elements.Right_DiagonalDown: (4, 9),
    railos_enums.Elements.DiagonalDown_Right: (1, 6),
    railos_enums.Elements.Right_DiagonalUp: (3, 4),
    railos_enums.Elements.Up_DiagonalUp: (6, 8),
    railos_enums.Elements.Up_DiagonalRight: (1, 8),
    railos_enums.Elements.Down_DiagonalRight: (2, 9),
    railos_enums.Elements.Down_DiagonalLeft: (2, 7),
    railos_enums.Elements.Junction_Right_Up_45Angle: (3, 4, 6),
    railos_enums.Elements.Junction_Left_Up_45Angle: (1, 4, 6),
    railos_enums.Elements.Junction_Right_Down_45Angle: (4, 6, 9),
    railos_enums.Elements.Junction_Left_Down_45Angle: (4, 6, 7),
    railos_enums.Elements.Junction_Up_Left_45Angle: (1, 2, 8),
    railos_enums.Elements.Junction_Up_Right_45Angle: (2, 3, 8),
    railos_enums.Elements.Junction_Down_Left_45Angle: (2, 7, 8),
    railos_enums.Elements.Junction_Down_Right_45Angle: (2, 8, 9),
    railos_enums.Elements.Junction_DiagonalDown_Up_45Angle: (1, 2, 9),
    railos_enums.Elements.Junction_DiagonalUp_Up_45Angle: (2, 3, 8),
    railos_enums.Elements.Junction_DiagonalUp_Down_45Angle: (3, 7, 8),
    railos_enums.Elements.Junction_DiagonalDown_Down_45Angle: (1, 8, 9),
    railos_enums.Elements.Junction_DiagonalDown_Left_45Angle: (1, 4, 9),
    railos_enums.Elements.Junction_DiagonalUp_Right_45Angle: (3, 6, 7),
    railos_enums.Elements.Junction_DiagonalUp_Left_45Angle: (3, 4, 7),
    railos_enums.Elements.Junction_DiagonalDown_Right_45Angle: (1, 6, 9),
    railos_enums.Elements.Crossing_DiagonalDown_Vertical: (1, 2, 8, 9),
    railos_enums.Elements.Crossing_DiagonalUp_Vertical: (2, 3, 7, 8),
    railos_enums.Elements.Crossing_DiagonalUp_Horizontal: (3, 4, 6, 7),
    railos_enums.Elements.Crossing_DiagonalDown_Horizontal: (1, 4, 6, 9),
    railos_enums.Elements.Vertical_Over_Horizontal: (2, 4, 6, 8),
    railos_enums.Elements.Horizontal_Over_Vertical: (2, 4, 6, 8),
    railos_enums.Elements.DiagonalUp_Over_Right_Down: (1, 3, 7, 9),
    railos_enums.Elements.DiagonalDown_Over_Right_Up: (1, 3, 7, 9),
    railos_enums.Elements.Vertical_Over_DiagonalDown: (1, 2, 8, 9),
    railos_enums.Elements.Vertical_Over_DiagonalUp: (2, 3, 7, 8),
    railos_enums.Elements.DiagonalUp_Over_Vertical: (2, 3, 7, 8),
    railos_enums.Elements.DiagonalDown_Over_Vertical: (1, 2, 8, 9),
    railos_enums.Elements.Horizontal_Over_DiagonalUp: (3, 4, 6, 7),
    railos_enums.Elements.Horizontal_Over_DiagonalDown: (1, 4, 6, 9),
    railos_enums.Elements.DiagonalDown_Over_Horizontal: (1, 4, 6, 9),
    railos_enums.Elements.DiagonalUp_Over_Horizontal: (3, 4, 6, 7),
    railos_enums.Elements.TrackEnd_Left: (6,),
    railos_enums.Elements.TrackEnd_Right: (4,),
    railos_enums.Elements.TrackEnd_Down: (2,),
    railos_enums.Elements.TrackEnd_Up: (8,),
    railos_enums.Elements.TrackEnd_Up_Left: (9,),
    railos_enums.Elements.TrackEnd_Up_Right: (7,),
    railos_enums.Elements.TrackEnd_Down_Left: (3,),
    railos_enums.Elements.TrackEnd_Down_Right: (1,),
    railos_enums.Elements.Signal_Right: (4, 6),
    railos_enums.Elements.Signal_Left: (4, 6),
    railos_enums.Elements.Signal_Up: (2, 8),
    railos_enums.Elements.Signal_Down: (2, 8),
    railos_enums.Elements.Signal_Up_Left: (1, 9),
    railos_enums.Elements.Signal_Up_Right: (3, 7),
    railos_enums.Elements.Signal_Down_Left: (3, 7),
    railos_enums.Elements.Signal_Down_Right: (1, 9),
    railos_enums.Elements.Platform_Up: tuple(),
    railos_enums.Elements.Platform_Left: tuple(),
    railos_enums.Elements.Platform_Right: tuple(),
    railos_enums.Elements.Platform_Down: tuple(),
    railos_enums.Elements.Exit_Left: (6,),
    railos_enums.Elements.Exit_Right: (4,),
    railos_enums.Elements.Exit_Down: (2,),
    railos_enums.Elements.Exit_Up: (8,),
    railos_enums.Elements.Exit_Down_Left: (3,),
    railos_enums.Elements.Exit_Down_Right: (1,),
    railos_enums.Elements.Exit_Up_Left: (9,),
    railos_enums.Elements.Exit_Up_Right: (7,),
    railos_enums.Elements.Connection_Down: (2,),
    railos_enums.Elements.Connection_Up: (8,),
    railos_enums.Elements.Connection_Left: (6,),
    railos_enums.Elements.Connection_Right: (4,),
    railos_enums.Elements.Connection_Down_Left: (3,),
    railos_enums.Elements.Connection_Down_Right: (1,),
    railos_enums.Elements.Connection_Up_Left: (9,),
    railos_enums.Elements.Connection_Up_Right: (7,),
    railos_enums.Elements.Bridge_End_Up_Right_Wing_Down: tuple(),
    railos_enums.Elements.Bridge_End_Up_Left_Wing_Down: tuple(),
    railos_enums.Elements.Bridge_End_Down_Right_Wing_Up: tuple(),
    railos_enums.Elements.Bridge_End_Down_Left_Wing_Up: tuple(),
    railos_enums.Elements.Bridge_End_Down_Left_Wing_Right: tuple(),
    railos_enums.Elements.Bridge_End_Down_Right_Wing_Left: tuple(),
    railos_enums.Elements.Bridge_End_Up_Left_Wing_Right: tuple(),
    railos_enums.Elements.Bridge_End_Up_Right_Wing_Right: tuple(),
    railos_enums.Elements.Bridge_Center_Diagonal_Down: tuple(),
    railos_enums.Elements.Bridge_Center_Diagonal_Up: tuple(),
    railos_enums.Elements.Bridge_Wing_Down_Wing_Right: tuple(),
    railos_enums.Elements.Bridge_Wing_Down_Wing_Left: tuple(),
    railos_enums.Elements.Bridge_Wing_Up_Wing_Right: tuple(),
    railos_enums.Elements.Bridge_Wing_Up_Wing_Left: tuple(),
    railos_enums.Elements.Bridge_End_Right_Wing_Down_Left: tuple(),
    railos_enums.Elements.Bridge_End_Left_Wing_Down_Right: tuple(),
    railos_enums.Elements.Bridge_End_Right_Wing_Up_Left: tuple(),
    railos_enums.Elements.Bridge_End_Left_Wing_Up_Right: tuple(),
    railos_enums.Elements.Bridge_End_Down_Wing_Up_Right: tuple(),
    railos_enums.Elements.Bridge_End_Down_Wing_Up_Left: tuple(),
    railos_enums.Elements.Bridge_End_Up_Wing_Down_Right: tuple(),
    railos_enums.Elements.Bridge_End_Up_Wing_Down_Left: tuple(),
    railos_enums.Elements.Bridge_Center_Vertical: tuple(),
    railos_enums.Elements.Bridge_Wing_Up_Right_Down_Right: tuple(),
    railos_enums.Elements.Bridge_Wing_Down_Left_Down_Right: tuple(),
    railos_enums.Elements.Bridge_Wing_Up_Left_Up_Right: tuple(),
    railos_enums.Elements.Bridge_Wing_Up_Left_Down_Left: tuple(),
    railos_enums.Elements.Concourse: tuple(),
    railos_enums.Elements.Non_Station_Location: tuple(),
    railos_enums.Elements.Arrow_Horizontal_Left: (4, 6),
    railos_enums.Elements.Arrow_Horizontal_Right: (4, 6),
    railos_enums.Elements.Arrow_Vertical_Down: (2, 8),
    railos_enums.Elements.Arrow_Vertical_Up: (2, 8),
    railos_enums.Elements.Arrow_Up_Left: (1, 9),
    railos_enums.Elements.Arrow_Down_Left: (3, 7),
    railos_enums.Elements.Arrow_Down_Right: (1, 9),
    railos_enums.Elements.Arrow_Up_Right: (3, 7),
    railos_enums.Elements.Bridge_Vertical: (4, 6),
    railos_enums.Elements.Bridge_Horizontal: (2, 8),
    railos_enums.Elements.Junction_UpLeft_UpRight: (1, 3, 8),
    railos_enums.Elements.Junction_RightUp_RightDown_45Angle: (3, 4, 9),
    railos_enums.Elements.Junction_DownLeft_DownRight_45Angle: (2, 7, 9),
    railos_enums.Elements.Junction_LeftUp_LeftDown: (1, 6, 7),
    railos_enums.Elements.Junction_Left_45Angle_Up_45Angle: (2, 4, 9),
    railos_enums.Elements.Junction_Right_45Angle_Up_45Angle: (2, 6, 7),
    railos_enums.Elements.Junction_Right_45Angle_Down_45Angle: (1, 6, 8),
    railos_enums.Elements.Junction_Left_45Angle_Down_45Angle: (3, 4, 8),
    railos_enums.Elements.Arrow_Up_Right: (3, 7),
    railos_enums.Elements.Arrow_Up_Left: (1, 9),
    railos_enums.Elements.Arrow_Down_Left: (3, 7),
    railos_enums.Elements.Arrow_Down_Right: (1, 9),
    railos_enums.Elements.Level_Crossing: tuple(),
    railos_enums.Elements.Underpass_Vertical: (4, 6),
    railos_enums.Elements.Underpass_Horizontal: (2, 8),
}


def can_connect(
    element_one_type: railos_enums.Elements,
    element_two_type: railos_enums.Elements,
    coord_1: typing.Optional[typing.Tuple[int, int]] = None,
    coord_2: typing.Optional[typing.Tuple[int, int]] = None,
) -> bool:
    """Return whether two element types form a connection.

    If coordinates are provided a comparison is also made to
    check that the two elements are adjacent.

    Parameters
    ----------
    element_one_type: Elements
        the first map element type
    element_two_type: Elements
        the second map element type
    coord_1: Tuple[int, int], optional
        the coordinates of element one
    coord_2: Tuple[int, int], optional
        the coordinates of element two
    """

    # Based on the file specfications definition for an elements connection points
    #      1 ----- 2 ----- 3
    #      |               |
    #      4               6
    #      |               |
    #      7------ 8 ----- 9
    #

    _neighbour_mapping: typing.Dict[int, int] = {
        1: 9,
        2: 8,
        3: 7,
        4: 6,
        6: 4,
        7: 3,
        8: 2,
        9: 1,
    }

    # Find the join points of the first element
    _permitted_join_positions: typing.List[int] = [
        _neighbour_mapping[i] for i in CONNECTIONS[element_one_type]
    ]

    # Find the join point of the first element that connects to the second
    _connections: typing.List[int] = [
        i for i in _permitted_join_positions if i in CONNECTIONS[element_two_type]
    ]

    if not _connections:
        return False
    elif not all([coord_1, coord_2]):
        return True

    _connects: bool = False

    # There are multiple ways of positioning the two elements so check all
    for connection in _connections:
        if connection in {4, 6}:
            _connects |= (
                abs(coord_1[0] - coord_2[0]) == 1 and coord_1[1] - coord_2[1] == 0
            )
        elif connection in {2, 8}:
            _connects |= (
                abs(coord_1[1] - coord_2[1]) == 1 and coord_1[0] - coord_2[0] == 0
            )
        elif connection in {1, 9, 3, 7}:
            _connects |= (
                abs(coord_1[1] - coord_2[1]) == 1 and abs(coord_1[0] - coord_2[0]) == 1
            )

    return _connects
