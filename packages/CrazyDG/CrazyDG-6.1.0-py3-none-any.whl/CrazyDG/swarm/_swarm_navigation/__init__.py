from ...crazy import CrazyDragon

from threading import Thread

from ..swarm_handler import SwarmHandler

from scipy.spatial.transform import Rotation

from ..._base._navigation_base.imu       import IMU
from ..._base._navigation_base.imu_setup import preflight_sequence
from ..._base._navigation_base.qualisys  import Qualisys

from time import sleep



class SwarmNavigation( Thread, SwarmHandler ):

    def __init__( self, _cfs: dict ):

        super().__init__()

        self.daemon = True

        self.cfs = _cfs
        self.qtm = Qualisys( _cfs )
        self.imu = {}

        for bodyname, _cf in _cfs.items():
            self.imu[bodyname] = IMU( _cf )

        sleep( 1 )

        self.qtm.on_pose = __class__._on_pose

        self.parallel_run( preflight_sequence, self.cfs )

        sleep( 1 )

        self.parallel_run( self.imu_start, self.cfs, args_dict=self.imu )


    @classmethod
    def _on_pose( cls, cf: CrazyDragon, data: list ):
        
        cf.pos[:] = data[0:3]

        R = Rotation.from_euler( 'zyx', cf.att[::-1], degrees=True )
        q = R.as_quat()

        cf.rot[:,:] = R.as_matrix()

        cf.extpos.send_extpose( data[0], data[1], data[2], q[0], q[1], q[2], q[3] )


    def imu_start( self, imu: IMU ):

        imu.start_get_acc()
        imu.start_get_vel()
        imu.start_get_att()