User
import os

def find_added_svg_file(root_folder, svg_file_name):
	added_svg_files = []
	for root,dirs,files in os.walk(root_folder):
		for file in files:
			if file == svg_file_name and file.endswith(".svg"):
				added_svg_files.append(os.path.join(root,file))
				
	if added_svg_files:
		print("Dosya bulundu.")
		
	return added_svg_files
		
if __name__ == "__main__":
	root_folder = "/home/hicran/Resource_merger_script/Orion_obs"
	svg_file_name = "stajyer_script_1.svg"
	result = find_added_svg_file(root_folder, svg_file_name)
	if result:
		print("Bulunan dosya yollari: ")
		for file_path in result:
			print(file_path)

