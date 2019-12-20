execute @e[type=char] ~ ~ ~ tp @s ~1 ~ ~
summon char 0 0 0
scoreboard players input @e[type=char,x=0,y=0,z=0,c=1] chars
execute @e[type=char,x=0,y=0,z=0,c=1,r=0,scores={chars=!0}] ~ ~ ~ function loop