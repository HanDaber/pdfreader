# ML API

import os, sys, requests, json, urllib.parse

def main(*args):
    # print("ML Analysis for Job")
    # print(" ".join(args))

    job_id = args[0]
    job_file = args[1]

    url = 'https://westus2.api.cognitive.microsoft.com/customvision/v3.0/Prediction/f1b76c02-5fc5-4f7d-bb13-2d4b4bc71a27/detect/iterations/Iteration3/image'

    headers = {
        'Content-Type': 'application/octet-stream',
        'Prediction-key': '45b1c87da4be4e30801ccdab520f6cab',
    }

    params = urllib.parse.urlencode({
        'application': '{string}',
    })

    response = {'id': 'NULL'}

    with open(job_file, 'rb') as finput:
        response_data = requests.post(url, data=finput, headers=headers)
        response = response_data.json()

        slice_results_file = job_file.replace(f'artifacts/{job_id}/slices/', "").replace(".png", ".json")

        with open(f'artifacts/{job_id}/results/{slice_results_file}', 'w') as outfile:
            json.dump(response, outfile)

    return response['id']

if __name__ == '__main__':
    main(*sys.argv[1:])