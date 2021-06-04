# Survival for Mages - Made by Mark (marcosgribeiro@gmail.com) @ September, 2020.

from datetime import datetime, timedelta
from System.Collections.Generic import List
from System import Byte 


#------------------ VARIABLES
#**CHAGE_ME** 
PET = 0x000628C0
#**CHAGE_ME** 


# ---------------------------------------------------------------------
# --------------------------- TIMERS ----------------------------------
# ---------------------------------------------------------------------
timer_warning = datetime.now()- timedelta(seconds=10)
timer_healpot = datetime.now()- timedelta(seconds=11)
timer_apple = datetime.now()- timedelta(seconds=122) 
alert_mortal = True  
    
# ---------------------------------------------------------------------
# --------------------------- STATUS ----------------------------------
# ---------------------------------------------------------------------
status_str = 121
status_dex = 57
guardzone = False

guardlines = [['Heartwood'],[6911, 255],[7168, 512],['Cove'],[2200, 1110],[2250, 1160],['Cove'],[2200, 1160],[2286, 1246],['Britain'],[1416, 1498],[1740, 1777],['Britain'],[1500, 1408],[1546, 1498],['Britain'],[1385, 1538],[1416, 1777],['Britain'],[1416, 1777],[1740, 1837],['Britain'],[1385, 1777],[1416, 1907],['Britain'],[1093, 1538],[1385, 1907],['Britain'],[1492, 1602],[1500, 1621],['Britain'],[1500, 1610],[1508, 1626],['Britain'],[1576, 1584],[1600, 1600],['Britain'],[1456, 1512],[1472, 1528],['Britain'],[1472, 1512],[1480, 1520],['Britain'],[1486, 1684],[1494, 1692],['Britain'],[1494, 1676],[1502, 1700],['Britain'],[1424, 1712],[1432, 1736],['Britain'],[1432, 1712],[1440, 1724],['Britain'],[1608, 1584],[1632, 1592],['Britain'],[1616, 1576],[1624, 1584],['Britain'],[1544, 1760],[1560, 1776],['Britain'],[1560, 1760],[1568, 1768],['AWheatfieldinBritain1'],[1120, 1776],[1152, 1808],['AWheatfieldinBritain2'],[1184, 1808],[1216, 1840],['AWheatfieldinBritain3'],[1216, 1872],[1248, 1904],['ACarrotFieldinBritain1'],[1208, 1712],[1224, 1736],['AnOnionFieldinBritain1'],[1224, 1712],[1240, 1736],['ACabbageFieldinBritain1'],[1176, 1672],[1192, 1695],['ATurnipFieldinBritain1'],[1192, 1672],[1208, 1696],['AWheatfieldinBritain4'],[1104, 1608],[1136, 1640],['AWheatfieldinBritain5'],[1136, 1560],[1168, 1592],['ATurnipFieldinBritain2'],[1208, 1592],[1224, 1616],['ACarrotFieldinBritain2'],[1224, 1592],[1240, 1616],['Jhelom'],[1303, 3670],[1492, 3895],['Jhelom'],[1338, 3895],[1412, 3923],['Jhelom'],[1383, 3951],[1492, 4045],['Jhelom'],[1352, 3800],[1368, 3832],['Jhelom'],[1368, 3808],[1376, 3824],['Jhelom'],[1432, 3768],[1464, 3776],['Jhelom'],[1440, 3776],[1464, 3784],['Minoc'],[2411, 366],[2546, 607],['Minoc'],[2548, 495],[2620, 550],['Minoc'],[2564, 585],[2567, 627],['Minoc'],[2567, 585],[2628, 646],['Minoc'],[2499, 627],[2567, 690],['Minoc'],[2457, 397],[2497, 405],['Minoc'],[2465, 405],[2473, 413],['Minoc'],[2481, 405],[2489, 413],['Ocllo'],[3587, 2456],[3706, 2555],['Ocllo'],[3706, 2460],[3708, 2555],['Ocllo'],[3587, 2555],[3693, 2628],['Ocllo'],[3590, 2628],[3693, 2686],['Ocllo'],[3693, 2555],[3754, 2699],['Ocllo'],[3754, 2558],[3761, 2699],['Ocllo'],[3761, 2555],[3768, 2699],['Ocllo'],[3695, 2699],[3761, 2712],['Ocllo'],[3664, 2608],[3680, 2624],['Ocllo'],[3664, 2640],[3672, 2656],['Ocllo'],[3672, 2648],[3680, 2656],['Trinsic'],[1856, 2636],[1931, 2664],['Trinsic'],[1816, 2664],[2099, 2895],['Trinsic'],[2099, 2782],[2117, 2807],['Trinsic'],[1970, 2895],[2017, 2927],['Trinsic'],[1796, 2696],[1816, 2763],['Trinsic'],[1800, 2796],[1816, 2848],['Trinsic'],[1834, 2728],[1856, 2744],['Trinsic'],[2024, 2784],[2040, 2804],['Trinsic'],[2026, 2804],[2040, 2806],['Trinsic'],[2024, 2806],[2040, 2813],['Trinsic'],[1923, 2786],[1935, 2808],['Trinsic'],[1935, 2786],[1942, 2800],['Vesper'],[2893, 598],[3014, 648],['Vesper'],[2816, 648],[3065, 1013],['Vesper'],[2734, 944],[2816, 948],['Vesper'],[2728, 948],[2816, 1001],['Vesper'],[2952, 864],[2968, 896],['Vesper'],[2968, 872],[2976, 888],['Vesper'],[2776, 952],[2792, 984],['Vesper'],[2768, 960],[2776, 976],['Vesper'],[2892, 901],[2908, 920],['Vesper'],[2908, 904],[2916, 912],['Yew'],[92, 656],[441, 881],['Yew'],[441, 746],[657, 881],['Yew'],[258, 881],[657, 1261],['Yew'],[657, 922],[699, 1229],['Yew'],[657, 806],[674, 834],['Yew'],[718, 874],[756, 896],['Yew'],[600, 808],[624, 832],['AFieldofSheepinYew1'],[664, 928],[686, 950],['AFieldofSheepinYew2'],[664, 1168],[686, 1190],['AFarminYew'],[560, 1088],[582, 1110],['AWheatfieldinYew1'],[560, 1232],[576, 1248],['AWheatfieldinYew2'],[368, 1176],[382, 1208],['Wind'],[5294, 19],[5366, 139],['Wind'],[5132, 58],[5213, 126],['Wind'],[5197, 126],[5252, 204],['Wind'],[5132, 3],[5202, 58],['Wind'],[5252, 112],[5294, 170],['Wind'],[5213, 98],[5252, 126],['Wind'],[5279, 57],[5294, 112],['Wind'],[5252, 170],[5284, 178],['Wind'],[5286, 25],[5294, 57],['Wind'],[5252, 178],[5272, 183],['Wind'],[5252, 183],[5262, 193],['Wind'],[5159, 15],[5184, 24],['Wind'],[5159, 24],[5168, 40],['Wind'],[5175, 24],[5184, 32],['Wind'],[5212, 159],[5221, 183],['Wind'],[5221, 171],[5228, 183],['Wind'],[5206, 164],[5212, 179],['Wind'],[5303, 28],[5319, 42],['SerpentsHold'],[2868, 3324],[3073, 3519],['SerpentsHold'],[2960, 3400],[2976, 3416],['SerpentsHold'],[2968, 3416],[2976, 3432],['SerpentsHold'],[3008, 3450],[3022, 3464],['SkaraBrae'],[538, 2107],[688, 2297],['SkaraBrae'],[600, 2232],[616, 2256],['SkaraBrae'],[592, 2240],[600, 2256],['SkaraBrae'],[616, 2240],[624, 2256],['SkaraBrae'],[552, 2168],[568, 2192],['SkaraBrae'],[568, 2168],[576, 2176],['Nujelm'],[3475, 1000],[3835, 1435],['Nujelm'],[3736, 1184],[3752, 1207],['Nujelm'],[3728, 1192],[3736, 1207],['Nujelm'],[3728, 1288],[3751, 1303],['Nujelm'],[3728, 1303],[3744, 1312],['Nujelm'],[3728, 1312],[3740, 1320],['Nujelm'],[3728, 1320],[3744, 1343],['Nujelm'],[3744, 1328],[3751, 1343],['Nujelm'],[3760, 1216],[3772, 1240],['Nujelm'],[3772, 1220],[3776, 1236],['Nujelm'],[3776, 1224],[3784, 1232],['Nujelm'],[3728, 1248],[3744, 1272],['Nujelm'],[3744, 1264],[3752, 1272],['Nujelm'],[3744, 1248],[3752, 1256],['Moonglow'],[4535, 844],[4555, 847],['Moonglow'],[4530, 847],[4561, 908],['Moonglow'],[4521, 914],[4577, 963],['Moonglow'],[4278, 915],[4332, 934],['Moonglow'],[4283, 944],[4336, 1017],['Moonglow'],[4377, 1015],[4436, 1052],['Moonglow'],[4367, 1050],[4509, 1195],['Moonglow'],[4539, 1036],[4566, 1054],['Moonglow'],[4517, 1053],[4540, 1075],['Moonglow'],[4389, 1198],[4436, 1237],['Moonglow'],[4466, 1211],[4498, 1236],['Moonglow'],[4700, 1108],[4717, 1126],['Moonglow'],[4656, 1127],[4682, 1140],['Moonglow'],[4678, 1162],[4703, 1187],['Moonglow'],[4613, 1196],[4636, 1218],['Moonglow'],[4646, 1212],[4660, 1229],['Moonglow'],[4677, 1214],[4703, 1236],['Moonglow'],[4622, 1316],[4644, 1340],['Moonglow'],[4487, 1353],[4546, 1374],['Moonglow'],[4477, 1374],[4546, 1409],['Moonglow'],[4659, 1387],[4699, 1427],['Moonglow'],[4549, 1482],[4578, 1509],['Moonglow'],[4405, 1451],[4428, 1474],['Moonglow'],[4483, 1468],[4504, 1481],['Moonglow'],[4384, 1152],[4392, 1176],['Moonglow'],[4392, 1160],[4408, 1168],['Moonglow'],[4400, 1152],[4408, 1160],['Moonglow'],[4480, 1056],[4488, 1072],['Moonglow'],[4488, 1060],[4492, 1068],['Moonglow'],[4476, 1060],[4480, 1068],['Magincia'],[3653, 2046],[3680, 2094],['Magincia'],[3752, 2046],[3804, 2094],['Magincia'],[3680, 2045],[3752, 2094],['Magincia'],[3652, 2094],[3812, 2274],['Magincia'],[3649, 2256],[3703, 2303],['Magincia'],[3680, 2152],[3704, 2160],['Magincia'],[3720, 2216],[3736, 2232],['Delucia'],[5123, 3942],[5315, 4064],['Delucia'],[5147, 4064],[5272, 4084],['Delucia'],[5235, 3930],[5315, 3942],['Delucia'],[5194, 4053],[5204, 4073],['Papua'],[5639, 3095],[5831, 3318],['Papua'],[5831, 3237],[5851, 3267],['Papua'],[5757, 3150],[5781, 3174],['PalaceofParoxysmus'],[6191, 311],[6561, 671],['Moongates'],[1330, 1991],[1343, 2004],['Moongates'],[1494, 3767],[1506, 3778],['Moongates'],[2694, 685],[2709, 701],['Moongates'],[1823, 2943],[1834, 2954],['Moongates'],[761, 741],[780, 762],['Moongates'],[638, 2062],[650, 2073],['Moongates'],[4459, 1276],[4475, 1292],['Moongates'],[3554, 2132],[3572, 2150]]

