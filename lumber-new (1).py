from datetime import datetime, timedelta
from py_stealth import *
import json
from pprint import pprint
from common_utilss import *
import common_utilss


# Version: 2.0.1
# Made by: Quaker and Mark. based on scirpt found on github (https://github.com/ohbob/ultima-online---stealth-scripts/blob/master/mining_demise.py)
# What to change: Look for "**CHAGE_ME**" along the script
# Everyday at 12:00 and 00:00 the script will try to make a 1.000.0000 check on the bank.
# 
# Changelog:
# 2.0.1: Bug fix. Not dressing after ress. SaveSet() missing at the beginning
#
#

# ======================================================================================================================
# CONSTANTS
# ======================================================================================================================

# ======================================================================================================================
# AQUI VAI O WEEBHOOK DO DISCORD
# ======================================================================================================================

DISCORD_WEBHOOK_Marcos = ""

common_utilss.DEBUG = False
common_utilss.SUPER_DEBUG = False

#protection if UOStealth don't find your name. LAG is the main reason
while (CharName() == 'Unknown Name') or (not CharName()):
    Wait(5000)


chars = {}
#**CHAGE_ME** 
#**CHAGE_ME** 
#**CHAGE_ME** 
#[Axetype, Vendor_context, [Wood_runebooks], House_runebook, Max_weigth, Sell_Wood, Bank/Home, [RelativecoordX, RelativecoordY] - position to cut tree
# 0 - Put the name of runebooks with the marked tree here.
# 1 - Put the name of the runebook with vendor, bank and/or home runes. 
# 2 - Put "False" (case sensitive) here if you don't want to sell boards.
# 3 - Put 'Bank' if you want to use bank as container to drop wood, or the container ID in your house that will hold the boards
# 4 - Relative Tile to set the target. (0, -1) = Runes marked with trees on the North tile
chars[CharName()] =   [['Wood1','Wood2'],'Home',True,'Bank',[0,-1]]
# Obs.: If you have different characters with different configurations, you can create multiple lines like above, changing "CharName()" for your chars name!
#**CHAGE_ME** 
#**CHAGE_ME** 
#**CHAGE_ME** 

#**CHAGE_ME** REAL RUNE POSITIONS ON THE HOME BOOK! Sequential (eg.: 1,2,3,4,5). NOT like UOSteam (5,7,etc...)
VENDOR_RUNE_POSITION = 1
BANK_RUNE_POSITION = 2
HOME_RUNE_POSITION = 3 




if ObjAtLayer(LhandLayer()) > 0:
    AXE_TYPE = GetType(ObjAtLayer(LhandLayer()))
else:
    if FindType(0xf43, Backpack()) > 0:
        #last resort. Try to find a commom axe on the backpack
        AXE_TYPE = GetType(FindItem())
    else:
        print("Axe not found! Please equip!")
        exit()

WOOD_RUNEBOOKS = chars[CharName()][0]

HOUSE_RUNEBOOK = chars[CharName()][1]

MAX_WEIGTH = MaxWeight() - 50

SELL_WOOD = chars[CharName()][2]

STORAGE_CONTAINER = chars[CharName()][3]

#Relative Tile to set the target. (0, -1) = Runes marked with trees on the North tile
RELATIVE_X = chars[CharName()][4][0]
RELATIVE_Y = chars[CharName()][4][1]




WOOD_GOODIES_TYPE = [0x1bdd,0x1bd7,0x318f,0x3199,0x3190,0x2f5f,0x3191,0xeed]

GOLD = [0xeed]

LOG_TYPE = 0x1bdd #Type of Log to chop on the backpack


TREE_TYPES = [3274, 3275, 3277, 3280, 3281, 3282, 3283, 3286, 3288, 3290, 3293, 3296, 3299, 3302, 3303, 3320, 3323, 3326, 3329, 3393, 3394, 3395, 3396, 3415, 3416, 3418, 3419, 3438, 3439, 3440, 3441, 3442, 3460, 3461, 3462, 3476, 3478, 3480, 3482, 3484, 3492, 3496, 4802, 4801, 4803]


if GetSkillValue('Magery') >= 60:
    TRAVEL = "recall"
if GetSkillValue('Chivalry') >= 50:
    TRAVEL = "chiva"


