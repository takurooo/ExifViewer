# -----------------------------------
# import
# -----------------------------------
from yattag import Doc, indent

# -----------------------------------
# define
# -----------------------------------
TYPE_TEXT = 'text'
TYPE_IMG = 'img'
TYPE_LINK = 'link'


# -----------------------------------
# class
# -----------------------------------
class Cell:
    def __init__(self, type, text=None, link=None, img=None):
        if type == TYPE_TEXT:
            assert text is not None, "text None"
        elif type == TYPE_LINK:
            assert link is not None, "link None"
            assert text is not None or img is not None, "text and img  None"
        elif type == TYPE_IMG:
            assert img is not None, "img None"

        self.type = type
        self.text = text
        self.link = link
        self.img = img


class HtmlTableWriter:
    def __init__(self, html_fname, title=None, header=None, css_fname=None):
        self.html_fname = html_fname
        self.css_fname = css_fname
        self.rows = []
        self.summaries = []

        if title:
            self.title = title
        else:
            self.title = self.html_fname

        if header:
            self.header = header
        else:
            self.header = self.html_fname


    def add_summary(self, summary):
        if isinstance(summary, list):
            self.summaries.extend(summary)
        else:
            self.summaries.append(summary)

    def add_row(self, row):
        if isinstance(row, list):
            self.rows.append(row)
        else:
            self.rows.append([row])

    def write(self):
        html = self._generate()
        with open(self.html_fname, 'w') as f:
            f.write(html)

    def _put_cell(self, cell, doc, tag, text, line):
        if cell.type == TYPE_TEXT:
            text(cell.text)
        elif cell.type == TYPE_IMG:
            doc.stag('img', src=cell.img)
            if cell.text:
                text(cell.text)
        elif cell.type == TYPE_LINK:
            # ---------------------------
            # a href
            # ---------------------------
            with tag("a", href=cell.link):
                if cell.text:
                    text(cell.text)
                else:
                    doc.stag('img', src=cell.img)
                    if cell.text:
                        text(cell.text)

    def _generate(self):
        doc, tag, text, line = Doc().ttl()
        # ---------------------------
        # html
        # ---------------------------
        with tag('html'):
            # ---------------------------
            # head
            # ---------------------------
            with tag('head'):
                doc.asis('<meta charset="utf-8">')
                doc.asis('<meta name="viewport" content="width=device-width, initial-scale=1">')
                if self.css_fname:
                    doc.asis('<link rel="stylesheet" type="text/css" href="{}">'.format(self.css_fname))
                line('title', self.title)
            # ---------------------------
            # body
            # ---------------------------
            with tag('body'):
                line('h1', self.header, align="left")

                if len(self.summaries) != 0:
                    with tag('div', klass='summary'):
                        with tag('ul'):
                            for summary in self.summaries:
                                with tag('li'):
                                    self._put_cell(summary, doc, tag, text, line)

                # ---------------------------
                # table
                # ---------------------------
                with tag('table'):
                    for i, row in enumerate(self.rows):
                        # ---------------------------
                        # tr
                        # ---------------------------
                        with tag('tr'):
                            if i == 0:
                                tag_name = 'th'
                            else:
                                tag_name = 'td'

                            for cell in row:
                                # ---------------------------
                                # th or td
                                # ---------------------------
                                with tag(tag_name):
                                    self._put_cell(cell, doc, tag, text, line)

        html = doc.getvalue()
        indented_html = indent(html,
                               indentation='  ',
                               newline='\n',  # windows:\r\n
                               indent_text=None)
        return indented_html


# -----------------------------------
# function
# -----------------------------------


# -----------------------------------
# main
# -----------------------------------
if __name__ == '__main__':
    pass
