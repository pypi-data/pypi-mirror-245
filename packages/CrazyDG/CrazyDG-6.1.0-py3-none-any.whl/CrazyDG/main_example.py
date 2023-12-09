from crazy      import CrazyDragon # >>> from CrazyDG import CrazyDragon
from navigation import Navigation  # >>> from CrazyDG import Navigation
from control    import Controller  # >>> from CrazyDG import Controller
from recorder   import Recorder    # >>> from CrazyDG import Recorder
from guidance   import utils       # >>> from CrazyDG import utils

from cflib                         import crtp
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.utils                   import uri_helper

import datetime


cfs = {
    'cf1': None
}

ctr_config = {
    'dt': 0.1,
    'n' : 5
}


d = datetime.datetime.now()
date      = f'{d.year}-{d.month}-{d.day:02}-{d.hour:02}-{d.minute:02}-{d.second:02}'



uri = uri_helper.uri_from_env( default='radio://0/80/2M/E7E7E7E702' )


if __name__ == "__main__":

    crtp.init_drivers()
    
    _cf = CrazyDragon()

    NAV = Navigation( _cf )
    CTR = Controller( _cf, ctr_config )
    RCD = Recorder( _cf, CTR, 'cf1', date )

    cfs['cf1'] = _cf

    with SyncCrazyflie( uri, cf=_cf ) as scf:

        Navigation.init_qualisys( cfs )

        NAV.start()
        CTR.start()
        RCD.start()

        ## your guidance function ##
        CTR.init_send_setpoint()
        ##       from here        ##

        utils.takeoff( _cf )

        utils.hover( _cf, T=2 )

        utils.goto( _cf, [2.0,2.0,2.0], T=5 )

        utils.hover( _cf, T=2 )

        utils.landing_supporter( _cf, RCD )

        ############################

        CTR.stop_send_setpoint()

        NAV.join()
        CTR.join()
        RCD.join()

    NAV.qtm.close()
