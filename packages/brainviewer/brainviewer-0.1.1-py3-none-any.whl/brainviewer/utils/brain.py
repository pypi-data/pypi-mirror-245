# -*- coding: UTF-8 -*-
"""
@Project ：BrainViewer
@File    ：brain.py
@Author  ：Barry
@Date    ：2022/3/16 15:27 
"""
import os.path as op
import numpy as np
import pyvista as pv
from pyvistaqt import QtInteractor

from .surface import read_fs_surface, create_roi_surface
from .config import color, brain_kwargs, text_kwargs, roi_kwargs


class Brain(QtInteractor):
    def __init__(self, parent=None):
        # Must Add this parent=None is this format
        # otherwise error shows up
        # for this widget would be added to a Layout
        # it needs a parent, no change of this!
        super(Brain, self).__init__(parent)
        self.background_color = 'w'
        self.enable_depth_peeling()
        self.enable_anti_aliasing()
        self.line_smoothing =True
        self.point_smoothing =True

        self.brain_surface = {}
        self.brain_actors = {}
        self.roi_actors = {}
        self.text_actors = {}
        self.viz_rois = []
        self.roi_color = {}

    def add_brain(self, surf_path, opacity):
        hemi = 'lh' if 'lh' in surf_path else 'rh'
        coords, faces = read_fs_surface(surf_path)
        self.brain_surface[hemi] = pv.PolyData(coords, faces)
        brain_kwargs['opacity'] = opacity
        for h in self.brain_surface:
            self.brain_actors[h] = self.add_mesh(self.brain_surface[h], name=h, **brain_kwargs)

    def enable_brain_viz(self, viz, hemi):
        if isinstance(hemi, list):
            [self.brain_actors[name].SetVisibility(viz) for name in self.brain_actors]
        else:
            if hemi in self.brain_actors:
                self.brain_actors[hemi].SetVisibility(viz)

    def set_background_color(self, bk_color):
        self.set_background(color=bk_color)

    def set_brain_color(self, brain_color):
        [self.brain_actors[name].GetProperty().SetColor(brain_color) for name in self.brain_actors]

    def set_brain_opacity(self, opacity):
        [self.brain_actors[name].GetProperty().SetOpacity(opacity) for name in self.brain_actors]

    def set_brain_hemi(self, hemi):
        if isinstance(hemi, list):
            [self.brain_actors[name].SetVisibility(True) for name in self.brain_actors]
        else:
            nviz_hemi = ['lh', 'rh']
            nviz_hemi.remove(hemi)
            if hemi in self.brain_actors:
                self.brain_actors[hemi].SetVisibility(True)
            if nviz_hemi[0] in self.brain_actors:
                self.brain_actors[nviz_hemi[0]].SetVisibility(False)

    def add_rois(self, mgz, roi, lut_path):
        roi_mesh, roi_color = create_roi_surface(mgz, roi, lut_path)
        if roi_mesh is not None:
            print(f'Add ROI {roi}')
            self.roi_actors[roi] = self.add_mesh(roi_mesh, name=roi, label=roi,
                                                 color=roi_color, **roi_kwargs)
            self.roi_color[roi] = roi_color

    def enable_rois_viz(self, mgz, roi, lut_path, viz):
        if roi not in self.roi_actors and viz:
            self.add_rois(mgz, roi, lut_path)
            self.viz_rois.append(roi)
            self.add_rois_text(self.viz_rois)
        elif roi in self.roi_actors:
            self.roi_actors[roi].SetVisibility(viz)
            if viz:
                self.viz_rois.append(roi)
            else:
                self.viz_rois.remove(roi)
            self.add_rois_text(self.viz_rois)

    def disable_rois_viz(self, viz):
        [self.roi_actors[roi].SetVisibility(viz) for roi in self.roi_actors]
        [self.text_actors[roi].SetVisibility(viz) for roi in self.text_actors]

    def add_rois_text(self, rois):
        if len(self.text_actors):
            [self.remove_actor(self.text_actors[roi]) for roi in self.text_actors]
            self.text_actors = {}
        start_pos = np.array([5, 10])
        font_size = 9 if len(rois) < 15 else 6
        for index, roi in enumerate(rois):
            text_pos = start_pos + np.array([0, index*25])
            roi_color = self.roi_color[roi]
            self.text_actors[f'{roi} text'] = self.add_text(text=roi, position=text_pos,
                                                            font_size=font_size, color=roi_color)

    def set_roi_opacity(self, opacity):
        [self.roi_actors[roi].GetProperty().SetOpacity(opacity) for roi in self.roi_actors]

    def clean_rois(self):
        [self.remove_actor(self.roi_actors[roi]) for roi in self.roi_actors]
        [self.remove_actor(self.text_actors[roi]) for roi in self.text_actors]
        self.text_actors = {}
        self.roi_actors = {}
        self.viz_rois = []


