# wrap imagemagick for PDF to PNG conversion

import os, sys

def main(*args):
    print(f"Slice Drawings for Job {' '.join(args)}")

    job_id = args[0]
    job_path = args[1]

    base_width = 3400
    base_height = 2200
    rows = 4
    columns = 6
    width_overlap = 50
    height_overlap = 50

    nominal_width = base_width/columns
    nominal_height = base_height/rows

    width = int(nominal_width) + width_overlap
    height = int(nominal_height) + height_overlap

    cmd_crop = f'magick convert {job_path}{job_id}-*.png -set filename:base \'%[basename]\' -crop '
    slices_path = job_path+"slices"

    cmd_meta = "echo 'SLICING'"
    print_cmd_meta = ""

    for row in range(rows):
        height_offset = int(row * (nominal_height - (height_overlap/2)))
        for col in range(columns):
            width_offset = int(col * (nominal_width - (width_overlap/2)))

            cmd = f'{cmd_crop}{str(width)}x{str(height)}+{str(width_offset)}+{str(height_offset)} {slices_path}/%[filename:base]_slice_{str(row)}-{str(col)}.png'
            cmd_meta += " && "+cmd
            print_cmd_meta += "\n"+cmd

    # print(cmd_meta)
    ret = os.popen(cmd_meta)
    wat = ret.read()
    # print(wat)

    return slices_path

    

if __name__ == '__main__':
    main(*sys.argv[1:])