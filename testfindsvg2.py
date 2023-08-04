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
	root_folder = "/home/hicran/Resource_merger_script/Orion_obs"
	svg_file_name = "stajyer_script_1.svg"
	result = find_added_svg_file(root_folder, svg_file_name)
	if result:
		print("Bulunan dosya yollari: ")
		for file_path in result:
			print(file_path)

