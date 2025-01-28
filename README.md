# SkyScenes Dataset Processing

This repository contains tools for downloading and processing the SkyScenes dataset into FiftyOne format for easier visualization and analysis.

This dataset is also [available via the Hugging Face Hub](https://huggingface.co/datasets/harpreetsahota/SkyScenes). To download from there:

```python
import fiftyone as fo
from fiftyone.utils.huggingface import load_from_hub

# Load the dataset
# Note: other available arguments include 'max_samples', etc
dataset = load_from_hub("Voxel51/SkyScenes")
```

## SkyScenes Dataset Overview

SkyScenes is a comprehensive synthetic dataset for aerial scene understanding that was recently accepted to ECCV 2024. The dataset contains 33,600 aerial images captured from UAV perspectives using the CARLA simulator.

### Dataset Structure
- **Images**: RGB images captured across multiple variations:
  - 8 different town layouts (7 urban + 1 rural)
  - 5 weather/time conditions (ClearNoon, ClearSunset, ClearNight, CloudyNoon, MidRainyNoon)
  - 12 viewpoint combinations (3 heights × 4 pitch angles)

### Annotations
Each image comes with dense pixel-level annotations for:
- Semantic segmentation (28 classes)
- Instance segmentation
- Depth information

### Key Variations
1. **Heights**: 15m, 35m, 60m
2. **Pitch Angles**: 0°, 45°, 60°, 90°
3. **Weather/Time**: Various conditions to test robustness
4. **Layouts**: Different urban and rural environments




## Usage

### 1. Download Dataset

Use the `download_dataset.sh` script to download specific subsets of the dataset:

```shell

bash ./download_dataset.sh
```

The script allows customization of:
- Heights and pitch angles (default: H_15_P_0, H_35_P_0, H_60_P_0)
- Weather conditions (default: ClearNoon)
- Town layouts (default: Town01, Town02, Town05, Town07)
- Data modalities (Images, Depth, Segmentation)

### 2. Create FiftyOne Dataset

After downloading, use `create_fo_dataset.py` to organize the data into a FiftyOne dataset.

This code includes utilities which:
- Groups related images by camera angle
- Associates RGB images with corresponding depth and segmentation masks
- Sets up proper color mapping for segmentation visualization
- Creates a searchable/viewable dataset structure

## Benefits of FiftyOne Implementation

The FiftyOne implementation provides several advantages:

- **Grouped Views**: Images from different angles are grouped together

- **Multi-modal Support**: Handles RGB, depth, and segmentation data

- **Visualization**: Built-in support for viewing segmentation masks using the defined color map

- **Easy Navigation**: Structured access to the dataset's various components

This organization makes it easier to:
- Browse and visualize the dataset
- Train and evaluate models
- Analyze different viewpoints and conditions
- Compare annotations across modalities

## References

- [SkyScenes Dataset on HuggingFace](https://huggingface.co/datasets/hoffman-lab/SkyScenes)
- [SkyScenes Official Website](https://hoffman-group.github.io/SkyScenes/)

## Citation

```bibex
@misc{khose2023skyscenes,
      title={SkyScenes: A Synthetic Dataset for Aerial Scene Understanding}, 
      author={Sahil Khose and Anisha Pal and Aayushi Agarwal and Deepanshi and Judy Hoffman and Prithvijit Chattopadhyay},
      year={2023},
      eprint={2312.06719},
      archivePrefix={arXiv},
      primaryClass={cs.CV}
}
```