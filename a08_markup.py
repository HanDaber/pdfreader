# cron A -> query external jobs db and populate local jobs queue db 
# cron B -> query local jobs queue db and for each -> call api on partNum
# api -> call pipeline on partNum
    # download/copy pdf -> convert -> slice -> analyze -> crop -> extract -> markup
    # ^DB stages
# process_pdf_directory -> pdf dirs (each) -> pipeline
# api -> get jobs, status, results
# ui -> templates + api

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
                value = result['value']
                value_probability = result['value_probability']
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
                    text_top = '75'
                if (page_row == 1):
                    top += 25
                    text_top = '-50'
                if (page_row == 2):
                    top += 0
                    text_top = '75'
                if (page_row == 3):
                    top += -25
                    text_top = '-50'
                right = int(left + (sym_bb_width * 616))
                bottom = int(top + (sym_bb_height * 600))

                # text_left = str(left) # '-75' if (symbol_bounding_box['left'] > 0.33) else '75'
                # text_top = str(top) # '-45' if (symbol_bounding_box['top'] > 0.33) else '75'
                text = f"'{symbol} ({symbol_probability})\n{value} ({value_probability})'"

                # print(f'R: {str(page_row)}; C: {str(page_col)}; S: {symbol}; L: {left}; R: {right}; Page: {page_file_page}')

                # from drawing onto sliced image
                # cmd = f'magick convert {job_path}slices/{result["slice_file"]}.png'

                cmd += f' +repage -draw "'
                cmd += f' fill rgba(255, 215, 0 , 0.25) stroke red stroke-width 1 roundrectangle {left - 75},{top - 25} {left - 75 + 250},{top - 25 + 75} 5,5'
                cmd += f' fill none stroke red stroke-width 2 roundrectangle {left},{top} {right},{bottom} 5,5'
                cmd += f' fill red stroke red stroke-width 1 font Courier font-size 16 translate {text_left},{text_top} text {left},{top} {text}"'
                
                # cmd += f" -set filename:t '%d/%t_markup' '%[filename:t].png'"

        cmd += f" -set filename:t '%d/markup/%t_markup' '%[filename:t].png'"
        print(cmd)
        ret = os.popen(f'{cmd}')
        # wat = ret.read()
        # print(wat)
    
    time.sleep(4)
    pdf_cmd = f"magick {job_path}markup/*.png {job_path}markup/{job_id}_markup.pdf"
    ret = os.popen(f'{pdf_cmd}')

    return f'artifacts/{job_id}'


# magick convert artifacts/715-022382-001_a/slices/715-022382-001_a-000_slice_0-1.png \
# +repage -draw "fill tomato  circle 250,30 310,30 \
# fill limegreen  circle 55,75 15,80 \
# font Courier  font-size 72  decorate UnderLine \
# fill dodgerblue  stroke navy  stroke-width 2 \
# translate 10,110 rotate -15 text 0,0 ' yoyo ' \
# fill none  circle 150,105 10,10 \
# font Courier  font-size 12  decorate UnderLine \
# fill dodgerblue  stroke navy  stroke-width 4 \
# translate 10,10 rotate -15 text 0,0 ' cool ' " \
# -set filename:t '%d/%t-change' '%[filename:t].png'


# magick convert artifacts/715-022382-001_a/slices/715-022382-001_a-000_slice_2-1.png +repage -draw \
# "fill rgba(255, 215, 0 , 0.25) stroke red stroke-width 1 roundrectangle 158,118 408,193 5,5 fill none stroke red stroke-width 2 roundrectangle 233,143 256,171 5,5 fill red stroke red stroke-width 1 font Courier font-size 14 translate -70,70 text 233.39971423999998,143.31154800000002 'diameter (0.7126751) \n0.250 (0.5)'" \
# -set filename:t '%d/%t_markup' '%[filename:t].png'


if __name__ == '__main__':
    main(*sys.argv[1:])