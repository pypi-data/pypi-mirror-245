import os
import pixelgreat as pg
from PIL import Image
from PyQt5.QtCore import Qt, QUrl, QTimer, QSize
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtWidgets import (
    QMainWindow, QWidget,
    QGridLayout, QHBoxLayout, QVBoxLayout,
    QLabel, QPushButton,
    QFileDialog, QAction, QSizePolicy,
    QDialog, QDialogButtonBox, QComboBox, QLineEdit, QCheckBox,
    QSpinBox, QDoubleSpinBox,
    QMessageBox, QTextEdit,
    QAbstractButton,
    QSlider,
    QStyle,
    QProgressDialog,
    QGraphicsView
)
from PyQt5.QtGui import (
    QImage, QPixmap, QIcon,
    QPainter, QColor, QPalette
)

from . import constants, helpers, widgets, settings


# ---- MAIN WINDOW ----

# My QMainWindow class
#   Used to customize the main window.
class MyQMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Setup window title and icon
        self.setWindowTitle(f"{constants.TITLE}")
        self.setWindowIcon(QIcon(constants.ICON_PATHS["program"]))

        # Declare variables
        self.padding_px = 10
        self.status_padding_px = 5
        self.filename = None
        self.source = None
        self.color_mode = None
        self.input_size = None
        self.output_size = None
        self.filter = None
        self.filtered_image = None
        self.status = None
        self.last_save_location = constants.PROG_PATH
        self.last_open_location = constants.PROG_PATH

        # Make main settings object
        self.settings = settings.PixelgreatSettings()

        # Set main window size restrictions
        self.setMinimumSize(300, 300)

        # Setup main viewer
        self.viewer = widgets.PhotoViewer(self, background=QColor(constants.COLORS["viewer"]))
        self.viewer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Declare settings elements
        #   Screen Type
        self.screen_type_entry = QComboBox()
        self.screen_type_entry.addItems(["LCD", "CRT TV", "CRT Monitor"])
        if self.settings.get_screen_type() == pg.ScreenType.LCD:
            self.screen_type_entry.setCurrentIndex(0)
        elif self.settings.get_screen_type() == pg.ScreenType.CRT_TV:
            self.screen_type_entry.setCurrentIndex(1)
        elif self.settings.get_screen_type() == pg.ScreenType.CRT_MONITOR:
            self.screen_type_entry.setCurrentIndex(2)
        self.screen_type_entry.currentIndexChanged.connect(self.screen_type_entry_changed)
        #   Pixel Size
        self.pixel_size_entry = QSpinBox()
        self.pixel_size_entry.setMinimum(3)
        self.pixel_size_entry.setMaximum(9999)
        self.pixel_size_entry.setSingleStep(1)
        self.pixel_size_entry.setSuffix("px")
        self.pixel_size_entry.setValue(self.settings.get_setting("pixel_size"))
        self.pixel_size_entry.valueChanged.connect(self.pixel_size_entry_changed)
        #   Pixel Padding
        self.pixel_padding_entry = QDoubleSpinBox()
        self.pixel_padding_entry.setMinimum(0.0)
        self.pixel_padding_entry.setMaximum(100.0)
        self.pixel_padding_entry.setSingleStep(10.0)
        self.pixel_padding_entry.setSuffix("%")
        self.pixel_padding_entry.setValue(self.settings.get_setting("pixel_padding") * 100)
        self.pixel_padding_entry.valueChanged.connect(self.pixel_padding_entry_changed)
        #   Grid Direction
        self.direction_entry = QComboBox()
        self.direction_entry.addItems(["Vertical", "Horizontal"])
        if self.settings.get_setting("direction") == pg.Direction.VERTICAL:
            self.direction_entry.setCurrentIndex(0)
        elif self.settings.get_setting("direction") == pg.Direction.HORIZONTAL:
            self.direction_entry.setCurrentIndex(1)
        self.direction_entry.currentIndexChanged.connect(self.direction_entry_changed)
        #   Washout
        self.washout_entry = QDoubleSpinBox()
        self.washout_entry.setMinimum(0.0)
        self.washout_entry.setMaximum(100.0)
        self.washout_entry.setSingleStep(10.0)
        self.washout_entry.setSuffix("%")
        self.washout_entry.setValue(self.settings.get_setting("washout") * 100)
        self.washout_entry.valueChanged.connect(self.washout_entry_changed)
        #   Brighten
        self.brighten_entry = QDoubleSpinBox()
        self.brighten_entry.setMinimum(0.0)
        self.brighten_entry.setMaximum(100.0)
        self.brighten_entry.setSingleStep(10.0)
        self.brighten_entry.setSuffix("%")
        self.brighten_entry.setValue(self.settings.get_setting("brighten") * 100)
        self.brighten_entry.valueChanged.connect(self.brighten_entry_changed)
        #   Blur
        self.blur_entry = QDoubleSpinBox()
        self.blur_entry.setMinimum(0.0)
        self.blur_entry.setMaximum(100.0)
        self.blur_entry.setSingleStep(10.0)
        self.blur_entry.setSuffix("%")
        self.blur_entry.setValue(self.settings.get_setting("blur") * 100)
        self.blur_entry.valueChanged.connect(self.blur_entry_changed)
        #   Bloom Size
        self.bloom_size_entry = QDoubleSpinBox()
        self.bloom_size_entry.setMinimum(0.0)
        self.bloom_size_entry.setMaximum(100.0)
        self.bloom_size_entry.setSingleStep(10.0)
        self.bloom_size_entry.setSuffix("%")
        self.bloom_size_entry.setValue(self.settings.get_setting("bloom_size") * 100)
        self.bloom_size_entry.valueChanged.connect(self.bloom_size_entry_changed)
        #   Pixel Aspect
        self.pixel_aspect_entry = QDoubleSpinBox()
        self.pixel_aspect_entry.setMinimum(33.0)
        self.pixel_aspect_entry.setMaximum(300.0)
        self.pixel_aspect_entry.setSingleStep(10.0)
        self.pixel_aspect_entry.setSuffix("%")
        self.pixel_aspect_entry.setValue(self.settings.get_setting("pixel_aspect") * 100)
        self.pixel_aspect_entry.valueChanged.connect(self.pixel_aspect_entry_changed)
        #   Pixel Rounding
        self.rounding_entry = QDoubleSpinBox()
        self.rounding_entry.setMinimum(0.0)
        self.rounding_entry.setMaximum(100.0)
        self.rounding_entry.setSingleStep(10.0)
        self.rounding_entry.setSuffix("%")
        self.rounding_entry.setValue(self.settings.get_setting("rounding") * 100)
        self.rounding_entry.valueChanged.connect(self.rounding_entry_changed)
        #   Scanline Spacing
        self.scanline_spacing_entry = QDoubleSpinBox()
        self.scanline_spacing_entry.setMinimum(33.0)
        self.scanline_spacing_entry.setMaximum(300.0)
        self.scanline_spacing_entry.setSingleStep(10.0)
        self.scanline_spacing_entry.setSuffix("%")
        self.scanline_spacing_entry.setValue(self.settings.get_setting("scanline_spacing") * 100)
        self.scanline_spacing_entry.valueChanged.connect(self.scanline_spacing_entry_changed)
        #   Scanline Size
        self.scanline_size_entry = QDoubleSpinBox()
        self.scanline_size_entry.setMinimum(0.0)
        self.scanline_size_entry.setMaximum(100.0)
        self.scanline_size_entry.setSingleStep(10.0)
        self.scanline_size_entry.setSuffix("%")
        self.scanline_size_entry.setValue(self.settings.get_setting("scanline_size") * 100)
        self.scanline_size_entry.valueChanged.connect(self.scanline_size_entry_changed)
        #   Scanline Blur
        self.scanline_blur_entry = QDoubleSpinBox()
        self.scanline_blur_entry.setMinimum(0.0)
        self.scanline_blur_entry.setMaximum(100.0)
        self.scanline_blur_entry.setSingleStep(10.0)
        self.scanline_blur_entry.setSuffix("%")
        self.scanline_blur_entry.setValue(self.settings.get_setting("scanline_blur") * 100)
        self.scanline_blur_entry.valueChanged.connect(self.scanline_blur_entry_changed)
        #   Scanline Strength
        self.scanline_strength_entry = QDoubleSpinBox()
        self.scanline_strength_entry.setMinimum(0.0)
        self.scanline_strength_entry.setMaximum(100.0)
        self.scanline_strength_entry.setSingleStep(10.0)
        self.scanline_strength_entry.setSuffix("%")
        self.scanline_strength_entry.setValue(self.settings.get_setting("scanline_strength") * 100)
        self.scanline_strength_entry.valueChanged.connect(self.scanline_strength_entry_changed)
        #   Bloom Strength
        self.bloom_strength_entry = QDoubleSpinBox()
        self.bloom_strength_entry.setMinimum(0.0)
        self.bloom_strength_entry.setMaximum(100.0)
        self.bloom_strength_entry.setSingleStep(10.0)
        self.bloom_strength_entry.setSuffix("%")
        self.bloom_strength_entry.setValue(self.settings.get_setting("bloom_strength") * 100)
        self.bloom_strength_entry.valueChanged.connect(self.bloom_strength_entry_changed)
        #   Grid Strength
        self.grid_strength_entry = QDoubleSpinBox()
        self.grid_strength_entry.setMinimum(0.0)
        self.grid_strength_entry.setMaximum(100.0)
        self.grid_strength_entry.setSingleStep(10.0)
        self.grid_strength_entry.setSuffix("%")
        self.grid_strength_entry.setValue(self.settings.get_setting("grid_strength") * 100)
        self.grid_strength_entry.valueChanged.connect(self.grid_strength_entry_changed)
        #   Output Scale
        self.output_scale_entry = QDoubleSpinBox()
        self.output_scale_entry.setMinimum(25.0)
        self.output_scale_entry.setMaximum(9999.0)
        self.output_scale_entry.setSingleStep(25.0)
        self.output_scale_entry.setSuffix("%")
        self.output_scale_entry.setValue(self.settings.get_setting("output_scale") * 100)
        self.output_scale_entry.valueChanged.connect(self.output_scale_entry_changed)
        #   Pixelate
        self.pixelate_entry = QCheckBox()
        self.pixelate_entry.setChecked(self.settings.get_setting("pixelate"))
        self.pixelate_entry.stateChanged.connect(self.pixelate_entry_changed)
        #   Apply Button
        self.apply_button = QPushButton("Apply Settings")
        self.apply_button.clicked.connect(self.apply_button_clicked)
        #   Reset Settings Button
        self.reset_button = QPushButton("Reset Settings")
        self.reset_button.clicked.connect(self.reset_button_clicked)
        #   Original Image Button
        self.original_button = QPushButton("Original Image")
        self.original_button.clicked.connect(self.original_button_clicked)

        # Declare settings area
        self.settings_area = QGridLayout()
        self.settings_area.setContentsMargins(self.padding_px, 0, self.padding_px, 0)
        self.settings_area.setSpacing(self.padding_px)

        # Populate settings area
        self.entries_array = [
            [   # Col 0-1
                [QLabel("Brighten Source:"), self.brighten_entry],
                [QLabel("Washout Source:"), self.washout_entry],
                [QLabel("Blur Source:"), self.blur_entry],
                [QLabel("Output Scale:"), self.output_scale_entry],
            ],
            [   # Col 2-3
                [QLabel("RGB Filter Type:"), self.screen_type_entry],
                [QLabel("RGB Filter Direction:"), self.direction_entry],
                [QLabel("Pixel Size:"), self.pixel_size_entry],
                [QLabel("Pixel Aspect:"), self.pixel_aspect_entry],
            ],
            [   # Col 4-5
                [QLabel("RGB Filter Strength:"), self.grid_strength_entry],
                [QLabel("RGB Pixel Padding:"), self.pixel_padding_entry],
                [QLabel("RGB Pixel Rounding:"), self.rounding_entry],
                [QLabel("Pixelate Source:"), self.pixelate_entry],
            ],
            [   # Col 6-7
                [QLabel("Scanline Strength:"), self.scanline_strength_entry],
                [QLabel("Scanline Spacing:"), self.scanline_spacing_entry],
                [QLabel("Scanline Size:"), self.scanline_size_entry],
                [QLabel("Scanline Blur:"), self.scanline_blur_entry],
            ],
            [   # Col 8-9
                [QLabel("Bloom Strength:"), self.bloom_strength_entry],
                [QLabel("Bloom Size:"), self.bloom_size_entry],
                [QLabel(), self.original_button],
                [self.reset_button, self.apply_button]
            ],
        ]
        for column, column_group in enumerate(self.entries_array):
            for row, row_group in enumerate(column_group):
                if row_group is not None:
                    self.settings_area.addWidget(
                        row_group[0],
                        row,
                        column * 2,
                        alignment=Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight
                    )
                    self.settings_area.addWidget(
                        row_group[1],
                        row,
                        (column * 2) + 1,
                        alignment=Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft
                    )

        # Start the settings area disabled
        self.set_settings_entries_enabled(False)

        # Declare status bar elements
        self.status_label = QLabel()
        self.set_status("No File Loaded")

        # Declare status bar container
        self.status_container = QWidget(self)
        self.status_container.setContentsMargins(
            self.padding_px,
            self.status_padding_px,
            self.padding_px,
            self.status_padding_px
        )
        self.status_container.setStyleSheet("background-color:{bg}; color:{text}".format(
            bg=constants.COLORS["status_background"],
            text=constants.COLORS["status_text"])
        )

        # Declare status area
        self.status_area = QHBoxLayout(self.status_container)
        self.status_area.setContentsMargins(0, 0, 0, 0)
        self.status_area.setSpacing(self.padding_px)

        # Populate status area layout
        self.status_area.addWidget(
            self.status_label,
            alignment=Qt.AlignmentFlag.AlignCenter
        )

        # Declare main layout
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(self.padding_px)

        # Populate main layout
        self.main_layout.addWidget(self.viewer)
        self.main_layout.addLayout(self.settings_area)
        self.main_layout.addWidget(self.status_container)

        # Set main layout as the central widget
        self.main_widget = QWidget()
        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)

        # Declare a menu bar
        self.main_menu = self.menuBar()

        # Declare a "File" menu
        self.file_menu = self.main_menu.addMenu("File")

        # Populate the "File" menu
        self.file_menu_open = QAction("Open...", self)
        self.file_menu_open.triggered.connect(self.open_clicked)
        self.file_menu.addAction(self.file_menu_open)

        self.file_menu_close = QAction("Close", self)
        self.file_menu_close.triggered.connect(self.close_clicked)
        self.file_menu.addAction(self.file_menu_close)

        # Declare the "Export" menu
        self.export_menu = self.main_menu.addMenu("Export...")
        self.export_menu.setEnabled(False)

        # Populate the export menu
        self.export_menu_image = QAction("Image...", self)
        self.export_menu_image.triggered.connect(self.export_image_clicked)
        self.export_menu.addAction(self.export_menu_image)

        # Declare the "Help" menu
        self.help_menu = self.main_menu.addMenu("Help")

        # Populate the "Help" menu
        self.help_menu_about = QAction("About...", self)
        self.help_menu_about.triggered.connect(self.about_clicked)
        self.help_menu.addAction(self.help_menu_about)

        # Finally, set the window size based on it's sizeHint after 10 millis
        QTimer.singleShot(10, self.setup_window_size)

    def setup_window_size(self):
        size_hint = self.sizeHint()
        start_size = QSize(size_hint.width(), size_hint.height() * 3)
        min_size = QSize(size_hint.width(), size_hint.height() * 2)
        self.setMinimumSize(min_size)
        self.resize(start_size)

    def set_viewer_image(self, image=None):
        if image is not None:
            self.viewer.set_photo(helpers.image_to_pixmap(image))
        else:
            self.viewer.set_photo(None)

    def set_source(self, filename=None):
        self.filename = filename
        if self.filename is not None:
            self.source = Image.open(self.filename)
            self.color_mode = self.source.mode
            self.set_viewer_image(self.source)
            self.set_settings_entries_enabled(True)
            self.input_size = self.source.size
            self.output_size = (
                    round(self.input_size[0] * self.settings.get_setting("output_scale")),
                    round(self.input_size[1] * self.settings.get_setting("output_scale"))
            )
            self.export_menu.setEnabled(True)
            self.set_status(f"Loaded file: {self.filename}")
        else:
            self.source = None
            self.color_mode = None
            self.set_viewer_image(None)
            self.set_settings_entries_enabled(False)
            self.input_size = None
            self.output_size = None
            self.filter = None
            self.filtered_image = None
            self.export_menu.setEnabled(False)
            self.set_status("No File Loaded")

    def set_settings_entries_enabled(self, enabled):
        for element in [
            self.screen_type_entry,
            self.direction_entry,
            self.washout_entry,
            self.pixel_padding_entry,
            self.brighten_entry,
            self.blur_entry,
            self.bloom_size_entry,
            self.pixel_aspect_entry,
            self.rounding_entry,
            self.scanline_spacing_entry,
            self.scanline_size_entry,
            self.scanline_blur_entry,
            self.scanline_strength_entry,
            self.bloom_strength_entry,
            self.grid_strength_entry,
            self.output_scale_entry,
            self.pixelate_entry,
            self.apply_button,
            self.pixel_size_entry,
            self.reset_button,
            self.original_button,
        ]:
            element.setEnabled(enabled)

    # Called when the Screen Type is changed
    # Therefore, the Screen Type entry is NOT updated here
    def update_settings_entries(self):
        if self.settings.get_setting("direction") == pg.Direction.VERTICAL:
            self.direction_entry.setCurrentIndex(0)
        elif self.settings.get_setting("direction") == pg.Direction.HORIZONTAL:
            self.direction_entry.setCurrentIndex(1)

        # Set the percentage inputs
        for element, name in [
            [self.washout_entry, "washout"],
            [self.pixel_padding_entry, "pixel_padding"],
            [self.brighten_entry, "brighten"],
            [self.blur_entry, "blur"],
            [self.bloom_size_entry, "bloom_size"],
            [self.pixel_aspect_entry, "pixel_aspect"],
            [self.rounding_entry, "rounding"],
            [self.scanline_spacing_entry, "scanline_spacing"],
            [self.scanline_size_entry, "scanline_size"],
            [self.scanline_blur_entry, "scanline_blur"],
            [self.scanline_strength_entry, "scanline_strength"],
            [self.bloom_strength_entry, "bloom_strength"],
            [self.grid_strength_entry, "grid_strength"],
            [self.output_scale_entry, "output_scale"],
        ]:
            element.setValue(self.settings.get_setting(name) * 100)

        # Set boolean values
        for element, name in [
            [self.pixelate_entry, "pixelate"],
        ]:
            element.setChecked(self.settings.get_setting(name))

        # Set integer values
        for element, name in [
            [self.pixel_size_entry, "pixel_size"],
        ]:
            element.setValue(self.settings.get_setting(name))

    def screen_type_entry_changed(self, idx):
        if idx == 0:
            self.settings.set_screen_type(pg.ScreenType.LCD)
        elif idx == 1:
            self.settings.set_screen_type(pg.ScreenType.CRT_TV)
        elif idx == 2:
            self.settings.set_screen_type(pg.ScreenType.CRT_MONITOR)

        self.update_settings_entries()

    def direction_entry_changed(self, idx):
        if idx == 0:
            self.settings.set_setting("direction", pg.Direction.VERTICAL)
        elif idx == 1:
            self.settings.set_setting("direction", pg.Direction.HORIZONTAL)

    def washout_entry_changed(self, value):
        self.settings.set_setting("washout", value / 100)

    def pixel_padding_entry_changed(self, value):
        self.settings.set_setting("pixel_padding", value / 100)

    def brighten_entry_changed(self, value):
        self.settings.set_setting("brighten", value / 100)

    def blur_entry_changed(self, value):
        self.settings.set_setting("blur", value / 100)

    def bloom_size_entry_changed(self, value):
        self.settings.set_setting("bloom_size", value / 100)

    def pixel_aspect_entry_changed(self, value):
        self.settings.set_setting("pixel_aspect", value / 100)

    def rounding_entry_changed(self, value):
        self.settings.set_setting("rounding", value / 100)

    def scanline_spacing_entry_changed(self, value):
        self.settings.set_setting("scanline_spacing", value / 100)

    def scanline_size_entry_changed(self, value):
        self.settings.set_setting("scanline_size", value / 100)

    def scanline_blur_entry_changed(self, value):
        self.settings.set_setting("scanline_blur", value / 100)

    def scanline_strength_entry_changed(self, value):
        self.settings.set_setting("scanline_strength", value / 100)

    def bloom_strength_entry_changed(self, value):
        self.settings.set_setting("bloom_strength", value / 100)

    def grid_strength_entry_changed(self, value):
        self.settings.set_setting("grid_strength", value / 100)

    def pixel_size_entry_changed(self, value):
        self.settings.set_setting("pixel_size", value)

    def output_scale_entry_changed(self, value):
        self.settings.set_setting("output_scale", value / 100)
        self.output_size = (
            round(self.input_size[0] * self.settings.get_setting("output_scale")),
            round(self.input_size[1] * self.settings.get_setting("output_scale"))
        )

    def pixelate_entry_changed(self, value):
        if value == 0:
            self.settings.set_setting("pixelate", False)
        else:
            self.settings.set_setting("pixelate", True)

    def update_filter(self):
        self.filter = pg.Pixelgreat(
            output_size=self.output_size,
            pixel_size=self.settings.get_setting("pixel_size"),
            screen_type=self.settings.get_screen_type(),
            direction=self.settings.get_setting("direction"),
            pixel_aspect=self.settings.get_setting("pixel_aspect"),
            pixelate=self.settings.get_setting("pixelate"),
            brighten=self.settings.get_setting("brighten"),
            blur=self.settings.get_setting("blur"),
            washout=self.settings.get_setting("washout"),
            scanline_strength=self.settings.get_setting("scanline_strength"),
            scanline_spacing=self.settings.get_setting("scanline_spacing"),
            scanline_size=self.settings.get_setting("scanline_size"),
            scanline_blur=self.settings.get_setting("scanline_blur"),
            grid_strength=self.settings.get_setting("grid_strength"),
            pixel_padding=self.settings.get_setting("pixel_padding"),
            rounding=self.settings.get_setting("rounding"),
            bloom_strength=self.settings.get_setting("bloom_strength"),
            bloom_size=self.settings.get_setting("bloom_size"),
            color_mode=self.color_mode
        )

    def get_filtered_image(self):
        if self.source is not None and self.filter is not None:
            return self.filter.apply(self.source)
        else:
            return self.source

    def update_filtered_image(self):
        self.filtered_image = self.get_filtered_image()

    def set_status(self, status):
        self.status = status
        self.status_label.setText(self.status)

    def apply_button_helper(self, end_status):
        self.update_filter()
        self.update_filtered_image()
        self.set_viewer_image(self.filtered_image)
        self.set_status(end_status)

    def apply_button_clicked(self):
        self.viewer.fitInView()
        self.set_status("Applying settings...")
        QTimer.singleShot(10, lambda: self.apply_button_helper(f"Loaded file: {self.filename} (converted)"))

    def reset_button_clicked(self):
        self.settings.set_to_defaults()

        if self.settings.get_screen_type() == pg.ScreenType.LCD:
            self.screen_type_entry.setCurrentIndex(0)
        elif self.settings.get_screen_type() == pg.ScreenType.CRT_TV:
            self.screen_type_entry.setCurrentIndex(1)
        elif self.settings.get_screen_type() == pg.ScreenType.CRT_MONITOR:
            self.screen_type_entry.setCurrentIndex(2)

        self.update_settings_entries()

    def original_button_clicked(self):
        self.set_viewer_image(self.source)
        self.set_status(f"Loaded file: {self.filename}")

    def open_clicked(self):
        filename, filetype = QFileDialog.getOpenFileName(
            self,
            "Open File",
            self.last_open_location,
            "Image Files (*.png *.jpg *.bmp)"
        )

        if filename != "":
            file_path, file_title = os.path.split(filename)
            self.last_open_location = file_path
            self.set_source(filename)

    def export_helper(self, filename):
        self.get_filtered_image().save(filename)
        self.set_status(f"Saved file: {filename}")

    def export_image_clicked(self):
        path, fullname = os.path.split(self.filename)
        name, ext = os.path.splitext(fullname)
        filename, filetype = QFileDialog.getSaveFileName(
            self,
            "Export Image As...",
            os.path.join(self.last_save_location, f"{name}_pixelated{ext}"),
            f"PNG (*.png);;"
            f"JPEG (*.jpg);;"
            f"BMP (*.bmp)"
        )

        if filename != "":
            file_path, file_title = os.path.split(filename)
            self.last_save_location = file_path
            self.set_status(f"Exporting image...")
            QTimer.singleShot(10, lambda: self.export_helper(filename))

    def close_clicked(self):
        self.set_source(None)

    def about_clicked(self):
        popup = About(parent=self)

        result = popup.exec()

    def resizeEvent(self, event):
        self.viewer.fitInView()


