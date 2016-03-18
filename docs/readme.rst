.. include:: ../README.rst


Image Formats Supported
-----------------------

In general, if an image file format is supported by Pillow (the Python 3.x fork of the Python Imaging Library), 
then IMM supports it; however, the only image file formats tested by the author are:

    png, gif, jpg, ico, tif/tiff, tga, xbm, ppm
    
Any limitations regarding specific file formats that PIL has, IMM will also have of course. 
For example, regarding the .ico format, only the largest resolution icon is loaded.
