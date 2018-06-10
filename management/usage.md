# How this works

This folder contains all the management with the database directly, or, possibly later on, with the self-built API. You can use it in any Python file that is connected with the bot.

## Relevant files

The folder contains a few files. Here's an explanation of what everything is and what it all does.

### __init__.py
This file is merely to add the folder to the PYTHONPATH and have it seen as a module. This means that ./management can be imported as a package (management)

### db.py
This is the relevant file that contains all the commands you need. If one wishes to import these functions, one could either use

    import management.db as db
    db.execute("SELECT * FROM game")
    
or one could work with the commands like

    from management.db import emoji_to_player, get_user
    emoji_to_player(":smirk:")

#### execute(command)
This command is used if one directly wishes to use a command upon the SQL database. Use of this function is discouraged, as it may not always be SQL-injection proof.
An example is

    execute("SELECT * FROM game")

#### emoji_to_player(emoji)
The **emoji_to_player()**-function takes a given emoji as an input and looks through the database if there's a participant with that emoji. This function is resistant to SQL-injection, and returns a user's id if it has found a match, and returns None if it cannot find a participant.

    emoji_to_player(":smirk:")
    emoji_to_player(":hugs:")

#### get_user(id)
Gather all information of a participant. However, this information is still unparsed, and using **db_get()** where possible is encouraged.

    get_user("248158876799729664")

#### db_get(user_id,column)
Find a certain aspect of a participant. Find out if they're enchanted, demonized, what their emoji is, how many amulets they carry, et cetera. It is SQL-injection proof, but will raise an error if **column** does not exist in the database. Read the subsection [position.py](#position) for the possible values for **column**.
The **user_id** value can be either a string or an integer. If it cannot find the user, however, it will return None. **column** does need to be a string.

    db_get("248158876799729664","enchanted")
    db_get("248158876799729664","id") # Stupid, but who knows. Perhaps needed, at some point.
    db_get("248158876799729664","sleepers")
    db_get("248158876799729664","uses")
    
#### db_set(user_id,column,value)
Change a certain aspect of a given participant. Note that SQL does not understand True or False, so values like *demonized* and *enchanted* have values like 0 and 1. The function does not return anything. If the program doesn't raise an error, you may assume the function worked as intended.
**Watch out:** the value **column** is not SQL-injection proof! Always make sure to type the **column** value yourself rather than filling in a variable. Never blindly trust the user!
Once again, **user_id** can be either an integer or a string, and **value** van be either, depending on what the database wants.

    db_set(248158876799729664,"uses",0)
    db_set("248158876799729664","votes","1")
    db_set(248158876799729664,"powdered","1")

#### db_test()
This function is to be ignored. It is used for testing purposes and should not be used in actual code.

### <a head="#position"></a>position.py

This function is not needed to be used, but it lists what column is present and to which number it translates. However, if you need to look up what columns there are, you can find them listed down here;

0 - id
1 - name
2 - emoji
3 - activity
4 - channel
5 - role
6 - fakerole
7 - uses
8 - votes
9 - threatened
10 - enchanted
11 - demonized
12 - powdered
13 - frozen
14 - undead
15 - bites
16 - bitten
17 - souls
18 - lovers
19 - sleepers
20 - amulets
21 - zombies

If you need another column to be added, ask @Randium#6521 about it, or discuss it with the community.