from ...crazy import CrazyDragon

from .imu_setup import *

from cflib.crazyflie.log import LogConfig



period_in_ms = 10


class IMU:

    def __init__( self, cf: CrazyDragon ):

        self.cf = cf


    def start_get_vel( self, period_in_ms=period_in_ms ):
        log_conf = LogConfig( name="velocity", period_in_ms=period_in_ms )
        log_conf.add_variable( 'stateEstimate.vx', 'FP16' )
        log_conf.add_variable( 'stateEstimate.vy', 'FP16' )
        log_conf.add_variable( 'stateEstimate.vz', 'FP16' )

        self.cf.log.add_config( log_conf )
        log_conf.data_received_cb.add_callback( self.velocity_callback )
        log_conf.start()
 

    def start_get_acc(self, period_in_ms=period_in_ms):
        log_conf = LogConfig( name='acceleration', period_in_ms=period_in_ms )
        log_conf.add_variable( 'acc.x', 'FP16' )      ## m/s^2
        log_conf.add_variable( 'acc.y', 'FP16' )      ## m/s^2
        log_conf.add_variable( 'acc.z', 'FP16' )      ## m/s^2

        self.cf.log.add_config( log_conf )
        log_conf.data_received_cb.add_callback( self.accelerate_callback )
        log_conf.start()


    def start_get_att( self, period_in_ms=period_in_ms ):
        log_conf = LogConfig( name='Euler_angle', period_in_ms=period_in_ms )
        log_conf.add_variable( 'stateEstimate.roll' , 'FP16' )
        log_conf.add_variable( 'stateEstimate.pitch', 'FP16' )
        log_conf.add_variable( 'stateEstimate.yaw'  , 'FP16' )

        self.cf.log.add_config( log_conf )
        log_conf.data_received_cb.add_callback( self.euler_callback )
        log_conf.start()


    def velocity_callback( self, timestamp, data, logconf ):
        self.cf.vel[0] = data['stateEstimate.vx']
        self.cf.vel[1] = data['stateEstimate.vy']
        self.cf.vel[2] = data['stateEstimate.vz']


    def accelerate_callback( self, timestamp, data, logconf ):
        self.cf.acc[0] = data['acc.x'] * 9.81
        self.cf.acc[1] = data['acc.y'] * 9.81
        self.cf.acc[2] = data['acc.z'] * 9.81
    

    def euler_callback(self, timestamp, data, logconf):
        self.cf.att[0] = data['stateEstimate.roll']
        self.cf.att[1] = data['stateEstimate.pitch']
        self.cf.att[2] = data['stateEstimate.yaw']