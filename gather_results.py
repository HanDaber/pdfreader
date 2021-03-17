# main pipeline

import sys, glob, time
import pipeline as pipeline

def main(*args):
    print("Gather rersults from all jobs")
    print(" ".join(args))

    pdf_dir = args[0]

    print(f'PDF directory {pdf_dir}')

    with open(f'all_values.txt', 'w') as outfile:
        for pdf_file in glob.iglob(f'{pdf_dir}/*.pdf'):
            job_id = pdf_file.split(pdf_dir)[-1].split(".pdf")[0]
            print(f'Getting results for job {job_id}')

            with open(f'{job_id}/results/values.txt', 'r') as finput:
                outfile.write(finput.read()+"\n")

if __name__ == '__main__':
    main(*sys.argv[1:])