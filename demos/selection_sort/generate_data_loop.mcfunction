# Increates iterator score by 1
scoreboard players add @s data_iter 1

# Create a new element at end of list and assign random value
summon elem ~ ~ ~
scoreboard players random @e[type=elem,c=1] data 0 100

# Shift iterator one block in array
tp @s ~1 ~ ~

# Run this function while the iterators score is less than 99
execute @s[scores={data_iter=..99}] ~ ~ ~ function generate_data_loop