import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget, QInputDialog, QFileDialog, QMessageBox
from pygame import mixer
from PlayList import PlayList, Composition

class PlayListApp(QWidget):
    def __init__(self):
        super().__init__()

        self.playlist_manager = PlayList()

        self.init_ui()
        mixer.init()

    def init_ui(self):
        # Главное окно
        self.setWindowTitle('Playlist Manager')
        self.setGeometry(300, 100, 600, 400)

        layout = QVBoxLayout()

        # Левый список - плейлисты
        self.playlist_list = QListWidget()
        self.playlist_list.clicked.connect(self.on_playlist_selected)
        layout.addWidget(self.playlist_list)

        # Правый список - треки в плейлисте
        self.track_list = QListWidget()
        layout.addWidget(self.track_list)

        # Нижняя панель с кнопками
        btn_layout = QHBoxLayout()

        # Кнопки управления плейлистом
        btn_add_playlist = QPushButton('Создать плейлист')
        btn_add_playlist.clicked.connect(self.create_playlist)
        btn_delete_playlist = QPushButton('Удалить плейлист')
        btn_delete_playlist.clicked.connect(self.delete_playlist)
        
        btn_layout.addWidget(btn_add_playlist)
        btn_layout.addWidget(btn_delete_playlist)

        # Кнопки управления треками
        btn_add_track = QPushButton('Добавить трек')
        btn_add_track.clicked.connect(self.add_track)
        btn_remove_track = QPushButton('Удалить трек')
        btn_remove_track.clicked.connect(self.remove_track)

        btn_layout.addWidget(btn_add_track)
        btn_layout.addWidget(btn_remove_track)

        # Кнопки для перемещения треков
        btn_move_up = QPushButton('Переместить вверх')
        btn_move_up.clicked.connect(self.move_up)
        btn_move_down = QPushButton('Переместить вниз')
        btn_move_down.clicked.connect(self.move_down)

        btn_layout.addWidget(btn_move_up)
        btn_layout.addWidget(btn_move_down)

        # Кнопки управления воспроизведением
        btn_play = QPushButton('Проиграть')
        btn_play.clicked.connect(self.play_track)
        btn_next = QPushButton('Следующий')
        btn_next.clicked.connect(self.play_next)
        btn_previous = QPushButton('Предыдущий')
        btn_previous.clicked.connect(self.play_previous)

        btn_layout.addWidget(btn_play)
        btn_layout.addWidget(btn_next)
        btn_layout.addWidget(btn_previous)

        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def show_error_message(self, message):
        """Отображение сообщения об ошибке"""
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setText(message)
        msg_box.setWindowTitle("Ошибка")
        msg_box.exec_()

    def create_playlist(self):
      """Создание нового плейлиста"""
      name, ok = QInputDialog.getText(self, 'Создать плейлист', 'Введите название:')
      if ok and name:
          if name in self.playlist_manager.playlists:
              self.show_error_message(f"Плейлист с именем '{name}' уже существует.")
          else:
              self.playlist_manager.create_playlist(name)
              self.playlist_list.addItem(name)
      else:
          self.show_error_message("Введите корректное название плейлиста.")


    def delete_playlist(self):
        """Удаление плейлиста"""
        selected_playlist = self.playlist_list.currentItem()
        if selected_playlist:
            self.playlist_manager.delete_playlist(selected_playlist.text())
            self.playlist_list.takeItem(self.playlist_list.currentRow())
            self.track_list.clear()
        else:
            self.show_error_message("Выберите плейлист для удаления.")

    def add_track(self):
        """Добавление трека в плейлист"""
        selected_playlist = self.playlist_list.currentItem()
        if selected_playlist:
            track_path, _ = QFileDialog.getOpenFileName(self, 'Выбрать трек')
            if track_path:
                self.playlist_manager.add_track(selected_playlist.text(), track_path)
                self.track_list.addItem(track_path)
            else:
                self.show_error_message("Не удалось загрузить трек.")
        else:
            self.show_error_message("Выберите плейлист для добавления трека.")

    def remove_track(self):
        """Удаление трека из плейлиста"""
        selected_playlist = self.playlist_list.currentItem()
        selected_track = self.track_list.currentItem()
        if selected_playlist and selected_track:
            self.playlist_manager.remove_track(selected_playlist.text(), selected_track.text())
            self.track_list.takeItem(self.track_list.currentRow())
        else:
            self.show_error_message("Выберите трек для удаления.")

    def play_track(self):
        """Проигрывание текущего трека"""
        selected_track = self.track_list.currentItem()
        if selected_track:
            self.playlist_manager.play_track(selected_track.text())
        else:
            self.show_error_message("Выберите трек для воспроизведения.")

    def play_next(self):
        """Проигрывание следующего трека"""
        current_row = self.track_list.currentRow()
        if current_row < self.track_list.count() - 1:
            self.track_list.setCurrentRow(current_row + 1)
            self.play_track()
        else:
            self.track_list.setCurrentRow(0)
            self.play_track()

    def play_previous(self):
        """Проигрывание предыдущего трека"""
        current_row = self.track_list.currentRow()
        if current_row > 0:
            self.track_list.setCurrentRow(current_row - 1)
            self.play_track()
        else:
            self.show_error_message("Это первый трек в списке.")

    def move_up(self):
        """Перемещение трека вверх"""
        current_row = self.track_list.currentRow()
        if current_row > 0:
            current_item = self.track_list.takeItem(current_row)
            self.track_list.insertItem(current_row - 1, current_item)
            self.track_list.setCurrentRow(current_row - 1)
        else:
            self.show_error_message("Трек уже на первой позиции.")

    def move_down(self):
        """Перемещение трека вниз"""
        current_row = self.track_list.currentRow()
        if current_row < self.track_list.count() - 1:
            current_item = self.track_list.takeItem(current_row)
            self.track_list.insertItem(current_row + 1, current_item)
            self.track_list.setCurrentRow(current_row + 1)
        else:
            self.show_error_message("Трек уже на последней позиции.")

    def on_playlist_selected(self):
      """Загрузка треков при выборе плейлиста"""
      selected_playlist = self.playlist_list.currentItem()
      if selected_playlist:
          self.track_list.clear()
          playlist = self.playlist_manager.playlists[selected_playlist.text()]
          for item in playlist:
              self.track_list.addItem(str(item.data))



def main():
    app = QApplication(sys.argv)
    window = PlayListApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
