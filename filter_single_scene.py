# filiter.py
import argparse
import os
import json
import numpy as np
import cv2
import open3d as o3d

def save_image_with_mask(points_image, mask_values,idx):
    h, w = 720, 1280
    image = np.zeros((h, w, 3), dtype=np.uint8)  


    for point, mask_value in zip(points_image, mask_values):
        x, y = point[0], point[1]
        color = (0, 255, 0) if mask_value > 0 else (0, 0, 255)  # 绿色或红色，根据 mask 值
        cv2.circle(image, (x, y), radius=1, color=color, thickness=-1) 

    cv2.imwrite(os.path.join("vis", f"points_image_visualization_with_mask{idx}.jpg"), image)

def visualize_aabb(point_cloud, bbox):
    o3d.visualization.draw_geometries([point_cloud, bbox])

def project_to_image(points, K, extrinsic):
    point_homogeneous = np.hstack((points, np.ones((points.shape[0], 1))))
    point_camera = (extrinsic @ point_homogeneous.T).T
    point_image = (K @ point_camera[:, :3].T).T
    point_image /= point_image[:, 2][:, np.newaxis]
    
    return point_image[:, :2].astype(int)

def remove_outliers(point_cloud):
    # 使用统计方法移除离群点
    cl, ind = point_cloud.remove_statistical_outlier(nb_neighbors=20, std_ratio=2.0)
    return point_cloud.select_by_index(ind)

def calculate_aabb(point_cloud):
    # 计算AABB
    bbox = point_cloud.get_axis_aligned_bounding_box()
    min_bounds = bbox.min_bound
    max_bounds = bbox.max_bound
    return {'aabb': [min_bounds[0], min_bounds[1], min_bounds[2], max_bounds[0], max_bounds[1], max_bounds[2]]}, bbox

def save_as_json(data, output_path):
    with open(output_path, 'w') as f:
        json.dump(data, f, indent=4)

def main():
    # 获取mask目录
    parser = argparse.ArgumentParser()
    parser.add_argument('--project_dir', type=str, required=True, help='scene dictionary')
    
    args = parser.parse_args()
    project_dir = args.project_dir
    json_path = os.path.join(project_dir, "space.json")
    with open(json_path, 'r') as f:
        data = json.load(f)

    cx, cy, fx, fy = data["cx"], data["cy"], data["fx"], data["fy"]
    frames = data["frames"]
    h,w = data['h'], data['w']

    K = np.array([[fx, 0, cx], [0, fy, cy], [0, 0, 1]])

    point_cloud = o3d.io.read_point_cloud(os.path.join(project_dir, "point_cloud.ply"))
    points = np.asarray(point_cloud.points)
    colors = np.asarray(point_cloud.colors)
    valid_indices = np.zeros(len(points), dtype=int)
    threshold = int(len(frames)/3)

    for i, frame in enumerate(frames):
        img_path = os.path.join(project_dir, frame["file_path"]) 
        mask_path = os.path.join(project_dir, "dilated_masks", os.path.basename(frame["file_path"]))
        mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)
        mask = cv2.flip(mask, 1)
        C2W = np.array(frame["transform_matrix"])
        extrinsic = np.linalg.inv(C2W)
        points_image = project_to_image(points, K, extrinsic)
        valid_mask = (points_image[:, 0] >= 0) & (points_image[:, 0] < w) & \
                     (points_image[:, 1] >= 0) & (points_image[:, 1] < h)
        points_image = points_image[valid_mask]
        filter_points = points[valid_mask]
        mask_values = mask[points_image[:, 1], points_image[:, 0]]

        depths = filter_points[:, 2]
        mean_depth = np.mean(depths)
        std_depth = np.std(depths)
        low_bound = mean_depth - 1.5 * std_depth  
        upper_bound = mean_depth + 1.5 * std_depth
        noise_filtered_mask = (depths > low_bound) & (depths < upper_bound)
        
        # save_image_with_mask(points_image, noise_filtered_mask,i)
        valid_indices[valid_mask] += (mask_values == 255) & noise_filtered_mask

    filtered_point_cloud = o3d.geometry.PointCloud()
    filtered_points = points[(valid_indices > threshold)]
    filtered_point_cloud.points = o3d.utility.Vector3dVector(filtered_points)
    if colors.size != 0:
        filtered_color = colors[(valid_indices > threshold)]
        filtered_point_cloud.colors = o3d.utility.Vector3dVector(filtered_color)

    o3d.io.write_point_cloud(os.path.join(project_dir, "filtered_point_cloud.ply"), filtered_point_cloud)
    
    filtered_point_cloud = remove_outliers(filtered_point_cloud)
    aabb, bbox = calculate_aabb(filtered_point_cloud)

    json_output_path = os.path.join(project_dir, 'aabb.json')
    save_as_json(aabb, json_output_path)
    print(f'AABB saved to {json_output_path}')
    # visualize_aabb(point_cloud, bbox)
    
if __name__ == "__main__":
    main()