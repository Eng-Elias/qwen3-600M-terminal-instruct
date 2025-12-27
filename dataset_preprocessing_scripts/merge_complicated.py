import json
import os
import glob

def merge_complicated_files():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    raw_dir = os.path.join(base_dir, "datasets", "generated", "raw")
    
    print(f"Scanning {raw_dir} for complicated datasets...")
    
    # Find all complicated files
    complicated_files = glob.glob(os.path.join(raw_dir, "*_complicated.json"))
    
    for comp_file in complicated_files:
        filename = os.path.basename(comp_file)
        main_filename = filename.replace("_complicated.json", ".json")
        main_file = os.path.join(raw_dir, main_filename)
        
        if not os.path.exists(main_file):
            print(f"Warning: Main file {main_file} not found for {filename}. Skipping.")
            continue
            
        print(f"Merging {filename} into {main_filename}...")
        
        try:
            with open(main_file, 'r', encoding='utf-8') as f:
                main_data = json.load(f)
                
            with open(comp_file, 'r', encoding='utf-8') as f:
                comp_data = json.load(f)
                
            # Create a set of existing IDs to prevent duplicates
            existing_ids = {item.get('id') for item in main_data}
            
            added_count = 0
            for item in comp_data:
                if item.get('id') not in existing_ids:
                    main_data.append(item)
                    existing_ids.add(item.get('id'))
                    added_count += 1
            
            if added_count > 0:
                with open(main_file, 'w', encoding='utf-8') as f:
                    json.dump(main_data, f, indent=2, ensure_ascii=False)
                print(f"  Added {added_count} items to {main_filename}")
            else:
                print(f"  No new items to add (all IDs exist in target).")
                
        except Exception as e:
            print(f"Error merging {filename}: {str(e)}")

if __name__ == "__main__":
    merge_complicated_files()
