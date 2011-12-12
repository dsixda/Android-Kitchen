This folder is for variants of the original Samsung Galaxy S2 (i.e. the Exynos processor-based version), so that the kitchen will recognize your device as a Galaxy S2 I9I00.  The ROMs consist of factoryfs.img, cache.img, zImage and modem.bin.

In your /system/build.prop file there is a parameter called ro.product.device. The value of this parameter will be used as the name of the file to be placed in this folder.  This file can be empty; the kitchen will not read its contents.
