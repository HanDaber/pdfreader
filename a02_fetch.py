import sys
import os

def main(*args):
    print("Download file for Job")
    print(" ".join(args))
    file_name = args[0]+".pdf"
    ret = os.popen("wget -O "+file_name+" "+args[1])
    wat = ret.read()
    print(wat)
    return file_name

if __name__ == '__main__':
    main(sys.argv)