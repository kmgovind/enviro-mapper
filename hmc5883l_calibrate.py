#              .';:cc;.
#            .,',;lol::c.
#            ;';lddddlclo
#            lcloxxoddodxdool:,.
#            cxdddxdodxdkOkkkkkkkd:.
#          .ldxkkOOOOkkOO000Okkxkkkkx:.
#        .lddxkkOkOOO0OOO0000Okxxxxkkkk:
#       'ooddkkkxxkO0000KK00Okxdoodxkkkko
#      .ooodxkkxxxOO000kkkO0KOxolooxkkxxkl
#      lolodxkkxxkOx,.      .lkdolodkkxxxO.
#      doloodxkkkOk           ....   .,cxO;
#      ddoodddxkkkk:         ,oxxxkOdc'..o'
#      :kdddxxxxd,  ,lolccldxxxkkOOOkkkko,
#       lOkxkkk;  :xkkkkkkkkOOO000OOkkOOk.
#        ;00Ok' 'O000OO0000000000OOOO0Od.
#         .l0l.;OOO000000OOOOOO000000x,
#            .'OKKKK00000000000000kc.
#               .:ox0KKKKKKK0kdc,.
#                      ...
#
# Author: peppe8o
# https://peppe8o.com
#
# This script helps defining values to calibrate and correct hmc5883l direction

from i2c_hmc5883l import HMC5883
from time import sleep

i2c_HMC5883l = HMC5883(gauss=1.3)
# Set declination according to your position
i2c_HMC5883l.set_declination(-9,62)

Xmin=1000
Xmax=-1000
Ymin=1000
Ymax=-1000

while True:
    try:
     x, y, z = i2c_HMC5883l.get_axes()
     Xmin=min(x,Xmin)
     Xmax=max(x,Xmax)
     Ymin=min(y,Ymin)
     Ymax=max(y,Ymax)
     print(i2c_HMC5883l.get_axes())
     print("Xmin="+str(Xmin)+"; Xmax="+str(Xmax)+"; Ymin="+str(Ymin)+"; Ymax="+str(Ymax))
     sleep(0.01)

    except KeyboardInterrupt:
        print()
        print('Got ctrl-c')

        xs=1
        ys=(Xmax-Xmin)/(Ymax-Ymin)
        xb =xs*(1/2*(Xmax-Xmin)-Xmax)
        yb =xs*(1/2*(Ymax-Ymin)-Ymax)
        print("Calibration corrections:")
        print("xs="+str(xs))
        print("ys="+str(ys))
        print("xb="+str(xb))
        print("yb="+str(yb))
        break
