# wrap imagemagick for PDF to PNG conversion

import os
import sys

def main(*args):
    print("Slice Drawings for Job")
    print(" ".join(args))
    width = 1300
    width_offset = 1150
    height = 1300
    height_offset = 900
    
    ret = os.popen("magick convert "+args[0]+"-*.png -crop "+width+"x"+height+"+"+0+"+"+0+" fler-000-0.png")
    wat = ret.read()
    print(wat)
    # ret = os.popen("magick convert 515-208105-001_A_ramaswamyd-000.png -crop 360x240+340+0 fler-000-1.png")
    # wat = ret.read()
    # print(wat)
    return "ok"

if __name__ == '__main__':
    main(sys.argv)