scoreboard players operation @s prime_tmp = @s prime
scoreboard players add @s prime_calc 1
scoreboard players operation @s prime_tmp %= @s prime_calc
execute @s[scores={prime_tmp=!0}] ~ ~ ~ function loop