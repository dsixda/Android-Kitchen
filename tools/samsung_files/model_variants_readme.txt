Under the "tools/samsung_files/model_variants" folder, each sub-folder represents a variant name. Each of these sub-folders contains blank files representing different model names that share this variant's properties.  

Each variant (sub-folder) name has its mount points defined in a file under the "tools/edify_defs" folder.  

e.g. 

tools/samsung_files/model_variants/galaxy_s2 folder:

- contains the GT-I9100 variant sub-folder

- this GT-I9100 variant has properties that are common to the following models (represented by files inside this folder):
  - GT-I9100
  - GT-I9100G
  - GT-I9100M
  - GT-N7000
  - etc...

- the mount points are defined in the file tools/edify_defs/GT-I9100 (same name as the above sub-folder)

