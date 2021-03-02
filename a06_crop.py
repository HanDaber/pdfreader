# wrap imagemagick for PDF to PNG conversion

import os, sys

def main(*args):
    print("Crop out Values for Job")
    print(" ".join(args))

    job_id = args[0]
    job_path = args[1]

    prediction = {
      "probability": 0.0,
      "tagId": "00000000-0000-0000-0000-000000000000",
      "tagName": "string",
      "boundingBox": {
        "left": 500,
        "top": 200,
        "width": 300,
        "height": 150
      },
      "tagType": "Regular"
    }
    width = prediction['boundingBox']['width']
    height = prediction['boundingBox']['height']
    left = prediction['boundingBox']['left']
    top = prediction['boundingBox']['top']

    ret = os.popen("magick convert "+job_path+job_id+"_WATWATWAT_-A-0.png -crop "+str(width)+"x"+str(height)+"+"+str(left)+"+"+str(top)+" "+job_path+job_id+"_WATWATWAT_-A-0_CROP_1.png")
    wat = ret.read()
    print(wat)

    return "ok"

if __name__ == '__main__':
    main(sys.argv)