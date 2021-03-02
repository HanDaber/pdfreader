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

    cleandir = os.popen("rm "+job_id+"/*")
    dircleaned = cleandir.read()
    print(dircleaned)

    ret = os.popen("wget -O "+output_file_path+" "+file_url)
    wat = ret.read()
    print(wat)

    return job_id+"/"

if __name__ == '__main__':
    main(sys.argv)