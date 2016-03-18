===============
Usage - IMM CLI
===============

The Image Module Maker package also ships with a command line utilty that utilizes the IMM library to faciliate processing a directory of images files
and generating a Python module containing the embedded image data.

This command line utility is also called **imm**.

In this section we will:

  1. Provide a general discussion of the basic command line interface of **imm**
  2. Provide direction on interacting with the **imm** help sub-system


But first, a few words about invoking **imm**.

The **imm** command line utility can be invoked in a few different ways depending on the host operating system.

The most portable way to invoke **imm** is::
    
    python immcli.py [OPTIONS]

On Windows there is a batch file that allows::

    imm [OPTIONS]

On Linux-like operating systems there is a shell file that allows::

    imm [OPTIONS]

In the discussion below the following nomenclature will be used for brevity::

    imm [OPTIONS]


CLI Basic Formats
-----------------

*Use case #1 - Scanning a directory of image files*::

    imm --input DIR --module MODULE [--code CODE_PATH]


The **imm** utility will scan the input directory DIR for all supported image files and generate a Python module named MODULE that 
contains the image files' binary data in strings. MODULE will be created in the path CODE_PATH if it is specified, if not, the current directory is used.


*Use case #2 - Reading a single image file rather than a directory*::

    imm --input FILE --module MODULE [--code CODE_PATH]

The **imm** utility will read the input image FILE and generate a Python module named MODULE that contains the image FILE's binary data in strings. 
MODULE will be created in the path CODE_PATH if it is specified, if not, the current directory is used.


Other options are available that primarily affect the code generation of MODULE. Details of these other options are available via use of the **imm** help sub-system which is explained later in this section.


Visual Check
------------

If the command line option **--show** is specified as in::

    imm --input DIR --module MODULE [--code CODE_PATH] --show

then two additional Python modules will be generated in the same location as MODULE -- their file names are:

    * **show.py**
    * **image_meta_data.py**

The **show** module will then be executed to provide a visual interface for interacting with the images embedded in MODULE.
The **image_meta_data** module provides image information used by the **show** module to display image information when an
image is selected.


Help Sub-System
----------------

The **imm** utilty provides a extension help sub-system. An overview of the help sub-system is avaiable via any of the following command lines::

    imm

    imm --help

    imm --help topics

    imm --help help


The entire **imm** user manual can be read in a paged format by using command line::

    imm --help all


The entire **imm** user manual can be output in a non-paged format suitable for redirection to a text file by using the command line::

    imm --help redirect > imm_user_manual.txt
