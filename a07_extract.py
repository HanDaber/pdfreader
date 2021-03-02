# extract vales with tesseract

import sys, os

def main(*args):
    print("Extract Symbols & Values for Job")
    print(" ".join(args))

    job_id = args[0]
    job_path = args[1]

    print('NOOP')
    return "ok"

if __name__ == '__main__':
    main(sys.argv)