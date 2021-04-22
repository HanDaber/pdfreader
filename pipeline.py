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
    open_flag = ('--open' in FLAGS or '-o' in FLAGS) or False

    a01_skip_flag = ('--skip-1' in FLAGS or '-1' in FLAGS) or False
    a02_skip_flag = ('--skip-2' in FLAGS or '-2' in FLAGS) or False
    a03_skip_flag = ('--skip-3' in FLAGS or '-3' in FLAGS) or False
    a04_skip_flag = ('--skip-4' in FLAGS or '-4' in FLAGS) or False
    a05_skip_flag = ('--skip-5' in FLAGS or '-5' in FLAGS) or False
    a06_skip_flag = ('--skip-6' in FLAGS or '-6' in FLAGS) or False
    a07_skip_flag = ('--skip-7' in FLAGS or '-7' in FLAGS) or False
    a08_skip_flag = ('--skip-8' in FLAGS or '-8' in FLAGS) or False
    
    markup_symbol_flag = False
    markup_symbol_flag_matches = [x for x in FLAGS if '--markup-symbol=' in x]
    if len(markup_symbol_flag_matches) > 0:
        markup_symbol_flag = markup_symbol_flag_matches[0].split("=")[1].split(" ")[0]

    print(f'force_flag: "{force_flag}"')
    print(f'debug_flag: "{debug_flag}"')
    print(f'open_flag: "{open_flag}"')
    print(f'markup_symbol_flag: "{markup_symbol_flag}"')

    try:
        # try a better query
        Jobs.insert((datetime.now(), job_id, 'PENDING', 10, 5.00))
        # Jobs.hydrate()
    except:
        print("Job Exists!")
        if not force_flag:
            print("Aborting")
            return False

    # all_jobs = Jobs.list_jobs()
    # print(f'All Jobs: {all_jobs}')

    # # SET UP FILE SYSTEM
    madedir = os.popen(f'mkdir -p artifacts').read()
    print(f"Initialized Directories {madedir}")

    Jobs.update_status(job_id, 'INITIALIZING')
    print(f'Job {job_id} INITIALIZING')
    job_path = f"artifacts/{job_id}/"
    print(f"Job Path {job_path}")

    dirmade = os.popen(f'mkdir -p {job_path} {job_path}slices {job_path}crops {job_path}results {job_path}markup && ls {job_path}')
    madedir = dirmade.read().replace('\n', ' ')
    print(f"Initialized Artifact Directories {madedir}")

    Jobs.update_status(job_id, 'CONVERTING')
    print(f'Job {job_id} CONVERTING')
    if a03_skip_flag:
        print("\nNOOP\n")
    else:
        converted_files = convert.main(job_id, pdf_path)
        print(f'\nFinished Converting {converted_files}\n')
    
    Jobs.update_status(job_id, 'SLICING')
    print(f'Job {job_id} SLICING')
    sliced_path = job_path+"slices"
    if a04_skip_flag:
        print("\nNOOP\n")
    else:
        sliced_path = make_slices.main(job_id, job_path)
        print(f'\nFinished Slicing {sliced_path}\n')
    
    Jobs.update_status(job_id, 'ANALYZING')
    print(f'Job {job_id} ANALYZING')
    if a05_skip_flag:
        print("\nNOOP\n")
    else:
        for slice_file in glob.iglob(f'{sliced_path}/*.png'):
            analyzed = analyze.main(job_id, slice_file.rstrip())
            time.sleep(0.1)
        print(f'\nFinished Analyzing {job_id}\n')
    
    Jobs.update_status(job_id, 'CROPPING')
    print(f'Job {job_id} CROPPING')
    results_path = job_path+"results"
    if a06_skip_flag:
        print("\nNOOP\n")
    else:
        for results_file in glob.iglob(f'{results_path}/*.json'):
            cropped_values = crop.main(job_id, results_file.rstrip())
        print(f'\nFinished Cropping {job_id}\n')

    Jobs.update_status(job_id, 'EXTRACTING')
    print(f'Job {job_id} EXTRACTING')
    if a07_skip_flag:
        print("\nNOOP\n")
    else:
        extracted_values = extract.main(job_id, job_path)
        print(f'\nFinished Extracting Values {extracted_values}\n')

    Jobs.update_status(job_id, 'REDLINING')
    print(f'Job {job_id} REDLINING')
    marked_up_drawings_file_path = None
    if a08_skip_flag:
        print("\nNOOP\n")
    else:
        marked_up_drawings_file_path = markup.main(job_id, job_path, markup_symbol_flag)
        print(f'\nFinished Redlining Drawings {marked_up_drawings_file_path}\n')

    Jobs.update_status(job_id, 'COMPLETE')
    print(f'Job {job_id} COMPLETE')

    # results = Results.find(job_id)
    # print(f'Results {results}'.replace("{", "\n\t{").replace("}", "}\n"))

    if not debug_flag:
        dircleaned = os.popen(f'rm -r {job_path}slices/ {job_path}crops/')
        cleaneddir = dircleaned.read().replace('\n', ' ')
        print(f"Cleanup Artifact Directories {cleaneddir}")

    if open_flag:
        open_file = os.popen(f'open {marked_up_drawings_file_path}')
        opened = open_file.read().replace('\n', ' ')
        print(f"Open redline {opened}")

    return job_path

def list_artifacts_dirs(job_path):
    for path in ['slices', 'crops', 'results']:
        ls = os.popen(f'ls -l {job_path}{path}').read()
        print(f"List {path}: {ls}")

# def _setup():
# def _convert():
# def _slice():
# def _analyze():
# def _crop():
# def _extract():
# def _markup():



if __name__ == '__main__':
    main(*sys.argv[1:])