# ML API

import os, sys, requests, json, urllib.parse

def main(*args):
    print("ML Analysis for Job")
    print(" ".join(args))

    job_id = args[0]
    job_file = args[1]

    # https://westus2.api.cognitive.microsoft.com/customvision/v3.0/Prediction/aa3bd785-c90f-4d43-a8fc-1567467df42e/detect/iterations/3x3_phase1/image
    # Set Prediction-Key Header to : da69c82337ea46a1a5b53b517c48abfe
    # Set Content-Type Header to : application/octet-stream
    # Set Body to : <image file>
    
    url = 'https://westus2.api.cognitive.microsoft.com/customvision/v3.1/Prediction/aa3bd785-c90f-4d43-a8fc-1567467df42e/detect/iterations/3x3_phase1/image'

    headers = {
        # Request headers
        'Content-Type': 'application/octet-stream',
        'Prediction-key': 'da69c82337ea46a1a5b53b517c48abfe',
    }

    params = urllib.parse.urlencode({
        # Request parameters
        'application': '{string}',
    })

    # job_file = job_file+"slices/"+job_id+"-000_slice_0.png"

    filethere = os.popen("ls "+job_file)
    isfilethere = filethere.read()
    print(isfilethere)

    with open(job_file, 'rb') as finput:
        response_data = requests.post(url, data=finput, headers=headers)
        response = response_data.json()

        slice_results_file = job_file.replace(f'{job_id}/slices/', "").replace(".png", ".json")
        # with open(f'{job_id}/results/{job_file.replace("test_2/slices/", "").replace(".png", ".json")}', 'w') as outfile:
        with open(f'{job_id}/results/{slice_results_file}', 'w') as outfile:
            json.dump(response, outfile)
    
    # print("SKIPPING API CALL")
    # with open("example.json") as example:
    #     response = json.load(example)

    return response['id']

if __name__ == '__main__':
    main(*sys.argv[1:])