from py_stealth import *
from datetime import datetime, timedelta
import json
from pprint import pprint
#import subprocess
import os


try:
    import requests
except ModuleNotFoundError:
    print("No 'requests' module found. Install it using 'pip install requests' ")
    exit()
try:
    from discord_webhook import DiscordWebhook
except ModuleNotFoundError:
    print("No 'discord_webhook' module found. Install it using 'pip install discord_webhook' ")
    exit()


# ======================================================================================================================
# CONSTANTS
# ======================================================================================================================

DEBUG = False #Enable Debug Globally
SUPER_DEBUG = False #Enable Super Debug Globally
WAIT_TIME = 500 #Default Wait Time
WAIT_LAG_TIME = 10000 #Default Wait Lag Time
STUCK_TIME = 10000 #Default Stuck Time
# ======================================================================================================================
# AQUI VAI O WEEBHOOK DO DISCORD
# ======================================================================================================================
DISCORD_WEBHOOK =""

WAV_AFK = "C:\\alarm.wav"

GUMP_DEBUG_FILE = '/Scripts/gump-debug.txt'

JAIL_X_TOP_LEFT = 5270
JAIL_Y_TOP_LEFT = 1160
JAIL_X_BOTTOM_RIGHT = 5310
JAIL_Y_BOTTOM_RIGHT = 1190

AFK_GUMP = 0xc37345f3

# ======================================================================================================================
# Variables
# ======================================================================================================================

InJail = False
GMGumpFound = False
GMGumpAnswered = False

# ======================================================================================================================
# Check Connection
# ======================================================================================================================

def check_connection():
    if not Connected():
        AddToSystemJournal('No connection.')
        while not Connected():
            AddToSystemJournal('trying to connect...')
            Wait(5000)
        AddToSystemJournal('There is a connection.')
        close_gumps()
    return


# ======================================================================================================================
# Check World is Saving
# ======================================================================================================================

#TBD

# ======================================================================================================================
# Check HP, say guards and alarm if HP low
# ======================================================================================================================

def check_hp():
    if GetHP(Self()) == MaxLife():
        return
    SetAlarm()
    AddToSystemJournal('Someone is attacking you.')
    SendTextToUO('Guards')
    return

# ======================================================================================================================
# Check MANA
# ======================================================================================================================

def check_mana():
    if not Dead():
        while Mana() < 20:
            UseSkill("Meditation")
            Wait(5000)
            if Dead():
                print("DEAD ON check_mana! ABORT!")
                return

# ======================================================================================================================
# Check Insured
# ======================================================================================================================


def check_insured():
    wearable_layers = (RhandLayer(), LhandLayer(), ShoesLayer(), PantsLayer(),
        ShirtLayer(), HatLayer(), GlovesLayer(), RingLayer(),
        NeckLayer(), WaistLayer(), TorsoLayer(), BraceLayer(),
        TorsoHLayer(), EarLayer(), ArmsLayer(), CloakLayer(),
        EggsLayer(), LegsLayer()) #RobeLayer()
    for x in wearable_layers:
        obj = ObjAtLayerEx(x,Self())
        if obj != 0:
            valida = str(GetTooltip(obj))
            if valida.find("Insured") < 0:
                if valida.find("Blessed") < 0:
                    print("Non Insured and non blessed wearable found! item id: " +str(obj) + ". Tooltip:"+str(valida) + ". Insured:"+str(valida.find("Insured")) + ". Blessed: "+str(valida.find("Blessed")))
                    return False
    return True

# ======================================================================================================================
# Ress Utils
# ======================================================================================================================


