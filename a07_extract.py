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

        image_file_name = image_file.rstrip()
        job_file = job_path+"crops/"+image_file_name
        tag = image_file_name.split("crop_")[-1].split("_")[0]
    
        # cmd = "tesseract "+job_file+" "+job_path+"results/result_"+str(index)+"_"+image_file_name+" digits"
        # cmd = f'tesseract {job_file} {job_path}results/result_{str(index)}_{image_file_name} digits'
        cmd = f'tesseract {job_file} stdout --oem 1 --dpi 72 digits'
        # print(cmd)

        ret = os.popen(cmd)
        wat = ret.read().rstrip().lstrip().split('\n')

        results = [value for value in wat if value.rstrip()]
        if len(results) > 0:
            value = results[-1]
            if value.startswith('0'):
                value = f'0.{value}'
            output += f'\n{job_id} {tag} {value} {image_file_name}'
    
    with open(f'{job_id}/results/values.txt', 'w') as outfile:
            outfile.write(output)

    return "ok"

if __name__ == '__main__':
    main(sys.argv)