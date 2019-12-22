## Creates objectives
scoreboard objectives add n dummy
scoreboard objectives add mod_3 dummy
scoreboard objectives add mod_5 dummy
## Adds 0 to @s so it definitely has a score
scoreboard players add @s n 0
## Sets constants
scoreboard objectives add const dummy
scoreboard players set n3 const 3
scoreboard players set n5 const 5