def SaveSet():
    global gloves
    global hat
    global sleeves
    global brace
    global legs
    global lhand
    global neck
    global ring
    global robe
    global chest

    global shoes
    global talisman
    global cloak
    global ear
    global rhand
    global waist

    global torsoH
    global shirt
    global eggs
    

    global Armor_Item_List 
    if ObjAtLayer(GlovesLayer()) > 0:
        gloves = ObjAtLayer(GlovesLayer())
    if ObjAtLayer(HatLayer()) > 0:
        hat = ObjAtLayer(HatLayer())
    if ObjAtLayer(ArmsLayer()) > 0:
        sleeves = ObjAtLayer(ArmsLayer())
    if ObjAtLayer(BraceLayer()) > 0:
        brace = ObjAtLayer(BraceLayer())
    if ObjAtLayer(LegsLayer()) > 0:
        legs = ObjAtLayer(LegsLayer())
    if ObjAtLayer(PantsLayer()) > 0:
        legs = ObjAtLayer(PantsLayer())
    if ObjAtLayer(LhandLayer()) > 0:
        lhand = ObjAtLayer(LhandLayer())
    if ObjAtLayer(NeckLayer()) > 0:
        neck = ObjAtLayer(NeckLayer())
    if ObjAtLayer(RingLayer()) > 0:
        ring = ObjAtLayer(RingLayer())
    if ObjAtLayer(RobeLayer()) > 0:
        robe = ObjAtLayer(RobeLayer())
    if ObjAtLayer(TorsoLayer()) > 0:
        chest = ObjAtLayer(TorsoLayer())

    if ObjAtLayer(ShoesLayer()) > 0:
        shoes = ObjAtLayer(ShoesLayer())
    if ObjAtLayer(TalismanLayer()) > 0:
        talisman = ObjAtLayer(TalismanLayer())
    if ObjAtLayer(CloakLayer()) > 0:
        cloak = ObjAtLayer(CloakLayer())
    if ObjAtLayer(EarLayer()) > 0:
        ear = ObjAtLayer(EarLayer())
    if ObjAtLayer(RhandLayer()) > 0:
        rhand = ObjAtLayer(RhandLayer())
    if ObjAtLayer(WaistLayer()) > 0:
        waist = ObjAtLayer(WaistLayer())

    if ObjAtLayer(TorsoHLayer()) > 0:
        torsoH = ObjAtLayer(TorsoHLayer())   
    if ObjAtLayer(ShirtLayer()) > 0:
        shirt = ObjAtLayer(ShirtLayer())
    if ObjAtLayer(EggsLayer()) > 0:
        eggs = ObjAtLayer(EggsLayer())



    Armor_Item_List = [hat,neck,sleeves,chest,legs,gloves,lhand,ring,brace,robe,shoes,talisman,cloak,ear,rhand,waist,torsoH,shirt,eggs]

    return 


def MyDress():
    for j in range(len(Armor_Item_Layers)):
        while (ObjAtLayer(Armor_Item_Layers[j]) != Armor_Item_List[j]):
            if UnEquip(Armor_Item_Layers[j]):
                wait_lag(1000)
            print("EQUIPING. Item: " + str(j) + " layer:" + str(Armor_Item_Layers[j]) + " item:" + str(Armor_Item_List[j]))
            Equip(Armor_Item_Layers[j], Armor_Item_List[j])
            wait_lag(500) 
    return

def MyUnDress():
    for j in range(len(Armor_Item_Layers)):
        print("UNEquiping")
        if UnEquip(Armor_Item_Layers[j]):
            Wait(1000)  
    return 
    
            
 

def walkStepCheckingGump(direction,gumpID,times):
    SetMoveThroughNPC(True)
    for i in range(times): 
        Step(direction,False)
        if GumpExists(gumpID):
            return
        Wait(18)

