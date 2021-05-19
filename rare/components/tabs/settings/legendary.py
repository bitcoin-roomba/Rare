from logging import getLogger

from PyQt5.QtWidgets import QFileDialog, QMessageBox, QStackedWidget

from custom_legendary.core import LegendaryCore
from rare.ui.components.tabs.settings.legendary import Ui_legendary_settings
from rare.utils.extra_widgets import PathEdit
from rare.utils.utils import get_size

logger = getLogger("LegendarySettings")


class LegendarySettings(QStackedWidget, Ui_legendary_settings):
    def __init__(self, core: LegendaryCore):
        super(LegendarySettings, self).__init__()
        self.setupUi(self)

        self.core = core

        # Default installation directory
        self.install_dir = PathEdit(core.get_default_install_dir(),
                                    file_type=QFileDialog.DirectoryOnly,
                                    save_func=self.save_path)
        self.layout_install_dir.addWidget(self.install_dir)

        # Max Workers
        max_workers = self.core.lgd.config["Legendary"].get("max_workers", fallback=0)
        self.max_worker_select.setValue(int(max_workers))
        self.max_worker_select.valueChanged.connect(self.max_worker_save)

        # Cleanup
        self.clean_button.clicked.connect(
            lambda: self.cleanup(False)
        )
        self.clean_button_without_manifests.clicked.connect(
            lambda: self.cleanup(True)
        )
        self.setCurrentIndex(0)

        self.back_button.clicked.connect(lambda: self.setCurrentIndex(0))

        if self.core.egl_sync_enabled:
            self.sync_button.setText(self.tr("Disable sync"))
        else:
            self.sync_button.setText(self.tr("Enable Sync"))

        self.sync_button.clicked.connect(self.sync)

    def sync(self):
        if self.core.egl_sync_enabled:
            # disable_sync()
            pass
        else:
            self.setCurrentIndex(1)

    def save_path(self):
        self.core.lgd.config["Legendary"]["install_dir"] = self.install_dir.text()
        if self.install_dir.text() == "" and "install_dir" in self.core.lgd.config["Legendary"].keys():
            self.core.lgd.config["Legendary"].pop("install_dir")
        else:
            logger.info("Set config install_dir to " + self.install_dir.text())
        self.core.lgd.save_config()

    def max_worker_save(self, num_workers: str):
        if num_workers == "":
            self.core.lgd.config.remove_option("Legendary", "max_workers")
            self.core.lgd.save_config()
            return
        num_workers = int(num_workers)
        if num_workers == 0:
            self.core.lgd.config.remove_option("Legendary", "max_workers")
        else:
            self.core.lgd.config.set("Legendary", "max_workers", str(num_workers))
        self.core.lgd.save_config()

    def cleanup(self, keep_manifests):
        before = self.core.lgd.get_dir_size()
        logger.debug('Removing app metadata...')
        app_names = set(g.app_name for g in self.core.get_assets(update_assets=False))
        self.core.lgd.clean_metadata(app_names)

        if not keep_manifests:
            logger.debug('Removing manifests...')
            installed = [(ig.app_name, ig.version) for ig in self.core.get_installed_list()]
            installed.extend((ig.app_name, ig.version) for ig in self.core.get_installed_dlc_list())
            self.core.lgd.clean_manifests(installed)

        logger.debug('Removing tmp data')
        self.core.lgd.clean_tmp_data()

        after = self.core.lgd.get_dir_size()
        logger.info(f'Cleanup complete! Removed {(before - after) / 1024 / 1024:.02f} MiB.')
        if (before - after) > 0:
            QMessageBox.information(self, "Cleanup", self.tr("Cleanup complete! Successfully removed {}").format(
                get_size(before - after)))
        else:
            QMessageBox.information(self, "Cleanup", "Nothing to clean")

