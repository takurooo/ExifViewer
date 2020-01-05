# -----------------------------------
# import
# -----------------------------------
import os
import common.htmlwriter as htmlwriter
from common.htmlwriter import HtmlTableWriter, Cell


# -----------------------------------
# define
# -----------------------------------

# -----------------------------------
# class
# -----------------------------------


class ExifHtmlWriter:

    def __init__(self, css="style/sample.css", display_max_len=50):
        self.css = css
        self.display_max_len = display_max_len

    def write(self, fname, ifds):
        writer = HtmlTableWriter(fname,
                                 title='Exif Viewer',
                                 header='Exif Viewer',
                                 css_fname=self.css)

        writer.add_summary([
            Cell(htmlwriter.TYPE_LINK, text='Exif Specification',
                 link='http://www.cipa.jp/std/documents/j/DC-008-2012_J.pdf'),
            # Cell(htmlwriter.TYPE_TEXT, text='ByteOrder : {}'.format(str(self.tiff_header.byteorder).upper()))
        ])

        writer.add_row([
            Cell(htmlwriter.TYPE_TEXT, text='tag id'),
            Cell(htmlwriter.TYPE_TEXT, text='tag name'),
            Cell(htmlwriter.TYPE_TEXT, text='file pos'),
            Cell(htmlwriter.TYPE_TEXT, text='val type'),
            Cell(htmlwriter.TYPE_TEXT, text='val cnt'),
            Cell(htmlwriter.TYPE_TEXT, text='val')
        ])

        for ifd_name, ifd in ifds.items():
            for _, tag in ifd.items():
                val = tag.val
                if len(str(tag.val)) > self.display_max_len:
                    val = '-- NOT DISPLAY --'

                writer.add_row([
                    Cell(htmlwriter.TYPE_TEXT, text='{:#06x}'.format(tag.id)),
                    Cell(htmlwriter.TYPE_TEXT, text=str(tag.name)),
                    Cell(htmlwriter.TYPE_TEXT, text='{:#06x}'.format(tag.start_pos)),
                    Cell(htmlwriter.TYPE_TEXT, text='{}({})'.format(tag.typesize, tag.typename)),
                    Cell(htmlwriter.TYPE_TEXT, text=str(tag.cnt)),
                    Cell(htmlwriter.TYPE_TEXT, text=str(val))
                ])

        writer.write()


# -----------------------------------
# function
# -----------------------------------


# -----------------------------------
# main
# -----------------------------------

if __name__ == '__main__':
    pass