# serial do healer de cove 0x8aacf
def ressme():
    if Dead():
        AddToSystemJournal('Ressme!!!')
        if GumpExists(523845830):
            AddToSystemJournal('Murdered')
            #Murder Gump present! Close it
            waitgumpid_press(523845830,1,5)
        currentX = GetX(Self())
        currentY = GetY(Self())
        HelpRequest()
        waitgumpidWithoutUseObject(0xb3423a1d,5)
        waitgumpid_press(0xb3423a1d,2,5)
        waitgumpidWithoutUseObject(0x1e88ca33,5)
        
        if InGump("Delucia"):
            AddToSystemJournal("T2A Ress")
            #T2A - DELUCIA RESS
            waitgumpid_press(0x1e88ca33,2,5) 
            Wait(1000)
            close_gumps()
            while currentX == GetX(Self()) and currentY == GetY(Self()):
                AddToSystemJournal('Char paralyzed. Waiting to be teleported - T2A.')
                Wait(5000)
            AddToSystemJournal('Moving to Healer - T2A.')
            NewMoveXY(5208,3993,True,0,True)
            NewMoveXY(5201,3997,True,0,True)
            walkStepCheckingGump(7,0xb04c9a31,20)
            starttime = datetime.now()
            count = 0
            while not GumpExists(0xb04c9a31):
                count = count + 1
                print("Trying to ress again. try:"+str(count))
                #Gump nao existe.... sair e entrar no healer de novo
                walkStepCheckingGump(3,0xb04c9a31,10)
                #if ((InJournalBetweenTimes("cannot be resurrected", starttime, datetime.now())) > 0): #Healer não aceita ressurect!!! Esperar 5 minutos
                #    print("Healer não aceita ressurect!!! Esperar 5 minutos e tentar de novo")
                #    Wait(300000)
                Wait(5000)
                walkStepCheckingGump(7,0xb04c9a31,10)
                if datetime.now() >= starttime+timedelta(minutes=10):
                        print("SECURITY BREAK RESS!!! COULD NOT RESS AFTER "+str(count)+ "TRIES! QUITING!")
                        SetARStatus(False)
                        Disconnect()
                        exit()
        else:
            AddToSystemJournal("Cove Ress")
            #FEL OR TRAM - COVE RESS
            waitgumpid_press(0x1e88ca33,6,5) 
            Wait(1000)
            close_gumps()
            while currentX == GetX(Self()) and currentY == GetY(Self()):
                AddToSystemJournal('Char paralyzed. Waiting to be teleported.')
                Wait(5000)
            AddToSystemJournal('Moving to Healer.')
            NewMoveXY(2249,1229,True,0,True)
            AddToSystemJournal('Im next to the Healer.')
            walkStepCheckingGump(6,0xb04c9a31,6)
            starttime = datetime.now()
            count = 0
            while not GumpExists(0xb04c9a31):
                count = count + 1
                print("Trying to ress again. try:"+str(count))
                #Gump nao existe.... sair e entrar no healer de novo
                walkStepCheckingGump(2,0xb04c9a31,6)
                #if ((InJournalBetweenTimes("cannot be resurrected", starttime, datetime.now())) > 0): #Healer não aceita ressurect!!! Esperar 5 minutos
                #    print("Healer não aceitou ressurect!!! Esperar 5 minutos e tentar de novo")
                #    Wait(300000)
                Wait(5000)
                walkStepCheckingGump(6,0xb04c9a31,6)
                if datetime.now() >= starttime+timedelta(minutes=10):
                        print("SECURITY BREAK RESS!!! COULD NOT RESS AFTER "+str(count)+ "TRIES! QUITING!")
                        SetARStatus(False)
                        Disconnect()
                        exit()
  
        waitgumpidWithoutUseObject(0xb04c9a31,5)
        waitgumpid_press(0xb04c9a31,1,5)        
        Wait(1000)
        MyDress() 
        Wait(1000)
        healSelf()
        Wait(1000)
        MyDress() 
        Wait(10000)   
        return


# serial do healer de cove 0x8aacf
def healSelf():
    if GetSkillValue('Magery') >= 50: 
        Cast('Greater Heal')
        WaitTargetSelf()   
        Wait(1000)
        Cast('Greater Heal')
        WaitTargetSelf()
        Wait(1000)
        Cast('Greater Heal')
        WaitTargetSelf()
        Wait(1000)  
    elif GetSkillValue('Chivalry') >= 50:
        Cast('Close Wounds')
        WaitTargetSelf()   
        Wait(1000)
        Cast('Close Wounds')
        WaitTargetSelf()
        Wait(1000)
        Cast('Close Wounds')
        WaitTargetSelf()
        Wait(1000)  
    



# ======================================================================================================================
# Other Utils
# ======================================================================================================================



def wait_lag(wait_time=WAIT_TIME, lag_time=WAIT_LAG_TIME):
    Wait(wait_time)
    CheckLag(lag_time)
    return

def debug(message):
    if DEBUG:
        print(message)
        #print(f'{message}')
        ClientPrintEx(Self(), 66, 1, message)

