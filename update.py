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
            if dir in file_names:
                added_files.append(os.path.join(root, dir))
                # veya sadece klasör adını eklemek isterseniz:
                # added_files.append(dir)

        for file in files:
            if file in file_names:
                added_files.append(os.path.join(root, file))
            elif file == "component.mak":
                component_mak_folders.append(root)

        for dir in dirs:
            if dir.startswith("app_orion_"):
                dir_path = os.path.join(root, dir)
                for dir_root, dir_dirs, dir_files in os.walk(dir_path):
                    for file in dir_files:
                        if file in file_names:
                            added_files.append(os.path.join(dir_root, file))
                    if "component.mak" in dir_files:
                        component_mak_folders.append(dir_path)
                    if "erf" in dir_dirs:
                        erf_folders.append(os.path.join(dir_root, "erf"))

    #return added_files, component_mak_folders, erf_folders
                    
                
                
    if added_files:
        print("file found. \n")
        for file_path in added_files:
            print(f"Found file: {file_path}\n")
            
            relative_path_parts = os.path.relpath(file_path, root_folder).split(os.path.sep)
            new_line = relative_path_parts[-1]
            print("new line: ",new_line)
            new_file_path = os.path.join(root_folder, relative_path_parts[0], "component.mak")
            print("New File Path:", new_file_path)
           
            #find_line_addition(new_file_path, new_line,component_mak_folders)
            
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
            
            
            
            for root, dirs, files in os.walk(root_folder):
                #print("Current directory: ",root)
                if "app_orion_" in root:  # Klasör adı içerisinde "app_orion_" var mı kontrol et
                    target_folder = os.path.join(root, *other_parts)
                
                    if os.path.exists(target_folder):
                        source_file = os.path.basename(file_path) #dosyanin adini al.
                        copy(file_path, target_folder)
                  #  update_erf_files(erf_file, target_folder2, os.path.basename(file_path),relative_path_parts)
                    #if source_file.lower().endswith(".png"):
                     #   update_erf_for_png(file_path)
                    #else:
                     #   copy(file_path, target_folder)
            find_line_addition(new_file_path, new_line,component_mak_folders)        
                  
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
    
 
 
def find_last_line(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        if lines:
            last_line = lines[-1].strip()
            return last_line if last_line and last_line != " " else None
    return None
    
    
    
def copy_last_line_to_erf_files(source_last_line, source_erf_path, erf_folders):
    print(f"source erf path: {source_erf_path}")
    root_folder = os.getcwd()
    relative_path_parts = os.path.relpath(source_erf_path, root_folder).split(os.path.sep)

    other_parts2 = relative_path_parts[2:]
    for erf_folder in erf_folders:
        for root, dirs, files in os.walk(erf_folder):
            for file in files:
                if file.lower().endswith(".erf"):
                    target_erf_path = os.path.join(erf_folder, *other_parts2)
                    print(f"Copying to {target_erf_path}")  # .erf dosyasının yolunu yazdır
                    with open(target_erf_path, 'r') as target_erf:
                        lines = target_erf.readlines()
                    if lines:
                        last_line = lines[-1].strip()
                        if not last_line or last_line == "":
                            with open(target_erf_path, 'a') as target_erf:
                                target_erf.write('\n')
                                target_erf.write(source_last_line)
                            print(f"Copied last line to {target_erf_path}")
                    else:
                        print(f"Could not read {target_erf_path}")
                    


def copy(source_path, target_path):
   if source_path == target_path:
       print(f"Skipping copy, source and target are the same: {source_path}")
       return True
   try:
       if os.path.isfile(source_path):
           shutil.copy(source_path, target_path)
           print(f"Copied: {source_path[45:]} -> {target_path[45:]}")
       elif os.path.isdir(source_path):
           shutil.copytree(source_path, os.path.join(target_path, os.path.basename(source_path)))
           print(f"Copied folder: {source_path} -> {target_path}")
   except Exception as e:
       print(f"An error occured: {e}")
     

     

def main():
    
    parser = argparse.ArgumentParser(description="Find and copy specified files.")
    parser.add_argument("file_names", nargs="+", help="File names to search and copy.")
    parser.add_argument("--erf_file", help="Güncellenecek .erf dosyasının adı.", default=None)
    parser.add_argument("--source_erf_path", help="Path to the source .erf file.")

    args = parser.parse_args()
    
    if args.erf_file is None:
        added_files, component_mak_folders, erf_folders = find(args.file_names, None)
    else:
        added_files, component_mak_folders, erf_folders = find(args.file_names, args.erf_file)
        
    if args.source_erf_path:
        source_last_line = find_last_line(args.source_erf_path)
        if source_last_line:
            copy_last_line_to_erf_files(source_last_line, args.source_erf_path, erf_folders)
        else:
            print(f"Could not find a suitable last line in {args.source_erf_path}")    

if __name__ == "__main__":
    main()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
