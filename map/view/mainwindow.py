import logging
from PyQt5.QtWidgets import QMainWindow, QFileDialog
from map.ui.mainwindow_ui import MainWindowUI
from map import __directory__


class MainWindow(QMainWindow, MainWindowUI):

    def __init__(self, model):

        super().__init__()

        self.setupUi(model)

        self.root_log = logging.getLogger('root')

        self.show()

    def open_about(self):
        ''' UNDER CONSTRUCTION '''
        print('Open About')

    def open_readme(self):
        ''' UNDER CONSTRUCTION '''
        print('Open README')

    def open_general_settings(self):
        ''' UNDER CONSTRUCTION '''
        print('Open General Settings')

    def open_logging_settings(self):
        ''' UNDER CONSTRUCTION '''
        print('Open Logging Settings')

    def open_file(self):

        self.root_log.info('Loading new file(s)...')

        file_paths, _ = QFileDialog.getOpenFileNames(
            None, 'Open file',
            __directory__,
            'hdf5 files (*.hdf5 *.h5);; All Files (*)')

        if file_paths:
            for file_path in file_paths:
                self.model.load_sliced_data_from_filepath(file_path)
