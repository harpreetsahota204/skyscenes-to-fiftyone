from pathlib import Path
from collections import defaultdict
import fiftyone as fo

def collect_frame_filepaths(base_dir):
    """Collects all filepaths for each frame, angle, and modality.
    
    Returns:
        dict: {frame_id: {angle: {modality: filepath}}}
    """
    base_path = Path(base_dir).resolve()  # Removed the / "SkyScenes" since it's already in the path
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
                    "instance": base_path / "Instance" / camera_angle / "ClearNoon" / town,
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

# Usage
frame_data = collect_frame_filepaths("./SkyScenes")
print(f"Found {len(frame_data)} frames")