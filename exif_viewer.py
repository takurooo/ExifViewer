# -----------------------------------
# import
# -----------------------------------
import os
import sys
import argparse

from PySide2.QtWidgets import QApplication, QMainWindow, QAction, QWidget
from PySide2.QtWidgets import QStackedWidget, QSplitter, QTextEdit, QTreeWidget, QTreeWidgetItem
from PySide2.QtWidgets import QHBoxLayout, qApp, QFileDialog
from PySide2.QtGui import QTextCursor, QFont, QColor, QIcon
from PySide2.QtCore import QSize, Qt

from common.exif_reader import ExifReader


# -----------------------------------
# define
# -----------------------------------

# -----------------------------------
# function
# -----------------------------------


def get_args():
    parser = argparse.ArgumentParser(description="Exif Viewer.")
    parser.add_argument("path", type=str, help="path2your_file", default=None)
    return parser.parse_args()


def qt_util_init_tree(qw_tree, header_list):
    qw_tree.setAlternatingRowColors(False)
    qw_tree.setColumnCount(len(header_list))
    qw_tree.setHeaderLabels([*header_list])


def qt_util_init_text_edit(qw_text_edit):
    qw_text_edit.clear()
    qw_text_edit.setReadOnly(False)
    qw_text_edit.setFontPointSize(14)
    fixed_font = QFont("Monaco")
    fixed_font.setStyleHint(QFont.Helvetica)
    qw_text_edit.setFont(fixed_font)
    qw_text_edit.setTextColor(QColor(0, 0, 0, 255))


def qt_util_reset_text_edit_cursor(qw_text_edit):
    first_row_block = qw_text_edit.document().findBlockByLineNumber(0)  # 1行目のblockを取得
    qg_text_cursor = QTextCursor(first_row_block)
    qw_text_edit.setTextCursor(qg_text_cursor)  # cursorを1行目に設定


def qt_util_append_text_edit(qw_text_edit, tag, head=False, display_max_len=100):
    if head:
        qw_text_edit.setTextColor(QColor(0, 0, 255, 128))
        line = '{:<4}\t{:<4}\t{:<25}\t{}'.format('file_pos', 'tag_id', 'tag_name', 'val')
    else:
        if display_max_len < len(str(tag.val)):
            qw_text_edit.setTextColor(QColor(0, 0, 0, 128))
            tag_val = 'value too long!!'
        else:
            qw_text_edit.setTextColor(QColor(0, 0, 0, 255))
            tag_val = tag.val
        line = '0x{:04x}\t0x{:04x}\t{:<25}\t{}'.format(tag.start_pos, tag.id, tag.name, tag_val)
    qw_text_edit.append(line)


# -----------------------------------
# class
# -----------------------------------


class ExifViewer(QMainWindow):
    WINDOW_SIZE = {'width': 900, 'height': 600}

    def __init__(self, parent=None):
        super().__init__(parent)
        self.qw_tree = None
        self.qw_stack = None
        self.tree_type_to_stack_idx = None
        self.exif_reader = None

        self.setWindowTitle("exif viewer")
        self.resize(self.WINDOW_SIZE['width'], self.WINDOW_SIZE['height'])

    def make_viewer(self, exif_reader):
        self.exif_reader = exif_reader
        ifds = self.exif_reader.get_exif()

        self.qw_tree = QTreeWidget()
        qt_util_init_tree(self.qw_tree, header_list=['ifd_name'])

        self.qw_stack = QStackedWidget()
        self.tree_type_to_stack_idx = {}
        for tree_item_type, (ifd_name, ifd) in enumerate(ifds.items()):
            # -----------------------
            # treeにifd nameを書き込んでroot_treeに登録する.
            # -----------------------
            qw_tree_item = QTreeWidgetItem(['{} ifd'.format(ifd_name), ''], type=tree_item_type)
            self.qw_tree.addTopLevelItem(qw_tree_item)

            # -----------------------
            # text_editにexif情報を書き込んでstacked_widgetに登録する.
            # -----------------------
            qw_text_edit = QTextEdit()
            qt_util_init_text_edit(qw_text_edit)
            qt_util_append_text_edit(qw_text_edit, None, head=True)
            for _, tag in ifd.items():
                qt_util_append_text_edit(qw_text_edit, tag, head=False, display_max_len=50)
            qt_util_reset_text_edit_cursor(qw_text_edit)

            idx = self.qw_stack.addWidget(qw_text_edit)
            self.tree_type_to_stack_idx[tree_item_type] = idx
        else:
            self.qw_tree.itemClicked.connect(self._slot_tree_item_clicked)

        # -----------------------
        # widgetをlayoutに登録する.
        # -----------------------
        widgets = [self.qw_tree, self.qw_stack]
        self._make_layout(widgets)
        self._make_toolbar()

        self.show()  # widgetを表示する.

    def _save_text(self):
        filename = QFileDialog.getSaveFileName(self, '名前を付けて保存')
        out_path = filename[0]
        if out_path:
            self.exif_reader.save_log(out_path)

    def _make_toolbar(self):
        action_to_text = QAction(QIcon(os.path.join('icon', 'text.png')), 'save', self)
        action_to_text.triggered.connect(self._save_text)
        action_ext = QAction(QIcon(os.path.join('icon', 'exit.png')), 'exit', self)
        action_ext.triggered.connect(qApp.quit)

        # ツールバー作成
        self.toolbar = self.addToolBar('tool bar')
        self.toolbar.setIconSize(QSize(25, 25))
        self.toolbar.setFixedHeight(25)
        self.toolbar.addAction(action_to_text)
        self.toolbar.addAction(action_ext)

    def _make_layout(self, widgets):
        qw_splitter = QSplitter()
        for widget in widgets:
            qw_splitter.addWidget(widget)
        qw_splitter.setSizes([self.WINDOW_SIZE['width'] * 0.1, self.WINDOW_SIZE['width'] * 0.9])

        # layout = QHBoxLayout()
        # layout.addWidget(qw_splitter)
        # qw = QWidget()
        # qw.setLayout(layout)
        # self.setCentralWidget(qw)

        # self.setWindowFlags(Qt.WindowStaysOnTopHint) # 常に手前に表示する.

        # MainWindowのCentral領域にWidgetを設定
        self.setCentralWidget(qw_splitter)

    def _slot_tree_item_clicked(self, item, column):
        self.qw_stack.setCurrentIndex(self.tree_type_to_stack_idx[item.type()])
        current_text_edit = self.qw_stack.currentWidget()
        qt_util_reset_text_edit_cursor(current_text_edit)


# -----------------------------------
# main
# -----------------------------------
def main(args):
    exif_reader = ExifReader(args.path)
    exif_reader.print_log()

    app = QApplication(sys.argv)

    exif_viewer = ExifViewer()
    exif_viewer.make_viewer(exif_reader)

    sys.exit(app.exec_())


if __name__ == "__main__":
    main(get_args())
