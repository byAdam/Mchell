def loop
	say 1
	function loop

scoreboard objectives add x dummy
scoreboard players input @s x
execute @s[scores={x=1}] ~ ~ ~ function loop
say 0