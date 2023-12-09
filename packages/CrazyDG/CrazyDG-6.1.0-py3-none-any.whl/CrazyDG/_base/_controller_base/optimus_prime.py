from numpy        import arcsin, rad2deg
from numpy        import sqrt
from numpy        import cos, sin, deg2rad

from numpy.linalg import norm



def _command_is_not_in_there( euler, acc_cmd ):
    ## yaw position
    yaw = euler[2]              ## [deg]
    yaw = deg2rad( yaw )        ## [rad]

    ## basic
    cy, sy = cos( yaw ), sin( yaw )

    ## update
    aE = cy * acc_cmd[0] + sy * acc_cmd[1]
    aN = cy * acc_cmd[1] - sy * acc_cmd[0]

    ## store
    acc_cmd[0] = aE
    acc_cmd[1] = aN

    return acc_cmd


def _command_as_RPY( acc_cmd, command ):
    """
    this function translates acc_cmd in ENU coordinate,
    to drone's body coordinate roll, pitch, yaw, acc

    coordinate rotates in 3 -> 2 -> 1 order

    command:
    1. roll
    2. pitch
    3. yaw
    4. acc
    """
    ## unpack acceleration command
    aE, aN, aU = acc_cmd        ## ENU coordinate

    ## acceleration to z-direction in drone's coordinate
    ## 3. yaw
    command[2] = 0              ## do not rotate, [deg/s]

    ## 2. pitch
    acc_str = sqrt( aE**2 + aU**2 )
    if acc_str:
        pitch_in_rad = arcsin( aE / acc_str )       ## [rad]
    else:
        pitch_in_rad = 0
    command[1] = rad2deg( pitch_in_rad )            ## [deg]

    ## 1. roll
    acc_str = sqrt( aN**2 + acc_str**2 )
    if acc_str:
        roll_in_rad = arcsin( -aN / acc_str )       ## [rad]
    else:
        roll_in_rad = 0
    command[0] = rad2deg( roll_in_rad )             ## [deg]

    ## acc strength
    command[3] = norm( acc_cmd )                    ## m/s^2