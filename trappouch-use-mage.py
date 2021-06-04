def MultiTrapPouchUse():
    pouches = []
    try:
        with open(str(Misc.CurrentScriptDirectory())+'\\'+Player.Name+"-pouches.txt", 'r') as pouches_file:
            # Read and print the entire file line by line
            for line in pouches_file:
                for item in Player.Backpack.Contains:
                    if "pouch" in str(item) and str(item.Serial) in str(line):
                        pouches.append(line.rstrip())
    except EnvironmentError:
        pouches_file = open(str(Misc.CurrentScriptDirectory())+'\\'+Player.Name+"-pouches.txt", 'w')
    
    with open(str(Misc.CurrentScriptDirectory())+'\\'+Player.Name+"-pouches.txt", 'w') as pouches_file:
        for item in Player.Backpack.Contains:
            if "pouch" in str(item) and str(item.Serial) not in str(pouches):
                pouches.append(str(item.Serial) + ", False")
        used = False
        i = -1
        for pouch in pouches:
            i += 1
            if "True" in str(pouch):
                Player.HeadMessage( 13, "USING POUCH")
                Items.UseItem(int(pouch.split(',')[0]))
                Misc.Pause(100)
                pouches[i] = str(pouch.split(',')[0]) + ", False" 
                used = True
                break
        for pouch in pouches:
            pouches_file.write(str(pouch))
            pouches_file.write("\n")
        if not used:
            Player.HeadMessage( 13, "NO POUCHES TRAPPED")
    return    

MultiTrapPouchUse()
Misc.Pause(10)