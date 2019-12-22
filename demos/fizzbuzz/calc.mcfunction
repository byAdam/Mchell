## If the entity does not have a non 0 score, ask for input
execute @s[scores={n=0}] ~ ~ ~ scoreboard players input @s n
## Calculate mods
scoreboard players operation @s mod_3 = @s n
scoreboard players operation @s mod_5 = @s n
scoreboard players operation @s mod_3 %= n3 const
scoreboard players operation @s mod_5 %= n5 const

execute @s[scores={mod_3=0,mod_5=0}] ~ ~ ~ say Fizzbuzz
execute @s[scores={mod_3=0,mod_5=!0}] ~ ~ ~ say Fizz
execute @s[scores={mod_3=!0,mod_5=0}] ~ ~ ~ say Buzz
execute @s[scores={mod_3=!0,mod_5=!0}] ~ ~ ~ say @s*n