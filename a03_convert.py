# wrap imagemagick for PDF to PNG conversion

import sys, os

def main(*args):
    print("Convert PDF to PNG for Job")
    print(" ".join(args))

    job_id = args[0]
    # job_path = args[1]
    pdf_path = args[1]

    # ret = os.popen("magick convert -density 200 -quality 50 -alpha remove -resample 200 -antialias "+job_path+job_id+".pdf "+job_path+job_id+"-%03d.png")
    ret = os.popen(f'magick convert -density 200 -quality 50 -alpha remove -resample 200 -antialias {pdf_path} {job_id}/{job_id}-%03d.png')
    wat = ret.read()
    print(wat)

    return "ok"

if __name__ == '__main__':
    main(*sys.argv[1:])