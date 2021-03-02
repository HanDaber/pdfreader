# ML API

import os, sys, http.client, urllib.request, urllib.parse, urllib.error, base64

def main(*args):
    print("ML Analysis for Job")
    print(" ".join(args))

    job_id = args[0]
    job_path = args[1]

    # https://westus2.api.cognitive.microsoft.com/customvision/v3.0/Prediction/aa3bd785-c90f-4d43-a8fc-1567467df42e/detect/iterations/3x3_phase1/image
    # Set Prediction-Key Header to : da69c82337ea46a1a5b53b517c48abfe
    # Set Content-Type Header to : application/octet-stream
    # Set Body to : <image file>

    headers = {
        # Request headers
        'Content-Type': 'application/octet-stream',
        'Prediction-key': 'da69c82337ea46a1a5b53b517c48abfe',
    }

    params = urllib.parse.urlencode({
        # Request parameters
        'application': '{string}',
    })

    job_file_a = job_path+job_id+"_WATWATWAT_-A-0.png"

    filethere = os.popen("ls -l "+job_file_a)
    isfilethere = filethere.read()
    print(isfilethere)

    return "ok"

    # url_path = "/customvision/v3.1/Prediction/aa3bd785-c90f-4d43-a8fc-1567467df42e/detect/iterations/3x3_phase1/image"

    # try:
    #     conn = http.client.HTTPSConnection('westus2.api.cognitive.microsoft.com')
    #     conn.request("POST", url_path+"?%s" % params, open(job_file_a, "rb"), headers)
    #     # conn.request("POST", "/customvision/v3.1/Prediction/aa3bd785-c90f-4d43-a8fc-1567467df42e/detect/iterations/3x3_phase1/image?%s" % params, "{body}", headers)
    #     response = conn.getresponse()
    #     data = response.read()
    #     print("Data: "+str(data))
    #     conn.close()
    # except Exception as e:
    #     print("[Errno {0}] {1}".format(e.errno, e.strerror))

    # return "ok"

if __name__ == '__main__':
    main(sys.argv)