def InGuardLines():
    i = 0
    while i< len(guardlines):
        zone =  guardlines[i][0]
        Px = guardlines[i+1][0]
        Py = guardlines[i+1][1]
        Rx = guardlines[i+2][0]
        Ry = guardlines[i+2][1]
        if( (Player.Position.X <= max(Px, Rx)) and (Player.Position.X >= min(Px, Rx)) and (Player.Position.Y <= max(Py, Ry)) and (Player.Position.Y >= min(Py, Ry)) ):
            #Player.HeadMessage(13,"ZONE -> " + zone)
            return True
        i = i + 3
    return False

def MultiTrapPouchUse():
    pouches = []
    with open(str(Misc.CurrentScriptDirectory())+'\\'+Player.Name+"-pouches.txt", 'r') as pouches_file:
        # Read and print the entire file line by line
        for line in pouches_file:
            pouches.append(line.rstrip())
    
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
                Misc.Pause(650)
                pouches[i] = str(pouch.split(',')[0]) + ", False" 
                used = True
                break
        for pouch in pouches:
            pouches_file.write(str(pouch))
            pouches_file.write("\n")
        if not used and Timer.Check("pouches") == False:
            Player.HeadMessage( 13, "NO POUCHES TRAPPED")
            Timer.Create("pouches",3000)
    return    
    
