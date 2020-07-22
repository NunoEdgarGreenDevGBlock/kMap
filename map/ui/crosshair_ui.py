from map.ui.abstract_ui import AbstractUI
from PyQt5.QtWidgets import (
    QCheckBox, QHBoxLayout, QVBoxLayout, QLabel, QGridLayout, QDoubleSpinBox)
from PyQt5.QtWidgets import QSizePolicy as QSP
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class CrosshairUI(AbstractUI):

    def _initialize_content(self):

        self.setTitle('Crosshair')
        self.setStyleSheet('QGroupBox { font-weight: bold; } ')

        # Enable Label
        enable_label = QLabel('Enable:')

        # Show Crosshair
        self.enable_crosshair = QCheckBox('Crosshair')

        # Top Layout
        self.top_layout = QHBoxLayout()
        self.top_layout.addWidget(enable_label)
        self.top_layout.addWidget(self.enable_crosshair)

        # Label
        x_label = QLabel('x-Pos.')
        y_label = QLabel('y-Pos.')

        # Spinboxes
        self.x_spinbox = QDoubleSpinBox()
        self.x_spinbox.setSuffix('  Å^-1')
        self.x_spinbox.setMinimum(self.v_line.bounds()[0])
        self.x_spinbox.setMaximum(self.v_line.bounds()[1])
        self.x_spinbox.setDecimals(2)
        self.x_spinbox.setSingleStep(0.02)
        self.y_spinbox = QDoubleSpinBox()
        self.y_spinbox.setSuffix('  Å^-1')
        self.y_spinbox.setMinimum(self.h_line.bounds()[0])
        self.y_spinbox.setMaximum(self.h_line.bounds()[1])
        self.y_spinbox.setDecimals(2)
        self.y_spinbox.setSingleStep(0.02)

        # Value Label
        distance_label = QLabel('<html><head/><body><p>k<span style="' +
                                'vertical-align:sub;">||</span></p>' +
                                '</body></html>')
        point_label = QLabel('Int. (Point)')

        # Value
        self.distance_value = QLabel('0.0  Å^-1')
        self.point_value = QLabel('0.0  a.u.')

        # Bottom Layout
        self.bottom_layout = QGridLayout()
        self.bottom_layout.addWidget(x_label, 0, 0)
        self.bottom_layout.addWidget(y_label, 1, 0)
        self.bottom_layout.addWidget(self.x_spinbox, 0, 1)
        self.bottom_layout.addWidget(self.y_spinbox, 1, 1)
        self.bottom_layout.addWidget(distance_label, 0, 2)
        self.bottom_layout.addWidget(point_label, 1, 2)
        self.bottom_layout.addWidget(self.distance_value, 0, 3)
        self.bottom_layout.addWidget(self.point_value, 1, 3)

        # Main Layout
        main_layout = QVBoxLayout()
        main_layout.addLayout(self.top_layout)
        main_layout.addLayout(self.bottom_layout)

        self.setLayout(main_layout)

    def _initialize_connections(self):

        self.x_spinbox.valueChanged.connect(self._move_crosshair_from_spinbox)
        self.y_spinbox.valueChanged.connect(self._move_crosshair_from_spinbox)

        self.enable_crosshair.stateChanged.connect(self._enable_crosshair)

        self.v_line.sigDragged.connect(self._move_crosshair_from_drag)
        self.h_line.sigDragged.connect(self._move_crosshair_from_drag)
        self.plot_item.view.scene().sigMouseClicked.connect(
            self._move_crosshair_from_click)


class CrosshairROIUI(CrosshairUI):

    def _initialize_content(self):

        super()._initialize_content()

        # Show ROI
        self.enable_roi = QCheckBox('ROI')
        self.top_layout.addWidget(self.enable_roi)

        # Label
        roi_label = QLabel('Radius')
        self.bottom_layout.addWidget(roi_label, 2, 0)

        # Spinboxes
        self.roi_spinbox = QDoubleSpinBox()
        self.roi_spinbox.setSuffix('  Å^-1')
        self.roi_spinbox.setMinimum(0.01)
        self.roi_spinbox.setMaximum(10)
        self.roi_spinbox.setDecimals(2)
        self.roi_spinbox.setValue(self.roi.size()[0] / 2)
        self.roi_spinbox.setSingleStep(0.02)
        self.bottom_layout.addWidget(self.roi_spinbox, 2, 1)

        # Value Label
        area_label = QLabel('Int. (Area)')
        self.bottom_layout.addWidget(area_label, 2, 2)

        # Value
        self.area_value = QLabel('0.0  a.u.')
        self.bottom_layout.addWidget(self.area_value, 2, 3)

    def _initialize_connections(self):

        super()._initialize_connections()

        self.enable_roi.stateChanged.connect(self._enable_roi)

        self.roi_spinbox.valueChanged.connect(self._resize_roi_from_spinbox)
        self.roi.sigRegionChangeFinished.connect(self._resize_roi_from_drag)
        self.roi.sigRegionChangeStarted.connect(self._dragging_roi)


class CrosshairAnnulusUI(CrosshairROIUI):

    def _initialize_content(self):

        super()._initialize_content()

        # Show Annulus
        self.enable_an = QCheckBox('Annulus')
        self.top_layout.addWidget(self.enable_an)

        # Label
        an_label = QLabel('Width')
        self.bottom_layout.addWidget(an_label, 3, 0)

        # Spinboxes
        self.an_spinbox = QDoubleSpinBox()
        self.an_spinbox.setSuffix('  Å^-1')
        self.an_spinbox.setMinimum(0.01)
        self.an_spinbox.setMaximum(10)
        self.an_spinbox.setDecimals(2)
        self.an_spinbox.setValue(
            (self.annulus.size()[0] - self.roi.size()[0]) / 2)
        self.an_spinbox.setSingleStep(0.01)
        self.bottom_layout.addWidget(self.an_spinbox, 3, 1)

        # Value Label
        ring_label = QLabel('Int. (Annulus)')
        self.bottom_layout.addWidget(ring_label, 3, 2)

        # Value
        self.ring_value = QLabel('0.0  a.u.')
        self.bottom_layout.addWidget(self.ring_value, 3, 3)

    def _initialize_connections(self):

        super()._initialize_connections()

        self.enable_an.stateChanged.connect(self._enable_an)

        self.an_spinbox.valueChanged.connect(self._resize_annulus_from_spinbox)
        self.annulus.sigRegionChangeFinished.connect(
            self._resize_annulus_from_drag)
        self.annulus.sigRegionChangeStarted.connect(self._dragging_an)
