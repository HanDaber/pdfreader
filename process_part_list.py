# main pipeline

import sys, glob, time, os
import pipeline as pipeline

def main(*args):
    print("Process PDFs in from a list")
    print(" ".join(args))

    part_list_file = args[0]
    source_pdf_directory = args[1]
    target_pdf_directory = args[2]

    print(f'Part List file {part_list_file}')
    print(f'Source PDF dir {source_pdf_directory}')
    print(f'Target PDF dir {target_pdf_directory}')
    
    part_numbers = []
    with open(part_list_file, 'r') as part_list:
        part_numbers = [x.strip() for x in part_list.readlines()]
    print(f'part_numbers: {part_numbers}')

    for part_number in part_numbers:
        ret = os.popen(f'ls {source_pdf_directory}/{part_number}.pdf')
        wat = ret.read().strip()
        if wat:
            print(f'source file {wat}')
            ret = os.popen(f'cp {source_pdf_directory}/{part_number}.pdf {target_pdf_directory}')
            wat = ret.read().strip()

            pdf_file = f'{target_pdf_directory}/{part_number}.pdf'
            job_id = pdf_file.split(target_pdf_directory)[-1].split('/')[1].split(".pdf")[0]
            print(f'Running pipeline for job {job_id} on file {pdf_file}')
            ran_pipeline = pipeline.main(pdf_file)
            print(ran_pipeline)
        else:
            print(f'no source file found for {part_number}')

if __name__ == '__main__':
    main(*sys.argv[1:])