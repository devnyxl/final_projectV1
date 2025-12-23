import os
import shutil

# Paths (adjust based on download)
data_dir = 'final_project\\datasetV2\\train'  # Example for train set
obstacle_dir = 'final_project\\datasetV2\\obstacle'
no_obstacle_dir = 'final_project\\datasetV2\\no_obstacle'

os.makedirs(obstacle_dir, exist_ok=True)
os.makedirs(no_obstacle_dir, exist_ok=True)

safe_classes = {1}  # wooden floor, footpath, wall

for img_file in os.listdir(data_dir):
    if img_file.endswith('.jpg'):
        label_file = img_file.replace('.jpg', '.txt')
        label_path = os.path.join(data_dir, label_file)
        
        if not os.path.exists(label_path):
            # No annotations: assume no obstacle
            shutil.copy(os.path.join(data_dir, img_file), no_obstacle_dir)
            continue
        
        has_obstacle = False
        with open(label_path, 'r') as f:
            for line in f:
                class_id = int(line.split()[0])
                if class_id not in safe_classes:
                    has_obstacle = True
                    break
        
        if has_obstacle:
            shutil.copy(os.path.join(data_dir, img_file), obstacle_dir)
        else:
            shutil.copy(os.path.join(data_dir, img_file), no_obstacle_dir)

# Repeat for val/test folders if available.