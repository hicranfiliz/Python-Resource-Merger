import os
import shutil
import argparse


def find(file_names):
    added_files = []
    component_mak_folders = []
    
    root_folder = os.getcwd()
    print(root_folder)
    
    # dosyayı buldu ve kopyaladı. component.mak bulamadı.
    for root, dirs, files in os.walk(root_folder):
        for dir in dirs:
            if dir.startswith("app_orion_"):
                for dir_root, dir_dirs, dir_files in os.walk(os.path.join(root, dir)):
                    for file in dir_files:
                        if file in file_names:
                            added_files.append(os.path.join(dir_root, file))
                    if "component.mak" in dir_files:
                        component_mak_folders.append(os.path.join(root, dir))
                
                
    if added_files:
        print("file found. \n")
        for file_path in added_files:
            print(f"Found file: {file_path}\n")
            relative_path_parts = os.path.relpath(file_path, root_folder).split(os.path.sep)
            other_parts = relative_path_parts[1:-1]
            for root, dirs, _ in os.walk(root_folder):
                target_folder = os.path.join(root, *other_parts)
                
                if os.path.exists(target_folder):
                    source_file = os.path.basename(file_path) #dosyanin adini al.
                    
                    copy(file_path, target_folder)
                    
    else:
        print("File not found.\n")
            
    return added_files, component_mak_folders
                
                
def copy(source_path, target_path):
   if source_path == target_path:
       print(f"Skipping copy, source and target are the same: {source_path}")
       return True
   try:
       if os.path.isfile(source_path):
           shutil.copy(source_path, target_path)
           print(f"Copied: {source_path} -> {target_path}")
       elif os.path.isdir(source_path):
           shutil.copytree(source_path, os.path.join(target_path, os.path.basename(source_path)))
           print(f"Copied folder: {source_path} -> {target_path}")
   except Exception as e:
       print(f"An error occured: {e}")
     
  

def main():
    #root_folder = "/home/hicran/Resource_merger_script/orion_obs"
    
    parser = argparse.ArgumentParser(description= "Find and copy specified files.")
    parser.add_argument("file_names", nargs = "+", help = "File names to search and copy.")
    
    args = parser.parse_args()
    
    added_files, component_mak_folders = find(args.file_names)
    
    print("Files found: \n")
    for file_path in added_files:
        print(file_path)
    
    
    print("\nComponent.mak Folders: \n")
    for component_mak in component_mak_folders:
        print(component_mak)
        

if __name__ == "__main__":
    main()
