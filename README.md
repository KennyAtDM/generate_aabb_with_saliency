# generate_aabb_with_saliency

This repository contains scripts for parallel processing of scenes in a directory and filter pointcloids/generate aabb box with saliency masks detection.

## Overview

The main script (`generate_aabb.py`) orchestrates the processing of multiple scenes concurrently. Each scene directory undergoes two processing steps:

1. **Saliency detection**: Utilizes the BiRefNet-massive-epoch_240 model for high-resolution dichotomous image segmentation.
GitHub Repository: BiRefNet GitHub Repository [https://github.com/ZhengPeng7/BiRefNet]
2. **Opening**: Opening binary masks in each scene using `opening_op_single_scene.py`.
3. **Filtering**: Applies additional filtering on processed scenes using `filter_single_scene.py`.

## Getting Started

### Prerequisites

- Python 3.x
- Required Python packages (listed in `requirements.txt`)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/KennyAtDM/generate_aabb_with_saliency.git
   cd generate_aabb_with_saliency
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Usage

1. Set the `project_dir` variable in `generate_aabb.py` to the directory containing your scene directories.

2. Run `generate_aabb.py`:
   ```bash
   python generate_aabb.py
   ```

   This will initiate parallel processing of all scene directories found in `project_dir`.

## Scripts

### `generate_aabb.py`

The main script that initiates parallel scene processing using `ProcessPoolExecutor`.

#### Usage:

```bash
python generate_aabb.py
```

### `dilation_single_scene.py`

Script for dilating binary masks in a single scene directory.

#### Usage:

```bash
python opening_op_single_scene.py --project_dir /path/to/scene_directory
```

### `filter_single_scene.py`

Script for additional filtering on a single processed scene directory.

#### Usage:

```bash
python filter_single_scene.py --project_dir /path/to/scene_directory
```