def superDebug(message):
    if SUPER_DEBUG:
        print(message)
        #print(f'{message}')
        ClientPrintEx(Self(), 66, 1, message)

def checkTimeThreshold (starttime,time_limit_in_miliseconds):
    currentTime = datetime.now()
    timeDifference = currentTime - starttime
    differenceInMiliseconds = timeDifference.total_seconds() * 1000
    if differenceInMiliseconds > time_limit_in_miliseconds:
        return True
    return False

def check_weight(itemTypeToDrop, color=0xFFFF, dropX = -1, dropY = 0, qtdToDrop = 7):
    if Weight() > MaxWeight():
        check_connection()
        drop_item(itemTypeToDrop, color, dropX, dropY, qtdToDrop)    
    return

def drop_item(itemType, color, dropX = -1, dropY = 0, qtdToDrop = 7):
    counter = 0
    starttime = datetime.now()
    while True:
        if Dead():
            print("DEAD ON DROPPING ITEM! ABORT!")
            return
        #counter += 1
        FindTypeEx(itemType, color, Backpack(), False)
        if Weight() < MaxWeight():
            break
        wait_lag()
        #if counter == 1:
        Drop(FindItem(), qtdToDrop, GetX(Self()) + dropX, GetY(Self()) + dropY, GetZ(Self()))
        if checkTimeThreshold (starttime,8000):
            print("Security break dropping item")
            break

    return

# ======================================================================================================================
# GUMP Utils
# ======================================================================================================================


def close_gumps():
    
    while IsGump():
        if not Connected():
            return False
        if not IsGumpCanBeClosed(GetGumpsCount() - 1):
            return False
            #WaitGump('0')
        else:
            CloseSimpleGump(GetGumpsCount() - 1)
    return True


def waitgumpid(gumpid, object, timeout=15):
    maxcounter = 0
    UseObject(object)
    while maxcounter < timeout * 10:
        if IsGump():
            for currentgumpnumb in range(0, (GetGumpsCount())):
                currentgump = GetGumpInfo(currentgumpnumb)
                if 'GumpID' in currentgump:  # got to check if key exists or we might get an error
                    if currentgump['GumpID'] == gumpid:
                        return True
                if IsGumpCanBeClosed(currentgumpnumb):
                    CloseSimpleGump(currentgumpnumb)
        maxcounter += 1
        CheckLag(100000)
    return False


def waitgumpidWithoutUseObject(gumpid, timeout=15):
    maxcounter = 0
    while maxcounter < timeout * 10:
        if IsGump():
            for currentgumpnumb in range(0, (GetGumpsCount())):
                currentgump = GetGumpInfo(currentgumpnumb)
                if 'GumpID' in currentgump:  # got to check if key exists or we might get an error
                    if currentgump['GumpID'] == gumpid:
                        return True
                if IsGumpCanBeClosed(currentgumpnumb):
                    CloseSimpleGump(currentgumpnumb)
        maxcounter += 1
        CheckLag(100000)
    return False


def waitgumpid_press(gumpid, number=0, pressbutton=True, timeout=15):
    maxcounter = 0
    while maxcounter < timeout * 10:
        if IsGump():
            for currentgumpnumb in range(0, (GetGumpsCount())):
                currentgump = GetGumpInfo(currentgumpnumb)
                if 'GumpID' in currentgump:  # got to check if key exists or we might get an error
                    if currentgump['GumpID'] == gumpid:
                        if pressbutton:
                            NumGumpButton(currentgumpnumb, number)
                        else:
                            return currentgump
                        return True
                if IsGumpCanBeClosed(currentgumpnumb):
                    CloseSimpleGump(currentgumpnumb)
        maxcounter += 1
        CheckLag(100000)
    return False


def waitgumpid_checkbox(gumpid, number=0, pressbutton=True, value=0, timeout=15):
    maxcounter = 0
    #print ("entrou")
    while maxcounter < timeout * 10:
        #print ("entrou whuike")
        if IsGump():
            for currentgumpnumb in range(0, (GetGumpsCount())):
                #print ("entrou for")
                currentgump = GetGumpInfo(currentgumpnumb)
                if 'GumpID' in currentgump:  # got to check if key exists or we might get an error
                    #print ("if gump id")
                    if currentgump['GumpID'] == gumpid:
                        #print ("id = id")
                        if pressbutton:
                            #print ("press button")
                            NumGumpCheckBox(currentgumpnumb, number, value)
                        else:
                            return currentgump
                        return True
                if IsGumpCanBeClosed(currentgumpnumb):
                    CloseSimpleGump(currentgumpnumb)
        maxcounter += 1
        CheckLag(100000)
    return False

