import sys
import argparse
from PySide2.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QTreeWidget, QTreeWidgetItem
from common.exif_reader import ExifReader


def get_args():
    parser = argparse.ArgumentParser(description="Exif Viewer.")
    parser.add_argument("exif_path", type=str, help="path2your_exif", default=None)
    return parser.parse_args()


class ExifViewer(QMainWindow):
    WINDOW_SIZE = (500, 500)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("exif viewer")
        self.resize(*self.WINDOW_SIZE)

        self.tree_widget = None
        self.ifds = None

    def make_tree(self, ifds):

        self.tree_widget = QTreeWidget()
        self.tree_widget.setAlternatingRowColors(True)
        self.tree_widget.setColumnCount(3)
        self.tree_widget.setHeaderLabels(["TagName", "filepos", "Value"])

        # -----------------------
        # treeの要素を設定
        # -----------------------
        top_level_items = []
        for ifd_name, ifd in ifds.items():
            top_level_item = QTreeWidgetItem(['{} ifd'.format(ifd_name), ''])
            for tag_name, tag in ifd.items():
                child_row = []
                child_row.append('(0x{:04x}){}'.format(tag.id, tag_name))
                child_row.append('0x{:04x}'.format(tag.start_pos))
                child_row.append(str(tag.val))
                child_item = QTreeWidgetItem(child_row)
                top_level_item.addChild(child_item)
            top_level_items.append(top_level_item)

        self.tree_widget.addTopLevelItems(top_level_items)

        # -----------------------
        # layoutの設定
        # -----------------------
        layout = QVBoxLayout()
        layout.addWidget(self.tree_widget)
        self.setLayout(layout)

        self.tree_widget.expandAll() # 全てのツリーを開いた状態に設定

        self.setCentralWidget(self.tree_widget)
        # self.adjustSize()


def main(args):
    exif_reader = ExifReader(args.exif_path)
    exif_reader.print_log()

    app = QApplication(sys.argv)

    exif_viewer = ExifViewer()
    exif_viewer.make_tree(exif_reader.get_exif())
    exif_viewer.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main(get_args())
