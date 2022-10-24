# ASSDialogueMerger

Program to merge the dialogue of one subtitle into the timings of another.

This tool merges the translations from one subtitle into the timings of another, ignoring non-dialogue lines such as signs & songs.
An example is to merge the translations from one fansub group with the timings (and remaining non-dialogue lines) of another group.

The script works by first iterating through all lines and detecting lines that have to be removed from the base subtitle file (the one with the correct timings) and lines that have to be copied over from the dialogue subtitle file (the one with the better dialogue/translations). These lines are logged in the console output, the script user will have to manually re-time the copied-over lines after the script has completely finished. 

Next, all changes are applied and the number of dialogue lines should match perfectly. Then the text is simply copied over from the dialogue subtitle into the base subtitle. Much like Paste From Pad from [Myaamori's Script Collection](https://github.com/TypesettingTools/Myaamori-Aegisub-Scripts). In addition, the style tag is copied over too in case the dialogue subtitle used an default-alt style where the base subtitle did not.

## **Warning**
This is an experimental tool! This is mostly a test to find out what principles can be used to merge dialogue from one subtitle onto another. It will work in most cases, but beware to follow all steps properly to resolve any possible issues created by the script.

Additionally, the script will copy over the style tag to keep the styling of your dialogue subtitle. However, it will **not** check if the base subtitle actually has the required style(s). You will have to manage the styles manually for now.

The goal is to eventually make a GUI application that allows the user to fully control what will happen.


## Dependencies
- [Python 3.9 or higher](https://www.python.org/downloads/)
- [Python ass](https://pypi.org/project/ass/)

## Installation
1. Download ZIP or do `git clone https://github.com/royvds/assDialogueMerger.git` in your terminal.
2. Navigate to the root folder `assDialogueMerger` or do `cd assDialogueMerger`.
3. `pip install .`

## Usage
```console
$ assdialoguemerger --help
usage: cli.py [-h] -bf BASE_FOLDER -df DIALOGUE_FOLDER [-dc DIALOGUE_CHANGES] [-f FILTER]

optional arguments:
  -h, --help            show this help message and exit
  -bf BASE_FOLDER, --base-folder BASE_FOLDER
                        Directory path containing the base subtitle files
  -df DIALOGUE_FOLDER, --dialogue-folder DIALOGUE_FOLDER
                        Directory path containing the dialogue subtitle files
  -dc DIALOGUE_CHANGES, --dialogue-changes DIALOGUE_CHANGES
                        The maximum similarity between the base sub and dialogue sub dialogue for it to be added to the output file that contains a list of all overwritten dialogue. 1 = 100%
  -f FILTER, --filter FILTER
                        Regex for filtering the events (in both files), see README for default value
```

# Example

As an example use case I will run the application on the anime 86, using the official Crunchyroll as dialogue subtitle and Kantai's fansubs as the base subtitle.

## Step 1 | Running the application

First run the command with your preferred settings, here I am using a custom regex filter since one or more of the subtitles used "Flashback" as a style name, which is not in the default regex filter. Additionally, I set the dialogue changes option to 0.5, this enables logging the overwritten dialogue lines for every line that is less than 50% similar to its original. 
```console
assdialoguemerger -df "D:\Anime\86\CR\s01" -bf "D:\Anime\86\Kantai\s01" -dc 0.5 -f "^Default|^Main|^Italics|^Top|^Alt|^Flashback"
```

After this you will have your new .ass files, logs in your console, and depending on whether you used the -dc option, _changes.txt files that contain all dialogue overwrites.

### **Important**
If the program crashes, it is most likely that one of the two subtitles that were being compared at the time had a stylename that was not in your filter! Open the subtitle file, check all style names that were used for **dialogue** subtitle lines and updated your regex filter.

## Step 2 | Checking & retiming the added/removed lines

For every subtitle file in the folder that you are using you will get a log in your console, similar to the one below (unless no lines had to be removed or copied over). These are simply the lines as they are saved within the original .ass files, preceded by either a + or a -. A + indicates that the line was copied over from the dialogue line to the base subtitle. A - indicates that a line from the base subtitle has been dropped. 

```console
 -  Dialogue: 20,0:00:06.15,0:00:07.20,Top,,0,0,0,,Forced to fight.
 -  Dialogue: 20,0:00:07.20,0:00:10.53,Top,,0,0,0,,You get to watch us from afar;\Nhiding behind the safety of the walls.
 -  Dialogue: 20,0:00:10.53,0:00:12.49,Top,,0,0,0,,Ordering us around without batting a goddamn eye.
 -  Dialogue: 20,0:00:12.49,0:00:14.54,Top,,0,0,0,,That's you right now.
 +  Dialogue: 0,0:00:48.13,0:00:48.81,Italics,L,0,0,0,,Um—
 +  Dialogue: 0,0:03:17.50,0:03:19.02,Main,Voices,0,0,0,,Go!
 -  Dialogue: 20,0:09:48.36,0:09:50.19,Default,,0,0,0,,The battlefield of the 86th Sector.
 -  Dialogue: 20,0:12:26.85,0:12:32.23,Default,,0,0,0,,You get to watch us from afar;\Nhiding behind the safety of the walls.
 -  Dialogue: 20,0:12:32.23,0:12:34.11,Default,,0,0,0,,That's you right now.
 +  Dialogue: 0,0:13:46.04,0:13:47.10,Main,L,0,0,0,,Um...
86 - Eighty-Six - s01e04 - Real Name.mkv.ass  |  s01e04.ass
```

In my example there were quite a lot of changes to be made before the lines were ready to be merged. It is important that you lookup these lines inside of your new .ass files, since these changes are likely to have timing mistakes. All added lines (indicated by the +) still have the timings of the dialogue subtitle file, this almost guarantees that the timing will be wrong and must be manually adjusted. The removed lines (indicated by the -) is a bit different. 
In most cases they will be safe to ignore, but sometimes the lines before and/or after it may be mistimed depending on why the line had to be removed. So, if you are not planning to do a quality check on your subtitles, make sure to check the surrounding lines of these removed lines just in case.

## Step 3 | (optional)
This step is optional, but recommended. If you decided to log the dialogue changes / overwrites with the -dc option, you should now have a _changes.txt file for every subtitle that you merged. You should quickly skim through all these .txt files and see if there are any peculiar overwrites made. If a dialogue change seems to be completely wrong (e.g. the replacement text has a completely different meaning than the original) then something might have gone wrong with merging, and the file should be manually checked for any errors that could be caused by the script.


## Defaults
Default style match regex: ```^Default|^Main|^Italics|^Top|^Alt```\
Default dialogue changes logging: ```-1 (off)```

## Roadmap
- (Possibly) generate difference view (much like diffchecker.com) instead of text log.
- Copy over other fields such as actor.
- Customizable output filenames.
- Better split-line support to reduce manual retiming work.
- Line numbers in the console output for the generated .ass files.
- GUI application (will be another repository)
