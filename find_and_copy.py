import os
import shutil

def copy_file(source_path, target_path):
    if source_path == target_path:
    	print(f"Skipping copy, source and target are the same: {source_path}")
    	return True
    try:
        shutil.copy(source_path, target_path)
        #print(f"Copied: {source_path} -> {target_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

def find_and_copy_svg_files(root_folder, svg_file_names):
    added_svg_files = []
    
    for root, dirs, files in os.walk(root_folder):
        for file in files:
            if file in svg_file_names:
                added_svg_files.append(os.path.join(root,file))
                
    if added_svg_files:
        print("svg files found .\n")
        for svg_file_path in added_svg_files:
            print(f"Found svg file: {svg_file_path}\n")
            relative_path_parts = os.path.relpath(svg_file_path , root_folder).split(os.path.sep)
            other_parts = relative_path_parts[1:-1]
            for root, dirs, _ in os.walk(root_folder):
                target_folder = os.path.join(root,*other_parts)
                
                if os.path.exists(target_folder):
                    #print("Target folder: ",target_folder)
                    copy_file(svg_file_path, target_folder)
                    #print(f"SVG file copied to : {target_folder}")
            #for root, dirs, _ in os.path.join(root)


if __name__ == "__main__":
    root_folder = "/home/hicran/Resource_merger_script/orion_obs"
    svg_file_names = ["stajyer_script_1.svg", "stajyer_script_2.svg"]
    
    find_and_copy_svg_files(root_folder, svg_file_names)

