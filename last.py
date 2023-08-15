import os
import shutil
import argparse


def find(file_names):
    added_files = []
    component_mak_folders = []
    erf_folders = []
    
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
                    if "erf" in dir_dirs:
                        erf_folders.append(os.path.join(dir_root,"erf"))
                    
                
                
    if added_files:
        print("file found. \n")
        for file_path in added_files:
            #print(f"Found file: {file_path}\n")
            #/path/to/your/project/app_orion_folder/subfolder/your_file.png  -> file path buysa; root folder da /path/to/your/project  bu ise;
            #relative_path_parts bunu root' a gore ayiracagi icin relative_path_parts  /app_orion_folder/subfolder/your_file.png   bu olur.
            relative_path_parts = os.path.relpath(file_path, root_folder).split(os.path.sep)
            # other_parts -> /subfolder/ bu olur.
            other_parts = relative_path_parts[1:-1]
            for root, dirs, _ in os.walk(root_folder):
                target_folder = os.path.join(root, *other_parts)
                
                if os.path.exists(target_folder):
                    source_file = os.path.basename(file_path) #dosyanin adini al.
                    copy(file_path, target_folder)
                    #if source_file.lower().endswith(".png"):
                     #   update_erf_for_png(file_path)
                    #else:
                     #   copy(file_path, target_folder)
                    
    else:
        print("File not found.\n")
            
    return added_files, component_mak_folders,erf_folders
 
 
def update_erf_for_png(png_file_path):
    root_folder = os.getcwd()

    # Find the corresponding erf file
    for root, _, files in os.walk(root_folder):
        for file in files:
            if file.lower().endswith(".erf"):
                erf_file_path = os.path.join(root, file)
                with open(erf_file_path, 'r') as erf_file:
                    if png_file_path in erf_file.read():
                        update_erf_file(erf_file_path, png_file_path)
                        print(f"Updated {erf_file_path} for {png_file_path}")
                        return               
                
def copy(source_path, target_path):
   if source_path == target_path:
       print(f"Skipping copy, source and target are the same: {source_path}")
       return True
   try:
       if os.path.isfile(source_path):
           shutil.copy(source_path, target_path)
           #print(f"Copied: {source_path} -> {target_path}")
       elif os.path.isdir(source_path):
           shutil.copytree(source_path, os.path.join(target_path, os.path.basename(source_path)))
           #print(f"Copied folder: {source_path} -> {target_path}")
   except Exception as e:
       print(f"An error occured: {e}")
     

     

def main():
    #root_folder = "/home/hicran/Resource_merger_script/orion_obs"
    
    parser = argparse.ArgumentParser(description= "Find and copy specified files.")
    parser.add_argument("file_names", nargs = "+", help = "File names to search and copy.")
    
    args = parser.parse_args()
    
    added_files, component_mak_folders, erf_folders = find(args.file_names)
    
    print("Files found: \n")
    for file_path in added_files:
        print(file_path)
    
    
    print("\nComponent.mak Folders: \n")
    for component_mak in component_mak_folders:
        print(component_mak)
        
    print("\nerf files found:\n")
    for erf_folder in erf_folders:
        print(erf_folder)
        

if __name__ == "__main__":
    main()
