from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import *
from legendary.core import LegendaryCore

from Rare.Components.Tabs.Games.GameWidgetInstalled import GameWidgetInstalled
from Rare.Components.Tabs.Games.GameWidgetUninstalled import GameWidgetUninstalled
from Rare.utils.QtExtensions import FlowLayout


class GameList(QScrollArea):
    install_game = pyqtSignal(dict)
    show_game_info = pyqtSignal(str)

    def __init__(self, core: LegendaryCore):
        super(GameList, self).__init__()
        self.core = core
        self.widgets = []

        self.setObjectName("list_widget")
        self.setWidgetResizable(True)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.init_ui()

    def init_ui(self):
        self.widget = QWidget()
        self.widgets = []
        self.layout = FlowLayout()
        self.updates = []
        # Installed Games
        for game in sorted(self.core.get_installed_list(), key=lambda x: x.title):
            widget = GameWidgetInstalled(self.core, game)
            if widget.update_available:
                self.updates.append(widget.game.app_name)
            self.layout.addWidget(widget)
            widget.update_list.connect(self.update_list)

            widget.show_info.connect(lambda app_name: self.show_game_info.emit(app_name))

        uninstalled_games = []
        installed = [i.app_name for i in self.core.get_installed_list()]
        # get Uninstalled games
        for game in sorted(self.core.get_game_list(), key=lambda x: x.app_title):
            if not game.app_name in installed:
                uninstalled_games.append(game)
        # add uninstalled to gui
        for game in uninstalled_games:
            widget = GameWidgetUninstalled(self.core, game)
            widget.install_game.connect(lambda options: self.install_game.emit(options))
            self.layout.addWidget(widget)
            self.widgets.append(widget)

        self.widget.setLayout(self.layout)
        self.setWidget(self.widget)

    def filter(self, text: str):
        for w in self.widgets:
            if text.lower() in w.game.app_title.lower() + w.game.app_name.lower():
                w.setVisible(True)
            else:
                w.setVisible(False)

    def installed_only(self, i_o: bool):
        # TODO save state
        for w in self.widgets:
            w.setVisible(not i_o)

    def update_list(self):
        print("Updating List")
        self.setWidget(QWidget())
        self.init_ui()
        self.update()
