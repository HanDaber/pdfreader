# main pipeline

import sys, os, glob, time
from datetime import datetime

# import a01_query as query
# import a02_fetch as fetch
import a03_convert as convert
import a04_slice as make_slices
import a05_analyze as analyze
import a06_crop as crop
import a07_extract as extract

import JobsDB as Jobs


db_name = 'TEST_DB_1'
table_name = 'test_table_1'

def main(*args):
    print("Run Pipeline for Job")
    print(" ".join(args))

    job_id = args[0]
    pdf_path = args[1]

    force_flag = False
    try:
        if args[2] == '--force' or args[2] == '-f':
            force_flag = True
    except:
        pass

    print(f'Job ID: {job_id}')

    Jobs.init(db_name, table_name)

    try:
        Jobs.insert(db_name, table_name, (datetime.now(), job_id, 'PENDING', 10, 5.00))
        # Jobs.hydrate(db_name, table_name)
    except:
        print("Job Exists!")
        if not force_flag:
            print("Exiting")
            exit(0)
    
    all_jobs = Jobs.list_jobs(db_name, table_name)

    print(f'All Jobs: {all_jobs}')

    # TEST RUNS:
    # job_id = "test_2"
    # job_file_url = "https://www.a.com/file.pdf"

    # job_id = "bcd_234"
    # job_file_url = "https://ed.iitm.ac.in/~raman/Autodesk%20Inventor%20Practice%20Part%20Drawings.pdf"

    print(f'Job {job_id}')

    # QUERY FOR JOBS:
    # got_jobs = query.main("abc", "123")
    # print(got_jobs)

    dirmade = os.popen(f'mkdir {job_id} {job_id}/slices {job_id}/crops {job_id}/results')
    madedir = dirmade.read()
    print(madedir)
    
    # job_path = fetch.main(job_id, job_file_url)
    # print(job_path)
    job_path = job_id+"/"

    converted_files = convert.main(job_id, pdf_path)
    print(converted_files)

    sliced_path = make_slices.main(job_id, job_path)
    print(sliced_path)
    # sliced_path = job_path+"slices"

    for slice_file in glob.iglob(f'{sliced_path}/*.png'):
        print(f'Analyzing {slice_file}')

        analyzed = analyze.main(job_id, slice_file.rstrip())
        print(f'{analyzed}\n')

        time.sleep(0.1)

    results_path = job_path+"results"

    for results_file in glob.iglob(f'{results_path}/*.json'):
        cropped_values = crop.main(job_id, results_file.rstrip())
        print(cropped_values)

    extracted_values = extract.main(job_id, job_path)
    print(extracted_values)

    Jobs.update_status(db_name, table_name, job_id, 'COMPLETE')

    all_jobs = Jobs.list_jobs(db_name, table_name)

    print(f'All Jobs: {all_jobs}')

    return job_path

if __name__ == '__main__':
    main(*sys.argv[1:])