scoreboard objectives add prime dummy
scoreboard objectives add prime_tmp dummy
scoreboard objectives add prime_calc dummy

scoreboard players input @s prime
scoreboard players set @s prime_calc 1

execute @s[scores={prime_tmp=!0,prime=2..}] ~ ~ ~ function loop

scoreboard players operation @s prime_calc -= @s prime
execute @s[scores={prime_calc=0}] ~ ~ ~ say Prime
execute @s[scores={prime_calc=!0}] ~ ~ ~ say Not Prime