# ---- POPUP WINDOWS ----

# About dialog
#   Gives info about the program
class About(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        # Setup window title and icon
        self.setWindowTitle(f"About {constants.TITLE}")
        self.setWindowIcon(QIcon(constants.ICON_PATHS["program"]))

        # Hide "?" button
        self.setWindowFlags(self.windowFlags() ^ Qt.WindowContextHelpButtonHint)

        self.icon_size = 200

        self.icon_label = QLabel()
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.icon_label.setPixmap(QPixmap(constants.ICON_PATHS["program"]))
        self.icon_label.setScaledContents(True)
        self.icon_label.setFixedSize(self.icon_size, self.icon_size)

        self.about_text = QLabel(
            f"{constants.TITLE} v{constants.VERSION}\nby {constants.COPYRIGHT}\nCopyright 2023\n\n"
            f"{constants.DESCRIPTION}\n\n"
            f"Project Home Page:\n{constants.PROJECT_URL}\n\n"
            f"Patreon:\n{constants.DONATE_URL}")
        self.about_text.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.confirm_buttons = QDialogButtonBox(QDialogButtonBox.Ok)
        self.confirm_buttons.accepted.connect(self.accept)

        self.main_layout = QGridLayout()

        self.main_layout.addWidget(self.icon_label, 0, 0, 2, 1)
        self.main_layout.addWidget(self.about_text, 0, 1)
        self.main_layout.addWidget(self.confirm_buttons, 1, 0, 1, 2)

        self.setLayout(self.main_layout)

        self.resize_window()

    def resize_window(self):
        self.setFixedSize(self.sizeHint())
