# wrap imagemagick for PDF to PNG conversion

import sys, os

def main(*args):
    print("Convert PDF to PNG for Job")
    print(" ".join(args))

    job_id = args[0]
    job_path = args[1]

    ret = os.popen("magick convert "+job_path+job_id+".pdf "+job_path+job_id+"-%03d.png")
    wat = ret.read()
    print(wat)

    return "ok"

if __name__ == '__main__':
    main(sys.argv)