import shutil
import os

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
		
		
def update_component_mak(root_folder):
	component_mak_filename = "component.mak"
	for root, _, files in os.walk(root_folder):
		if component_mak_filename in files:
			component_mak_path = os.path.join(root, component_mak_filename)
			#remove_last_n_lines(component_mak_path, 14)
			with open(component_mak_path, 'a') as component_mak_file:
				component_mak_file.write("\n# added svg file")
		

def find_added_svg_file(root_folder, svg_file_name):
    added_svg_files = []
    for root, dirs, files in os.walk(root_folder):
        for file in files:
            if file == svg_file_name and file.endswith(".svg"):
                added_svg_files.append(os.path.join(root, file))
                
    if added_svg_files:
        print("File found.")
        for file_path in added_svg_files:
            for root, dirs, _ in os.walk(root_folder):
                target_folder = os.path.join(root, "svg/GameControlBoard")
                
                if os.path.exists(target_folder):
                    copy_file(file_path, target_folder)
    else:
        print("File not found.")
        
    return added_svg_files
		
if __name__ == "__main__":
	root_folder = "/root_folderpath"
	svg_file_name = "file.svg"
	update_component_mak(root_folder)
	result = find_added_svg_file(root_folder, svg_file_name)
	if result:
		print("Bulunan dosya yollari: ")
		for file_path in result:
			print(file_path)
			
	for file_path in result:
    		remove_file(file_path)

