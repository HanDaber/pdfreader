# wrap imagemagick for PDF to PNG conversion

import sys, os

def main(*args):
    print(f"Convert PDF to PNG for Job {' '.join(args)}")

    job_id = args[0]
    # job_path = args[1]
    pdf_path = args[1]

    params = '-density 200 -quality 50 -alpha remove -resample 200 -colorspace RGB -antialias'
    ret = os.popen(f'magick convert {params} {pdf_path} artifacts/{job_id}/{job_id}-%03d.png')
    wat = ret.read()
    print(wat)

    return f'artifacts/{job_id}'

if __name__ == '__main__':
    main(*sys.argv[1:])