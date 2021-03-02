# wrap imagemagick for PDF to PNG conversion

import os, sys

def main(*args):
    print("Slice Drawings for Job")
    print(" ".join(args))

    job_id = args[0]
    job_path = args[1]

    width = 1300
    # width = 640
    width_offset = 1150
    # width_offset = 540
    height = 1300
    # height = 480
    height_offset = 900
    # height_offset = 380
    
    ret = os.popen("magick convert "+job_path+job_id+"-*.png -crop "+str(width)+"x"+str(height)+"+"+str(0)+"+"+str(0)+" "+job_path+job_id+"_WATWATWAT_-A-0.png")
    wat = ret.read()
    print(wat)
    
    ret = os.popen("magick convert "+job_path+job_id+"-*.png -crop "+str(width)+"x"+str(height)+"+"+str(width_offset)+"+"+str(0)+" "+job_path+job_id+"_WATWATWAT_-A-1.png")
    wat = ret.read()
    print(wat)
    
    return "ok"

if __name__ == '__main__':
    main(sys.argv)