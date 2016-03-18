@python "%~dpn0cli.py" %*

@echo off
:: Invoke from the command line via Windows Batch file
:: A %0 appearing in a batch file gets translated to at run-time to the text
:: that was typed to invoke the batch file excluding arguments.
:: The ~ followed by some reserved letters (dpnx) cause the reserved letters
:: to be translated at run-time to the following filename components:
::       d - Driver Letter
::       p - Directory Path
::       n - File Name
::       x - File Extension (not used above)
::
:: The %* translates to the remaining command line arguments
:: The @ prefix is a short-cut that tells the batch file interpreter NOT to
:: echo the statement being executed.
::
:: So if you invoke this script like this:  example arg1 arg2 arg3
:: and you are in the directory: C:\some\path\
:: then the above line will be translated to: 
::
:: @python C:\some\path\example.py arg1 arg2 arg3