# ======================================================================================================================
# Variables
# ======================================================================================================================

madeCheck = False #Boolean to check if a money checl has been made




# Defining global variables for equip
common_utilss.hat = 0
common_utilss.neck = 0
common_utilss.sleeves = 0
common_utilss.chest = 0
common_utilss.legs = 0
common_utilss.gloves = 0
common_utilss.lhand = 0
common_utilss.ring = 0
common_utilss.brace = 0
common_utilss.robe = 0
common_utilss.shoes = 0
common_utilss.talisman = 0
common_utilss.cloak = 0
common_utilss.ear = 0
common_utilss.rhand = 0
common_utilss.waist = 0
common_utilss.torsoH = 0
common_utilss.shirt = 0
common_utilss.eggs = 0
common_utilss.Armor_Item_List = []
common_utilss.Armor_Item_Layers  = [HatLayer(),NeckLayer(),ArmsLayer(),TorsoLayer(),PantsLayer(),GlovesLayer(),LhandLayer(),RingLayer(),BraceLayer(),RobeLayer(),ShoesLayer(),TalismanLayer(),CloakLayer(),EarLayer(),RhandLayer(),WaistLayer(),TorsoHLayer(),ShirtLayer(),EggsLayer()]


# ======================================================================================================================
# Utils
# ======================================================================================================================

def checkTimeAndMakeCheck():
    global madeCheck
    currentTime = datetime.utcnow()
    #debug("BEFORE IF")
    #debug(currentTime)
    if (currentTime.hour == 12) or (currentTime.hour == 0):
        if not madeCheck:
            #debug("INSIDE FIRST IF")
            UOSay("check 1000000")
            madeCheck = True
            #print("MADE A CHECK!")
    if (currentTime.hour != 12) and (currentTime.hour == 0):
        #debug("INSIDE SECOND IF")
        madeCheck = False


# ======================================================================================================================
# Sell And Unload
# ======================================================================================================================

def sellAndUnload():
    VENDOR_CONTEXT = ""
    check_weight(0x1BD7,0,1)
    #RECALLAR PARA VENDOR E VENDER
    runebook(HOUSE_RUNEBOOK, TRAVEL, VENDOR_RUNE_POSITION)
    wait_lag(800)
    #debug("Recalled to Vendor")
    Wait(800)  
    SetFindDistance(25)
    # try to find carpenter NPC around
    NPC_TYPES = [0x0190, 0x0191]
    if FindTypesArrayEx(NPC_TYPES ,[0xFFFF],[Ground()],False):
        founds = GetFindedList()
        for found in founds:
            vendor_name = GetAltName(found)
            if (vendor_name.find('carpenter') != -1): 
                VENDOR_CONTEXT = found
    
    if VENDOR_CONTEXT:
        #SELL FIRST
        FindType(0x1bd7, Backpack())
        if (FindTypeEx(0x1bd7, 0x0000, Backpack(), False)): #If commom board found on backpack
            #debug("Found Board. Setting autosell and sell")
            AutoSell(0x1bd7, 0x0000, 999)
            wait_lag(100)
            SetContextMenuHook(VENDOR_CONTEXT, 2)
            wait_lag(100)
            RequestContextMenu(VENDOR_CONTEXT)
            wait_lag(200)
            #RESET CONTEXT
            SetContextMenuHook(0, 0)
            AutoSell(0, 0, 0)
            # 2 TIME SJUST TO  MAKE SURE WE SOLD EVERYTHING
            AutoSell(0x1bd7, 0x0000, 999)
            wait_lag(100)
            SetContextMenuHook(VENDOR_CONTEXT, 2)
            wait_lag(100)
            RequestContextMenu(VENDOR_CONTEXT)
            wait_lag(200)
            #RESET CONTEXT
            SetContextMenuHook(0, 0)
            AutoSell(0, 0, 0)
    
    #RECALLAR PARA BANCO E CHAMAR "unload"
    runebook(HOUSE_RUNEBOOK, TRAVEL, BANK_RUNE_POSITION)
    wait_lag (200)
    UOSay('bank')
    wait_lag (200)
    bank = ObjAtLayer(BankLayer())
    if (bank):
        if STORAGE_CONTAINER == 'Bank':
            unload(WOOD_GOODIES_TYPE,bank)
        else:
            unload(GOLD,bank)
        UOSay('saldo')
        checkTimeAndMakeCheck()
    if STORAGE_CONTAINER != 'Bank':
        runebook(HOUSE_RUNEBOOK, TRAVEL, HOME_RUNE_POSITION)
        Wait (200)
        UseObject(STORAGE_CONTAINER)
        unload(WOOD_GOODIES_TYPE,STORAGE_CONTAINER)


