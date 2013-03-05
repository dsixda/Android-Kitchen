This folder is for Qualcomm-based variants of the Samsung Galaxy S2 (like the AT&T Skyrocket), so that the kitchen will recognize your device as a newer Galaxy S2.  The ROMs normally consist of system.img.ext4, cache.img.ext4 and boot.img.

In your /system/build.prop file there is a parameter called ro.product.device. The value of this parameter will be used as the name of the file to be placed in this folder.  This file can be empty; the kitchen will not read its contents.
