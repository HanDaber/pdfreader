# extract vales with tesseract

import sys, os

def main(*args):
    print("Extract Symbols & Values for Job")
    print(" ".join(args))

    job_id = args[0]
    job_path = args[1]

    ret = os.popen("tesseract "+job_path+job_id+"_WATWATWAT_-A-0_CROP_1.png stdout digits")
    wat = ret.read()
    print(wat)

    return "ok"

if __name__ == '__main__':
    main(sys.argv)