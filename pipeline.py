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
import a08_markup as markup

import JobsDB as Jobs
import CropsDB as Crops
import ResultsDB as Results
import ArtifactsDB as Artifacts

def main(*args):
    print(f"Run Pipeline on File: {' '.join(args)}")
    # print(" ".join(args))

    # job_id = args[0]
    # pdf_path = args[1]
    
    pdf_path = args[0]
    FLAGS = args[1:]

    job_id = pdf_path.split("/")[-1].split(".")[0]

    print(f'Job ID: {job_id}')

    Jobs.init()
    Crops.init()
    Results.init()
    Artifacts.init()

    force_flag = ('--force' in FLAGS or '-f' in FLAGS) or False
    debug_flag = ('--debug' in FLAGS or '-d' in FLAGS) or False

    print(f'Flags: --force={force_flag}, --debug={debug_flag}')

    try:
        Jobs.insert((datetime.now(), job_id, 'PENDING', 10, 5.00))
        # Jobs.hydrate()
    except:
        print("Job Exists!")
        if not force_flag:
            print("Aborting")
            return False
    
    # all_jobs = Jobs.list_jobs()
    # print(f'All Jobs: {all_jobs}')

    # TEST RUN DATA:
    # job_id = "test_2"
    # job_file_url = "https://www.a.com/file.pdf"
    # job_id = "bcd_234"
    # job_file_url = "https://ed.iitm.ac.in/~raman/Autodesk%20Inventor%20Practice%20Part%20Drawings.pdf"



    # QUERY FOR JOBS - keep
    # got_jobs = query.main("abc", "123")
    # print(got_jobs)

    # # SET UP FILE SYSTEM
    madedir = os.popen(f'mkdir -p artifacts').read()
    print(f"Initialized Directories {madedir}")

    Jobs.update_status(job_id, 'INITIALIZING')
    print(f'Job {job_id} INITIALIZING')
    # job_path = fetch.main(job_id, job_file_url) # skip for now
    # print(job_path)
    # job_path = job_id+"/"
    job_path = f"artifacts/{job_id}/"
    print(f"Job Path {job_path}")

    dirmade = os.popen(f'mkdir -p {job_path} {job_path}slices {job_path}crops {job_path}results {job_path}markup && ls {job_path}')
    madedir = dirmade.read().replace('\n', ' ')
    print(f"Initialized Artifact Directories {madedir}")
    """
    Jobs.update_status(job_id, 'CONVERTING')
    print(f'Job {job_id} CONVERTING')
    converted_files = convert.main(job_id, pdf_path)
    print(f'\nFinished Converting {converted_files}\n')

    Jobs.update_status(job_id, 'SLICING')
    print(f'Job {job_id} SLICING')
    sliced_path = make_slices.main(job_id, job_path)
    print(f"Sliced Path {sliced_path}")
    print(f'\nFinished Slicing {sliced_path}\n')
    # """
    sliced_path = job_path+"slices"
    """
    Jobs.update_status(job_id, 'ANALYZING')
    print(f'Job {job_id} ANALYZING')
    if debug_flag:
        print("\nNOOP\n")
    else:
        print(f'Analyzing {job_id}')
        for slice_file in glob.iglob(f'{sliced_path}/*.png'):
            analyzed = analyze.main(job_id, slice_file.rstrip())
            time.sleep(0.1)
        print(f'\nFinished Analyzing {job_id}\n')

    Jobs.update_status(job_id, 'CROPPING')
    print(f'Job {job_id} CROPPING')
    results_path = job_path+"results"
    print(f"Results Path {sliced_path}")
    print(f'Cropping {job_id}')
    for results_file in glob.iglob(f'{results_path}/*.json'):
        cropped_values = crop.main(job_id, results_file.rstrip())
    print(f'\nFinished Cropping {job_id}\n')
    """
    Jobs.update_status(job_id, 'EXTRACTING')
    print(f'Job {job_id} EXTRACTING')
    print(f'Extracting Values for {job_id}')
    extracted_values = extract.main(job_id, job_path)
    print(f'\nFinished Extracting Values {extracted_values}\n')

    Jobs.update_status(job_id, 'MARKING')
    print(f'Job {job_id} MARKING')
    print(f'Marking up Drawings for {job_id}')
    marked_up_drawings_dir = markup.main(job_id, job_path)
    print(f'\nFinished Marking up Drawings {marked_up_drawings_dir}\n')
    # """
    Jobs.update_status(job_id, 'COMPLETE')
    print(f'Job {job_id} COMPLETE')

    # results = Results.find(job_id)
    # print(f'Results {results}'.replace("{", "\n\t{").replace("}", "}\n"))

    # all_jobs = Jobs.list_jobs()
    # print(f'All Jobs: {all_jobs}')

    if not debug_flag:
        dircleaned = os.popen(f'rm -r {job_path}slices/ {job_path}crops/')
        cleaneddir = dircleaned.read().replace('\n', ' ')
        print(f"Cleanup Artifact Directories {cleaneddir}")

    return job_path

def list_artifacts_dirs(job_path):
    for path in ['slices', 'crops', 'results']:
        ls = os.popen(f'ls -l {job_path}{path}').read()
        print(f"List {path}: {ls}")



if __name__ == '__main__':
    main(*sys.argv[1:])