
import breakdown_ccda
import os
import lxmlcompare
from datetime import datetime
from deepdiff.helper import SetOrdered

file1 = "base_ccda.xml"
file2 = "compare_ccda.xml"
currenttime = datetime.now().strftime("%Y%m%d_%H%M%S")
output_file = "Logs_"+currenttime
missing_sections = "missing_sections"+currenttime

#breaking the two files into multiple xmls based on the title of the sections
#ensuring if broken sections are already present in the directory then these method won't be called

if not os.path.isdir("extracted_sections_base") or not os.path.isdir("extracted_sections_compare"):

    breakdown_ccda.extract_and_save_components(file1)
    breakdown_ccda.extract_and_save_components(file2)
else:
    print("Broken sections are already present in the directory ")
    print("======================================================\n")

#now we have two directories which contain broken sections of ccda files

directory_to_base_Sections = "extracted_sections_base"
directory_to_compare_Sections = "extracted_sections_compare"


#traversing through the directories

missing_resources=[]
mismactchlogs = "mismatchlogs_"+currenttime

for filename in os.listdir(directory_to_base_Sections):
    if filename in os.listdir(directory_to_compare_Sections):
        #filenames in the dircetory 
        file1 = os.path.join(directory_to_base_Sections,filename)
        file2 = os.path.join(directory_to_compare_Sections,filename)
        diff = lxmlcompare.compare_cda(file1,file2)
        # print(f"diff{diff}")
        categories = lxmlcompare.categories_difference(diff)
        
        if len(categories['item added']) > 0 or len(categories['item deleted'])>0 or len(categories['item updated'])>0 or len(categories['others'])>0:
            
            # writting detailed logs into output file 
            with open(output_file, "a") as file:
                file.write(f"Comparing Section : {filename.upper()}\n")
                file.write("=====================================================\n")
                for category_name, changes in categories.items():
                    file.write(f"{category_name}:\n\n")
                    for change in changes:
                            file.write(f"  - {change}\n\n")

                            if isinstance(change, SetOrdered):
                                changed_paths = change
                            else:
                                changed_paths = [list(change.keys())[0] for change in changes]
                            with open(mismactchlogs,"a")as mismatch:
                                mismatch.write(f"Comparing Section : {filename.upper()}\n")
                                mismatch.write("=====================================================\n")
                                
                                mismatch.write(changed_paths[0])

                                mismatch.write("\n\n\n")

                                print(changed_paths)

                                  

    else:
        missing_resources.append(filename)
    

    
with open(missing_sections ,"w")as mfile:
    if missing_resources:

        for i in missing_resources:
            mfile.write(f"{i}\n")
    else:
        mfile.write("All resources are present in the Compared CCDA")
    
print(f"Differences written to log file")





