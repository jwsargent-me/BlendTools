import bpy
import os
import shutil


def set_dirs(l):
    print(blend_file)
    for i in l:
        if os.path.isdir(blend_file + i) == False:
            os.mkdir(blend_file + i)


def init_fonts(font):
    font_src = repo + font
    l = bpy.data.fonts.load(font_src)
    t = bpy.data.objects[text_object]
    
    t.data.body = init_text
    t.data.font = l


def scan_cycle(i):
    t = bpy.data.objects[text_object]
    t.data.body = init_text
    
    bpy.context.view_layer.update()
    dim_target = t.dimensions[1] + error_margin
    safe_test = False
    
    for j in range(test_cycles):
        t.data.body = t.data.body + i

        bpy.context.view_layer.update()
        
        # Check if dimensions are within target range
        if t.dimensions[1] <= dim_target:
            safe_test = True
        
        # Check if dimensions exceed target
        elif t.dimensions[1] > dim_target:
            safe_test = False
        
        # Break in case of exception    
        else:
            break
        
        # Terminate as soon as dimensions exceed limits and return False bool
        if safe_test == False:
            return safe_test
        
    return safe_test
        

# Edit 'repo' to point to the target font repository directory
repo = "C:/Windows/Fonts/"

blend_file = bpy.path.abspath("//")
init_text = "SOME TEXT HERE"
text_object = "Text"

# Number of additional characters to test the font with, I suggest 20-30 
# You can decrease this if you are having performance issues, it just won't be as thorough
test_cycles = 30

# Testing variable, should not need to be modified
error_margin = 0.01

# Ensure new repo directories and lists are set
dirs_list = ["safe/", "error/"]
set_dirs(dirs_list)

safe_repo = blend_file + dirs_list[0]
error_repo = blend_file +  dirs_list[1]

safe_list = []
error_list = []

for f in os.listdir(repo):
    # Check for applicable font files (Blender only accepts otf and ttf)
    if f.endswith((".ttf", ".otf")):
        # Load new font, then update text object and font
        init_fonts(f)
        
        # Add characters and test dimensions for n test_cycles
        text_scan = scan_cycle("a")
        
        # Results ouput as lists of font names and new sorted repositories 
        if text_scan == True:
            # Append font name to list of safe fonts
            safe_list.append(f)
            # Copy font file to new directory relative to blend file            
            shutil.copy(repo + f, safe_repo)
        
        elif text_scan == False:
            # Append font name to list of fonts with errors
            error_list.append(f)
            # Copy font file to new directory relative to blend file
            shutil.copy(repo + f, error_repo)            

# Print results to console
print("\n \n >> SAFE LIST")
print(len(safe_list))
print(safe_list)
print("\n \n >> ERROR LIST")
print(len(error_list))
print(error_list)


'''
>>README<<

Description:
 A quick and dirty way to scan a font repository for potentially problematic 
files that will trigger a rare Scale to Fit bug


Directions:
 Change the 'repo' path to point to your font repository before running the script. 
 The script will copy the font files to new directories relative to the project file, 
 labelled safe or error. You can safely disable this if you do not want sorted repositories

 If you are having performance issues you can lower the test_cycles as low as 20 or so. 
 Preferably no less as a lower number is less thorough and might not catch an error

'''
