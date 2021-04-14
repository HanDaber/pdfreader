# main pipeline

import sys, glob, os
import pipeline as pipeline

def main(*args):
    print("Gather markups from all jobs")
    print(" ".join(args))

    pdf_dir = args[0]

    print(f'PDF directory {pdf_dir}')
    ret = os.popen(f'mkdir redlines')
    wat = ret.read()
    print(wat)

    cmd_move = "echo 'GATHERING REDLINES'"

    for redline in glob.iglob(f'artifacts/**/markup/*.pdf'):
        # print(f'markup: {redline}')
        cmd_move += f' && mv {redline} redlines/'

    ret = os.popen(cmd_move)
    wat = ret.read()
    print(wat)

if __name__ == '__main__':
    main(*sys.argv[1:])