def waitgumpid_textentry(gumpid, textEntryId=0, value='', timeout=15):
    maxcounter = 0
    while maxcounter < timeout * 10:
        if IsGump():
            for currentgumpnumb in range(0, (GetGumpsCount())):
                currentgump = GetGumpInfo(currentgumpnumb)
                if 'GumpID' in currentgump:  # got to check if key exists or we might get an error
                    if currentgump['GumpID'] == gumpid:
                        print("ACHOU TEXT ENTRIE!")
                        NumGumpTextEntry(currentgumpnumb, textEntryId, value)
                        return True
                if IsGumpCanBeClosed(currentgumpnumb):
                    CloseSimpleGump(currentgumpnumb)
        maxcounter += 1
        CheckLag(100000)
    return False


def GumpExists(gumpid):
    for i in range(GetGumpsCount()):  
        if gumpid and gumpid == GetGumpID(i):
            return True
    return False     


def InGump(text, value=999):
    found = None
    t = 1
    while (found == None):
        #print ("while")
        for i in range(GetGumpsCount()):
            infogump = GetGumpInfo(i)
            #print ("for")
            index = i
            if not found and len(infogump['XmfHtmlGump']) > 0:
                #for j in infogump['XmfHtmlGump']:
                #    GetClilocByID(x['ClilocID']).upper()
                #print("HTML")
                found = next((GetClilocByID(x['ClilocID']).upper() for x in infogump['XmfHtmlGump'] if
                              text.upper() in GetClilocByID(x['ClilocID']).upper()), None)
                break
            if not found and len(infogump['XmfHTMLGumpColor']) > 0:
                #print("HTML color")
                found = next((GetClilocByID(x['ClilocID']).upper() for x in infogump['XmfHTMLGumpColor'] if
                              text.upper() in GetClilocByID(x['ClilocID']).upper()), None)
                break
            elif not found and len(infogump['Text']) > 0:
                #print("text")
                found = next((x[0].upper() for x in infogump['Text'] if text.upper() in x[0].upper()), None)
                break
        Wait(100)
        t += 1
        if t > 10:
            return found
        CheckLag()
    if value != 999:
        NumGumpButton(GetGumpsCount() - 1, value)
    return found

# ======================================================================================================================
# Recalling
# ======================================================================================================================


