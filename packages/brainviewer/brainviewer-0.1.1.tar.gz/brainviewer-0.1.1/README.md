# 🧠 BrainViewer

![BrainViewer](BrainViewer/fig/main_window.png)  

> *A Python-based 3D Viewer for Visualizing ROIs using FreeSurfer Reconstruction*

## 👁️‍🗨️ Overview

A Python-based 3D Viewer for viszalizing ROIs using the result of FreeSurfer reconstruction. The main functions of this software are brain surface visualization, ROIs visualization and relative settings.

## 🔆Highlights

- Brain surface files (.pial .white)
- Brain segmentation files (.nii .nii.gz .mgz)
- ROIs selection and visualization (marching cubes)
- Settings of colors and views

## 🖥️ Installation

```bash
git clone https://github.com/BarryLiu97/BrainViewer.git
conda create -n viewer python=3.8
conda activate viewer 
cd BrainViewer
pip install -r requirements.txt
```

## 🗝️ Usage

```bash
cd BrainViewer
python main.py
```
