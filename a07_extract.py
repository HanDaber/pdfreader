# extract vales with tesseract

import sys, os, json

import ResultsDB as Results
# update to add values

def main(*args):
    print(f"Extract Symbols & Values for Job {' '.join(args)}")

    job_id = args[0]
    job_path = args[1]

    results = Results.find(job_id)

    filelist = os.popen("ls "+job_path+"crops/ | grep '.png'")
    for index, image_file in enumerate(filelist):

        # if index != 13:
        #     continue

        image_file_name = image_file.rstrip()
        job_file = job_path+"crops/"+image_file_name
        tag_and_id = image_file_name.split("crop_")[-1].split("_")
        tag = tag_and_id[0]
        tag_index = tag_and_id[1].split(".")[0]

        matched_results = [result for result in results if result['slice_file'] in image_file_name and result['symbol'] == tag and result['symbol_id'] == tag_index]

        cmd = f'tesseract {job_file} {job_path}results/result_{str(index)}_{image_file_name} --oem 1 --psm 6 --dpi 300 -c tessedit_char_whitelist=.0123456789 quiet tsv'
        # cmd = f'tesseract {job_file} {job_path}results/result_{str(index)}_{image_file_name} --oem 1 --psm 6 --dpi 300 -c tessedit_char_whitelist=.0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ quiet tsv'
        # cmd = f'tesseract {job_file} {job_path}results/result_{str(index)}_{image_file_name} --oem 1 --psm 6 --dpi 300 -c quiet tsv'
        # print(f"Command: {cmd}\n")

        ret = os.popen(f'{cmd}')
        wat = ret.read().rstrip().lstrip().split('\n')
        # print(wat)

        with open(f'{job_path}results/result_{str(index)}_{image_file_name}.tsv') as f:
            lines = f.read().split('\n')[:-1]
            column_names = []
            for i, line in enumerate(lines):
                if i == 0: # header
                    column_names = line.split()
                    # print(f"col names {column_names}")
                else:
                    data = line.split()
                    # print(f"data line {data}")

                    result_dict = dict(zip(column_names, data))

                    try:
                        text = result_dict["text"]
                        if text.startswith('0') and not text.contains('.'):
                            text = f'.{text}'
                        if text.endswith('.'):
                            text = text[:-1]
                            
                        # print(f'Try: {text}')
                        value = float(text)
                        # print(f'Value: {value}')

                        for match in matched_results:
                            Results.add_value(match['rowid'], value) #, val_prob, val_bb)
                
                    except KeyError as keyErr:
                        # print(f'\n\tCaught KeyError: {keyErr}')
                        pass
                    except ValueError as valErr:
                        print(f'\n\tCaught ValueError: {valErr}')
                        pass

def format_value(v):
    if v.startswith('0'):
        v = f'0.{v[:3]}'
    elif v.startswith('.'):
        v = f'0{v[:4]}'
    return v

if __name__ == '__main__':
    main(*sys.argv[1:])