# ======================================================================================================================
# Unload
# ======================================================================================================================

def unload(items, container, msg = 'wood'):
    #AddToSystemJournal('Unload ')
    starttime = datetime.now()
    while FindTypesArrayEx(items, [0xFFFF], [Backpack()], False):
        MoveItem(FindItem(), 65000, container, 0, 0, 0)
        wait_lag(500)
        if checkTimeThreshold (starttime,8000):
            break

    #AddToSystemJournal('Unloaded.')
    return



def TypeQuantity(type, color=0x0000, container=Backpack()):
    FindTypeEx(type, color, container, True)
    return FindFullQuantity()


def identifyTile (x, y, relativeX, relativeY, tileType = []):
    absRelativeX = abs(relativeX)
    absRelativeY = abs(relativeY)

    processedAbsRelativeX = absRelativeX + 2
    processedAbsRelativeY = absRelativeY + 2

    wantedPositionX = x + relativeX
    wantedPositionY = y + relativeY

    #debug ("relative X " + str(x-relativeX) + "," + str(x+relativeX))
    #debug ("relative Y " + str(y-relativeY) + "," + str(y+relativeY))
    for xx in range(x-processedAbsRelativeX,x+processedAbsRelativeX):
        for yy in range(y-processedAbsRelativeY,y+processedAbsRelativeY):
            r = ReadStaticsXY(xx, yy, WorldNum())
            for result in r:
                #print(r)
                if result:
                    #pprint(result)
                    if (result['X'] == wantedPositionX) and (result['Y'] == wantedPositionY):
                        #debug("found a tile on the relative position")
                        if tileType: #If array of tiletype is set, we need to check for a specific tile type!
                            if (result['Tile'] in tileType):
                                #debug("FOUND TILE TYPE: " + str(result['Tile']))
                                return result
                        else: #if not, return the first tile
                            return result


def equipAxe(axeType):
    foundAxe = False
    if ObjAtLayer(RhandLayer()) != 0 and (GetType(ObjAtLayer(RhandLayer()))) == axeType: #Object on the right hand is different from found object on backpack. unequip
        foundAxe = ObjAtLayer(RhandLayer())
        #superDebug("OBJ AT RIGHT HAND:"+str(foundAxe))
    if ObjAtLayer(LhandLayer()) != 0 and (GetType(ObjAtLayer(LhandLayer()))) == axeType: #Object on the right hand is different from found object on backpack. unequip
        foundAxe = ObjAtLayer(LhandLayer())
        #superDebug("OBJ AT LEFT HAND:"+str(foundAxe))
    if not foundAxe: #Axe not found on hand! Equip
        #debug("Axe not found on hand! Equip")
        if FindType(axeType, Backpack()):
            Equip(RhandLayer(),FindItem())
            Wait(500)
            foundAxe = FindItem()
    return foundAxe


             
