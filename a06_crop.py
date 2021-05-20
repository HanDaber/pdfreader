# wrap imagemagick for cropping

import os, glob, sys, json

import ResultsDB as Results
import CropsDB as Crops

MINIMUM_CONFIDENCE_THRESHOLD = 0.5

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

    cmd_crop = f"echo 'CROP' > /dev/null"
    cmd_filename = f'artifacts/{job_id}/crops/%[filename:base]_crop_'

    collect_results = []
    collect_crops = []

    with open(results_file, 'rb') as finput:
        vision_results = json.load(finput)
        predictions = vision_results['predictions']

        for index, prediction in enumerate(predictions):
            probability = prediction['probability']

            if probability < MINIMUM_CONFIDENCE_THRESHOLD:
                continue

            boundingBox = prediction['boundingBox']
            tag = prediction['tagName']
            tagId = prediction['tagId']

            left = int(boundingBox['left'] * 616) + int(boundingBox['width'] * 616) - 4
            top = int(boundingBox['top'] * 600) # - 5
            width = int(boundingBox['width'] * 616) * 5
            height = int(boundingBox['height'] * 600) # + 10

            if tag == 'plusminusvertical':
                width += 20
                height += 20

            # Only crop and save if its not cut off by too much
            if (left + width) > (616 + 100):
                continue

            # image_tweak_options = '-resize x600 +repage -sharpen 0x5.0'
            # image_tweak_options = '-density 300 +repage -sharpen 0x5.0'
            image_tweak_options = '-density 600 +repage -resize x200 +repage -sharpen 0x5'

            result_slice = results_file.replace("results", "slices").replace(".json", ".png")
            result_slice_file = result_slice.split("/")[-1].split(".")[0]

            # print(f"tag: ({index}):{tag}, probability: {probability}, left: {left}, top: {top}, width: {width}, height: {height}")

            crop_image_file = f'{result_slice_file}_crop_{tag}_{str(index)}.png'

            # print(f'{crop_image_file} RIGHT: {left + width} out of 616')

            crop_data = (job_id, crop_image_file, left, top, width, height)
            collect_crops.append(crop_data)

            tag_bb = json.dumps(boundingBox)
            val_bb = json.dumps({
                'left': left,
                'top': top,
                'width': width,
                'height': height,
            })
            results_data = (job_id, index, tag, probability, tag_bb, result_slice_file, None, None, val_bb)
            collect_results.append(results_data)

            cmd_convert = "magick convert "+result_slice+" +repage -set filename:base '%[basename]' -crop "
            cmd_crop += f" && {cmd_convert}{str(width)}x{str(height)}+{str(left)}+{str(top)} +repage {image_tweak_options} +repage {cmd_filename}{tag}_{str(index)}.png"

        # print(cmd_crop)
        ret = os.popen(f'{cmd_crop}')
        wat = ret.read()
        # print(wat)

    Results.insert_rows(collect_results) # ((job_id, index, tag, probability, json.dumps(boundingBox), result_slice_file, None, None, None))
    Crops.insert_rows(collect_crops)

    return "ok"

if __name__ == '__main__':
    main(*sys.argv[1:])