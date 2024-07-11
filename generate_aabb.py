import os
import subprocess
from concurrent.futures import ProcessPoolExecutor

def process_scene(scene, project_dir):
    path = os.path.join(project_dir, scene)
    print(f'Processing project directory: {path}')
    subprocess.run(['python', 'dilation_single_scene.py', '--project_dir', path])
    subprocess.run(['python', 'filter_single_scene.py', '--project_dir', path])

def main():
    project_dir = '/mnt/data/kennyyao/benchmark/'
    scenes = os.listdir(project_dir)
    
    with ProcessPoolExecutor() as executor:
        executor.map(process_scene, scenes, [project_dir] * len(scenes))

if __name__ == "__main__":
    main()
