import json
import glob
import os

def clean_preset(filepath):
    print(f"Cleaning {filepath}")
    try:
        with open(filepath, "r") as f:
            data = json.load(f)
        
        # Clean sample data
        if "settings" in data and "sample" in data["settings"]:
            data["settings"]["sample"] = {"length": 0, "name": "", "sample_rate": 44100, "samples": ""}
        
        # Clean wave data in wavetables
        if "settings" in data and "wavetables" in data["settings"]:
            for table in data["settings"]["wavetables"]:
                for group in table.get("groups", []):
                    for component in group.get("components", []):
                        for keyframe in component.get("keyframes", []):
                            keyframe["wave_data"] = ""
        
        # Save cleaned data
        with open(filepath, "w") as f:
            json.dump(data, f, indent=2)
        print(f"Successfully cleaned {filepath}")
    except Exception as e:
        print(f"Error cleaning {filepath}: {str(e)}")

def clean_all_presets():
    # Get the root directory (where this script is located)
    root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    # Find all .vital files recursively
    vital_files = []
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.vital'):
                vital_files.append(os.path.join(root, file))
    
    print(f"Found {len(vital_files)} preset files to clean")
    
    # Clean each preset
    for file in vital_files:
        clean_preset(file)

if __name__ == "__main__":
    clean_all_presets() 