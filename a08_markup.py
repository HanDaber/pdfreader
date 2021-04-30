# mark up values with imagemagick

import sys, os, glob, json, time, random

import ResultsDB as Results

def main(*args):
    print(f"Markup Symbols & Values for Job {' '.join(args[:2])}")

    job_id = args[0]
    job_path = args[1]
    markup_symbol_flag = args[2]

    results = Results.find(job_id)

    redline_file_suffix = '_redline'

    for page_file in glob.iglob(f'{job_path}/*.png'):

        cmd = f'magick convert {page_file}'

        result_legend_index = 0

        for result in results:

            symbol = result['symbol']
            if symbol == 'position':
                continue
            if markup_symbol_flag and markup_symbol_flag != symbol:
                continue

            page = result["slice_file"].split("_slice_")[0]
            page_row = int(result["slice_file"].split("_slice_")[1].split("-")[0])
            page_col = int(result["slice_file"].split("_slice_")[1].split("-")[1])
            page_file_page = page_file.split(job_path)[1].replace(".png", "")

            if page == page_file_page:

                result_legend_index += 1

                symbol_probability = result['symbol_probability']
                symbol_bounding_box = json.loads(result['symbol_bounding_box'])
                sym_bb_left = symbol_bounding_box["left"]
                sym_bb_top = symbol_bounding_box["top"]
                sym_bb_width = symbol_bounding_box["width"]
                sym_bb_height = symbol_bounding_box["height"]

                left = ((616 * page_col)) + int((sym_bb_left * 616)) - 50 * (page_col + 1)
                if (page_col == 0):
                    left += 50
                    text_left = '0'
                if (page_col == 1):
                    left += 25
                    text_left = '20'
                if (page_col == 2):
                    left += 0
                    text_left = '30'
                if (page_col == 3):
                    left += -25
                    text_left = '40'
                if (page_col == 4):
                    left += -50
                    text_left = '50'
                if (page_col == 5):
                    left += -75
                    text_left = '60'
                top = ((600 * page_row)) + int((sym_bb_top * 600)) - 50 * (page_row + 1)
                if (page_row == 0):
                    top += 50
                    text_top = '0'
                if (page_row == 1):
                    top += 25
                    text_top = '0'
                if (page_row == 2):
                    top += 0
                    text_top = '0'
                if (page_row == 3):
                    top += -25
                    text_top = '0'
                right = int(left + (sym_bb_width * 616))
                bottom = int(top + (sym_bb_height * 600))

                value = result['value']
                value_probability = result['value_probability']
                value_bounding_box = json.loads(result['value_bounding_box'])
                val_bb_left = value_bounding_box["left"]
                val_bb_top = value_bounding_box["top"]
                val_bb_width = value_bounding_box["width"]
                val_bb_height = value_bounding_box["height"]
                
                text = f" '*{result_legend_index}: {symbol} ({int(symbol_probability * 100)}%) "
                if value is None:
                    text += "\nValue: Unknown' "
                else:
                    if value_probability is None:
                        text += f"\nValue: {value}' "
                    else:
                        text += f"\nValue: {value} ({value_probability})' "
                
                legend_text_left = 0
                legend_text_top = 0
                if result_legend_index <= 27:
                    legend_text_left = 15
                    legend_text_top = 75 * result_legend_index
                else:
                    legend_text_left = 3400 - 280
                    legend_text_top = 75 * (result_legend_index - 27)

                asterisk_text_left_translate = str(random.randint(0, 150))
                asterisk_text_top_translate = '-5'

                randy_hex_color = '#%02X%02X%02X' % (randy_int(), randy_int(), randy_int())
                # text_color = invert_color(randy_hex_color)

                draw_val_box = f'{left + sym_bb_width},{top} {left + sym_bb_width + val_bb_width},{top + val_bb_height}'

                redline_text_font = f'fill {randy_hex_color} stroke {randy_hex_color} stroke-width 1 font-size 30'
                # # redline_text_area = f' fill red stroke red stroke-width 1 font-size 18 translate {text_left},{text_top} text {left},{top} {text}"'
                # # redline_text_area = f' fill {randy_hex_color} stroke {randy_hex_color} stroke-width 1 font-size 16 translate {text_left},{text_top} text {left},{top} {text}"'
                redline_text_area = f' {redline_text_font} text {legend_text_left},{legend_text_top} {text}'
                redline_area_asterisk = f' {redline_text_font} translate {asterisk_text_left_translate},{asterisk_text_top_translate} text {left},{top} \'*{result_legend_index}\''

                cmd += f' +repage -draw "' # note - important opening double quote
                cmd += f' fill none stroke {randy_hex_color} stroke-width 2 roundrectangle {draw_val_box} 3,3'
                cmd += f' fill none stroke {randy_hex_color} stroke-width 2 roundrectangle {left},{top} {right},{bottom} 3,3'
                cmd += f' fill none stroke {randy_hex_color} stroke-width 2 line {left},{top} {legend_text_left + 75},{legend_text_top + 10}'
                cmd += redline_text_area + redline_area_asterisk + '"' # note - important closing double quote

        cmd += f" -set filename:t '%d/markup/%t{redline_file_suffix}' '%[filename:t].png'"
        # print(cmd)
        ret = os.popen(f'{cmd}')
        wat = ret.read()
        # print(wat)
    
    if markup_symbol_flag:
        redline_file_suffix += f'_{markup_symbol_flag}'
    output_markup_file_path = f'{job_path}markup/{job_id}{redline_file_suffix}.pdf'
    pdf_cmd = f"magick {job_path}markup/*.png {output_markup_file_path}"
    ret = os.popen(f'{pdf_cmd}')
    wat = ret.read()
    # print(wat)

    return output_markup_file_path

def randy_int():
    return random.randint(0, 255)

# def invert_color(hex_code):
#     if hex_code.startswith('#'):
#         hex_code = hex_code[1:]

#     if len(hex_code) != 6:
#         print('Invalid HEX_code color.')
#         return hex_code

#     r = int(hex_code[0:2], 16)
#     g = int(hex_code[2:4], 16)
#     b = int(hex_code[4:6], 16)

#     # http://stackoverflow.com/a/3943023/112731
#     if (r * 0.299 + g * 0.587 + b * 0.114) > 186:
#         return '#000000'
#     else:
#         return '#FFFFFF'


if __name__ == '__main__':
    main(*sys.argv[1:])