def lumber(tileType,axeType,maxWeight):
    foundAxe = False
    message_fail = "You hack at | You put some | You chop some "
    message_end = "There is nothing here |" \
                  "There's not enough |" \
                  "You cannot mine |" \
                  "You have no line |" \
                  "That is too far |" \
                  "Try mining elsewhere |" \
                  "You can't mine |" \
                  "someone |" \
                  "Target cannot be |" \
                  "use an axe on that |" \
                  "axe must be equipped |"
    message_attack = "is attacking you"
    message_all = message_fail + "|" + message_end + "|" + message_attack
    journalBreakFirstTime = False
    #debug ("Starting to Lumber. Max Weight:"+str(maxWeight))
    checkGMGump('Lumber')
    checkIfInJail('Lumber')
    if not Dead():
        starttimeglobal = datetime.now()
        ClearJournal()
        ClearSystemJournal()
        #NewMoveXY(x, y, True, 1, True)
        lumberSpot = True
        if TargetPresent():
            CancelTarget()
        #UnEquip(RhandLayer())
        #Wait(1000)
        #check if we need to equip axe
        foundAxe = equipAxe(axeType)
        while lumberSpot:
            #superDebug ("WHILE")                  
            if foundAxe and Weight() < maxWeight+10:
                ClearJournal()
                #debug("start to chop")
                #UseObject(foundAxe)
                UseObject(ObjAtLayer(LhandLayer()))
                #superDebug ("A")
                starttime = datetime.now()
                WaitForTarget(1000)
                if TargetPresent():
                    #superDebug ("AA")
                    #debug ("Targeted Tile. X:"+str(tileType['X'])+ " Y:"+str(tileType['Y']) + " Z:"+str(tileType['Z']) + " Type:" + str(tileType['Tile']))
                    TargetToTile(tileType['Tile'], tileType['X'], tileType['Y'], tileType['Z']) 
                    #superDebug ("B")
                    #TargetToXYZ(0, -1, 0)  # for some reason i can target only mountains.
                    wait_lag(100)
                    #superDebug ("C")
                    WaitJournalLine(starttime, message_all, 7000)
                    #superDebug ("After Wait Jourtnal")
                    #chopLogs(foundAxe)
                    #if InJournal(message_attack):
                    #    print ("D")
                    #    UOSay("Guards")
                    #    Wait(1000)
                    #CHOP
                    if ((InJournalBetweenTimes(message_end, starttime, datetime.now())) > 0):
                    #if InJournal(message_end):
                        #superDebug ("E")
                        lumberSpot = False
                        wait_lag(200)
                    if (not (InJournalBetweenTimes(message_all, starttime, datetime.now())) > 0):
                        if (journalBreakFirstTime):
                            #superDebug ("NOT IN JOURNAL. BREAK")
                            break
                        else:
                            journalBreakFirstTime = True

                if (not (InJournalBetweenTimes(message_all, starttime, datetime.now())) > 0):
                    if (journalBreakFirstTime):
                        #superDebug ("NOT IN JOURNAL. BREAK")
                        break
                    else:
                        journalBreakFirstTime = True
                
                #SECURITY BREAK.
                #SECURITY BREAK.
                #SECURITY BREAK.
                if datetime.now() >= starttimeglobal+timedelta(seconds=30):
                    #print("SECURITY BREAK tree - dentro do while")
                    # print(f"{_x} {_y} WaitJournalLine timeout exceeded, bad tree?")
                    break
                
                #SECURITY BREAK.
                #SECURITY BREAK.
                #SECURITY BREAK.
            else:
                #superDebug ("F")
                if (not chopLogs(foundAxe,axeType)):
                    #superDebug ("G")
                    lumberSpot = False
                else:
                    #Reset Timer
                    starttimeglobal = datetime.now()
                wait_lag(150)
                check_weight(0x1BD7,0,1)
                #SECURITY BREAK.
                #SECURITY BREAK.
                #SECURITY BREAK.
                if datetime.now() >= starttimeglobal+timedelta(seconds=30):
                    #print("SECURITY BREAK tree - fora do while - else")
                    break
                #SECURITY BREAK.
                #SECURITY BREAK.
                #SECURITY BREAK.

                #UnEquip(RhandLayer())
                #Equip(RhandLayer(), 0x4019A26B)
                #runebook("Ore", "recall", 1)  # tower
                #sellAndUnload()
                #unload()
                #upload()
                #runebook("Ore", "recall", 2)  # mine
    if GetHP(Self()) < GetMaxHP(Self()) and GetSkillValue('Chivalry') >= 50:
        Cast('Dispel Evil')            
    if Dead():
        send_discord_message(DISCORD_WEBHOOK_Marcos,"******** (DEAD) @everyone ALERTA!!! FDP RODANDO MATANDO OS BOTS DE LUMBER!!! Char: "+ str(CharName()) +" ********")
        #debug("RESSME!")
        ressme()


