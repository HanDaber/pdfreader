# wrap imagemagick for PDF to PNG conversion

import os
import sys

def main(*args):
    print("Crop out Values for Job")
    print(" ".join(args))
    # ret = os.popen("magick convert -crop 515-208105-001_A_ramaswamyd.pdf \"515-208105-001_A_ramaswamyd-%03d.png\"")
    # ret = os.popen("ls -l")
    # wat = ret.read()
    # print(wat)
    return "ok"

if __name__ == '__main__':
    main(sys.argv)