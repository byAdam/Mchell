![Logo](icon.png "Logo")
### A Minecraft Bedrock Function interpreter and shell written in Python

# FAQ
## What is it?
It is a interpreter and shell for running Minecraft Bedrock functions and commands. It allows you to write command line programs just using Minecraft commands, essentially making it into a programming language! It has a few added features but at its core, it is the same as it is in Minecraft.

## How does it work?
When you use MCF, you create a virtual Minecraft world. You can interface with this Minecraft world, using the same command syntax as if you were really playing Minecraft.

## What can it do?
Many of the core Minecraft features have been implemented into MCF. These include: Manipulating Blocks, Manipulating Entities, Manipulating Scoreboards. I have also added some custom syntax to allow users to read from standard input (Using /scoreboard) and write to standard output. (Using /say)

## What can't it do?
At the moment, there is no ability to make any system calls except reading from STDIN and writing to STDOUT. MCF is turing complete though, so go nuts!

## Installation and Use
### Download MCF V1.0 for Windows

## Using MCF
When you install MCF, it adds "mcf" as a command to command prompt. 
You can run a function on the interpreter by specifying the path of the file as a command line argument. The directory of the function will act as the root directory. If no path is specified, the interpreter will enter the shell.
There is also a number of flags you can specify:
- -e = Run the function/shell relative to a player called "main"
- -l = Try to load world.json in the root directory
- -s = Save the world to "world.json" in the root directory on exit
- -t = Run the function 20 times per second until you exit


# Technical Details

## Implemented Commands
- /setblock
- /fill
- /summon 
- /kill
- /tp
- /execute
- /function
- /tag
- /scoreboard
- /say

## Implemented Selectors
- @a
- @e
- @p
- @r
- @s

## Implemented Selector Arguments
 - x, y, z
 - dx, dy, dz
 - r, rm
 - name
 - scores
 - tag
 - type
 - c

## Custom Syntax
scoreboard players input \<target> \<objective>
- This command will read a line from STDIN
- If the line is an integer, that integer will be saved to the target for that objective
- If the line consists of a single UNICODE character, the UNICODE character code will be saved to the target for that objective
- If the line consists of more than one UNICODE character, an error will be raised
- E.G scoreboard players input @a example

/say
- /say writes a line to STDOUT
- SELECTOR\*OBJECTIVE = Returns the score for the objective for the target entities
  - E.G @a\*example
- SELECTOR#OBJECTIVE = Returns the UNICODE Character corresponding to the score for the objective for the target entities
  - E.G @a#example

## Structure
### World
A world consist of: Blocks, Entities, Scoreboard Objectives
### Entity
An entity consist of: position, uuid, type, name, tags
### Block
A block consists of: a position, identifier, data value
### Scoreboard Objective
A scoreboard objective consits of: entities with a non-null score
