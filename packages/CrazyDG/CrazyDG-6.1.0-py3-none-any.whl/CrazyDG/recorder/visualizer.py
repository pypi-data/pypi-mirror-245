import matplotlib.pyplot as plt

from numpy import arange



def plot_T( acc, acccmd, vel, pos, poscmd, date, idx1, idx2, myName, dt=0.1 ):

    tim = arange( 0, len(acc[0,:]) ) * dt

    fig = plt.figure( figsize=(14,14) )

    ax1 = fig.add_subplot( 331 )
    ax2 = fig.add_subplot( 332 )
    ax3 = fig.add_subplot( 333 )
    ax4 = fig.add_subplot( 334 )
    ax5 = fig.add_subplot( 335 )
    ax6 = fig.add_subplot( 336 )
    ax7 = fig.add_subplot( 337 )
    ax8 = fig.add_subplot( 338 )
    ax9 = fig.add_subplot( 339 )

    ax1.plot( tim, acc[0,:]   , label='acc x' )
    ax2.plot( tim, acc[1,:]   , label='acc y' )
    ax3.plot( tim, acc[2,:]   , label='acc z' )
    ax1.plot( tim, acccmd[0,:], label='acc command x' )
    ax2.plot( tim, acccmd[1,:], label='acc command y' )
    ax3.plot( tim, acccmd[2,:], label='acc command z' )

    ax4.plot( tim, vel[0,:], label='velocity x' )
    ax5.plot( tim, vel[1,:], label='velocity y' )
    ax6.plot( tim, vel[2,:], label='velocity z' )

    ax7.plot( tim, pos[0,:]   , label='position x' )
    ax8.plot( tim, pos[1,:]   , label='position y' )
    ax9.plot( tim, pos[2,:]   , label='position z' )
    ax7.plot( tim, poscmd[0,:], label='position command x' )
    ax8.plot( tim, poscmd[1,:], label='position command y' )
    ax9.plot( tim, poscmd[2,:], label='position command z' )

    convenience( ax1 )
    convenience( ax2 )
    convenience( ax3 )
    convenience( ax4 )
    convenience( ax5 )
    convenience( ax6 )
    convenience( ax7 )
    convenience( ax8 )
    convenience( ax9 )

    axvline( ax1, tim, idx1, idx2 )
    axvline( ax2, tim, idx1, idx2 )
    axvline( ax3, tim, idx1, idx2 )
    axvline( ax4, tim, idx1, idx2 )
    axvline( ax5, tim, idx1, idx2 )
    axvline( ax6, tim, idx1, idx2 )
    axvline( ax7, tim, idx1, idx2 )
    axvline( ax8, tim, idx1, idx2 )
    axvline( ax9, tim, idx1, idx2 )

    plt.savefig( f'./flight_data/{date}/{myName}/T.png' )


def plot_Thrust( thrust, thrustcmd, date, idx1, idx2, myName, dt=0.1 ):

    tim = arange( 0, len(thrust[0,:]) ) * dt

    fig = plt.figure( figsize=(7,7) )

    ax1 = fig.add_subplot(111)
    ax1.plot( tim, thrust[0,:]   , label='thrust' )
    ax1.plot( tim, thrustcmd[0,:], label='thrust command' )

    convenience( ax1 )

    axvline( ax1, tim, idx1, idx2 )

    plt.savefig( f'./flight_data/{date}/{myName}/thrust.png' )


def plot_R( att, attcmd, date, idx1, idx2, myName, dt=0.1 ):

    tim = arange( 0, len(att[0,:]) ) * dt

    fig = plt.figure( figsize=(14,14) )

    ax1 = fig.add_subplot( 311 )
    ax2 = fig.add_subplot( 312 )
    ax3 = fig.add_subplot( 313 )

    ax1.plot( tim, att[0,:]   , label='euler att x' )
    ax2.plot( tim, att[1,:]   , label='euler att y' )
    ax3.plot( tim, att[2,:]   , label='euler att z' )
    ax1.plot( tim, attcmd[0,:], label='euler att command x' )
    ax2.plot( tim, attcmd[1,:], label='euler att command y' )
    ax3.plot( tim, attcmd[2,:], label='euler att command z' )

    convenience( ax1 )
    convenience( ax2 )
    convenience( ax3 )

    axvline( ax1, tim, idx1, idx2 )
    axvline( ax2, tim, idx1, idx2 )
    axvline( ax3, tim, idx1, idx2 )

    plt.savefig( f'./flight_data/{date}/{myName}/R.png' )




def convenience( axn: plt.Axes ):
    axn.tick_params( axis='both', labelsize=7 )
    axn.legend( fontsize=8 )
    axn.grid()


def axvline( axn: plt.Axes, tim, idx1: int, idx2: int ):

    if ( ( idx1 == -1 ) or ( idx2 == -1 ) ):
        return

    axn.axvline( tim[idx1], tim[idx2], color='g', alpha=0.3, label='killer mode' )