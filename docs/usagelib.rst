===================
Usage - IMM Library
===================

The IMM library is simple to use. It implements a with statement context manager.

In this section we will present some basic use cases that assume there are a few
image files available in the current directory from which we launch the Python interpreter.

For more detailed information about using the IMM library see the IMM library's :doc:`API section </api>`.

1. The simplest use case, writing image data to a text file using all the default values::

    >>> from imm import imagedata
    >>> with imagedata.Generator() as gid:
    ...    gid.write('Test_BMP_51.bmp')
    ...
    >>> ^Z
    $ type gfxmodule.py
    test_bmp_51_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00 ...

Note that the above does the following:

    a. Creates the default named Python module, **gfxmodule.py**, in the current directory
    b. Module gfxmodule.py contains the image data for the image file 'Test_BMP_51.bmp' defined in a variable named 'test_bmp_51_data'
    c. Since no image variable name was specified as a second parameter to the gid.write() method, a legal Python variable name was derived from the image file name
    d. The .bmp image file was converted in memory to a PNG file before being written to gfxmodule.py. (You can see the PNG header at the beginning of the test_bmp_51_data string partial output above from the 'type gfxmodule.py')


2. Simplest use case, writing image data to a text file with all default values without using the Generator's context manager::

    >>> from imm import imagedata
    >>> gid = imagedata.Generator()
    >>> gid.write('007.png')
    >>> gid.close()
    >>> ^Z
    type gfxmodule.py
    image_007_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00 ...


The most significant difference between this use case and the first use case, besides the obvious fact that this one does not
utilize the with statement context manager; is that the image variable name, though still derived from the image file name,
now has an 'image' prefix because the IMM library insures that image variable names, since they are Python identifiers, 
do not start with a number.

If the image file name consisted entirely of characters that are legal file name characters, but that cannot be in a 
Python identifier, then the IMM library will generate a random identifer as shown below::


    >>> from imm import imagedata
    >>> with imagedata.Generator() as gid:
    ...    gid.write('!#$@.png')
    ...
    >>> ^Z
    $ type gfxmodule.py
    image_2jhuzs8_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00 ...

The image file name (sans extension) of '!#$@'' cannot be used as a Python identifier, so the IMM library generates a random image variable name of 'image_2jhuzs8_data'.


3. Use case specifying a Python output module name::

    >>> from imm import imagedata
    >>> with imagedata.Generator('images.py') as gid:
    ...    gid.write('Test_TGA_51.tga')
    ...
    >>> ^Z
    $ type images.py
    test_tga_51_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00 ...


4. Use case specifying a Python output module and a image variable name::

    >>> from imm import imagedata
    >>> with imagedata.Generator('images.py') as gid:
    ...    gid.write('Test_GIF_51.gif', 'stop_button')
    ...
    >>> ^Z
    $ type images.py
    stop_button_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00 ...


5. Use case writing multiple images to the Python output module:

    >>> from imm import imagedata
    >>> with imagedata.Generator('images.py') as gid:
    ...    gid.write('007.png', 'pause_button')
    ...    gid.write('!#$@.png', 'play_button')
    ...    gid.write('Test_GIF_51.gif', 'stop_button')
    ...    gid.write('Test_TGA_51.tga', 'rewind_button')
    ...
    >>> ^Z
    $ $ type images.py
    pause_button_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00 ...
    ...
    play_button_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00 ...
    ...
    stop_button_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00 ...
    ...
    rewind_button_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00 ...


6. The final use case presented here will demonstrate providing all available inputs as named parameters using their default values where applicable::

    >>> from imm import imagedata
    >>> with imagedata.Generator(output='gfxmodule.py', writemode='WRITE', encoding='utf-8') as gid:
    ...    gid.write(imagefile='007.png', imagevarname=None)
    ...
    >>> ^Z
    type gfxmodule.py
    image_007_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00 ...

Of interesting note here is that the write mode can be 'WRITE' (the default) or 'APPEND' if the already existing output gfxmodule.py needs to be appended to by the write() method.



For more detailed information about using the IMM library see the IMM library's :doc:`API section </api>`.
