# wrap imagemagick for cropping

import os, glob, sys, json

import ResultsDB as Results

def main(*args):
    # print("Crop out Values for Job")
    # print(" ".join(args))

    job_id = args[0]
    results_file = args[1]

    # prediction = {
    #   "probability": 0.0,
    #   "tagId": "00000000-0000-0000-0000-000000000000",
    #   "tagName": "string",
    #   "boundingBox": {
    #     "left": 500,
    #     "top": 200,
    #     "width": 300,
    #     "height": 150
    #   },
    #   "tagType": "Regular"
    # }

    # results_path = job_path+"results/"
    cmd_crop = f"echo 'CROPPING'"
    cmd_filename = f'artifacts/{job_id}/crops/%[filename:base]_crop_'

    collect_results = []

    with open(results_file, 'rb') as finput:
        vision_results = json.load(finput)
        predictions = vision_results['predictions']

        for index, prediction in enumerate(predictions):
            probability = prediction['probability']

            if probability < 0.5:
                continue

            boundingBox = prediction['boundingBox']
            tag = prediction['tagName']
            tagId = prediction['tagId']
            # left = int(boundingBox['left'] * 1300) - 75
            left = int(boundingBox['left'] * 616) - 75
            # top = int(boundingBox['top'] * 1300) - 25
            top = int(boundingBox['top'] * 600) - 25
            width = 250
            height = 75

            result_slice = results_file.replace("results", "slices").replace(".json", ".png")
            result_slice_file = result_slice.split("/")[-1].split(".")[0]
            
            print(f"tag: ({index}):{tag}, probability: {probability}, left: {left}, top: {top}, width: {width}, height: {height}")
            
            # Results.insert((job_id, index, tag, probability, json.dumps(boundingBox), result_slice_file, None, None, None))
            collect_results.append((job_id, index, tag, probability, json.dumps(boundingBox), result_slice_file, None, None, None))

            cmd_convert = "magick convert "+result_slice+" +repage -set filename:base '%[basename]' -crop "
            cmd_crop += f" && {cmd_convert}{str(width)}x{str(height)}+{str(left)}+{str(top)} +repage -resize x600 +repage -sharpen 0x5.0 +repage {cmd_filename}{tag}_{str(index)}.png"

        # print(cmd_crop)
        ret = os.popen(f'{cmd_crop}')
        # wat = ret.read()
        # print(wat)

    Results.insert_rows(collect_results) # ((job_id, index, tag, probability, json.dumps(boundingBox), result_slice_file, None, None, None))

    return "ok"

if __name__ == '__main__':
    main(*sys.argv[1:])