# Subtract the currents elements score from the mimimum elements score
scoreboard players operation @e[type=elem,tag=min] min_calc = @e[type=elem,tag=min] data
scoreboard players operation @e[type=elem,tag=min] min_calc -= @e[type=elem,c=1,tag=!min] data

# If number is positive, the current elements score is small
# In this case, reassign the min value
tag @e[type=elem,tag=min,scores={min_calc=0..}] add min_tmp
tag @e[type=elem,tag=min_tmp] remove min
execute @e[type=elem,tag=min_tmp] ~ ~ ~ execute @e[type=sub_iter] ~ ~ ~ tag @e[type=elem,c=1,tag=!min_tmp] add min
tag @e[type=elem,tag=min_tmp] remove min_tmp

# Move the iterator
tp @s ~1 ~ ~
scoreboard players add @s data_iter 1

# Run this function while the iterators score is less than 99
execute @s[scores={data_iter=..99}] ~ ~ ~ function sub_loop