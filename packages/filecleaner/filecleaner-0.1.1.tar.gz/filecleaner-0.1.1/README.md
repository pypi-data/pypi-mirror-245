# File Manager
---
This Automation Script sorts your files according to their extensions and creates Folders and Subfolders, all files in the specified Directory get moved to. In the end you don't have any loose files in your Directory only Folders and Subfolders that match the Category of Files.

Currently the Script only works only with MacOS.



## Installation
---
Before you can use the Script you need to `pip install`.

You can do it like this:

    pip install filecleaner

## Supported Files
---
Currently Supported files are:

`jpeg`
`png`
`mov`
`mp4`
`avi`
`mpg`
`wmv`
`mp3`
`wav`
`mid`
`pptx`
`ppt`
`docx`
`doc`
`xlsx`
`xls`
`csv`
`json`
`txt`
`dmg`
`exe`
`zip`
`pdf`
`py`
`html`
`css`
`c`
`java`
`cs`
`PHP`
`swift`
`vb`
`asp`
`xhtml`
`db`
`js`
`md`


## Usage
---
You can use this Script by typing `cleanup` into the CLI. This will open a prompt asking you to type in an absolute path to the desired directory. This behavior represents the default. There are flags you can use to change that behavior.

The first flag is `-D`

    cleanup -D

This flag will tell the script to clean the Desktop directory.

The second flag is `-d`

    cleanup -d

This flag will tell the script to clean the Downloads directory

The default looks comes with no flag and looks like this

    cleanup

This will tell the script to clean the custom directory the user provide in the prompt


The script will creeate an error_log.txt file which stores every file the script couldn't move to a subfolder.
Those files will be moved to the Others directory

The Output on the terminal shows the files and their destination directory

    /Users/some_user/Downloads/png    ---    some_image.png
    /Users/some_user/Downloads/csv    ---    All Locations_temperature (F).csv
    /Users/some_user/Downloads/png    ---    some_image.png
    /Users/some_user/Downloads/png    ---    Bildschirm­foto 2023-07-10 um 12.16.02.png
    /Users/some_user/Downloads/avi    ---    Other0001-0130.avi



## License
---
This Package is licensed under the [MIT License](LICENSE)
