import os
import shutil
import argparse
import difflib


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
            new_line = relative_path_parts[-1]
            print("new line: ",new_line)
            new_file_path = os.path.join(root_folder, relative_path_parts[0], "component.mak")
            print("New File Path:", new_file_path)
            #new_line2 = "$(svg_path)/GameControlBoard/stajyer_script_1.svg"
            find_line_addition(new_file_path, new_line,component_mak_folders)
            # other_parts -> /subfolder/ bu olur.
            other_parts = relative_path_parts[1:-1]
            
            first_part = relative_path_parts[0]
            third_part = relative_path_parts[2]
            erf_part = 'erf'
            updated_parts2 = [root]
            updated_parts = [first_part,erf_part, third_part,erf_file]
            print(updated_parts)
            updated_parts = [part for part in [first_part, erf_part, third_part, erf_file] if part is not None]
            target_folder2 = os.path.join(root_folder, *updated_parts)
            print("Target folder2:", target_folder2)
            
            
            
            for root, dirs, _ in os.walk(root_folder):
                target_folder = os.path.join(root, *other_parts)
                
                if os.path.exists(target_folder):
                    source_file = os.path.basename(file_path) #dosyanin adini al.
                    #copy(file_path, target_folder)
                  #  update_erf_files(erf_file, target_folder2, os.path.basename(file_path),relative_path_parts)
                    #if source_file.lower().endswith(".png"):
                     #   update_erf_for_png(file_path)
                    #else:
                     #   copy(file_path, target_folder)
                     
                  
    else:
        print("File not found.\n")
            
    return added_files, component_mak_folders,erf_folders

def find_line_addition(file_path, partial_line, component_mak_folders):
    with open(file_path, 'r') as f:
        lines = f.readlines()

    for index, line in enumerate(lines):
        if partial_line in line:
            change_detected = True
            changed_line_number = index + 1
            full_line_content = line.strip()
            break
        else:
            change_detected = False
            changed_line_number = None
            full_line_content = None
    if change_detected:
        print(f"Change detected in file:")
        print(f"Changed Line: {changed_line_number}")
        print(f"Full Line Content: {full_line_content}")

        # Check if full_line_content is already present in component.mak file
        
        for folder in component_mak_folders:
            mak_file_path = os.path.join(folder, 'component.mak')
            with open(mak_file_path, 'r') as mak_file:
                if full_line_content in mak_file.read():
                    print(f"Full line content already exists in {mak_file_path}. Skipping update.")
                else:
                    update_component_mak([folder], changed_line_number,full_line_content)
                    

    else:
        print(f"No change detected in {file_path}")
        
    return change_detected, changed_line_number, full_line_content
        
        

def update_component_mak(component_mak_folders, line_number, new_line_content):
    for component_mak_folder in component_mak_folders:
        component_mak_path = os.path.join(component_mak_folder, "component.mak")
        print("component_mak_path: ",component_mak_path )

        if os.path.exists(component_mak_path):
            with open(component_mak_path, 'r') as f:
                lines = f.readlines()

            if 0 < line_number <= len(lines):

                for i in range(len(lines)):
                    if i == line_number - 2:
                        preceding_line = lines[i].strip()
                        lines[i] = "    " + preceding_line + "\\\n"
                        new_line = "    " + new_line_content + "\n"
                        lines.insert(i + 1, new_line)
                        break

                with open(component_mak_path, 'w') as f:
                    f.writelines(lines)
    
    
 
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
    parser.add_argument("--erf_file", help="Güncellenecek .erf dosyasının adı.", default=None)
    
    args = parser.parse_args()
    if args.erf_file is None:
        find(args.file_names, None)
    else:
        find(args.file_names, args.erf_file)

    #added_files, component_mak_folders, erf_folders = find(args.file_names, args.erf_file)
    

        

if __name__ == "__main__":
    main()