def CountTrapPouchUse():
    pouches = 0
    with open(str(Misc.CurrentScriptDirectory())+'\\'+Player.Name+"-pouches.txt", 'a+') as pouches_file:
        pouches_file.seek(0)
        # Read and print the entire file line by line
        for line in pouches_file:
            if "True" in str(line.rstrip()):
                pouches+=1
        return pouches   

if __name__ == '__main__':
    global guardzone
    while not Player.IsGhost: 
        # Do not interrupt if target is up or player is invisible
        if not Player.Visible or Target.HasTarget():
            continue
            
        # Handle bushido mage for keeping LS buff activated    
        if Player.GetSkillValue('Bushido') > 50 and not Player.SpellIsEnabled('Lightning Strike'):
            Spells.CastBushido("Lightning Strike")
            Misc.Pause(100)    
        
        if "Elizabeth" in Player.Name and Player.GetItemOnLayer("RightHand") is None and Player.GetItemOnLayer("LeftHand") is None and Timer.Check("disarmed") == False:
            Timer.Create("disarmed",5000)
            Player.HeadMessage(33, "[DANGER] UNARMED!!")
            Misc.Pause(100)
        
        # Auto chug strength and agility pots when target is close enough
        mob = Mobiles.FindBySerial(Target.GetLast())
        Misc.Pause(100)
        if mob is not None:
            if Player.DistanceTo(mob) < 16:
                if Player.Str < status_str and not Target.HasTarget():
                    Items.UseItemByID(0x0F09)
                    Misc.Pause(600)
                
                if Player.Dex < status_dex and not Target.HasTarget():
                    Items.UseItemByID(0x0F08)
                    Misc.Pause(600)

        # ---------------------------------------------------------------------
        # --------------------------- ALERTS ----------------------------------
        # ---------------------------------------------------------------------
        
        # CHECKING FOR ESSENTIAL PVP RESOURCES AND ALERT EVERY 10 seconds  
        if datetime.now() >= timer_warning+timedelta(seconds=10):
            timer_warning = datetime.now()
            Player.HeadMessage( 82, "[Running] Survival")
            # CHECKING FOR ---> BANDAGES <----  
            if Player.GetSkillValue('Healing') > 60:
                bands = Items.BackpackCount(0xe21, -1) 
                if bands == 0:
                    Player.HeadMessage( 32, "[DANGER] OUT OF Bandages!")
                else:
                    if bands < 3:
                        Player.HeadMessage( 34, "[Alert] Bandages!")
                    elif bands < 10:
                        Player.HeadMessage( 52, "[Warning] Bandages!")    
            # CHECKING FOR ---> REFRESH POTS <----
            refresh = Items.BackpackCount(0xf0b, -1) 
            if refresh == 0:
                Player.HeadMessage( 32, "[DANGER] OUT OF REFRESH!")
            else:
                if refresh < 3:
                    Player.HeadMessage( 34, "[Alert] Refresh pots!")
                elif refresh < 10:
                    Player.HeadMessage( 52, "[Warning] Refresh pots!") 
            # CHECKING FOR ---> POUCHES <----
            if CountTrapPouchUse() == 0:
                Player.HeadMessage( 32, "POUCH NOT TRAPPED")
            
        # ---------------------------------------------------------------------
        # ------------------------- BANDAGES ----------------------------------
        # --------------------------------------------------------------------- 
        # Handles bandage apply if char has Healing skill
        if Player.GetSkillValue('Healing') > 60 and not Player.BuffsExist("Healing") and Player.Hits < Player.HitsMax*0.8:
            lasttarget = Target.GetLast()
            Items.UseItemByID( 0x0E21, -1 )
            Target.WaitForTarget( 400, True )
            Target.Self()
            Target.SetLast(lasttarget) 
            Misc.Pause(600)         
                
                    
        # ---------------------------------------------------------------------
        # --------------------------- APPLE -----------------------------------
        # --------------------------------------------------------------------- 
        # Uses enhanced apple when char is at low life (< 50%)
        if datetime.now() >= timer_apple+timedelta(seconds=122):
            if Player.YellowHits and Player.Hits < Player.HitsMax*0.4:
                Player.HeadMessage( 52, "USING APPLE")  
                apple = Items.BackpackCount(0x2fd8, -1) 
                if(apple > 0): 
                    Items.UseItemByID(0x2fd8,-1)
                    Misc.Pause(600)
                    timer_apple = datetime.now() 
        
        # ---------------------------------------------------------------------  
        # ------------------------ CURE / HEAL --------------------------------
        # ---------------------------------------------------------------------
        # Auto chug cure and heal potions when needed
        if Player.Poisoned and not Target.HasTarget():
            Items.UseItemByID(0xf07,-1)
            Misc.Pause(600)
        if not Player.YellowHits and Player.Hits < Player.HitsMax*0.6 and not Player.Poisoned and not Target.HasTarget():
            if datetime.now() >= timer_healpot +timedelta(seconds=11):
                heal_pot = Items.BackpackCount(0xf0c, -1) 
                if(heal_pot > 0): 
                    Items.UseItemByID(0xf0c,-1)
                    timer_healpot = datetime.now()
                    Player.HeadMessage( 62, "Heal pot!!")
                    Misc.Pause(600)
        
        # ---------------------------------------------------------------------
        # --------------------------- REFRESH ---------------------------------
        # ---------------------------------------------------------------------
        if Player.Stam < Player.StamMax*0.3 and not Target.HasTarget():
            refresh = Items.BackpackCount(0xf0b, -1) 
            if(refresh > 0): 
                Items.UseItemByID(0xf0b,-1)
                Player.HeadMessage( 62, "Refresh pot!!")
                Misc.Pause(600)
        
        # ---------------------------------------------------------------------
        # ----------------------- Auto-Pouch if Paralyze ----------------------
        # ---------------------------------------------------------------------
        if Player.Paralized and Player.Hits > 80:
            MultiTrapPouchUse()
        Misc.Pause(50)
        
        
    
    # ---------------------------------------------------------------------
    # ----------------- Deslogar Morto - Proteger o PET--------------------
    # ---------------------------------------------------------------------
    if Player.IsGhost:
        Misc.Disconnect()           