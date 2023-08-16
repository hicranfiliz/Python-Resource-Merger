import os
import shutil
import argparse


def find(file_names,erf_file):
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
            print(f"Found file: {file_path}\n")
            
            #/path/to/your/project/app_orion_folder/subfolder/your_file.png  -> file path buysa; root folder da /path/to/your/project  bu ise;
            #relative_path_parts bunu root' a gore ayiracagi icin relative_path_parts  /app_orion_folder/subfolder/your_file.png   bu olur.
            relative_path_parts = os.path.relpath(file_path, root_folder).split(os.path.sep)
            # other_parts -> /subfolder/ bu olur.
            other_parts = relative_path_parts[1:-1]
            
            first_part = relative_path_parts[0]
            third_part = relative_path_parts[2]
            erf_part = 'erf'
            
            updated_parts = [first_part,erf_part, third_part,erf_file]
            print(updated_parts)
            target_folder2 = os.path.join(root_folder, *updated_parts)
            print("Target folder2:", target_folder2)
            
            update_erf_files(erf_file, target_folder2, os.path.basename(file_path),relative_path_parts)

            
            for root, dirs, _ in os.walk(root_folder):
                target_folder = os.path.join(root, *other_parts)
                
                if os.path.exists(target_folder):
                    source_file = os.path.basename(file_path) #dosyanin adini al.
                    #copy(file_path, target_folder)
                    #if source_file.lower().endswith(".png"):
                     #   update_erf_for_png(file_path)
                    #else:
                     #   copy(file_path, target_folder)
                    
    else:
        print("File not found.\n")
            
    return added_files, component_mak_folders,erf_folders
 
 
def update_erf_files(erf_file, target_folder2,added_png_name,relative_path_parts):
    
    if erf_file in ["GameControlBoardImages.erf", "GameControlBoardImages_link.erf"]:
        erf_file_path = os.path.join(target_folder2)  # .erf dosyasının yolu
        relative_path = os.path.sep.join(relative_path_parts[:-1])  # Relative path'i birleştirerek dizeye çeviriyoruz
        print(relative_path)
        
        if erf_file == "GameControlBoardImages.erf":
            line_to_add = f'defimage {added_png_name.upper()} "{os.path.join(relative_path, added_png_name)}" png'
        else:
            line_to_add = f'defimage {added_png_name.upper()} "{os.path.join(relative_path, added_png_name)}" png link'
            
        with open(erf_file_path, 'a') as erf_file:
            erf_file.write(line_to_add + "\n")
            print(f"Added content to .erf file: {line_to_add}")

        
   
        
"""
    # Update the .erf file
    for root, dirs, files in os.walk(target_folder2):
        for file in files:
            if file.lower().endswith('.erf') and file == erf_file:
                erf_file_path = os.path.join(root, file)
                print(f"Processing .erf file: {erf_file_path}")
                with open(erf_file_path, 'a') as erf_file:
                    erf_file.write(content_to_add)
                print(f"Added content to .erf file: {content_to_add}")
                
                
"""               
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
    parser.add_argument("erf_file", help="Güncellenecek .erf dosyasının adı.")
    
    args = parser.parse_args()
    
    added_files, component_mak_folders, erf_folders = find(args.file_names, args.erf_file)
    
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
