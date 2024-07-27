# Based on afdko

import argparse
import logging
import os
import sys

from fontTools.ttLib import sfnt, TTFont

def get_psname(font):
    if 'name' in font:
        psname = font['name'].getDebugName(6)
        if psname:
            return psname

def run(options):
    ttc_path = options.ttc_path
    if not is_ttc(ttc_path):
        print(f'The input file "{options.ttc_path}" is not an OpenType Collection font.')
        return
    with open(ttc_path, 'rb') as fp:
        num_fonts = sfnt.SFNTReader(fp, fontNumber=0).numFonts
    print(f'Input font: {os.path.basename(ttc_path)}\n')
    if options.output and os.path.isdir(options.output):
        output = options.output
    else:
        output=os.path.dirname(ttc_path)
    for ft_idx in range(num_fonts):
        font = TTFont(ttc_path, fontNumber=ft_idx, lazy=True)
        psname = get_psname(font)
        if options.keywd and not options.keywd in psname:
            continue
        if psname is None:
            ttc_name = os.path.splitext(os.path.basename(ttc_path))[0]
            psname = f'{ttc_name}-font{ft_idx}'
        ext = '.otf' if font.sfntVersion == 'OTTO' else '.ttf'
        font_filename = f'{psname}{ext}'
        save_path = os.path.join(output, font_filename)
        font.save(save_path)
        print(f'Saved {save_path}')
        font.close()

def is_ttc(font_file_path):
    if os.path.isfile(font_file_path):
        with open(font_file_path, 'rb') as f:
            fullhead = f.read(31)
            head = fullhead[0: 4]
            if head == b'ttcf':
                return True
    return False

def get_options(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('ttc_path')
    parser.add_argument("-o", "--output")
    parser.add_argument("-k", "--keywd")
    options = parser.parse_args(args)
    return options

def main(args=None):
    opts = get_options(args)
    try:
        run(opts)
    except Exception as exc:
        print(exc)
        return 1

if __name__ == "__main__":
    sys.exit(main())
