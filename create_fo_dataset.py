from pathlib import Path
from collections import defaultdict
import fiftyone as fo

INSTANCES_COLOR_MAP = {
    '#000000': 'unlabeled',
    '#464646': 'building',
    '#be9999': 'fence',
    '#375a50': 'other',
    '#dc143c': 'pedestrian',
    '#999999': 'pole',
    '#9dea32': 'roadline',
    '#804080': 'road',
    '#f423e8': 'sidewalk',
    '#6b8e23': 'vegetation',
    '#00008e': 'cars',
    '#66669c': 'wall',
    '#dcdc00': 'traffic sign',
    '#4682b4': 'sky',
    '#510051': 'ground',
    '#966464': 'bridge',
    '#e6968c': 'railtrack',
    '#b4a5b4': 'guardrail',
    '#faaa1e': 'traffic light',
    '#6ebea0': 'static',
    '#aa7832': 'dynamic',
    '#2d3c96': 'water',
    '#98fb98': 'terrain',
    '#ff0000': 'rider',
    '#770b20': 'bicycle',
    '#0000e6': 'motorcycle',
    '#003c64': 'bus',
    '#000046': 'truck'
}

from pathlib import Path
from collections import defaultdict
import fiftyone as fo

def collect_frame_filepaths(base_dir):
    """Collects all filepaths for each frame, angle, and modality.
    
    Returns:
        dict: {frame_id: {angle: {modality: filepath}}}
    """
    base_path = Path(base_dir).resolve()  
    frame_data = defaultdict(lambda: defaultdict(dict))
    
    for town in ["Town01", "Town02", "Town05", "Town07"]:
        for camera_angle in ["H_15_P_0", "H_35_P_0", "H_60_P_0"]:
            # Collect RGB images
            rgb_path = base_path / "Images" / camera_angle / "ClearNoon" / town
            if not rgb_path.exists():
                print(f"Path does not exist: {rgb_path.resolve()}")  # Debug print
                continue
                
            for img_file in rgb_path.glob("*.png"):
                prefix = img_file.name.split('_')[0]
                frame_data[prefix][camera_angle]["rgb"] = str(img_file.resolve())
                
                # Find corresponding files
                modality_paths = {
                    "depth": base_path / "Depth" / camera_angle / "ClearNoon" / town,
                    "segment": base_path / "Segment" / camera_angle / "ClearNoon" / town
                }
                
                for modality, path in modality_paths.items():
                    matching_files = list(path.glob(f"{prefix}_*.png"))
                    if matching_files:
                        frame_data[prefix][camera_angle][modality] = str(matching_files[0].resolve())
    
    if not frame_data:
        print("No data found! Check if the directory structure is correct:")
        print(f"Looking for: {base_path}/Images/[camera_angle]/ClearNoon/[town]")
    
    return dict(frame_data)  # Convert to regular dict before returning

def create_fiftyone_dataset(frame_data, dataset_name="SkyScenes"):
    """Creates a FiftyOne dataset from collected frame data."""
    dataset = fo.Dataset(dataset_name, overwrite=True)
    samples = []
    
    for frame_id, angles in frame_data.items():
        group = fo.Group()
        
        for angle, modalities in angles.items():
            if "rgb" not in modalities:
                continue
                
            sample = fo.Sample(filepath=modalities["rgb"])
            
            # Add modalities
            if "depth" in modalities:
                sample["depth"] = fo.Heatmap(map_path=modalities["depth"])
            
            if "segment" in modalities:
                sample["segmentation"] = fo.Segmentation(mask_path=modalities["segment"])

            # Add to group with angle name - using dictionary style access
            sample["group"] = group.element(angle)
            samples.append(sample)
    
    dataset.add_samples(samples)
    dataset.default_mask_targets= INSTANCES_COLOR_MAP
    dataset.save()
    
    print(f"Created dataset with {len(dataset)} samples")
    print(f"Number of groups: {len(dataset.distinct('group.id'))}")
    
    return dataset