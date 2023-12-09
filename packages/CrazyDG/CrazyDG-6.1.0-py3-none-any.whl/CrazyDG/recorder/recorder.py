from threading import Thread

from ..crazy import CrazyDragon

from ..control import Controller
from ..control import alpha

from .visualizer import plot_R, plot_T, plot_Thrust

from os import system

from pandas import DataFrame

from numpy import zeros, save

from time import sleep



class Recorder( Thread ):

    def __init__( self , _cf: CrazyDragon, CTR: Controller, myName:str, when: str, n=18000 ):

        super().__init__()

        self._cf = _cf
        self.CTR = CTR

        self.myName = myName
        self.date   = when

        self.recording = True

        self.G_Start = -1
        self.G_Stopd = -1

        self.idxn = 0

        self.record_datas = {
            'acc'   : zeros((3,n)),
            'acccmd': zeros((3,n)),
            'vel'   : zeros((3,n)),
            'relvel': zeros((3,n)),
            'pos'   : zeros((3,n)),
            'poscmd': zeros((3,n)),
            'att'   : zeros((3,n)),
            'cmd'   : zeros((4,n)),
            'thrust': zeros((1,n))
        }

        self.data_pointer = {
            'acc'   : _cf.acc,
            'acccmd': _cf.command,
            'vel'   : _cf.vel,
            'relvel': _cf.v_rel,
            'pos'   : _cf.pos,
            'poscmd': _cf.des,
            'att'   : _cf.att,
            'cmd'   : CTR.command,
            'thrust': CTR.thrust
        }


    def run( self ):

        data_pointer = self.data_pointer
        record_datas = self.record_datas

        while self.recording:

            for key, pointer in data_pointer.items():

                record_datas[key][:,self.idxn] = pointer[:]

            self.idxn += 1

            sleep( 0.1 )

    
    def join( self ):

        self.recording = False

        super().join()

        acc    = self.record_datas['acc'][:,:self.idxn]
        acccmd = self.record_datas['acccmd'][:,:self.idxn]
        vel    = self.record_datas['vel'][:,:self.idxn]
        relvel = self.record_datas['relvel'][:,:self.idxn]
        pos    = self.record_datas['pos'][:,:self.idxn]
        poscmd = self.record_datas['poscmd'][:,:self.idxn]
        att    = self.record_datas['att'][:,:self.idxn]
        cmd    = self.record_datas['cmd'][:,:self.idxn]
        thrust = self.record_datas['thrust'][:,:self.idxn]

        attcmd    = cmd[0:3,:self.idxn]
        thrustcmd = cmd[ 3 ,:self.idxn] * alpha

        system( f'cd ./flight_data/{self.date} && mkdir {self.myName}' )

        DF = DataFrame(
            {
                'acc_cmd x': acccmd[0,:],
                'acc_cmd y': acccmd[1,:],
                'acc_cmd z': acccmd[2,:],

                'acc x': acc[0,:],
                'acc y': acc[1,:],
                'acc z': acc[2,:],

                'vel x': vel[0,:],
                'vel y': vel[1,:],
                'vel z': vel[2,:],

                'rel_vel x': relvel[0,:],
                'rel_vel y': relvel[1,:],
                'rel_vel z': relvel[2,:],

                'pos_cmd x': poscmd[0,:],
                'pos_cmd y': poscmd[1,:],
                'pos_cmd z': poscmd[2,:],

                'pos x': pos[0,:],
                'pos y': pos[1,:],
                'pos z': pos[2,:],

                'command x': cmd[0,:],
                'command y': cmd[1,:],
                'command z': cmd[2,:],

                'att_cmd x': attcmd[0,:],
                'att_cmd y': attcmd[1,:],
                'att_cmd z': attcmd[2,:],

                'att x': att[0,:],
                'att y': att[1,:],
                'att z': att[2,:],

                'thrust'    : thrust[:],
                'thrust_cmd': thrustcmd[:]
            }
        )

        DF.to_csv( f'./flight_data/{self.date}/{self.myName}.csv' )

        plot_T( acc, acccmd, vel, pos, self.date, self.G_Start, self.G_Stopd, self.myName )
        plot_R( att, attcmd, self.date, self.G_Start, self.G_Stopd, self.myName )
        plot_Thrust( thrust, thrustcmd, self.date, self.G_Start, self.G_Stopd, self.myName )