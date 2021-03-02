# wrap imagemagick for PDF to PNG conversion

import os, sys

def main(*args):
    print("Crop out Values for Job")
    print(" ".join(args))

    job_id = args[0]
    job_path = args[1]

    ret = os.popen("magick convert "+job_path+job_id+"_WATWATWAT_-A-0.png -crop "+str(100)+"x"+str(30)+"+"+str(100)+"+"+str(100)+" "+job_path+job_id+"_WATWATWAT_-A-0_CROP_1.png")
    wat = ret.read()
    print(wat)

    return "ok"

if __name__ == '__main__':
    main(sys.argv)