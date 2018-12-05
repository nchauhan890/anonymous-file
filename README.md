# Anonymous File

Sublime Text 3 plugin to quickly create already-saved files to test code snippets.


### Intro

Have you ever thought of a brilliant idea and wanted to test out your code as fast as possible? You'd go through making a new file, writing the code out, saving the file somewhere, running it and then deleting it if the code failed. Now, with Anonymous File, you can quicken this workflow by creating pre-saved files which delete themselves upon closure.


### Configuration

Edit the AnonymousFile.sublime-settings files to configure this plugin. Open through `Preferences --> Package Settings --> AnonymousFile --> Settings - User` or the command palette.

Setting                                  | Description
----------------------------------------:|:------------------
`dir`    | Directory to save new files
`recently_closed` | Directory to move recently closed files to
`keep`   | Number of recently closed files to keep - must be between 0 and 100
`file_extension`  | Extension to create new files with - must contain the dot "." (e.g. ".py")

If the plugin detects any errors in the settings, such as numbers out of boundaries or file system locations which aren't directories or do not exist, a message will be shown in the status bar and in the console.


### Commands

Anonymous File has 2 commands and 1 to edit settings available through the command palette. The table below shows the internal command names.


Command                      | Command name
----------------------------:|:-----------------
Create Anonymous File        | anonymous_file
Save Anonymous File          | save_anonymous_file


### Context Menu

Anonymous File provides access to the `Create Anonymous File` and `Save Anonymous File` commands by default with their respective names unchanged.


### Usage and internals

To create a new Anonymous File, right-click the current view to open the Context Menu and click `Create Anonymous File`, or alternatively click the same command through the Command Palette. This file is saved in the directory set as `dir` in the AnonymousFile.sublime-settings file and has the extension designated by the `file_extension` setting also in the settings file mentioned. The file can be used as normal and any code written can be run without having to save the file beforehand.

Upon closure, the file is automatically deleted and moved to the directory set as `recently_closed` in the settings file. The `keep` setting specifies how many files will be kept in this directory; if the number is 0, the directory will remain empty. However, due to the nature of the code, the file is moved to the directory before being deleted so the `recently_closed` directory must be given regardless.

When an Anonymous File is closed, it's file name is written to `recent_files.txt` which is located in the directory specified as `dir` in settings. The order of the file names are oldest to newest. The plugin writes this data to a file so that when the whole Sublime Text application is closed, the file names are kept in order to ensure the oldest file(s) is/are removed from the `recently closed` folder even when Sublime Text is re-opened. However, if the file is deleted before Sublime Text opens, any files that were recorded are lost which will mean that they are not removed from the `recently_closed` directory, causing there to be more files than is specified by the `keep` setting.

Alternatively, the `Save Anonymous File` command can be invoked through the Context Menu or Command Palette which opens a `Save As` prompt to save the file. After saving, the file is removed from the plugin's list of currently open Anonymous Files so when closed, the file isn't deleted. Even if you save the file with the same `AF_xyz` name in the same directory, it still counts as saving the file and thus will not be deleted upon closure.
