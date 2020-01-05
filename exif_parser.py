# -----------------------------------
# import
# -----------------------------------
import os
import argparse
from collections import OrderedDict

from common.exif_reader import ExifReader
# from common.exif_htmlwriter import ExifHtmlWriter


# -----------------------------------
# define
# -----------------------------------


# -----------------------------------
# class
# -----------------------------------


# -----------------------------------
# function
# -----------------------------------
def get_args():
    parser = argparse.ArgumentParser(description="Exif parser.")
    parser.add_argument("img_path", type=str, help="path2your_image", default=None)
    return parser.parse_args()


def get_exif_with_PIL(file_path):
    from PIL import Image
    from PIL.ExifTags import TAGS, GPSTAGS
    img = Image.open(file_path)
    exif = img._getexif()

    exif_data = OrderedDict()
    for k, v in exif.items():
        exif_data[TAGS.get(k, k)] = v

    return exif_data


def test(file_path):
    # #
    # PILの結果と比較
    reference = get_exif_with_PIL(file_path)

    exif_reader = ExifReader(file_path)
    ifds = exif_reader.get_exif()
    ifd = ifds['0th']
    if ifds.get('exif', None):
        ifd.update(ifds['exif'])
    if ifds.get('gps', None):
        ifd.update(ifds['gps'])

    print('reference  tag len :', len(reference))
    print('ExifReader tag len :', len(ifd))

    for tag_name, tag in ifd.items():
        ref = reference.get(tag_name, None)
        if ref is not None:
            if tag.val != ref:
                print("NG : ", tag_name)
                print('    reference  :', ref)
                print('    read value :', tag.val)


# -----------------------------------
# main
# -----------------------------------
def main(args):
    exif_reader = ExifReader(args.img_path)
    exif_reader.print_log()

    # ifds = exif_reader.get_exif()
    # exif_html_writer = ExifHtmlWriter()
    # exif_html_writer.write('exif.html', ifds)

    # exif_reader.save_log('exif.txt')
    # test(args.img_path)


if __name__ == '__main__':
    main(get_args())
