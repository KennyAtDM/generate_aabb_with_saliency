import os
import subprocess
from concurrent.futures import ProcessPoolExecutor

def process_scene(scene, project_dir):
    path = os.path.join(project_dir, scene)
    if os.path.isdir(path):
        print(f'Processing scene: {scene}')
        try:
            subprocess.run(['python', 'opening_op_single_scene.py', '--project_dir', path], check=True)
            subprocess.run(['python', 'filter_single_scene.py', '--project_dir', path], check=True)
            print(f'Processing complete for scene: {scene}')
        except subprocess.CalledProcessError as e:
            print(f'Error processing scene {scene}: {e}')
    else:
        print(f'Error: {path} is not a valid directory.')

def main():
    project_dir = '/mnt/data/kennyyao/benchmark/'
    scenes = os.listdir(project_dir)
    
    with ProcessPoolExecutor() as executor:
        executor.map(process_scene, scenes, [project_dir] * len(scenes))

if __name__ == "__main__":
    main()
