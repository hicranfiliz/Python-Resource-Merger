import os
import shutil


def find(root_folder, file_names):
    added_files = []
    component_mak_folders = []
    
    for root, dirs, files in os.walk(root_folder):
        for file in files:
            if file in file_names:
                added_files.append(os.path.join(root,file))
            elif file == "component.mak":
                component_mak_folders.append(root)
        for dir in dirs:
            if dir in file_names:
                added_files.append(os.path.join(root,dir))
                
               
            
    return added_files, component_mak_folders
               
     


if __name__ == "__main__":
    root_folder = "/home/hicran/Resource_merger_script/orion_obs"
    file_names = ["Stajyer_script_3",
                  "stajyer_script_2.svg",
                  "stajyer_script_1.svg",
                  "stajyer_script_2.png",
                  "stajyer_script_3.png",
                  "stajyer_script_3.svg",
                  "StajyerScriptImages.erf"
                 ]
                 
    added_files, component_mak_folders = find(root_folder, file_names)
    
    print("Files found: \n")
    for file_path in added_files:
        print(file_path)
    
    
    print("\nComponent.mak Folders: \n")
    for component_mak in component_mak_folders:
        print(component_mak)
             
    print("\nFolders found: \n")
    for folder in all_folders:
        print(folder)
