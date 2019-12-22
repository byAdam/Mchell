# Creates objectives
scoreboard objectives add prime dummy
scoreboard objectives add prime_tmp dummy
scoreboard objectives add prime_calc dummy
scoreboard objectives add prime_calc_square dummy

## Waits for user input
say Make sure you are running this program with the -e flag!
say Enter your number:
scoreboard players input @s prime
scoreboard players set @s prime_calc 1

# Begins prime loop if input is greater than 1
execute @s[scores={prime_tmp=!0,prime=2..}] ~ ~ ~ function loop

scoreboard players operation @s prime_calc -= @s prime
## If the number that divides in is the same as the input, prime_calc will be 0
execute @s[scores={prime_calc=0}] ~ ~ ~ say Prime
execute @s[scores={prime_calc_square=1..}] ~ ~ ~ say Prime
execute @s[scores={prime_calc=!0,prime_calc_square=..0}] ~ ~ ~ say Not Prime