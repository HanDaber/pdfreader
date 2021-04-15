# mark up values with imagemagick

import sys, os, glob, json, time

import ResultsDB as Results

def main(*args):
    print(f"Markup Symbols & Values for Job {' '.join(args)}")

    job_id = args[0]
    job_path = args[1]

    results = Results.find(job_id)

    # FOR TESTING:
    # marked_up_slices = []
    
    for page_file in glob.iglob(f'{job_path}/*.png'):

        cmd = f'magick convert {page_file}'

        for result in results:

            # if result["slice_file"] != '715-022382-001_a-000_slice_2-1':
            # if result["slice_file"] != '715-022382-001_a-000_slice_1-2' and result["slice_file"] != '715-022382-001_a-000_slice_1-3':
            # if result["slice_file"] != '715-022382-001_a-000_slice_2-1' and result["slice_file"] != '715-022382-001_a-000_slice_1-2' and result["slice_file"] != '715-022382-001_a-000_slice_1-3':
                # continue

            page = result["slice_file"].split("_slice_")[0]
            page_row = int(result["slice_file"].split("_slice_")[1].split("-")[0])
            page_col = int(result["slice_file"].split("_slice_")[1].split("-")[1])
            page_file_page = page_file.split(job_path)[1].replace(".png", "")

            if page == page_file_page:

                symbol = result['symbol']
                symbol_probability = result['symbol_probability']
                symbol_bounding_box = json.loads(result['symbol_bounding_box'])
                sym_bb_left = symbol_bounding_box["left"]
                sym_bb_top = symbol_bounding_box["top"]
                sym_bb_width = symbol_bounding_box["width"]
                sym_bb_height = symbol_bounding_box["height"]

                base_width = 3400
                base_height = 2200

                # left = int((sym_bb_left * 616)) + ((616 - 50) * page_col)
                # top = int((sym_bb_top * 600)) + ((600 - 50) * page_row)
                left = ((616 * page_col)) + int((sym_bb_left * 616)) - 50 * (page_col + 1)
                if (page_col == 0):
                    left += 50
                    text_left = '175'
                if (page_col == 1):
                    left += 25
                    text_left = '-75'
                if (page_col == 2):
                    left += 0
                    text_left = '175'
                if (page_col == 3):
                    left += -25
                    text_left = '-75'
                if (page_col == 4):
                    left += -50
                    text_left = '-75'
                if (page_col == 5):
                    left += -75
                    text_left = '-75'
                top = ((600 * page_row)) + int((sym_bb_top * 600)) - 50 * (page_row + 1)
                if (page_row == 0):
                    top += 50
                    text_top = '70'
                if (page_row == 1):
                    top += 25
                    text_top = '-45'
                if (page_row == 2):
                    top += 0
                    text_top = '70'
                if (page_row == 3):
                    top += -25
                    text_top = '-45'
                right = int(left + (sym_bb_width * 616))
                bottom = int(top + (sym_bb_height * 600))

                # text_left = str(left) # '-75' if (symbol_bounding_box['left'] > 0.33) else '75'
                # text_top = str(top) # '-45' if (symbol_bounding_box['top'] > 0.33) else '75'

                value = result['value']
                value_probability = result['value_probability']
                value_bounding_box = json.loads(result['value_bounding_box'])
                val_bb_left = value_bounding_box["left"]
                val_bb_top = value_bounding_box["top"]
                val_bb_width = value_bounding_box["width"]
                val_bb_height = value_bounding_box["height"]
                
                text = f" 'Tag: {symbol} ({symbol_probability}) "
                if value is None:
                    text += "\nValue: Unknown' "
                else:
                    if value_probability is None:
                        text += f"\nValue: {value} (Unknown)' "
                    else:
                        text += f"\nValue: {value} ({value_probability})' "

                draw_val_box = f'{left + sym_bb_width},{top} {left + sym_bb_width + val_bb_width},{top + val_bb_height}'

                # from drawing onto sliced image
                # cmd = f'magick convert {job_path}slices/{result["slice_file"]}.png'

                cmd += f' +repage -draw "'
                # cmd += f' fill rgba(255, 215, 0 , 0.1) stroke red stroke-width 1 roundrectangle {left - 75},{top - 25} {left - 75 + 250},{top - 25 + 75} 5,5'
                cmd += f' fill rgba(255, 215, 0 , 0.1) stroke red stroke-width 1 roundrectangle {draw_val_box} 5,5'
                # cmd += f' fill rgba(0, 215, 0 , 0.25) stroke navy stroke-width 1 roundrectangle {draw_val_box} 2,2'
                cmd += f' fill none stroke red stroke-width 2 roundrectangle {left},{top} {right},{bottom} 5,5'
                cmd += f' fill red stroke red stroke-width 1 font-size 18 translate {text_left},{text_top} text {left},{top} {text}"'
                
                # cmd += f" -set filename:t '%d/%t_markup' '%[filename:t].png'"

        cmd += f" -set filename:t '%d/markup/%t_markup' '%[filename:t].png'"
        # print(cmd)
        ret = os.popen(f'{cmd}')
        wat = ret.read()
        # print(wat)
    
    # time.sleep(4)
    pdf_cmd = f"magick {job_path}markup/*.png {job_path}markup/{job_id}_markup.pdf"
    ret = os.popen(f'{pdf_cmd}')
    wat = ret.read()
    # print(wat)

    return f'artifacts/{job_id}'



if __name__ == '__main__':
    main(*sys.argv[1:])