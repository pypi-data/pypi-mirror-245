from ...crazy import CrazyDragon

from .constants import Kp, Kd, g

from numpy import array, zeros

from time import sleep



def takeoff( cf: CrazyDragon, h=1.5, T=3, dt=0.1 ):

    cur     = zeros(3)
    des     = zeros(3)
    acc_cmd = zeros(3)
    P_pos   = zeros(3)
    D_pos   = zeros(3)
    care_g  = array([0,0,g])

    print( 'take-off' )

    n = int( T / dt )
    t = 0

    command = cf.command

    cur[:] = cf.pos
    pos    = cf.pos
    vel    = cf.vel

    des[ 0 ] = cur[0]
    des[ 1 ] = cur[1]
    des[ 2 ] = h

    cf.des[:] = des

    for _ in range( n ):

        P_pos[:] = des - pos
        D_pos[:] = vel

        acc_cmd[:] = 0
        acc_cmd[:] += P_pos * Kp
        acc_cmd[:] -= D_pos * Kd
        acc_cmd[:] += care_g

        command[:] = acc_cmd

        t += dt

        sleep( dt )