# -*- coding: UTF-8 -*-
"""
@Project ：BrainViewer 
@File    ：viewer.py.py
@Author  ：Barry
@Date    ：2022/4/14 2:33 
"""
import numpy as np
import nibabel as nib

from PyQt5.QtWidgets import QMainWindow, QShortcut, QMessageBox, QDesktopWidget, QFileDialog, \
                            QColorDialog, QListWidgetItem, QCheckBox
from PyQt5.QtGui import QKeySequence, QBrush, QColor, QDesktopServices, QIcon
from PyQt5.QtCore import Qt, QUrl

from gui.viewer_ui import Ui_MainWindow
from utils.surface import check_hemi
from utils.config import view_dict
from utils.freesurfer import read_freesurfer_lut


# default_lut = 'utils/VepFreeSurferColorLut.txt'
default_lut = 'utils/FreeSurferColorLUT.txt'


class BrainViewer(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(BrainViewer, self).__init__()
        self.setupUi(self)
        self.center_win()
        self.setWindowTitle('BrainViewer')
        self.setWindowIcon(QIcon('fig/brain.ico'))
        self.slot_funcs()

        self.lut_path = None
        self.ids_atlas = None
        self.roi_color = None
        self.volume = None
        self.ids = None
        self.lh_rois = []
        self.rh_rois = []
        self.other_rois = []

        self.lut_path = default_lut
        _, self.ids_atlas, self.roi_color = read_freesurfer_lut(default_lut)

        QShortcut(QKeySequence(self.tr("F10")), self, self.showNormal)
        QShortcut(QKeySequence(self.tr("F11")), self, self.showMaximized)
        QShortcut(QKeySequence(self.tr("Ctrl+Q")), self, self.close)

    def center_win(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def slot_funcs(self):
        self._load_surface_action.triggered.connect(self._load_surface)
        self._load_volume_action.triggered.connect(self._load_volume)
        self._load_lut_action.triggered.connect(self._load_lut)

        self._bg_color_action.triggered.connect(self._set_background_color)
        self._brain_color_action.triggered.connect(self._set_brain_color)

        self._front_action.triggered.connect(self._set_front_view)
        self._back_action.triggered.connect(self._set_back_view)
        self._left_action.triggered.connect(self._set_left_view)
        self._right_action.triggered.connect(self._set_right_view)
        self._top_action.triggered.connect(self._set_top_view)
        self._bottom_action.triggered.connect(self._set_bottom_view)

        self._github_action.triggered.connect(self._open_github)

        self._brain_gp.clicked.connect(self._enable_brain)
        self._brain_hemi_cbx.currentTextChanged.connect(self._set_brain_hemi)
        self._brain_transparency_slider.valueChanged.connect(self._set_brain_transp)

        self._rois_gp.clicked.connect(self._enable_roi)
        self._roi_hemi_cbx.currentTextChanged.connect(self._set_roi_hemi)
        self._roi_transparency_slider.valueChanged.connect(self._set_roi_transp)
        self._lh_info_list.itemClicked.connect(self._enable_lh_roi)
        self._rh_info_list.itemClicked.connect(self._enable_rh_roi)
        self._other_info_list.itemClicked.connect(self._enable_other_roi)

    def _load_surface(self):
        surf_paths, _ = QFileDialog.getOpenFileNames(self, 'Surface',
                                                     filter="Surface (*.pial *.white)")
        if len(surf_paths):
            for surf_path in surf_paths:
                if len(surf_path.split('.')) == 2:
                    opacity = float(self._brain_transparency_slider.value()) / 100
                    self._plotter.add_brain(surf_path, opacity)
                else:
                    QMessageBox.warning(self, 'Surface', 'Only *h.pial or *h.white is supported')

    def _load_volume(self):
        mgz_path, _ = QFileDialog.getOpenFileName(self, 'MRI',  filter="MRI (*.nii *.nii.gz *.mgz)")
        if len(mgz_path):
            self.volume = nib.load(mgz_path)
            self.ids = np.unique(np.asarray(self.volume.dataobj))
            self._plotter.clean_rois()

            self.update_info()

    def _load_lut(self):
        self.lut_path, _ = QFileDialog.getOpenFileName(self, 'ColorLut',
                                                         filter="ColorLut (*.txt)")
        lut_path = self.lut_path
        if len(lut_path):
            _, self.ids_atlas, self.roi_color = read_freesurfer_lut(lut_path)
            print(f'Load Color Lut from {lut_path}')
            self.update_info()

    def update_info(self):
        if self.ids_atlas is None:
            return
        if self.ids is None:
            return
        self.lh_rois = []
        self.rh_rois = []
        self.other_rois = []
        try:
            rois = [self.ids_atlas[index] for index in self.ids]
        except:
            QMessageBox.warning(self, 'Color Lut', 'Color Lut Mismatch!')
            return
        for roi in rois:
            hemi = check_hemi(roi)
            if hemi == 'lh':
                self.lh_rois.append(roi)
            elif hemi == 'rh':
                self.rh_rois.append(roi)
            else:
                self.other_rois.append(roi)
        self._update_list()

    def _update_list(self):
        if len(self.lh_rois):
            self._lh_info_list.clear()
            for roi in self.lh_rois:
                roi_item = QListWidgetItem(roi)
                color = self.roi_color[roi]
                roi_item.setCheckState(Qt.Unchecked)
                roi_item.setBackground(QBrush(QColor(color[0], color[1], color[2])))
                self._lh_info_list.addItem(roi_item)
        if len(self.rh_rois):
            self._rh_info_list.clear()
            for roi in self.rh_rois:
                roi_item = QListWidgetItem(roi)
                color = self.roi_color[roi]
                roi_item.setCheckState(Qt.Unchecked)
                roi_item.setBackground(QBrush(QColor(color[0], color[1], color[2])))
                self._rh_info_list.addItem(roi_item)
        if len(self.other_rois):
            self._other_info_list.clear()
            for roi in self.other_rois:
                roi_item = QListWidgetItem(roi)
                color = self.roi_color[roi]
                roi_item.setCheckState(Qt.Unchecked)
                roi_item.setBackground(QBrush(QColor(color[0], color[1], color[2])))
                self._other_info_list.addItem(roi_item)

    def _enable_brain(self):
        hemi = check_hemi(self._brain_hemi_cbx.currentText())
        viz = self._brain_gp.isChecked()
        self._plotter.enable_brain_viz(viz, hemi)

    def _set_brain_hemi(self):
        hemi = check_hemi(self._brain_hemi_cbx.currentText())
        self._plotter.set_brain_hemi(hemi)

    def _set_brain_transp(self, transp):
        transp = float(transp) / 100
        self._plotter.set_brain_opacity(transp)

    def _enable_roi(self):
        viz = self._rois_gp.isChecked()
        self._plotter.disable_rois_viz(viz)

    def _set_roi_hemi(self):
        hemi = check_hemi(self._roi_hemi_cbx.currentText())
        hemi_index = {'lh': 0, 'rh': 1, 'other': 2}
        index = hemi_index[hemi]
        self._roi_stack.setCurrentIndex(index)

    def _set_roi_transp(self, transp):
        transp = float(transp) / 100
        self._plotter.set_roi_opacity(transp)

    def _enable_lh_roi(self, item):
        roi = item.text()
        viz = not (item.checkState() == Qt.Checked)
        check_state = Qt.Checked if viz else Qt.Unchecked
        item.setCheckState(check_state)
        self._plotter.enable_rois_viz(self.volume, roi, self.lut_path, viz)

    def _enable_rh_roi(self, item):
        roi = item.text()
        viz = not (item.checkState() == Qt.Checked)
        check_state = Qt.Checked if viz else Qt.Unchecked
        item.setCheckState(check_state)
        self._plotter.enable_rois_viz(self.volume, roi, self.lut_path, viz)

    def _enable_other_roi(self, item):
        roi = item.text()
        viz = not (item.checkState() == Qt.Checked)
        check_state = Qt.Checked if viz else Qt.Unchecked
        item.setCheckState(check_state)
        self._plotter.enable_rois_viz(self.volume, roi, self.lut_path, viz)

    def _set_background_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            # 第四位为透明度 color必须在0-1之间
            color = color.getRgbF()[:-1]
            print(f"change brain color to {color}")
            self._plotter.set_background_color(color)

    def _set_brain_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            # 第四位为透明度 color必须在0-1之间
            color = color.getRgbF()[:-1]
            print(f"change brain color to {color}")
            self._plotter.set_brain_color(color)

    def _set_front_view(self):
        view = view_dict['front']
        self._plotter.view_vector(view[0], view[1])

    def _set_back_view(self):
        view = view_dict['back']
        self._plotter.view_vector(view[0], view[1])

    def _set_left_view(self):
        view = view_dict['left']
        self._plotter.view_vector(view[0], view[1])

    def _set_right_view(self):
        view = view_dict['right']
        self._plotter.view_vector(view[0], view[1])

    def _set_top_view(self):
        view = view_dict['top']
        self._plotter.view_vector(view[0], view[1])

    def _set_bottom_view(self):
        view = view_dict['bottom']
        self._plotter.view_vector(view[0], view[1])

    @staticmethod
    def _open_github():
        url = QUrl('https://github.com/BarryLiu97/BrainViewer')
        QDesktopServices.openUrl(url)
