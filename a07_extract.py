# extract vales with tesseract

import sys, os

def main(*args):
    print("Extract Symbols & Values for Job")
    print(" ".join(args))

    job_id = args[0]
    job_path = args[1]

    output = ""

    filelist = os.popen("ls "+job_path+"crops/ | grep '.png'")
    for index, image_file in enumerate(filelist):

        # if index != 13:
        #     continue

        image_file_name = image_file.rstrip()
        job_file = job_path+"crops/"+image_file_name
        tag = image_file_name.split("crop_")[-1].split("_")[0]

        # cmd = f'tesseract {job_file} {job_path}results/result_{str(index)}_{image_file_name} digits'
        
        cmd = f'tesseract {job_file} stdout --oem 1 --dpi 72 digits'
        print(cmd)

        ret = os.popen(cmd)
        wat = ret.read().rstrip().lstrip().split('\n')
        # print(wat)

        results = [result for result in wat if result.rstrip()]
        print(index, results)

        # if len(results) > 0:
            # value = results[-1]
        for x, value in enumerate(results):
            print(value)
            vals = [f'.{v}' for v in value.split('.') if v.rstrip()]
            print(vals)

            if len(vals) > 1:
                v = format_value(vals[0])
                print('v', v)
                for val in vals[1:]:
                    tolerance = format_value(val)
                    print(tolerance)
                    if float(tolerance) > 0:
                        output += f'\n{index}-{x} {job_id} {tag}: {v} +/- {tolerance} @ probability ({image_file_name.split(".png")[0]})'
            else:
                value = format_value(value)
                print(value)
                if float(value) > 0:
                    output += f'\n{index}-{x} {job_id} {tag}: {value} @ probability ({image_file_name.split(".png")[0]})'
    
    with open(f'{job_id}/results/values.txt', 'w') as outfile:
            outfile.write(output)

    return "ok"

def format_value(v):
    if v.startswith('0'):
        v = f'0.{v[:3]}'
    elif v.startswith('.'):
        v = f'0{v[:4]}'
    return v

if __name__ == '__main__':
    main(*sys.argv[1:])