# Usage: runebook("runebook name", "recall/gate/charges", rune number)
def runebook(runebook_name, travel_method, rune_number, wait_time = 4000):
    usingregs = list((range(-1, 100, 6)))  # 5, 11, 17, 23, 29, 35, 41, 47, 53, 59, 65, 71, 77, 83, 89, 95
    usingcharges = list((range(-4, 98, 6)))  # 2, 8, 14, 20, 26, 32, 38, 44, 50, 56, 62, 68, 74, 80, 86, 92
    usinggate = list(range(0, 102, 6))  # 6, 12, 18, 24, 30, 36, 42, 48, 54, 60, 66, 72, 78, 84, 90, 96
    usingchiva = list(range(1, 103, 6))  #
    if Dead():
        print("DEAD ON RECALL! ABORT!")
        return
    check_mana()
    retry = 0
    x, y = GetX(Self()), GetY(Self())
    while GetX(Self()) == x and GetY(Self()) == y:
        retry += 1
        if Weight() >= MaxWeight() + 3:
            print("OVERWEIGTH ON RECALL LOOP! ABORT!")
            return
        if Dead():
            print("DEAD ON RECALL! ABORT!")
            return
        if retry > 1:
            debug("Travel retry -> " + str(retry) + "x")
        if retry > 10:
            debug("Travel EXITING -> Too many")
            return False

        if GetX(Self()) != x and GetY(Self()) != y:
            return True
        if open_rb(runebook_name):
            if travel_method == "chiva":
                debug("Traveling (chiv) -> "+str(runebook_name)+" -> "+str(rune_number))
                waitgumpid_press(1431013363, usingchiva[rune_number], True)
                #Wait(2000)
                starttime = datetime.now()
                while (not checkTimeThreshold(starttime,wait_time)):
                    Wait(10)
                    if GetX(Self()) != x and GetY(Self()) != y:
                        debug("Recalled! (chiv)")
                        Wait(50)
                        return True
            elif travel_method == "recall":
                debug("Traveling (recall) -> "+str(runebook_name)+" -> "+str(rune_number))
                waitgumpid_press(1431013363, usingregs[rune_number], True)
                #Wait(4000)
                starttime = datetime.now()
                while (not checkTimeThreshold(starttime,wait_time)):
                    Wait(10)
                    if GetX(Self()) != x and GetY(Self()) != y:
                        debug("Recalled! (recall)")
                        Wait(50)
                        return True
            elif travel_method == "gate":
                debug("Traveling (gate) -> "+str(runebook_name)+" -> "+str(rune_number))
                waitgumpid_press(1431013363, usinggate[rune_number], True)
                #Wait(4500)
                Wait(wait_time)
                if FindType(0x0F6C, Ground()):  # gate
                    UseObject(FindItem())
                    waitgumpid_press(3899019871, 2)
            elif travel_method == "charge":
                debug("Traveling (charge) -> "+str(runebook_name)+" -> "+str(rune_number))
                runebook_gump = waitgumpid_press(1431013363, usingcharges[rune_number], False)
                if runebook_gump:
                    if 'Text' in runebook_gump:
                        if int(runebook_gump["Text"][0][0]) > 1:  # checking if we got charges
                            waitgumpid_press(1431013363, usingcharges[rune_number])
                            starttime = datetime.now()
                            while (not checkTimeThreshold(starttime,wait_time)):
                                Wait(10)
                                if GetX(Self()) != x and GetY(Self()) != y:
                                    Wait(50)
                                    return True
                        else:
                            return False  # less than minimum charges
            else:
                debug("Travel method -> False")
                return False  # invalid travel method
    return True


def open_rb(name):
    if FindType(0x22C5, Backpack()):
        founds = GetFindedList()
        for found in founds:
            splitedToolTip = GetTooltip(found).rsplit('|', 1)
            if (len(splitedToolTip) > 0):
                if splitedToolTip[1] in (name):
                    while not waitgumpid(1431013363, found):
                        Wait(100)
                    return True
    else:
        debug("Runebook -> Not found. Trying to open backpack...")
        Wait(10000)
        UseObject(Backpack())
        return False
    return False


# ======================================================================================================================
# Discord Utils
# ======================================================================================================================
 

def send_discord_message(webhook_url, message):
    webhook = DiscordWebhook(url=webhook_url, content=str(message))
    webhook.execute()
    return 


'''def send_discord_message(webhook_url, message, username = "Freddy Krueger", messageColor = "16411130", avatarURL = "https://vignette.wikia.nocookie.net/dcheroesrpg/images/b/b2/Freddy_Krueger.jpg"):
    jsonPayload = {}
    jsonPayload['username'] = username
    jsonPayload['avatar_url'] = avatarURL
    
    jsonPayload['embeds'] =  []
    embeds = {}
    embeds['description'] = message
    embeds['color'] = messageColor
    jsonPayload['embeds'].append(embeds)

    payload = json.dumps(jsonPayload)

    headers = {
        'Content-Type': 'application/json',
    }
    response = requests.request("POST", webhook_url, headers=headers, data = payload)
    print(response.text.encode('utf8'))'''

def send_discord_message_multi_lines(webhook_url, arrayOfMessages, username = "Freddy Krueger", messageColor = "16411130", avatarURL = "https://vignette.wikia.nocookie.net/dcheroesrpg/images/b/b2/Freddy_Krueger.jpg"):
    jsonPayload = {}
    jsonPayload['username'] = username
    jsonPayload['avatar_url'] = avatarURL
    
    jsonPayload['embeds'] =  []
    for message in arrayOfMessages:
        embeds = {}
        embeds['description'] = message
        embeds['color'] = messageColor
        jsonPayload['embeds'].append(embeds)

    payload = json.dumps(jsonPayload)
    
    headers = {
        'Content-Type': 'application/json',
    }
    response = requests.request("POST", webhook_url, headers=headers, data = payload)
    print(response.text.encode('utf8'))


