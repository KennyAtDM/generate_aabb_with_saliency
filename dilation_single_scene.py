import cv2
import numpy as np
import os
import argparse

kernel = np.ones((5, 5), np.uint8)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--project_dir', type=str, required=True, help='Project directory containing masks')

    args = parser.parse_args()
    project_dir = args.project_dir

    mask_dir = os.path.join(project_dir, 'masks')
    dest_folder = os.path.join(os.path.dirname(mask_dir), 'dilated_masks')

    if os.path.exists(dest_folder):
        print(f"Dilated masks folder '{dest_folder}' already exists. Skipping dilation.")
        return
    else:
        os.makedirs(dest_folder, exist_ok=True)
        
        for img_path in os.listdir(mask_dir):
            if img_path.lower().endswith(('jpg', 'jpeg', 'png')):
                img = cv2.imread(os.path.join(mask_dir, img_path), 0)
                mask = img.astype(np.float32)
                binary_mask = (mask > 0.8 * 255).astype(np.uint8)
                # Perform dilation
                dilated_mask = cv2.morphologyEx(binary_mask, cv2.MORPH_OPEN, kernel)
                cv2.imwrite(os.path.join(dest_folder, img_path), dilated_mask * 255)

if __name__ == "__main__":
    main()
