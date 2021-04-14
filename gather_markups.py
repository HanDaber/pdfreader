# main pipeline

import sys, glob, os

def main(*args):
    print("Gather markups from all jobs")
    print(" ".join(args))

    pdf_dir = args[0]

    print(f'PDF directory {pdf_dir}')
    ret = os.popen(f'mkdir -p export export/redlines export/artifacts')
    wat = ret.read()
    print(wat)

    cmd_copy = "echo 'GATHERING REDLINES'"

    for redline in glob.iglob(f'artifacts/**/markup/*.pdf'):
        # print(f'markup: {redline}')
        cmd_copy += f' && cp {redline} export/redlines/'

    for page in glob.iglob(f'artifacts/**/markup/*.png'):
        print(f'page: {page}')
        cmd_copy += f' && mkdir -p export/artifacts/{page.split("/")[-3]} && cp {page} export/{page.replace("markup/", "").replace("_markup", "")}'

    ret = os.popen(cmd_copy)
    wat = ret.read()
    print(wat)

if __name__ == '__main__':
    main(*sys.argv[1:])