# ======================================================================================================================
# GM check Utils
# ======================================================================================================================



def CheckAFK(charFunction = ""):
    checkGMGump(charFunction)
    checkIfInJail(charFunction)
        #while GumpExists(afk_gump):  
        #    msg_disco(ProfileName() + ' * AFK GUMP *')  
        #    Wait(30000)           
        


def checkGMGump(charFunction = ""):
    global GMGumpFound
    if IsGump():
        print("IsGump")
        if GetGumpsCount() > 0:
            id = GetGumpID(GetGumpsCount()-1)
            if id == AFK_GUMP:
                try:
                    PlayWav(WAV_AFK)
                except:
                    pass
                if GMGumpFound is not True:
                    print("Found GUMP")
                    print ("######FOUND AFK CHECK GUMP ID#########")
                    send_discord_message(DISCORD_WEBHOOK,"******** (GUMP) @everyone ALERTA!!!! GM RODANDO! GUMP DE AFK DETECTADO!! Char: "+ str(CharName()) +". "+str(charFunction)+" ********")
                    GMGumpFound = True

                superDebug("Gumps Count:" + str(GetGumpsCount()))
                #id = GetGumpID(GetGumpsCount()-1)
                superDebug("Gump Id:" + str(id))
                #gumpFullInfo = GetGumpFullInfo(GetGumpsCount()-1)
                gumpInfo = GetGumpInfo(GetGumpsCount()-1)
                #with open('gump-debug.txt','w') as file:
                debugGumpFile = open(StealthPath()+GUMP_DEBUG_FILE, 'a+')
                #print(gumpInfo)
                debugGumpFile.writelines('\n\n\n---------------GUMP FOUND! Char:'+ str(CharName()) +'----------------')
                debugGumpFile.writelines('\n-------'+str(datetime.now())+'-------\n')
                json.dump(gumpInfo, debugGumpFile)
                
                gumpFullLines = GetGumpFullLines(GetGumpsCount()-1)
                print(gumpFullLines)
                debugGumpFile.writelines('\n-------FULL LINES-------\n')
                json.dump(gumpFullLines, debugGumpFile)
                for gump in range(GetGumpsCount()-1):
                    idd = GetGumpID(gump)
                    
                    debugGumpFile.writelines('\n-------ID - for-------\n')
                    gumpInfo = GetGumpInfo(idd)
                    json.dump(gumpInfo, debugGumpFile)

                    gumpFullLines = GetGumpFullLines(idd)
                    debugGumpFile.writelines('\n-------FULL LINES - for-------\n')
                    json.dump(gumpFullLines, debugGumpFile)

                debugGumpFile.close()
            if id == AFK_GUMP:
               

                if GMGumpFound is not True:
                    #TRYING TO PRESS CHECKBOX
                    print ("PRESSING CHECKBOX")
                    Wait (5000) #waiting 5 seconds just to pretend
                    button = gumpInfo['GumpButtons'][0]['ReturnValue']
                    waitgumpid_press(id, int(button), True, 5)
                    #Wait (600000) # Wait for 10 Minutes
            else:
                close_gumps()







def checkIfInJail(charFunction = ""):
    currentX = GetX(Self())
    currentY = GetY(Self())
    global InJail

    if (currentX >= JAIL_X_TOP_LEFT) and (currentX <= JAIL_X_BOTTOM_RIGHT):
        if (currentY >= JAIL_Y_TOP_LEFT) and (currentY <= JAIL_Y_BOTTOM_RIGHT):
            if InJail is not True:
                try:
                    PlayWav(WAV_AFK)
                except:
                    pass
                print("########IN JAIL!!!########")
                send_discord_message(DISCORD_WEBHOOK,"******** (JAIL) @everyone ALERTA!!! GM RODANDO! CHAR NA JAIL!!!!!! Char: "+ str(CharName()) +". "+str(charFunction)+" ********")
                InJail = True
