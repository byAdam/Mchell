# Copys input score
scoreboard players operation @s prime_tmp = @s prime
# Adds 1 to iterator
scoreboard players add @s prime_calc 1
# Gets prime_tmp % prime_calc
scoreboard players operation @s prime_tmp %= @s prime_calc

# If it does not divide in evenly, run this loop again
execute @s[scores={prime_tmp=!0}] ~ ~ ~ function loop