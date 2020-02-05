# How to use custom colors
The Color Identifier executable can be used as a standalone application, but also supports the use of custom colors. This folder contains optional color definition files which can be used to change the color names the app identifies.

## Install
- Copy one of the color definition files into the same directory as the executable.
- Rename the file to `colors.txt`.
- Close and re-open the application.

## Create your own color definitions
Don't like the default or optional color definitions? Why not create your own!

Create your own color definition files as follows:
- The file is a simple text file listing one color definition per line.
- The line format is like: `#<Hex Code>,<Color Name>` e.g. `#000000,Black`
- Lines that do not start with `#` will be ignored which allows you to comment your files.
- Use the optional color files as examples.