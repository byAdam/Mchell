# Creates objectives
## Stores data
scoreboard objectives add data dummy
## Stores where you are in loop
scoreboard objectives add data_iter dummy
## Used to calculate which number is small
scoreboard objectives add min_calc dummy

# Summons an iterator and sub iterator entity, and
summon iter ~ ~ ~
summon sub_iter ~ ~ ~

# Generate 100 bytes of data and outputs
execute @e[type=iter] ~ ~ ~ function generate_data_loop
say @e[type=elem,c=100]*data

# Resets iterator
tp @e[type=iter] ~ ~ ~
scoreboard players set @e[type=iter] data_iter 0

# Sets an inital minimum value and starts loop
tag @e[type=elem,c=1] add min
execute @e[name=iter] ~ ~ ~ function loop

# Outputs data (now sorted)
say @e[type=elem,c=100]*data