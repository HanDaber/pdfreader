# main pipeline

import sys, glob, time
import pipeline as pipeline

def main(*args):
    print("Process PDFs in directory")
    print(" ".join(args))

    pdf_dir = args[0]

    print(f'PDF directory {pdf_dir}')

    for pdf_file in glob.iglob(f'{pdf_dir}/*.pdf'):
        job_id = pdf_file.split(pdf_dir)[-1].split(".pdf")[0]
        print(f'Running pipeline for job {job_id} on file {pdf_file}')
        ran_pipeline = pipeline.main(job_id, pdf_file)
        print(ran_pipeline)

if __name__ == '__main__':
    main(*sys.argv[1:])