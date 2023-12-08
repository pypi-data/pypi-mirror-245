import os
import shutil
from datetime import datetime


def create_new_directory (jssp,gui): 
    current_datetime = datetime.now().strftime(f"{jssp.instanceID} -%Y-%m-%d_%H-%M")
    subfolder_name = os.path.join(os.getcwd(), "renders", current_datetime)
    
    # #star with cleaning empty logs 
    # for dirpath, dirnames, filenames in os.walk(gui.root_render_path, topdown=False):
    #     for dirname in dirnames:
    #       dir_to_check = os.path.join(dirpath, dirname)
    #       file_count = len(os.listdir(dir_to_check))
              
    #       if file_count < 100:
    #           print(f"Deleting {dirname} with {file_count} files.")
    #           shutil.rmtree(dir_to_check)
    #           dirnames.remove(dirname)  
    

    os.makedirs(subfolder_name, exist_ok=True)   
    gui.current_render_path=subfolder_name     
    gui.available_direct=[f.path for f in os.scandir(gui.root_render_path) if f.is_dir()]   
    
    # Create and write information to the 'info' file
    info_file_path = os.path.join(gui.current_render_path, '0-info.txt')
    with open(info_file_path, 'w') as info_file:
        info_file.write(f"Path of the current guiironment: {gui.current_render_path}\n")
        info_file.write(f"C_max  ({jssp.total_internal_steps} steps) \n")
        info_file.write(f"Total number of interaction  ({jssp.interaction_counter} steps) \n")