def chopLogs(axe,axeType = 0xf43):
    starttimeglobal = datetime.now()
    #debug("CUT LOGS. AXE:"+str(axe))
    axe = equipAxe(axeType)
    FindType(LOG_TYPE, Backpack())
    logsFound = GetFindedList()
    if len(logsFound) == 0:
        return False
    for log in logsFound:
        #superDebug ("H")
        time_before = datetime.now() - timedelta(microseconds=5)
        #debug("AXE INSIDE WHILE:"+str(axe))
        #UseObject(axe)
        UseObject(ObjAtLayer(LhandLayer()))
        superDebug ("HH")
        Wait(5)
        if InJournalBetweenTimes('must wait to perform', time_before, datetime.now()) > 0:
            #debug("Must wait to perform another action")
            UseObject(ObjAtLayer(LhandLayer()))
        while not InJournalBetweenTimes('What do you want to use this item on?', time_before, datetime.now()) > 0:
            Wait(1)
            #SECURITY BREAK.
            #SECURITY BREAK.
            #SECURITY BREAK.
            if datetime.now() >= starttimeglobal+timedelta(seconds=5):
                #print("SECURITY BREAK chop - dentro do for")
                # print(f"{_x} {_y} WaitJournalLine timeout exceeded, bad tree?")
                break
            #SECURITY BREAK.
            #SECURITY BREAK.
            #SECURITY BREAK.
        WaitTargetObject(log)
        #WaitForTarget(4000)
        #superDebug ("I")
        #if TargetPresent():
        #    superDebug ("J")
        #    TargetToObject(FindItem())
        #    superDebug ("K")
        wait_lag(150)
        #superDebug ("L")
        #SECURITY BREAK.
        #SECURITY BREAK.
        #SECURITY BREAK.
        if datetime.now() >= starttimeglobal+timedelta(seconds=5):
            #print("SECURITY BREAK chop - fora do for")
            # print(f"{_x} {_y} WaitJournalLine timeout exceeded, bad tree?")
            break
        #SECURITY BREAK.
        #SECURITY BREAK.
        #SECURITY BREAK.
    return True







if __name__ == '__main__':
    print("INICIO")
    Wait(2500)
    SaveSet()
    #SetSilentMode(False)
    SetARStatus(True)
    close_gumps()
    #start_cordinates = (GetX(Self()), GetX(Self()))
    #NewMoveXY(768, 628, True, 1, True)
    if Dead():
        send_discord_message(DISCORD_WEBHOOK_Marcos,"******** (DEAD) @everyone ALERTA!!! FDP RODANDO MATANDO OS BOTS DE LUMBER!!! Char: "+ str(CharName()) +" ********")	
        ressme()
    while True:                          
        for runeBook in WOOD_RUNEBOOKS:
            for runenumber in range(1, 17):
                SaveSet()
                check_weight(0x1BD7,0,1)
                #currentbook = f'Ore{i}'
                #debug("Runebook: " + str(runeBook) + ". Rune:" + str(runenumber))
                runebook(runeBook, TRAVEL, runenumber, 4000)
                #debug("Recalled")
                tile = identifyTile(GetX(Self()),GetY(Self()),RELATIVE_X,RELATIVE_Y,TREE_TYPES)
                #debug("After Tile")
                if Dead():
                    send_discord_message(DISCORD_WEBHOOK_Marcos,"******** (DEAD) @everyone ALERTA!!! FDP RODANDO MATANDO OS BOTS DE LUMBER!!! Char: "+ str(CharName()) +" ********")
                    ressme()
                if (tile):
                    lumber(tile, AXE_TYPE,MAX_WEIGTH)
                if Weight() >= MAX_WEIGTH:
                    chopLogs(AXE_TYPE)
                    if SELL_WOOD: #If its set to sell wood
                        sellAndUnload()
                    else:
                        if STORAGE_CONTAINER == 'Bank':
                            runebook(HOUSE_RUNEBOOK, TRAVEL, BANK_RUNE_POSITION)
                            Wait (200)
                            UOSay('bank')
                            bank = ObjAtLayer(BankLayer())
                            if (bank):
                                unload(WOOD_GOODIES_TYPE,bank)
                            UOSay('saldo')
                        else:
                            runebook(HOUSE_RUNEBOOK, TRAVEL, HOME_RUNE_POSITION)
                            Wait (200)
                            UseObject(STORAGE_CONTAINER)
                            unload(WOOD_GOODIES_TYPE,STORAGE_CONTAINER)
        #debug("finished")
        Wait(5000)





