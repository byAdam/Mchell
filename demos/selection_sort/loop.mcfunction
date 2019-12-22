# Sets sub iterator score equal to main iterator score and starts sub loop
scoreboard players operation @e[type=sub_iter] data_iter = @s data_iter
execute @e[type=sub_iter] ~ ~ ~ function sub_loop

## Swap the minimum value and closest value
tp @e[type=elem,c=1] @e[type=elem,tag=min]
tp @e[type=elem,tag=min] ~ ~ ~
tag @e[type=elem,tag=min] remove min

# Move iterator and sub iterator, sets a new initial minimum value
scoreboard players add @s data_iter 1
tp @s ~1 ~ ~
tp @e[type=sub_iter] ~1 ~ ~
tag @e[type=elem,c=1] add min

# Run this function while the iterators score is less than 99
execute @s[scores={data_iter=..99}] ~ ~ ~ function loop