import os
import sys
from PyQt5.QtWidgets import QApplication, QLabel, QDesktopWidget, QPushButton, QFileDialog, QMessageBox, QMainWindow
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

sys.path.append('face-alignment')
from utils import remove_eyebrow, change_save_dir_path, getOpenFilesAndDirs, remove_eyebrow_all

NO_ERROR = 0
ERROR_SAME_INPUT_AND_OUTPUT = 1
ERROR_NO_PREDICTION = 2

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Set Window
        # x, y, w, h
        # self.setGeometry(0, 0, 550, 430)
        self.setWindowTitle('Person De-Identification')
        self.center()
        self.resize(550, 430)        

        # File Button
        self.load_button = QPushButton('Open Folder/File', self)
        self.load_button.clicked.connect(self.load_inputs)
        self.load_button.setGeometry(25, 370, 150, 30)

        self.left_button = QPushButton('Previous', self)
        self.left_button.clicked.connect(self.previous_file)
        self.left_button.setGeometry(200, 370, 70, 30)

        self.right_button = QPushButton('Next', self)
        self.right_button.clicked.connect(self.next_file)
        self.right_button.setGeometry(280, 370, 70, 30)

        self.save_button = QPushButton('Save File', self)
        self.save_button.clicked.connect(self.save_file)
        self.save_button.setGeometry(375, 370, 150, 30)

        self.pre_label = QLabel(self)
        self.pre_label.move(20, 10)
        self.post_label = QLabel(self)
        self.post_label.move(280, 10)

        self.file_name = None
        self.dir_name = None
        self.file_names = []
        self.index = 0

        self.IMAGE_EXTENSIONS = ['jpg', 'png', 'jpeg', 'PNG', 'BMP', 'bmp', 'ppm', 'PPM']

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def check_extenstion(self, file_lists):
        for file in file_lists:
            if file.split('.')[-1] not in self.IMAGE_EXTENSIONS:
                return False
        return True

    def load_inputs(self):
        self.file_names = []
        self.file_name = getOpenFilesAndDirs()

        if self.file_name == []:
            QMessageBox.about(self, 'Warning', '파일 혹은 사진을 선택해주세요!')
        else:
            if os.path.isfile(self.file_name[0]):
                if len(self.file_name) == 1:
                    self.file_names.append(self.file_name[0])
                    if self.check_extenstion(self.file_names):
                        self.open_file(self.file_name[0])
                    else:
                        QMessageBox.about(self, 'Warning', '이미지가 아닌 파일이 있습니다!')
                else:
                    self.index = 0
                    temp_split = self.file_name[0].split('/')
                    self.dir_name = temp_split[0]
                    for temp in temp_split[1:-1]:
                        self.dir_name = self.dir_name + '/' + temp
                    for file_name in self.file_name:
                        self.file_names.append(file_name.split('/')[-1])
                    self.file_names.sort()
                    if self.check_extenstion(self.file_names):
                        self.open_file(self.dir_name + '/' + self.file_names[self.index])
                    else:
                        QMessageBox.about(self, 'Warning', '이미지가 아닌 파일이 있습니다!')
            else:
                self.dir_name = self.file_name[0]
                while(os.path.isdir(self.dir_name)):
                    self.file_names = os.listdir(self.dir_name)
                    if len(self.file_names):
                        if os.path.isdir(os.path.join(self.dir_name, self.file_names[0])):
                            self.dir_name = self.dir_name + '/' + self.file_names[0]
                        else:
                            break
                    else:
                        break

                if len(self.file_names):
                    self.index = 0
                    self.file_names.sort()
                    
                    if self.check_extenstion(self.file_names):
                        self.open_file(self.dir_name + '/' + self.file_names[self.index])
                    else:
                        QMessageBox.about(self, 'Warning', '이미지가 아닌 파일이 있습니다!')
                else:
                    QMessageBox.about(self, 'Warning', '빈 파일입니다. 다시 선택해주세요!')
    
    def open_file(self, file_name):
        # if file_name is directory
        if file_name:
            pixmap = QPixmap(file_name)
            pixmap = pixmap.scaledToWidth(250)

            width = pixmap.width()
            height = pixmap.height()

            self.pre_label.setPixmap(pixmap)
            self.pre_label.setContentsMargins(10, 10, 10, 10)
            self.pre_label.resize(250, 350)
            self.process_file(file_name)
        else:
            QMessageBox.about(self, 'Warning', 'No File Selected')

    def previous_file(self):
        if len(self.file_names) == 0:
            QMessageBox.about(self, 'Warning', '사진을 입력해주세요!')
        elif len(self.file_names) == 1:
            QMessageBox.about(self, 'Warning', '입력 사진이 한장입니다!')
        else:
            self.index = self.index - 1
            if self.index < 0:
                self.index = len(self.file_names) - 1
            self.open_file(self.dir_name + '/' + self.file_names[self.index])

    def next_file(self):
        if len(self.file_names) == 0:
            QMessageBox.about(self, 'Warning', '사진을 입력해주세요!')
        elif len(self.file_names) == 1:
            QMessageBox.about(self, 'Warning', '입력 사진이 한장입니다!')
        else:
            self.index = self.index + 1
            if self.index == len(self.file_names):
                self.index = 0

            # print('self.dir_name : ', self.dir_name)
            # print('self.file_names[self.index] : ', self.file_names[self.index])
            self.open_file(self.dir_name + '/' + self.file_names[self.index])

    def process_file(self, file_name):
        '''
        ## process ##
        Input : self.file_name[0]
        Output : save_path
        '''

        has_error, processed_image, ERROR_IDX = remove_eyebrow(file_name)
        if has_error:
            if ERROR_IDX == ERROR_NO_PREDICTION:
                QMessageBox.about(self, 'Warning', '입력 영상에서 얼굴을 찾을 수 없습니다!')
            elif ERROR_IDX == ERROR_SAME_INPUT_AND_OUTPUT:
                QMessageBox.about(self, 'Warning', '입력 폴더와 저장 폴더의 위치가 동일합니다!')
        else:
            pixmap = QPixmap.fromImage(processed_image)
            pixmap = pixmap.scaledToWidth(250)

            width = pixmap.width()
            height = pixmap.height()

            self.post_label.setPixmap(pixmap)
            self.post_label.setContentsMargins(10, 10, 10, 10)
            self.post_label.resize(250, 350)

    def save_file(self):

        '''
        ## save ##
        Input : where to save / saved_path
        Output : save image / del_saved_path
        '''

        save_dir_path = QFileDialog.getExistingDirectory(self, 'Find Folder')
        if not save_dir_path:
            QMessageBox.about(self, 'Warning', 'No File Selected')
        else:
            change_save_dir_path(save_dir_path)
            if len(self.file_names) < 1:
                QMessageBox.about(self, 'Warning', '사진을 입력해주세요!')
            else:
                has_error, ERROR_IDX = remove_eyebrow_all(self.dir_name, self.file_names)
                if(has_error):
                    if ERROR_IDX == ERROR_NO_PREDICTION:
                        QMessageBox.about(self, 'Warning', '입력 영상에서 얼굴을 찾을 수 없습니다!')
                    elif ERROR_IDX == ERROR_SAME_INPUT_AND_OUTPUT:
                        QMessageBox.about(self, 'Warning', '입력 폴더와 저장 폴더의 위치가 동일합니다!')
                else:
                    QMessageBox.information(self, 'Success', 'Success!')
        # save_results(self.file_name[0])

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())