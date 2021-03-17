import sys, os

def main(*args):
    print("Download file for Job")
    print(" ".join(args))

    job_id = args[0]
    file_url = args[1]

    file_name = job_id+".pdf"
    output_file_path = job_id+"/"+file_name

    dirmade = os.popen("mkdir "+job_id)
    madedir = dirmade.read()
    print(madedir)

    dirmade = os.popen("mkdir "+job_id+"/slices")
    madedir = dirmade.read()
    print(madedir)

    dirmade = os.popen("mkdir "+job_id+"/crops")
    madedir = dirmade.read()
    print(madedir)

    dirmade = os.popen("mkdir "+job_id+"/results")
    madedir = dirmade.read()
    print(madedir)

    # Cleanup
    cleandir = os.popen("rm "+job_id+"/*")
    dircleaned = cleandir.read()
    print(dircleaned)

    cleandir = os.popen("rm "+job_id+"/slices/*")
    dircleaned = cleandir.read()
    print(dircleaned)

    cleandir = os.popen("rm "+job_id+"/crops/*")
    dircleaned = cleandir.read()
    print(dircleaned)

    cleandir = os.popen("rm "+job_id+"/results/*")
    dircleaned = cleandir.read()
    print(dircleaned)

    # ret = os.popen("wget -O "+output_file_path+" "+file_url)
    local_pdf = './715-247054-004_A.pdf'
    print(f'SKIPPING FILE DOWNLOAD, COPY {local_pdf} INSTEAD')
    ret = os.popen("cp "+local_pdf+" "+output_file_path)
    wat = ret.read()
    print(wat)

    return job_id+"/"

if __name__ == '__main__':
    main(sys.argv)