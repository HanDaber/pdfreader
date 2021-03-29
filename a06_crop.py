# wrap imagemagick for PDF to PNG conversion

import os, glob, sys, json

def main(*args):
    print("Crop out Values for Job")
    print(" ".join(args))

    job_id = args[0]
    # job_path = args[1]
    results_file = args[1]
    # response = args[2]

    # predictions = response['predictions']

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

    # job_file_a = job_path+"slices/"+job_id+"-000_slice_0.png"
    # job_file_a = job_path+"customvisionpdf14003.png"
    # results_path = job_path+"results/"
    cmd_crop = "echo 'CROPPING'"
    cmd_filename = f'{job_id}/crops/%[filename:base]_crop_'

    # for results_file in glob.iglob(f'{results_path}/*.json'):

    with open(results_file, 'rb') as finput:
        print(results_file)
        vision_results = json.load(finput)
        predictions = vision_results['predictions']

        for index, prediction in enumerate(predictions):
            if prediction['probability'] < 0.25:
                continue
            
            tag = prediction['tagName']
            # left = int(prediction['boundingBox']['left'] * 1300) - 75
            left = int(prediction['boundingBox']['left'] * 616) - 75
            # top = int(prediction['boundingBox']['top'] * 1300) - 25
            top = int(prediction['boundingBox']['top'] * 600) - 25
            width = 250
            height = 75

            print(tag, left, top, width, height)

            result_slice = results_file.replace("results", "slices").replace(".json", ".png")
            cmd_convert = "magick convert "+result_slice+" +repage -set filename:base '%[basename]' -crop "
            # cmd_crop += " && "+cmd_convert+str(width)+"x"+str(height)+"+"+str(left)+"+"+str(top)+" "+cmd_filename+tag+"_"+str(index)+".png"
            cmd_crop += " && "+cmd_convert+str(width)+"x"+str(height)+"+"+str(left)+"+"+str(top)+" +repage -resize x600 +repage -sharpen 0x5.0 +repage "+cmd_filename+tag+"_"+str(index)+".png"
            
            # cmd_crop = cmd_convert+str(width)+"x"+str(height)+"+"+str(left)+"+"+str(top)+" "+cmd_filename+str(index)+".png"

        print(cmd_crop)
        ret = os.popen(cmd_crop)
        wat = ret.read()
        print(wat)

    return "ok"

if __name__ == '__main__':
    main(*sys.argv[1:])