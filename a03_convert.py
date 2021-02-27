# wrap imagemagick for PDF to PNG conversion

import sys
import os

def main(*args):
    print("Convert PDF to PNG for Job")
    print(" ".join(args))
    file_name = args[0]+".pdf"
    ret = os.popen("magick convert "+file_name+" "+args[0]+"-%03d.png")
    wat = ret.read()
    print(wat)
    return "ok"

if __name__ == '__main__':
    main(sys.argv)