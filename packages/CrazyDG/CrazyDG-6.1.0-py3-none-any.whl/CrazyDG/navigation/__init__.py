from ..crazy import CrazyDragon

from threading import Thread

from scipy.spatial.transform import Rotation

from .._base._navigation_base.imu       import IMU
from .._base._navigation_base.imu_setup import preflight_sequence
from .._base._navigation_base.qualisys  import Qualisys

from cflib.crazyflie.syncCrazyflie import SyncCrazyflie

from numpy import zeros

from time import sleep



class Navigation( Thread ):

    qtm = -1

    def __init__( self, cf: CrazyDragon, uri=None, need_velocity=False ):

        super().__init__()

        self.daemon = True

        if ( need_velocity ):
            thread = Thread( target=self._numerical_difference, args=[cf], daemon=True )
            thread.start()

        self.cf  = cf
        self.scf = None

        self.imu = IMU( cf )

        if ( uri != None ):
            self.scf = SyncCrazyflie( uri, cf )
            self.scf.open_link()

        self.navigate = True


    @classmethod
    def _on_pose( cls, cf: CrazyDragon, data: list ):
        
        cf.pos[:] = data[0:3]

        R = Rotation.from_euler( 'zyx', cf.att[::-1], degrees=True )
        q = R.as_quat()

        cf.rot[:,:] = R.as_matrix()

        cf.extpos.send_extpose( data[0], data[1], data[2], q[0], q[1], q[2], q[3] )


    @classmethod
    def init_qualisys( cls, cfs: dict ):

        cls.qtm = Qualisys( cfs )

        sleep( 1 )

        cls.qtm.on_pose = __class__._on_pose


    def run( self ):

        cf = self.cf

        imu = self.imu

        preflight_sequence( cf )

        sleep( 1 )

        imu.start_get_acc()
        imu.start_get_vel()
        imu.start_get_att()

        while self.navigate:

            sleep( 0.1 )


    @staticmethod
    def _numerical_difference( _cf: CrazyDragon, dt=0.01 ):

        p_pos = zeros(3)

        while True:

            _cf.vel[:] = ( _cf.pos - p_pos ) / dt

            p_pos[:] = _cf.pos

            sleep( dt )


    def join( self ):

        self.navigate = False

        self.close()

        super().join()

    
    def close( self ):

        if self.scf != None:
            self.scf.close_link()