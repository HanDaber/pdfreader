# extract vales with tesseract

import sys, os, json

import ResultsDB as Results
# update to add values

def main(*args):
    print(f"Extract Symbols & Values for Job {' '.join(args[:2])}")

    job_id = args[0]
    job_path = args[1]
    character_list = args[2]

    tesseract_config = 'quiet tsv'
    if character_list:
        tesseract_config = f'-c tessedit_char_whitelist={character_list} {tesseract_config}'

    results = Results.find(job_id)

    filelist = os.popen("ls "+job_path+"crops/ | grep '.png'")
    for index, image_file in enumerate(filelist):

        image_file_name = image_file.rstrip()
        job_file = job_path+"crops/"+image_file_name
        tag_and_id = image_file_name.split("crop_")[-1].split("_")
        tag = tag_and_id[0]
        tag_index = tag_and_id[1].split(".")[0]

        matched_results = [result for result in results if result['slice_file'] in image_file_name and result['symbol'] == tag and result['symbol_id'] == tag_index]

        cmd = f'tesseract {job_file} {job_path}results/result_{str(index)}_{image_file_name} --oem 1 --psm 6 --dpi 300 {tesseract_config}'

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
                    if tag == 'plusminusvertical':
                        print(f"data line {data}")

                    result_dict = dict(zip(column_names, data))

                    try:
                        text = result_dict["text"]
                        
                        # if tag == 'plusminusvertical':
                            # print(f"text line {text}")
                        
                        count = text.count('.') - 1

                        if text.endswith('.'):
                            text = text[:-1]
                        if text.startswith('0') and '.' not in text:
                            text = f'.{text}'
                        text = text.rsplit('.', count)[0]
                        
                        # if tag == 'plusminusvertical':
                            # print(f'Try: {text}')
                        
                        value = float(text)
                        # print(f'Value: {value}')

                        for match in matched_results:
                            # print(tag)
                            # if tag == 'plusminusvertical':
                            #     print(tag, value, match['rowid'])
                            #     if 'tolerance_plus' in match:
                            #         print(match['rowid'], value, 'minus')
                            #         Results.add_tolerance(match['rowid'], value, 'minus')
                            #     else:
                            #         print(match['rowid'], value, 'plus')
                            #         Results.add_tolerance(match['rowid'], value, 'plus')
                            # else: 
                            Results.add_value(match['rowid'], value) #, val_prob, val_bb)
                
                    except KeyError as keyErr:
                        # print(f'\n\tCaught KeyError for {result_dict}: {keyErr}')
                        pass
                    except ValueError as valErr:
                        print(f'\n\tCaught ValueError for {result_dict["text"]}: {valErr}')
                        pass

def format_value(v):
    if v.startswith('0'):
        v = f'0.{v[:3]}'
    elif v.startswith('.'):
        v = f'0{v[:4]}'
    return v

if __name__ == '__main__':
    main(*sys.argv[1:])