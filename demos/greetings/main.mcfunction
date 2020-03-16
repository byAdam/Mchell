def write_loop
	## Saves score to writer
	scoreboard players input @s store
	## Spawns character
	summon char ~ ~ ~
	scoreboard players operation @e[type=char,c=1] store = @s store

	## Moves and loops
	tp @s ~1 ~ ~
	execute @e[type=writer,scores={store=!0}] ~ ~ ~ function write_loop

scoreboard objectives add store dummy
summon writer ~ ~ ~
execute @e[type=writer] ~ ~ ~ function write_loop

say Hello, @e[type=char]#^store