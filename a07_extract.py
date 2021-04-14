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
        tag = image_file_name.split("crop_")[-1].split("_")[0]

        matched_results = [result for result in results if result['slice_file'] in image_file_name]

        # cmd = f'tesseract {job_file} stdout --oem 1 --dpi 72 digits'
        # cmd = f'tesseract {job_file} {job_path}results/result_{str(index)}_{image_file_name} --oem 1 --psm 6 --dpi 300 quiet digits tsv'
        cmd = f'tesseract {job_file} {job_path}results/result_{str(index)}_{image_file_name} --oem 1 --psm 6 --dpi 300 -c tessedit_char_whitelist=.0123456789 quiet tsv'
        # print(f"Command: {cmd}\n")

        ret = os.popen(f'{cmd}')
        wat = ret.read().rstrip().lstrip().split('\n')
        # print(f"Command results: {wat}")

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
                        value = float(result_dict['text'])

                        if value: # and int(val_prob) > 25:
                            val_prob = result_dict['conf']
                            val_bb = json.dumps({
                                'left': result_dict['left'],
                                'top': result_dict['top'],
                                'width': result_dict['width'],
                                'height': result_dict['height'],
                            })

                            # print(f"FOUND:\n\t{result_dict} - {image_file_name}\n")
                            # print(f"Crop ({image_file_name}) Slice ({matched_results})")
                            
                            if value > 99 and value < 1000:
                                value /= 1000
                            
                            # print(f"{value} @ {val_prob} - result_{str(index)}_{image_file_name}")
                            
                            for match in matched_results:
                                print(f"ADDING SAVING:\n\t{match}\n")
                                Results.add_value(match['rowid'], value, val_prob, val_bb)
                    
                    except KeyError as keyErr:
                        pass
                    except ValueError as valErr:
                        # print(f"{valErr}")
                        pass

        continue
    """
        results = [result for result in wat if result.rstrip()]
        print(index, results)

        # if len(results) > 0:
            # value = results[-1]
        for x, value in enumerate(results):
            print(f'value: {value}')
            vals = [f'.{v}' for v in value.split('.') if v.rstrip()]
            print(f'vals: {vals}')

            if len(vals) > 1:
                v = format_value(vals[0])
                print(f'v: {v}')
                for val in vals[1:]:
                    tolerance = format_value(val)
                    print(f'tolerance: {tolerance}')
                    try:
                        if float(tolerance) > 0:
                            Values.insert((job_id, tag, 50, v, tolerance, tolerance))
                            output += f'\n{index}-{x} {job_id} {tag}: {v} +/- {tolerance} @ probability ({image_file_name.split(".png")[0]})'
                    except ValueError:
                        print(f'Could not parse tolerance: {tolerance}')
            else:
                value = format_value(value)
                print(value)
                try:
                    if float(value) > 0:
                        Values.insert((job_id, tag, 50, value, None, None))
                        output += f'\n{index}-{x} {job_id} {tag}: {value} @ probability ({image_file_name.split(".png")[0]})'
                except ValueError:
                    print(f'Could not parse value: {value}')



    with open(f'artifacts/{job_id}/results/values.txt', 'w') as outfile:
            outfile.write(output)

    return "ok"
    """

def format_value(v):
    if v.startswith('0'):
        v = f'0.{v[:3]}'
    elif v.startswith('.'):
        v = f'0{v[:4]}'
    return v

if __name__ == '__main__':
    main(*sys.argv[1:])