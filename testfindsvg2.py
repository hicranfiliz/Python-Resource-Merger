import os
import shutil
## sorunsuz çalışan kod!
# dosyayi basariyla bulup digerlerine kopyalayip hepsinden siliyor.

def copy_file(source_path, target_path):
    if source_path == target_path:
    	print(f"Skipping copy, source and target are the same: {source_path}")
    	return True
    try:
        shutil.copy(source_path, target_path)
        print(f"Copied: {source_path} -> {target_path}")
    except Exception as e:
        print(f"An error occurred: {e}")
        
        
def remove_file(file_path):
	try:
		os.remove(file_path)
		print(f"Deleted: {file_path}")
	except Exception as e:
		print(f"An error occured: {e}")
	
	
def remove_last_n_lines(file_path, n):
	with open(file_path , 'r') as file:
		lines = file.readlines()
		
	with open(file_path, 'w') as file:
		file.writelines(lines[:-n])
	

def update_component_mak(component_mak_path, new_svg_file_path):
    with open(component_mak_path, "r") as file:
        lines = file.readlines()

    for i in range(len(lines) - 1, -1, -1):
        line = lines[i].strip()
        if line.startswith("$(svg_path)") and line.endswith(".svg"):
            lines[i] = line + " \\\n"
            new_line = "    " + new_svg_file_path + "\n"
            lines.insert(i + 1, new_line)
            break

    with open(component_mak_path, "w") as file:
        file.writelines(lines)


def find_added_svg_file(root_folder, svg_file_name):
    added_svg_files = []
    component_mak_folders = []
    
    for root, dirs, files in os.walk(root_folder):
        for file in files:
            if file == svg_file_name and file.endswith(".svg"):
                added_svg_files.append(os.path.join(root, file))
            elif file == "component.mak":
            	component_mak_folders.append(root)        
                
  
    if added_svg_files:
        print("SVG file found.")
        for file_path in added_svg_files:
            for root, dirs, _ in os.walk(root_folder):
                target_folder = os.path.join(root, "svg/GameControlBoard")
                
                if os.path.exists(target_folder):
                    copy_file(file_path, target_folder)
                    print(f"SVG file copied to: {target_folder}")
                    
                
                
        for component_mak_folder in component_mak_folders:
           component_mak_file = os.path.join(component_mak_folder, "component.mak")
           if os.path.exists(component_mak_file):
               print(f"component.mak file found at: {component_mak_file}")
               source_svg_file = f"$(svg_path)/GameControlBoard/{svg_file_name}"
               #remove_last_n_lines(component_mak_file,15)
               update_component_mak(component_mak_file, source_svg_file)
               #for file_path in added_svg_files:
                #    update_component_mak(component_mak_file, source_svg_file)
    else:
        print("File not found.")
      
    #return added_svg_files,component_mak_file

if __name__ == "__main__":
    root_folder = "/home/hicran/Resource_merger_script/orion_obs"
    svg_file_name = "stajyer_script_1.svg"
    
    find_added_svg_file(root_folder, svg_file_name)
"""    
    #result = find_added_svg_file(root_folder, svg_file_name)
    source_svg_file = f"$(svg_path)/GameControlBoard/{svg_file_name}"
    added_svg_files, component_mak_file = find_added_svg_file(root_folder, svg_file_name)
    
    if component_mak_file:
        print(f"component.mak found: {component_mak_file}")
        for file_path in added_svg_files:
            update_component_mak(component_mak_file, source_svg_file)
    else:
        print("component.mak not found.")
"""
"""
    #update_component_mak(root_folder)
    result = find_added_svg_file(root_folder, svg_file_name)
    source_svg_file = f"$(svg_path)/GameControlBoard/{svg_file_name}"
    for file_path in result:
    	component_mak_file = os.path.join(file_path, "component.mak")
    	update_component_mak(component_mak_file,file_path)
    	
    #if result:
     #   print("Found file paths:")
      #  for file_path in result:
       #     print(file_path)
           
    #for file_path in result:
    #	remove_file(file_path)
"""    

