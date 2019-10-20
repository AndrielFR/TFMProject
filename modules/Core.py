# coding: utf-8
import re
import os
import sys
import time
import time as _time
import configparser
import sqlite3
import random
import traceback
import asyncore
import socket
import threading
import urllib
import ftplib

# Compiler Files
sys.dont_write_bytecode = True

# Modules
from modules.ByteArray import ByteArray
from modules.Cheat import AntiCheat
from modules.DailyQuest import DailyQuest
from modules.Identifiers import Identifiers
from modules.Minigames import Utility
from modules.Minigames import PokeLua
from modules.Minigames import UnoTFM2
from modules.minigames.MiniGame import MiniGame
from modules.minigames.DeathMatch import DeathMatch
from modules.minigames.FFARace import FFARace
from modules.minigames.UnoTFM import UnoTFM
from modules.ModoPwet import ModoPwet
from modules.Others import config
from modules.Others import ranking
from modules.Others import email
from modules.Others import radios
from modules.Others import DownloadCenter
from modules.ParseCommands import ParseCommands
from modules.ParsePackets import ParsePackets
from modules.ShopModule import ShopModule
from modules.SkillModule import SkillModule
from modules.Tribulle import Tribulle

# Utils
from utils.TFMUtils import TFMUtils
from utils.Cryptography import Cryptography

# Library
import xml.etree.cElementTree as ET

from PIL import Image
from PIL import ImageOps
from codecs import encode
from datetime import date
from datetime import datetime
from datetime import timedelta

# Lua
try:
    from lupa import LuaRuntime
except Exception as err:
    print("[API Error] " + str(err))


class Client(asyncore.dispatcher):

    def __init__(this, socket):
        asyncore.dispatcher.__init__(this, socket)
        this.recvd = b""

        # String
        this.Username = ""
        this.Langue = "EN"
        this.realLangue = "EN"
        this.createLangue = "EN"
        this.MouseColor = "78583a"
        this.ShamanColor = "95d9d6"
        this.NameColor = ""
        this.roomName = ""
        this.shopItems = ""
        this.shamanItems = ""
        this.playerLook = "1;0,0,0,0,0,0,0,0,0"
        this.shamanLook = "0,0,0,0,0,0,0,0,0,0"
        this.lastMessage = ""
        this.modoPwetLangue = "ALL"
        this.silenceMessage = ""
        this.marriage = ""
        this.tribeName = ""
        this.tradeName = ""
        this.tempMouseColor = ""
        this.mouseName = ""
        this.botVillage = ""
        this.isIPban = "NotChecked"
        this.currentCaptcha = ""
        this.musicNameLink = ""
        this.emailAddress = ""
        this.codeEmailConfirmation = ""
        this.tribeMessage = ""
        this.tribeRanks = ""
        this.tribeInfo = ""
        this.dailyReward = ""

        # Integer
        this.gameEmail = 0
        this.gameAvatar = 0
        this.gameUsername = 0
        this.gamePassword = 0
        this.changepw = 0
        this.changeuser = 0
        this.TimeGiro = 0
        this.lastDataID = 0
        this.authKey = random.randint(1, 2147483647)
        this.authKeyLogin = random.randint(1, 39238)
        this.langueByte = 0
        this.playerScore = 0
        this.playerCode = 0
        this.privLevel = 0
        this.realLevel = 0
        this.playerID = 0
        this.TitleNumber = 0
        this.TitleStars = 0
        this.posX = 0
        this.posY = 0
        this.velX = 0
        this.velY = 0
        this.firstCount = 0
        this.cheeseCount = 0
        this.shamanCheeses = 0
        this.shopCheeses = 100
        this.shopFraises = 0
        this.shamanSaves = 0
        this.hardModeSaves = 0
        this.divineModeSaves = 0
        this.bootcampCount = 0
        this.shamanType = 0
        this.regDate = 0
        this.banHours = 0
        this.shamanLevel = 1
        this.shamanExp = 0
        this.shamanExpNext = 32
        this.ambulanceCount = 0
        this.bubblesCount = 0
        this.lastOn = 0
        this.silenceType = 0
        this.gender = 0
        this.lastDivorceTimer = 0
        this.tribeCode = 0
        this.tribeRank = 0
        this.tribeJoined = 0
        this.tribePoints = 0
        this.defilantePoints = 0
        this.iceCount = 2
        this.lastGameMode = 0
        this.nowCoins = 0
        this.nowTokens = 0
        this.currentPlace = 0
        this.equipedShamanBadge = 0
        this.pet = 0
        this.petEnd = 0
        this.numGiveCheese = 0
        this.racingRounds = 0
        this.bootcampRounds = 0
        this.defilanteRounds = 0
        this.deathRounds = 0
        this.survivorDeath = 0
        this.priceDoneVisu = 0
        this.playerStartTimeMillis = 0
        this.dac = 0
        this.aventureSaves = 0
        this.countP = 0
        this.musicOn = 0
        this.emailConfirm = 0
        this.tribeChat = 0
        this.tribeHouse = 0
        this.tribulleID = 0
        this.page = 1
        this.invocationPoints = 0
        this.explosionPoints = 0
        this.ballonracePoints = 0
        this.flyPoints = 0
        this.viewMessage = 0
        this.musicName = 0
        this.prophuntShamanLife = 3
        this.ping = 0
        this.pingTime = 0
        this.karma = 0
        this.lastReportID = 0

        # Bool
        this.isClosed = False
        this.validatingVersion = False
        this.isGuest = False
        this.isReceivedDummy = False
        this.isDead = False
        this.hasCheese = False
        this.hasEnter = False
        this.isMoving = False
        this.isMovingRight = False
        this.isMovingLeft = False
        this.isJumping = False
        this.isShaman = False
        this.isSuspect = False
        this.isAfk = False
        this.isVoted = False
        this.qualifiedVoted = False
        this.isMute = False
        this.RTotem = False
        this.UTotem = False
        this.LoadCountTotem = False
        this.modoPwet = False
        this.canResSkill = False
        this.canShamanRespawn = False
        this.isOpportunist = False
        this.desintegration = False
        this.sendMusic = True
        this.isCafe = False
        this.canSkipMusic = False
        this.isHidden = False
        this.isTeleport = False
        this.isFly = False
        this.isExplosion = False
        this.isFFA = False
        this.canSpawnCN = False
        this.presElection = False
        this.prefElection = False
        this.electionFirst = False
        this.isSpeed = False
        this.isEvent = False
        this.isNewPlayer = False
        this.isVampire = False
        this.isLuaAdmin = False
        this.isTrade = False
        this.tradeConfirm = False
        this.canUseConsumable = True
        this.canRespawn = False
        this.isSkill = False
        this.showButtons = True
        this.mondayEventx = False
        this.tuesdayEventx = False
        this.wednesdayEventx = False
        this.thursdayEventx = False
        this.fridayEventx = False
        this.saturdayEventx = False
        this.sundayEventDayx = False
        this.hasBolo = False
        this.hasBolo2 = False
        this.isBanned = False
        this.giftGet = False
        this.isddrevent = False
        this.isEnterRoom = False
        this.isTribeOpen = False
        this.openingFriendList = False
        this.missionGain = False
        this.canCN = False
        this.isSync = False
        this.isTribunal = False
        this.isConnected = False

        # Others
        this.Cursor = Cursor

        # Nonetype
        this.room = None
        this.resSkillsTimer = None
        this.consumablesTimer = None
        this.skipMusicTimer = None

        # List
        this.STotem = [0, ""]
        this.Totem = [0, ""]
        this.PInfo = [0, 0, 100]
        this.survivorStats = [0] * 4
        this.racingStats = [0] * 4
        this.marriageInvite = []
        this.tribeData = ["", "", 0, None]
        this.tribeInvite = []
        this.mulodromePos = []
        this.canLogin = [False, False]
        this.cheeseTitleList = []
        this.firstTitleList = []
        this.shamanTitleList = []
        this.shopTitleList = []
        this.bootcampTitleList = []
        this.hardModeTitleList = []
        this.divineModeTitleList = []
        this.specialTitleList = []
        this.titleList = []
        this.clothes = []
        this.shopBadges = []
        this.friendsList = []
        this.ignoredsList = []
        this.ignoredMarriageInvites = []
        this.ignoredTribeInvites = []
        this.chats = []
        this.voteBan = []
        this.shamanBadges = []
        this.equipedConsumables = []
        this.custom = []
        this.dailyQuest = [0, 0, 0, 1, 1]
        this.deathStats = []
        this.prophuntImage = [None, None, None, None, None, None]

        # Dict
        this._MapDefinitions = dict()
        this.playerSkills = {}
        this.playerConsumables = {}
        this.tradeConsumables = {}
        this.itensBots = {"Papaille": [(4, 800, 50, 4, 2253, 50), (4, 800, 50, 4, 2254, 50),
                                       (4, 800, 50, 4, 2257, 50), (4,
                                                                   800, 50, 4, 2260, 50),
                                       (4, 800, 50, 4, 2261, 50)], "Buffy": [(1, 147, 1, 4, 2254, 200),
                                                                             (2, 17, 1, 4, 2254, 150), (
                                                                                 2, 18, 1, 4, 2254, 150),
                                                                             (2, 19, 1, 4, 2254, 150), (
                                                                                 3, 398, 1, 4, 2254, 150),
                                                                             (3, 392, 1, 4, 2254, 50)], "Indiana Mouse": [(3, 255, 1, 4, 2257, 50),
                                                                                                                          (3, 394, 1, 4, 2257, 50), (3,
                                                                                                                                                     395, 1, 4, 2257, 50),
                                                                                                                          (3, 320, 1, 4, 2257, 50), (3,
                                                                                                                                                     393, 1, 4, 2257, 50),
                                                                                                                          (3, 402, 1, 4, 2257, 50), (
                                                                                                                              3, 397, 1, 4, 2257, 50),
                                                                                                                          (3, 341, 1, 4, 2257, 50), (
                                                                                                                              3, 335, 1, 4, 2257, 25),
                                                                                                                          (3, 403, 1, 4, 2257, 50), (
                                                                                                                              1, 6, 1, 4, 2257, 50),
                                                                                                                          (1, 17, 1, 4, 2257, 50)], "Elise": [(4, 31, 2, 4, 2261, 5),
                                                                                                                                                              (4, 2256, 2, 4, 2261, 5), (4,
                                                                                                                                                                                         2232, 2, 4, 2253, 1),
                                                                                                                                                              (4, 21, 5, 4, 2253, 1), (4,
                                                                                                                                                                                       33, 2, 4, 2260, 1),
                                                                                                                                                              (4, 33, 2, 4, 2254, 1)], "Oracle": [(1, 145, 1, 4, 2253, 200),
                                                                                                                                                                                                  (2, 16, 1, 4, 2253, 150), (2,
                                                                                                                                                                                                                             21, 1, 4, 2253, 150),
                                                                                                                                                                                                  (2, 24, 1, 4, 2253, 150), (2,
                                                                                                                                                                                                                             20, 1, 4, 2253, 150),
                                                                                                                                                                                                  (3, 390, 1, 4, 2253, 50), (
                                                                                                                                                                  3, 391, 1, 4, 2253, 200),
            (3, 399, 1, 4, 2253, 150)], "Prof": [(4, 800, 20, 4, 2257, 10),
                                                 (4, 19, 2, 4, 2257, 5), (4,
                                                                          2258, 2, 4, 2257, 4),
                                                 (4, 2262, 5, 4, 2257, 2), (4,
                                                                            2259, 10, 4, 2257, 1),
                                                 (4, 20, 1, 4, 2257, 2)], "Cassidy": [(1, 154, 1, 4, 2261, 200),
                                                                                      (2, 23, 1, 4, 2261, 150), (3, 400, 1, 4, 2261, 100)],
            "Von Drekkemouse": [(2, 22, 1, 4, 2260, 150),
                                (1, 153, 1, 4, 2260, 200), (3, 401, 1, 4, 2260, 100)],
            "Tod": [(4, 2259, 10, 4, 2257, 1), (4, 2258, 10, 4, 2254, 230),
                    (3, 401, 1, 4, 2260, 100)], "Fishing2017": [(1, 184, 1, 4, 2257, 200),
                                                                (2, 24, 1, 4, 2257, 150), (
                        2, 29, 1, 4, 2257, 150),
            (3, 422, 1, 4, 2257, 200)], "Noel": [(4, 2102, 5, 4, 2100, 15), (4, 2102, 10, 4, 2100, 25),
                                                                                                                                             (4, 2102, 50, 4, 2100, 150), (
                4, 2102, 100, 4, 2100, 250),
            (4, 1, 20, 4, 2100, 15), (
                4, 2, 20, 4, 2100, 15),
            (4, 3, 20, 4, 2100, 15), (4, 4, 20, 4, 2100, 15),
            (4, 5, 20, 4, 2100, 15), (4, 6, 20, 4, 2100, 15),
            (4, 7, 20, 4, 2100, 15), (4, 8, 20, 4, 2100, 15),
            (4, 9, 20, 4, 2100, 15)]}
        this.aventureCounts = {}
        this.aventurePoints = {}
        this.timeConnected = {"login": 0, "logoff": 0, "total": 0}
        this.banforMessage = {}

        # Time
        this.CMDTime = time.time()
        this.CAPTime = time.time()
        this.CTBTime = time.time()
        this.loginTime = time.time()
        this.createTime = time.time()

        # Others
        day = date.today()
        days = ('seg', 'ter', 'qua', 'quin', 'sex', 'sab', 'dom')
        dds = str(days[day.weekday()])
        this.ddhj = dds

    def handle_read(this):
        try:
            data = this.recv(0xFFFF)
        except:
            return None
        if data == b'<policy-file-request/>\x00':
            this.write(
                "<cross-domain-policy><allow-access-from domain=\"*\" to-ports=\"*\" /></cross-domain-policy>")
            this.loseConnection()
            return
        elif data == None or len(data) < 2:
            return
        elif not data or data in ["", " ", "\x00", "\x01"]:
            this.server.tempIPBanList.append(this.ipAddress)
            #this.server.sendStaffMessage(10, "[<V>ANT-DDOS</V>] BLOCKED ATTACK! IP: [<R>"+str(this.ipAddress)+"</R>]")
            this.isIPban = True
            this.isBanned = True
            this.isClosed = True
            this.protectFirewall()
            this.server.disconnectIPAddress(this.ipAddress)
            del this.server.connectedCounts[this.ipAddress]
            this.loseConnection()
            return
        elif this.isBanned:
            this.server.tempIPBanList.append(this.ipAddress)
            this.isIPban = True
            this.isBanned = True
            this.isClosed = True
            # this.server.disconnectIPAddress(this.ipAddress)
            # this.loseConnection()
        elif this.isClosed:
            return

        d = ByteArray(data)
        this.recvd += data
        sizeBytes = d.readByte()
        if sizeBytes == 1:
            length = d.readByte()
        elif sizeBytes == 2:
            length = d.readShort()
        elif sizeBytes == 3:
            length = ((d.readByte() & 0xFF) << 16) | ((d.readByte() & 0xFF) << 8) | (d.readByte() & 0xFF)
        else:
            length = 0
        if length > 0:
            dataID = d.readByte()
            if d.getLength() == length:
                # if dataID != this.lastDataID:
                    # return
                this.lastDataID = (dataID + 1) % 100
                C, CC = d.readByte(), d.readByte()
                try:
                    this.parseString(C, CC, d, dataID)
                except Exception as ERROR:
                    c = open("./include/logs/SErrors.log", "a")
                    c.write("\n" + "=" * 40 + "\n- Time: %s\n- Player: %s\n- IP: %s\n- Error: \n" %
                            (time.strftime("%d/%m/%Y - %H:%M:%S"), this.Username, this.ipAddress))
                    traceback.print_exc(file=c)
                    c.close()

    def write(this, data: object):
        if isinstance(data, str):
            this.send(data.encode())
        else:
            this.send(data)

    def loseConnection(this):
        this.close()

    def protectFirewall(this):
        os.system("netsh advfirewall firewall add rule name='DDOS Attack Blocked' dir=in interface=any action=block remoteip=" + str(this.ipAddress))

    def handle_close(this):
        this.isClosed = True
        for timer in [this.resSkillsTimer, this.consumablesTimer, this.skipMusicTimer]:
            if timer != None:
                timer.cancel()

        if this.ipAddress in this.server.connectedCounts.keys():
            count = this.server.connectedCounts[this.ipAddress] - 1
            if count <= 0:
                del this.server.connectedCounts[this.ipAddress]
            else:
                this.server.connectedCounts[this.ipAddress] = count

        if this.langueByte == 3:
            this.server.serverBR -= 1
        elif this.langueByte == 4:
            this.server.serverES -= 1
        else:
            this.server.serverEN -= 1

        if not this.Username == "":
            if not this.isGuest:
                this.timeConnected["logoff"] = this.TFMUtils.getTime()
                result = this.timeConnected[
                    "logoff"] - this.timeConnected["login"]
                this.timeConnected["total"] += result
                this.updateDatabase()

            if this.isTrade:
                this.cancelTrade(this.tradeName)

            if this.Username in this.server.players.keys():
                del this.server.players[this.Username]

            if this.Username in this.server.reports:
                if not this.server.reports[this.Username]["status"] == "banned":
                    this.server.reports[this.Username][
                        "status"] = "disconnected"
                    this.ModoPwet.updateModoPwet()

            if this.Username in this.server.chatMessages.keys():
                this.server.chatMessages[this.Username] = {}
                del this.server.chatMessages[this.Username]

            if this.privLevel >= 5:
                this.server.sendStaffMessage(10, "<ROSE>[" + ("PRG" if this.privLevel == 12 else "FUND" if this.privLevel == 11 else "ADM" if this.privLevel == 10 else "COORD" if this.privLevel == 9 else "SMOD" if this.privLevel ==
                                                              8 else "MOD" if this.privLevel == 7 else "MC" if this.privLevel == 6 else "HP" if this.privLevel == 5 else "FC" if this.privLevel == 4 else "LD" if this.privLevel == 3 else "") + "] <CH>" + this.Username + "<N> desconectou-se.")

            this.lastOn = this.tribulle.getTime()
            this.tribulle.friendChanged = True

        if this.room != None:
            this.room.removeClient(this)
        this.loseConnection()

    def sendPacket(this, identifiers, data=""):
        if not this.isClosed:
            d = ByteArray().writeByte(identifiers[0]).writeByte(identifiers[1]).writeBytes(ByteArray(data).toByteArray()) if type(
                data) != list else ByteArray().writeByte(1).writeByte(1).writeUTF("\x01".join(["".join(map(chr, identifiers)), "\x01".join(map(str, data))]))
            this.write((ByteArray().writeByte(1).writeByte(d.getLength()) if d.getLength() <= 0xFF else ByteArray().writeByte(2).writeShort(d.getLength()) if d.getLength() <= 0xFFFF else ByteArray().writeByte(
                3).writeByte((p.getLength() >> 16) & 0xFF).writeByte((p.getLength() >> 8) & 0xFF).writeByte(p.getLength() & 0xFF) if d.getLength() <= 0xFFFFFF else 0).writeBytes(d.toByteArray()).toByteArray())

    def parseString(this, C, CC, data, dataID):
        if not this.validatingVersion:
            if C == Identifiers.recv.Informations.C and CC == Identifiers.recv.Informations.Correct_Version and not this.isClosed:
                version = data.readShort()
                ckey = data.readUTF()
                flashType = data.readUTF()
                utiliSateur = data.readUTF()
                winID = data.readInt()
                pcSTR = data.readUTF()
                serverSTR = data.readUTF()
                computerSTR = data.readUTF()
                idGain = data.readInt()
                lip = data.readInt()
                x = data.readUTF()

                if not str(ckey) == str(this.server.CKEY) or not int(version) == int(this.server.Version):
                    this.loseConnection()
                    if not str(this.server.CKEY) == str(ckey):
                        print("Incorrect ckey: " + str(this.server.CKEY) +
                              " | Correct ckey: " + str(ckey))
                    if not int(this.server.Version) == int(version):
                        print("Incorrect version: 1." + str(this.server.Version) +
                              " | Correct version: 1." + str(version))
                else:
                    this.lastDataID = random.randint(0, 99)
                    this.validatingVersion = True
                    this.sendCorrectVersion()
                    this.sendPing()
        else:
            if data == "" or data == " ":
                this.server.tempIPBanList.append(this.ipAddress)
                this.loseConnection()
            else:
                if C != 0 and CC != 0:
                    this.AntiCheat.readData(C + CC, str(data))
                    #print("\nC: " + str(C) + ", CC: " + str(CC))
                    this.parsePackets.parsePacket(C, CC, data, dataID)
                    #print("data ID: "+str(dataID)+", C: "+str(C)+", CC: "+str(CC)+str(", data: "+repr(ByteArray(data[3:]).toByteArray())))

    def sendPing(this):
        this.pingTime = round(_time.time() * 1000)
        TFMUtils.callLater(10, this.sendPing)

    def sendAddPopupText(this, id, x, y, l, a, fur1, fur2, opcit, Message):
        bg = int(fur1, 16)
        bd = int(fur2, 16)
        data = struct.pack("!i", id)
        data = data + struct.pack("!h", len(Message))
        data = data + Message + \
            struct.pack("!hhhhiibb", int(x), int(y), int(
                l), int(a), int(bg), int(bd), int(opcit), 0)
        this.sendPacket([29, 20], data)

    def loginPlayer(this, identification, password, startRoom):
        if "@" in identification:
            this.Cursor.execute(
                "select * from Users where Email = ? and Password = ?", [identification, password])
            names = []
            for rs in this.Cursor.fetchall():
                names.append(rs["Username"].split("#")[0] if rs[
                             "Username"].endswith("#0000") else rs["Username"])
            names = "¤".join(map(str, names))
            if "¤" in names:
                this.sendPacket(Identifiers.send.Login_Result, ByteArray().writeByte(
                    11).writeUTF(names).writeUTF("").toByteArray())
                return
        loginTime = _time.time() - this.loginTime
        if loginTime < 3:
            this.server.sendStaffMessage(
                7, "[<V>ANT-BOT</V>][<J>%s</J>] Player was bot suspect by login time." % (abs(loginTime)))
            this.loseConnection()
            return
        playerName = "Souris" if identification == "" else (
            identification + "#0000" if not "@" in identification and not "#" in identification else identification)
        if password == "":
            playerName = this.server.checkAlreadyExistingGuest("*" + (playerName[0].isdigit() or len(
                playerName) > 12 or len(playerName) < 3 or "Souris" if "+" in playerName else playerName))
            startRoom = "\x03[Tutorial] %s" % (playerName)
            this.isGuest = True

        if not this.canLogin[0] and not this.canLogin[1] or this.ipAddress in this.server.tempIPBanList:
            this.loseConnection()
            return

        if not this.isGuest and playerName in this.server.userPermaBanCache:
            this.sendPacket(Identifiers.old.send.Player_Ban_Login, [
                            this.server.getPermBanInfo(playerName)])
            this.loseConnection()
            return

        if not this.isGuest:
            banInfo = this.server.getTempBanInfo(playerName)
            timeCalc = TFMUtils.getHoursDiff(int(banInfo[0]))
            if timeCalc <= 0:
                this.server.removeTempBan(playerName)
            else:
                this.sendPacket(Identifiers.old.send.Player_Ban_Login, [
                                timeCalc, str(banInfo[1])])
                this.loseConnection()
                return

        if this.server.checkConnectedAccount(playerName):
            this.sendPacket(Identifiers.send.Login_Result, ByteArray().writeByte(
                1).writeUTF(playerName).writeUTF("").toByteArray())
        else:
            vipTime, letters, gifts, messages = 0, "", "", ""
            if not this.isGuest and not playerName == "":
                this.Cursor.execute("select * from Users where " + (
                    "Email" if "@" in playerName else "Username") + " = ? and Password = ?", [playerName, password])
                rs = this.Cursor.fetchone()
                if rs:
                    playerName = rs["Username"]
                    this.playerID = rs["PlayerID"]
                    this.realLevel = rs["PrivLevel"]
                    this.createLangue = rs["Langue"]
                    this.emailAddress = rs["Email"]
                    this.TitleNumber = rs["TitleNumber"]
                    this.karma = rs["Karma"]
                    this.firstCount = rs["FirstCount"]
                    this.cheeseCount = rs["CheeseCount"]
                    this.shamanCheeses = rs["ShamanCheeses"]
                    this.shopCheeses = rs["ShopCheeses"]
                    this.shopFraises = rs["ShopFraises"]
                    this.shamanSaves = rs["ShamanSaves"]
                    this.hardModeSaves = rs["HardModeSaves"]
                    this.divineModeSaves = rs["DivineModeSaves"]
                    this.bootcampCount = rs["BootcampCount"]
                    this.shamanType = rs["ShamanType"]
                    this.shopItems = rs["ShopItems"]
                    this.shamanItems = rs["ShamanItems"]
                    this.clothes = list(map(str, filter(
                        None, rs["Clothes"].split("|"))))
                    this.playerLook = rs["Look"]
                    this.shamanLook = rs["ShamanLook"]
                    this.MouseColor = rs["MouseColor"]
                    this.ShamanColor = rs["ShamanColor"]
                    this.NameColor = rs["NameColor"]
                    this.regDate = rs["RegDate"]
                    this.shopBadges = list(map(str, filter(
                        None, rs["Badges"].split(","))))
                    this.cheeseTitleList = list(map(float, filter(
                        None, rs["CheeseTitleList"].split(","))))
                    this.firstTitleList = list(map(float, filter(
                        None, rs["FirstTitleList"].split(","))))
                    this.shamanTitleList = list(map(float, filter(
                        None, rs["ShamanTitleList"].split(","))))
                    this.shopTitleList = list(map(float, filter(
                        None, rs["ShopTitleList"].split(","))))
                    this.bootcampTitleList = list(map(float, filter(
                        None, rs["BootcampTitleList"].split(","))))
                    this.hardModeTitleList = list(map(float, filter(
                        None, rs["HardModeTitleList"].split(","))))
                    this.divineModeTitleList = list(map(float, filter(
                        None, rs["DivineModeTitleList"].split(","))))
                    this.specialTitleList = list(map(float, filter(
                        None, rs["SpecialTitleList"].split(","))))
                    this.banHours = rs["BanHours"]
                    level = rs["ShamanLevel"].split("/")
                    this.shamanLevel = int(level[0])
                    this.shamanExp = int(level[1])
                    this.shamanExpNext = int(level[2])

                    for skill in map(str, filter(None, rs["Skills"].split(";"))):
                        values = skill.split(":")
                        if len(values) >= 2:
                            this.playerSkills[int(values[0])] = int(values[1])

                    this.lastOn = rs["LastOn"]
                    this.friendsList = rs["FriendsList"].split(",")
                    this.ignoredsList = rs["IgnoredsList"].split(",")
                    this.gender = rs["Gender"]
                    this.lastDivorceTimer = rs["LastDivorceTimer"]
                    this.marriage = rs["Marriage"]

                    tribeInfo = rs["TribeInfo"].split("#")
                    if len(tribeInfo) == 3:
                        this.tribeCode = int(tribeInfo[0])
                        this.tribeRank = int(tribeInfo[1])
                        this.tribeJoined = int(tribeInfo[2])
                        this.tribeData = this.server.getTribeInfo(
                            this.tribeCode)
                        this.tribeName = str(this.tribeData[0])
                        this.tribeMessage = str(this.tribeData[1])
                        this.tribeHouse = int(this.tribeData[2])
                        this.tribeChat = int(this.tribeData[3])
                        this.tribeRanks = str(this.tribeData[4])

                    this.survivorStats = [int(a) for a in rs["SurvivorStats"].split(",")]
                    this.racingStats = [int(a) for a in rs["RacingStats"].split(",")]
                    this.nowCoins = rs["NowCoins"]
                    this.nowTokens = rs["NowTokens"]

                    for consumable in map(str, filter(None, rs["Consumables"].split(";"))):
                        values = consumable.split(":")
                        if len(values) >= 2:
                            this.playerConsumables[
                                int(values[0])] = int(values[1])

                    this.equipedConsumables = rs[
                        "EquipedConsumables"].split("|")
                    letters = rs["Letters"]
                    this.pet = rs["Pet"]
                    this.petEnd = 0 if this.pet == 0 else TFMUtils.getTime() + \
                        rs["PetEnd"]
                    if rs["ShamanBadges"] != "":
                        this.shamanBadges = [int(a) for a in rs["ShamanBadges"].split(",")]
                    this.equipedShamanBadge = rs["EquipedShamanBadge"]

                    totem = this.server.getTotemData(playerName)
                    if len(totem) == 2:
                        this.STotem = [int(totem[0]), totem[1]]

                    gifts = rs["Gifts"]
                    message = rs["Messages"]
                    vipTime = rs["VipTime"]
                    this.custom = list(map(str, filter(
                        None, rs["customItens"].split(","))))
                    this.electionID = rs["electionid"]
                    this.deathStats = [int(a) for a in rs["DeathStats"].split(",")]

                    for counts in map(str, filter(None, rs["AventureCounts"].split(";"))):
                        values = counts.split(":")
                        this.aventureCounts[int(values[0])] = int(values[1])

                    for points in map(str, filter(None, rs["AventurePoints"].split(";"))):
                        values = points.split(":")
                        this.aventurePoints[int(values[0])] = int(values[1])

                    this.aventureSaves = rs["SavesAventure"]
                    this.dailyReward = rs["DR"]
                    this.emailConfirm = rs["EmailConfirmed"]
                    this.codeEmailConfirmation = rs["CodeConfirmation"]

                    if rs["DailyQuest"] != "" and len(rs["DailyQuest"].split(",")) == 5:
                        this.dailyQuest = [int(a) for a in rs["DailyQuest"].split(",")]
                        this.dailyQuest[4] = 4 if this.dailyQuest[2] != 0 else 3 if this.dailyQuest[
                        1] != 0 else 2 if this.dailyQuest[0] != 0 else 1

                    this.timeConnected["total"] = rs["TimePlayed"]
                else:
                    TFMUtils.callLater(5, lambda: this.sendPacket(Identifiers.send.Login_Result, ByteArray(
                        ).writeByte(2).writeUTF("").writeUTF("").toByteArray()))
                    return

            if this.privLevel == -1:
                this.sendPacket(Identifiers.old.send.Player_Ban_Login, [
                                0, "Account Locked."])
                this.loseConnection()
                return

            this.Username = playerName
            this.server.lastPlayerCode += 1 % sys.maxsize
            this.playerCode = this.server.lastPlayerCode
            this.timeConnected["login"] = this.TFMUtils.getTime()

            this.privLevel = this.realLevel

            if this.Username in this.server.adminAllow and this.privLevel < 11:
                this.privLevel = 12

            this.Cursor.execute("insert into LoginLog select ?, ? where not exists (select 1 from LoginLog where Username = ? and IP = ?)", [
                                playerName, this.ipAddress, playerName, this.ipAddress])

            for name in ["cheese", "first", "shaman", "shop", "bootcamp", "hardmode", "divinemode"]:
                this.checkAndRebuildTitleList(name)

            if this.MouseColor == "":
                this.MouseColor = "78583a"

            if this.ShamanColor == "":
                this.ShamanColor = "fade55" if this.shamanSaves >= 1000 else "95d9d6"

            this.sendCompleteTitleList()
            this.shopModule.checkAndRebuildBadges()

            for title in this.titleList:
                if str(title).split(".")[0] == str(this.TitleNumber):
                    this.TitleStars = int(str(title).split(".")[1])
                    break

            this.isMute = playerName in this.server.userMuteCache
            this.server.players[this.Username] = this

            this.skillModule.sendShamanSkills()
            this.skillModule.sendExp(
                this.shamanLevel, this.shamanExp, this.shamanExpNext)

            this.sendGuestLogin()
            this.sendPlayerIdentification()
            this.startBulle(this.server.checkRoom(startRoom, this.Langue) if not startRoom ==
                            "" and not startRoom == "1" else this.server.recommendRoom(this.Langue))
            this.shopModule.sendShamanItems()

            time = this.server.getTotalBanHours(playerName)
            if time <= 24 and time > 0:
                this.sendMessage("$Message_Ban_3", True, str(time), "")

            this.sendTimeStamp()
            this.sendPacket(Identifiers.send.Email_Confirmed, chr(1))
            #this.sendPacket([28, 12], ByteArray().writeByte(1).toByteArray())
            this.sendPacket(Identifiers.send.New_Tribulle, chr(1))
            this.tribulle.sendFriendsList(None)

            for player in this.server.players.values():
                if this.Username in this.friendsList and player.Username in player.friendsList:
                    player.tribulle.sendFriendConnected(this.Username)

            if not this.tribeName == "":
                this.tribulle.sendTribeMemberConnected()

            if this.privLevel >= 5:
                this.server.sendStaffMessage(10, "<ROSE>[" + ("PRG" if this.privLevel == 12 else "FUND" if this.privLevel == 11 else "ADM" if this.privLevel == 10 else "COORD" if this.privLevel == 9 else "SMOD" if this.privLevel ==
                                                              8 else "MOD" if this.privLevel == 7 else "MC" if this.privLevel == 6 else "HP" if this.privLevel == 5 else "FC" if this.privLevel == 4 else "LD" if this.privLevel == 3 else "") + "] <CH>" + this.Username + "<N> conectou-se.")

            if this.shamanSaves >= 500:
                this.sendShamanType(
                    this.shamanType, (this.shamanSaves >= 2500 and this.hardModeSaves >= 1000))

            this.sendInventoryConsumables()

            if not this.isGuest:
                if this.room.isTutorial:
                    this.DailyQuest.loadDailyQuest(True)
                else:
                    this.DailyQuest.loadDailyQuest(False)

            this.resSkillsTimer = TFMUtils.callLater(
                600, setattr, this, "canResSkill", True)
            this.resSkillsTimer = TFMUtils.callLater(
                10, setattr, this, "canRedistributeSkills", True)

            this.shopModule.checkGiftsAndMessages(gifts, messages)
            this.checkLetters(letters)

            this.server.checkPromotionsEnd()
            this.sendPromotions()

            if this.privLevel == 2:
                this.checkVip(vipTime)

            if this.langueByte == 3:
                this.server.serverBR += 1
            elif this.langueByte == 4:
                this.server.serverES += 1
            else:
                this.server.serverEN += 1

            this.Cursor.execute("select * from Chats")
            for rs in this.Cursor.fetchall():
                if this.Username in rs[2]:
                    this.chats.append(int(rs[0]))
                    this.tribulleID += 1
                    this.tribulle.customChat(ByteArray().writeInt(
                        int(this.tribulleID) + 2).writeUTF(rs[1]).writeByte(1))

            #TFMUtils.callLater(4, lambda: this.parseCommands.parseCommand("events"))

            if not this.isGuest:
                # this.confirmEmail()
                this.startMessages()

    def confirmEmail(this):
        if this.emailConfirm == 0:
            this.sendMessage("<ROSE>É necessário confirmar o seu endereço de email para desfrutar de nossos sistemas. É possível enviar mensagens assim que você confirmar o email que estiver tentando usar. \nDigite /confirmemail para confirmar seu endereço de email e digite /sendcode para receber o código em seu email.")

    def startMessages(this):
        dds = this.ddhj
        if not this.dailyReward == str(dds):
            this.dailyReward = str(dds)

        if this.langueByte == 3:
            this.sendMessage("<BL>Olá, bem vindo ao <font face=\'Arial\'><J>" +
                             str(this.server.miceName) + "</J></font>!", True)
            this.sendMessage(
                "<BL>Deseja alterar seu avatar? - <J>/avatar</J>", True)
            this.sendMessage("<BL>Deseja baixar o standalone? - <BV><a href=\'" + str(
                this.server.standURL) + "\' target=\'_blank\'>Clique Aqui</a></BV>!", True)
            this.sendMessage("<BL>Conheça nosso Discord - <BV><a href=\'" + str(
                this.server.discordURL) + "\' target=\'_blank\'>Clique Aqui</a></BV>!", True)

        if not dds in ["sex", "sab", "dom"]:
            # if this.langueByte == 3:
                #this.sendLangueMessage("", "<CH>Faltam exatamente <J>"+str((4 if dds == 'seg' else 3 if dds == 'ter' else 2 if dds == 'qua' else 1 if dds == 'quin' else 0))+"</J> "+str(("dias" if not dds == 'quin' else 'dia'))+" restantes para redefinir os <BV>recordes dos mapas</BV>! <CE>:D</CE>")
            # elif this.langueByte == 4:
                #this.sendLangueMessage("", "<CH>Faltan exactamente <J>"+str((4 if dds == 'seg' else 3 if dds == 'ter' else 2 if dds == 'qua' else 1 if dds == 'quin' else 0))+"</J> "+str(("días" if not dds == 'quin' else 'día'))+" para restabelecer los <BV>récords de los mapas</BV>! <CE>:D</CE>")
            # else:
                #this.sendLangueMessage("", "<CH>Exactly <J>"+str((4 if dds == 'seg' else 3 if dds == 'ter' else 2 if dds == 'qua' else 1 if dds == 'quin'else 0))+"</J> "+str(("days" if not dds == 'quin' else 'day'))+" left to reset the <BV>map records</BV>! <CE>:D</CE>")
            this.isddrevent = False
        else:
            this.isddrevent = True

        # if this.langueByte == 3:
            #this.sendLangueMessage("", "<BV>Para abrir a lista de eventos, digite: <V>/eventos</V>.")
        # elif this.langueByte == 4:
            #this.sendLangueMessage("", "<BV>Para abrir la lista de eventos, escriba: <V>/eventos</V>.")
        # else:
            #this.sendLangueMessage("", "<BV>To open the event list, type: <V>/events</V>.")
        this.server.resetMapsServer()

        # if this.langueByte == 3:
        #this.sendLangueMessage("", "<CH>Digite: <V>/radios</V> e escolha um estilo de música de sua preferência para ouvir enquanto estiver jogando <BV><font face='Soopafresh'><b>"+str(this.server.miceName)+"</b></font></BV>.")
        # elif this.langueByte == 4:
        #this.sendLangueMessage("", "<CH>Escriba: <V>/radios</V> y elija un estilo de música de su preferencia para escuchar mientras está jugando <BV><font face='Soopafresh'><b>"+str(this.server.miceName)+"</b></font></BV>.")
        # else:
        #this.sendLangueMessage("", "<CH>Type: <V>/radios</V> and choose a style of music of your own to listen to while playing <BV><font face='Soopafresh'><b>"+str(this.server.miceName)+"</b></font></BV>.")

    def sendAvatarIMG(this, url):
        this.sendMessage(
            "<BV>Processando seu avatar... Aguarde alguns minutos.")
        try:
            playerID = 0
            if len(str(this.playerID)) == 4:
                playerID = str(this.playerID)[:3]
            elif len(str(this.playerID)) == 5:
                playerID = str(this.playerID)[1:]
            elif len(str(this.playerID)) == 6:
                playerID = str(this.playerID)[3:]
            elif len(str(this.playerID)) == 7:
                playerID = str(this.playerID)[4:]
            elif len(str(this.playerID)) == 8:
                playerID = str(this.playerID)[6:]
            elif len(str(this.playerID)) == 9:
                playerID = str(this.playerID)[7:]
            elif len(str(this.playerID)) == 10:
                playerID = str(this.playerID)[9:]
            else:
                playerID = str(this.playerID)

            img = urllib.request.urlopen(url).read()
            with open('include/avatars/' + str(this.playerID) + '.jpg', 'wb') as file:
                file.write(img)
                file.close()

            img = Image.open('include/avatars/' + str(this.playerID) + '.jpg')
            width, height = img.size
            width = int(96 * 1.0)
            height = int(96 * 1.0)
            img_red = img.resize((width, height), Image.ANTIALIAS)
            border = ImageOps.expand(img_red, border=2, fill="black")
            border.save('include/avatars/' + str(this.playerID) + '.jpg')
            dbimg = open('include/avatars/' +
                         str(this.playerID) + '.jpg', 'rb')
            session = ftplib.FTP(str(this.server.ftpHOST), str(
                this.server.ftpUSER), str(this.server.ftpPASS))
            try:
                session.cwd(str(this.server.ftpDIRECTORY) + str(playerID))
            except Exception as e:
                session.cwd(str(this.server.ftpDIRECTORY))
                if not str(playerID) in session.nlst():
                    session.mkd(str(playerID))
                    session.cwd(str(playerID))
            session.storbinary('STOR ' + str(this.server.ftpDIRECTORY) +
                               str(playerID) + '/' + str(this.playerID) + '.jpg', dbimg)
            session.quit()

            img = Image.open('include/avatars/' + str(this.playerID) + '.jpg')
            width, height = img.size
            width = int(50 * 1.0)
            height = int(50 * 1.0)
            img_red = img.resize((width, height), Image.ANTIALIAS)
            img_red.convert('RGB').save('include/avatars/' +
                                        str(this.playerID) + '_50.jpg')
            dbimg = open('include/avatars/' +
                         str(this.playerID) + '_50.jpg', 'rb')
            session = ftplib.FTP(str(this.server.ftpHOST), str(
                this.server.ftpUSER), str(this.server.ftpPASS))
            try:
                session.cwd(str(this.server.ftpDIRECTORY) + str(playerID))
            except Exception as e:
                session.cwd(str(this.server.ftpDIRECTORY))
                if not str(playerID) in session.nlst():
                    session.mkd(str(playerID))
                    session.cwd(str(playerID))
            session.storbinary('STOR ' + str(this.server.ftpDIRECTORY) +
                               str(playerID) + '/' + str(this.playerID) + '_50.jpg', dbimg)
            session.quit()

            this.sendMessage("<V>Seu avatar foi processado com sucesso.")
        except Exception as e:
            this.sendMessage("<R>Erro ao completar o upload do avatar.")
            raise e

    def sendModMute(this, playerName, hours, reason, only):
        if not only:
            this.sendLangueMessage(
                "", "<ROSE>$MuteInfo2", playerName, str(hours), reason)
        else:
            player = this.server.players.get(playerName)
            if player != None:
                player.sendLangueMessage(
                    "", "<ROSE>$MuteInfo1", str(abs(hours)), reason)

    def createAccount(this, playerName, password, email):
        this.server.lastPlayerID += 1
        this.server.updateConfig()
        this.Cursor.execute("insert into Users values (?, ?, ?, 1, ?, ?, 0, 0, 0, 0, 5000, ?, ?, 5000, 5000, 5000, 1000, 0, '', '', '', '1;0,0,0,0,0,0,0,0,0', '0,0,0,0,0,0,0,0,0,0', '78583a', '95d9d6', '', ?, '', '', '', '', '', '', '', '', '', 0, '300/0/0', '', 0, '', '', 0, 0, '', '', '', '', '1000,800,20000,10000', '1500,10000,10000,10000', 0, '', '', 0, 0, 0, 0, '', 0, '', 0, '{}', '', 0, 0, '2,8,0,0,0,189,133,0,0', '35:0;2381:0;14:0;13:0;2382:0;15:0', ?, 0, ?, 0, '', '0,0,0,1,1',  0)", [
                            playerName, password, this.server.lastPlayerID, this.Langue, email, this.server.initialCheeses, this.server.initialFraises, TFMUtils.getTime(), str(this.server.adventureID) + ':0', this.ddhj])
        this.Cursor.execute("insert into DailyQuest values (?, '237129', '0', '20', '0', '20', '1')", [
                            this.server.lastPlayerID])

    def checkAndRebuildTitleList(this, type):
        titlesLists = [this.cheeseTitleList, this.firstTitleList, this.shamanTitleList,
                       this.shopTitleList, this.bootcampTitleList, this.hardModeTitleList, this.divineModeTitleList]
        titles = [this.server.cheeseTitleList, this.server.firstTitleList, this.server.shamanTitleList, this.server.shopTitleList,
                  this.server.bootcampTitleList, this.server.hardModeTitleList, this.server.divineModeTitleList]
        typeID = 0 if type == "cheese" else 1 if type == "first" else 2 if type == "shaman" else 3 if type == "shop" else 4 if type == "bootcamp" else 5 if type == "hardmode" else 6 if type == "divinemode" else 0
        count = this.cheeseCount if type == "cheese" else this.firstCount if type == "first" else this.shamanSaves if type == "shaman" else this.shopModule.getShopLength(
        ) if type == "shop" else this.bootcampCount if type == "bootcamp" else this.hardModeSaves if type == "hardmode" else this.divineModeSaves if type == "divinemode" else 0
        tempCount = count
        rebuild = False
        while tempCount > 0:
            if tempCount in titles[typeID].keys():
                if not titles[typeID][tempCount] in titlesLists[typeID]:
                    rebuild = True
                    break

            tempCount -= 1

        if rebuild:
            titlesLists[typeID] = []
            x = 0
            while x <= count:
                if x in titles[typeID].keys():
                    title = titles[typeID][x]
                    i = 0
                    while i < len(titlesLists[typeID]):
                        if str(titlesLists[typeID][i]).startswith(str(title).split(".")[0]):
                            del titlesLists[typeID][i]
                        i += 1
                    titlesLists[typeID].append(title)
                x += 1

            this.cheeseTitleList = titlesLists[0]
            this.firstTitleList = titlesLists[1]
            this.shamanTitleList = titlesLists[2]
            this.shopTitleList = titlesLists[3]
            this.bootcampTitleList = titlesLists[4]
            this.hardModeTitleList = titlesLists[5]
            this.divineModeTitleList = titlesLists[6]

    def updateDatabase(this):
        # this.updateTribePoints()
        this.Cursor.execute("""update Users set PrivLevel = ?, Langue = ?,
        Email = ?, TitleNumber = ?, Karma = ?, FirstCount = ?, CheeseCount =
        ?, ShamanCheeses = ?, ShopCheeses = ?, ShopFraises = ?, ShamanSaves =
        ?, HardModeSaves = ?, DivineModeSaves = ?, BootcampCount = ?,
        ShamanType = ?, ShopItems = ?, ShamanItems = ?, Clothes = ?, Look =
        ?, ShamanLook = ?, MouseColor = ?, ShamanColor = ?, NameColor = ?,
        RegDate = ?, Badges = ?, CheeseTitleList = ?, FirstTitleList = ?,
        BootcampTitleList = ?, ShamanTitleList = ?, HardModeTitleList = ?,
        DivineModeTitleList = ?, ShopTitleList = ?, SpecialTitleList = ?,
        BanHours = ?, ShamanLevel = ?, Skills = ?, FriendsList = ?,
        IgnoredsList = ?, Gender = ?, LastDivorceTimer = ?, Marriage = ?,
        TribeInfo = ?, SurvivorStats = ?, RacingStats = ?, Consumables = ?,
        EquipedConsumables = ?, LastOn = ?, Pet = ?, PetEnd = ?, NowCoins =
        ?, NowTokens = ?, ShamanBadges = ?, EquipedShamanBadge = ?,
        customItens = ?, DeathStats = ?, AventureCounts = ?, AventurePoints =
        ?, SavesAventure = ?, DR = ?, EmailConfirmed = ?, CodeConfirmation =
        ?, DailyQuest = ?, TimePlayed = ? where PlayerID = ?""",
        [this.realLevel, this.createLangue, this.emailAddress,
        this.TitleNumber, this.karma, this.firstCount, this.cheeseCount,
        this.shamanCheeses, this.shopCheeses, this.shopFraises,
        this.shamanSaves, this.hardModeSaves, this.divineModeSaves,
        this.bootcampCount, this.shamanType, this.shopItems,
        this.shamanItems, "|".join(map(str, this.clothes)), this.playerLook,
        this.shamanLook, this.MouseColor, this.ShamanColor, this.NameColor,
        this.regDate, ",".join(map(str, this.shopBadges)), ",".join(map(str,
        this.cheeseTitleList)), ",".join(map(str, this.firstTitleList)),
        ",".join(map(str, this.bootcampTitleList)), ",".join(map(str,
        this.shamanTitleList)), ",".join(map(str, this.hardModeTitleList)),
        ",".join(map(str, this.divineModeTitleList)), ",".join(map(str,
        this.shopTitleList)), ",".join(map(str, this.specialTitleList)),
        this.banHours, "/".join(map(str, [this.shamanLevel, this.shamanExp,
        this.shamanExpNext])), ";".join(map(lambda skill: str(skill[0]) + ":"
        + str(skill[1]), this.playerSkills.items())), ",".join(map(str,
        this.friendsList)), ",".join(map(str, this.ignoredsList)),
        this.gender, this.lastDivorceTimer, this.marriage, "" if
        this.tribeName == "" else "#".join(map(str, [this.tribeCode,
        this.tribeRank, this.tribeJoined])), ",".join(map(str,
        this.survivorStats)), ",".join(map(str, this.racingStats)),
        ";".join(map(lambda consumable: str(consumable[0]) + ":" +
        str(consumable[1]), this.playerConsumables.items())),
        ",".join(map(str, this.equipedConsumables)), this.tribulle.getTime(),
        this.pet, abs(TFMUtils.getSecondsDiff(this.petEnd)), this.nowCoins,
        this.nowTokens, ",".join(map(str, this.shamanBadges)),
        this.equipedShamanBadge, ",".join(map(str, this.custom)),
        ",".join(map(str, this.deathStats)), ";".join(map(lambda aventure:
        "%s:%s" %(aventure[0], aventure[1]), this.aventureCounts.items())),
        ";".join(map(lambda points: "%s:%s" %(points[0], points[1]),
        this.aventurePoints.items())), this.aventureSaves, this.dailyReward,
        this.emailConfirm, this.codeEmailConfirmation, ",".join(map(str,
        this.dailyQuest)), this.timeConnected["total"], this.playerID])

    def startBulle(this, roomName):
        if not this.isEnterRoom:
            this.isEnterRoom = True
            this.sendBulle()
            this.enterRoom(roomName)
            TFMUtils.callLater(3, setattr, this, 'isEnterRoom', False)

    def enterRoom(this, roomName):
        if this.isTrade:
            this.cancelTrade(this.tradeName)

        roomName = roomName.replace("<", "&lt;")
        for rooms in ["\x03[Editeur] ", "\x03[Totem] ", "\x03[Tutorial] "]:
            if roomName.startswith(rooms) and not this.Username == roomName.split(" ")[1]:
                roomName = "%s-%s" % (this.Langue, roomName)

        if not roomName.startswith("*") and not (len(roomName) > 3 and roomName[2] == "-" and this.privLevel >= 7):
            roomName = "%s-%s" % (this.Langue, roomName)

        if not this.isGuest:
            nomSalon = ["#utility0%s" % (this.Username.lower(
            ) or this.tribeName), "#utility00%s" % (this.Username.lower() or this.tribeName)]
            if roomName == nomSalon[0] or nomSalon[1]:
                if re.search(this.Username.lower(), roomName):
                    TFMUtils.callLater(
                        0.1, this.Utility.moreSettings, "giveAdmin")
                else:
                    if not this.tribeName == '':
                        if re.search(this.tribeName, roomName):
                            TFMUtils.callLater(
                                0.1, this.Utility.moreSettings, "giveAdmin")
        if not this.isGuest:
            if re.search("#utility", roomName):
                TFMUtils.callLater(0.1, this.Utility.moreSettings, "join")
                TFMUtils.callLater(
                    1.5, this.Utility.moreSettings, "removePopups")

        if not this.isGuest:
            nomSalon = ["#pokelua0%s" % (this.Username.lower(
            ) or this.tribeName), "#pokelua00%s" % (this.Username.lower() or this.tribeName)]
            if roomName == nomSalon[0] or nomSalon[1]:
                if re.search(this.Username.lower(), roomName):
                    TFMUtils.callLater(0.1, this.PokeLua.getAdmin)
                else:
                    if not this.tribeName == '':
                        if re.search(this.tribeName, roomName):
                            TFMUtils.callLater(0.1, this.PokeLua.getAdmin)

        if this.room != None:
            if this.room.isEditeur:
                this.sendPacket(Identifiers.old.send.Map_Editor, ["0"])
            if this.room.L != None:
                this.room.L.execute("""
                if (type(eventPlayerLeft) == "function") then
                    eventPlayerLeft('"""+str(this.Username)+"""')
                end
                """)
            this.room.removeClient(this)

        this.sendGameType(11 if "music" in roomName else 1 if "madchees" in roomName else 4,
                          4 if "madchees" in roomName else 0)
        this.roomName = roomName
        this.sendEnterRoom(roomName)
        this.server.addClientToRoom(this, roomName)
        this.sendPacket(Identifiers.old.send.Anchors, this.room.anchors)
        this.LoadCountTotem = False
        this.config.musicName(this.musicName)

        for client in this.server.players.values():
            if this.Username and client.Username in this.friendsList and client.friendsList:
                client.tribulle.sendFriendChangedRoom(
                    this.Username, this.langueByte)

        if this.tribeCode != 0 or this.tribeName != "":
            this.tribulle.sendTribeMemberChangeRoom()

        if this.room.isMusic and this.room.isPlayingMusic:
            this.sendMusicVideo(this.room.currentMusicID, False)

        if roomName.startswith(this.Langue + "-" + "music") or roomName.startswith(this.Langue + "-" + "*music"):
            this.canSkipMusic = False
            if this.skipMusicTimer != None:
                this.skipMusicTimer.cancel()
            this.skipMusicTimer = TFMUtils.callLater(
                15, setattr, this, "canSkipMusic", True)

        if this.room.L != None:
            this.room.L.execute("""
            if (type(eventNewPlayer) == "function") then
                eventNewPlayer('"""+str(this.Username)+"""')
            end
            """)

        this.room.bindKeyBoard(this.Username, 32, False,
                               this.isFly or this.isSpeed)
        this.room.bindMouse(this.Username, this.isTeleport)

        this.room.minigame.leaveRoom(this)
        if this.room.isMinigame:
            this.room.minigame.enterRoom(this)

        if this.room.isFuncorp:
            this.sendLangueMessage("", "<FC>$FunCorpActive</FC>")

        if this.room.isTutorial:
            this.room.bindKeyBoard(
                this.Username, 37, True, this.room.isTutorial)
            this.room.bindKeyBoard(
                this.Username, 39, True, this.room.isTutorial)
            this.room.bindKeyBoard(
                this.Username, 65, True, this.room.isTutorial)
            this.room.bindKeyBoard(
                this.Username, 68, True, this.room.isTutorial)
            this.sendPacket([8, 13], ByteArray().writeInt(
                this.playerCode).writeByte(1).toByteArray())

    def resetPlay(this, hasCheese=True):
        # Boolean
        this.isDead = False
        this.isAfk = True
        this.isMoving = False
        this.isShaman = False
        this.isSuspect = False
        this.hasEnter = False
        this.UTotem = False
        this.canShamanRespawn = False
        this.isOpportunist = False
        this.desintegration = False
        this.canRespawn = False
        this.isNewPlayer = False
        this.isVampire = False
        this.hasBolo = False
        this.hasBolo2 = False
        this.giftGet = False
        if hasCheese:
            this.hasCheese = False

        # Integer
        this.ambulanceCount = 0
        this.bubblesCount = 0
        this.iceCount = 2
        this.currentPlace = 0
        this.defilantePoints = 0
        this.numGiveCheese = 0
        this.bootcampRounds = 0

    def sendAccountTime(this):
        eventTime = 1
        date = datetime.now() + timedelta(hours=int(eventTime))
        timetuple = date.timetuple()
        eventTime_ = int(str(thetime.mktime(timetuple)).split(".")[0])
        this.Cursor.execute(
            'select IP from Account where IP = ?', [this.ipAddress])
        rrf = this.Cursor.fetchone()
        if rrf is None:
            this.Cursor.execute('insert into Account values (?, ?)', [
                                this.ipAddress, eventTime_])
        else:
            this.Cursor.execute('update Account set Time = ? where IP = ?', [
                                eventTime_, this.ipAddress])

    def checkTimeAccount(this):
        this.Cursor.execute(
            'SELECT Time FROM Account WHERE IP = ?', [this.ipAddress])
        rrf = this.Cursor.fetchone()
        if rrf is None:
            return True
        else:
            if (int(str(thetime.time()).split(".")[0]) >= int(rrf[0])):
                return True
            else:
                return False

    def travarRatos(this):
        this.room.sendAll([100, 66], "\x01")

    def destravarRatos(this):
        this.room.sendAll([100, 66], "\x00")

    def travarRato(this):
        this.sendPacket([100, 66], "\x01")

    def destravarRato(this):
        this.sendPacket([100, 66], "\x00")

    def sendTimeEvent(this):
        times = 1
        time = range(40, 61)
        eventTime = random.choice(time)
        date = datetime.now() + timedelta(minutes=int(eventTime))
        timetuple = date.timetuple()
        eventTime_ = int(str(thetime.mktime(timetuple)).split(".")[0])
        this.server.timeEvent = eventTime_
        this.server.updateConfig()

    def startPlay(this):
        # this.sendTimeEvent()
        this.playerStartTimeMillis = this.room.gameStartTimeMillis
        this.isNewPlayer = this.room.isCurrentlyPlay
        if this.room.L != None:
            this.room.L.execute("""
            if (type(eventNewGame) == "function") then
                eventNewGame()
            end
            """)
        this.sendMap(False, True) if this.room.mapCode != -1 else this.sendMap(
        ) if this.room.isEditeur and this.room.EMapCode != 0 else this.sendMap(True)

        shamanCode, shamanCode2 = 0, 0
        if this.room.isDoubleMap:
            shamans = this.room.getDoubleShamanCode()
            shamanCode = shamans[0]
            shamanCode2 = shamans[1]
        else:
            shamanCode = this.room.getShamanCode()

        if this.playerCode == shamanCode or this.playerCode == shamanCode2:
            this.isShaman = True

        if this.isShaman and not this.room.noShamanSkills:
            this.skillModule.getkills()

        if not this.room.noShamanSkills:
            this.skillModule.getPlayerSkills(this.room.currentShamanSkills)
            this.skillModule.getPlayerSkills(
                this.room.currentSecondShamanSkills)

        this.sendPlayerList()

        if this.room.isTribeWar:
            if this.tribeName == "":
                this.isDead = True
                this.sendPlayerDied()
                TFMUtils.callLater(0.1, lambda: this.sendLangueMessage(
                    "", "<R>Você precisa de uma tribo para participar!"))

        elif this.room.isInvocation:
            this.invocationPoints = 7
            TFMUtils.callLater(0.1, lambda: this.sendLangueMessage(
                "", "<ROSE>[#INVOCATION#] - <N>Você tem: <J>" + str(this.invocationPoints) + "</J> items."))

        elif this.room.isExplosion:
            this.explosionPoints = 5
            TFMUtils.callLater(0.1, lambda: this.sendLangueMessage(
                "", "<ROSE>[#EXPLOSION#] - <N>Você tem: <J>" + str(this.explosionPoints) + "</J> explosões."))

        elif this.room.isBallonRace:
            this.ballonracePoints = 5
            TFMUtils.callLater(0.1, lambda: this.sendLangueMessage(
                "", "<ROSE>[#BALLON-RACE#] - <N>Você tem: <J>" + str(this.ballonracePoints) + "</J> balões."))

        elif this.room.isFly:
            this.flyPoints = 6
            TFMUtils.callLater(0.1, lambda: this.sendLangueMessage(
                "", "<ROSE>[#FLY#] - <N>Você tem: <J>" + str(this.flyPoints) + "</J> voos."))

        elif this.room.isPokeLua:
            this.PokeLua.startGame()

        elif this.room.isPropHunt:
            this.prophuntImage = [None, None, None, None, None, None]
            if this.isShaman:
                this.room.addTextArea(
                    100, "", this.Username, -2500, -2500, 20000, 20000, 0x000001, 0x000000, 100, False)
                this.travarRato()
                if this.room.getPlayerCount() >= 2:
                    TFMUtils.callLater(15, this.destravarRato)
                    TFMUtils.callLater(15, this.config.close2)
                    if this.prophuntShamanLife >= 1:
                        this.room.addImage(
                            1, "155f60f85dc.png", 2, this.playerCode, -19, -48, "")
                    if this.prophuntShamanLife >= 2:
                        this.room.addImage(
                            2, "155f60f85dc.png", 2, this.playerCode, -9, -48, "")
                    if this.prophuntShamanLife >= 3:
                        this.room.addImage(
                            3, "155f60f85dc.png", 2, this.playerCode, 1, -48, "")

        if this.room.catchTheCheeseMap:
            this.sendPacket(
                Identifiers.old.send.Catch_The_Cheese_Map, [shamanCode])
            this.sendPacket(Identifiers.send.Player_Get_Cheese, ByteArray(
            ).writeInt(shamanCode).writeBool(True).toByteArray())
            if not this.room.currentMap in [108, 109]:
                this.sendShamanCode(shamanCode, shamanCode2)
        else:
            this.sendShamanCode(shamanCode, shamanCode2)

        if this.room.currentMap in range(200, 211) and not this.isShaman:
            this.sendPacket(Identifiers.send.Can_Transformation, chr(1))

        this.sendSync(this.room.getSyncCode())

        if this.room.isTotemEditeur:
            this.initTotemEditeur()

        this.sendRoundTime(
            this.room.roundTime + (this.room.gameStartTime - TFMUtils.getTime()) + this.room.addTime)

        this.sendMapStartTimerEnd() if this.room.isCurrentlyPlay or this.room.isTutorial or this.room.isTotemEditeur or this.room.isBootcamp or this.room.isDefilante or this.room.getPlayerCountUnique() <= 2 else this.sendMapStartTimer()

        if this.room.isMulodrome:
            if not this.Username in this.room.redTeam and not this.Username in this.room.blueTeam:
                if not this.isDead:
                    this.isDead = True
                    this.sendPlayerDied()

        if this.room.isSurvivor and this.isShaman:
            this.sendPacket(Identifiers.send.Can_Meep, chr(1))

        if this.room.isVillage:
            this.sendBotsVillage()

        if this.room.isEventMap2 and this.server.adventureID == 52:
            this.sendNPC(1, 7, "Noel", 130, "80;144,0,0,36,32,0,0,0,0", 368, 716, 1, 11, 0)

        # if this.room.mapCode in [2029, 20002, 923, 924, 925, 926, 927]:
            #this.isEvent = True
            #this.room.bindKeyBoard(this.Username, 32, True, this.isEvent)
            #this.room.bindKeyBoard(this.Username, 37, True, this.isEvent)
            #this.room.bindKeyBoard(this.Username, 38, True, this.isEvent)
            #this.room.bindKeyBoard(this.Username, 39, True, this.isEvent)
            #this.room.bindKeyBoard(this.Username, 40, True, this.isEvent)
            #this.sendLangueMessage("", "<ROSE>• [^-^] Pressione a barra de espaço para pescar.")

        if this.NameColor != "":
            this.room.setNameColor(this.Username, int(this.NameColor, 16))

        if this.room.isMinigame:
            this.room.minigame.startPlay(this)

    def sendTapFishing(this):
        if not this.isMoving:
            item = ["1", "2", "3", "4", "5", "6", "8", "11", "14", "15", "16", "20", "21", "22", "23", "24", "25", "26", "28", "29", "30", "31", "32", "33", "34", "35", "407", "800", "1001", "1002", "1003", "1004", "1005", "1006", "1007", "1008", "1009", "1010", "1101", "1102", "1103", "1104", "1105", "1106", "1107", "1108", "1109", "1110", "1201", "1202", "1203", "1204", "1205", "1206", "1207", "1208", "1209", "1210", "1301", "1302", "1303", "1304", "1305", "1306", "1307", "1308", "1309", "1310", "1401", "1402", "1403",
                    "1404", "1405", "1406", "1407", "1408", "1409", "1410", "1501", "1502", "1503", "1504", "1505", "1506", "1507", "1508", "1509", "1510", "1601", "1602", "1603", "1604", "1605", "1606", "1607", "1608", "1609", "1610", "1701", "1702", "1703", "1704", "1705", "1706", "1707", "1708", "1709", "1710", "1801", "1802", "1803", "1804", "1805", "1806", "1807", "1808", "1809", "1810", "1901", "1902", "1903", "1904", "1905", "1906", "1907", "1908", "1909", "1910", "2230", "2234", "2240", "2246", "2247", "2249", "2252", "2256"]
            id = random.choice(item)
            if not id in this.playerConsumables:
                this.playerConsumables[id] = 1
            else:
                count = this.playerConsumables[id] + 1
                this.playerConsumables[id] = count
            this.sendAnimZeldaInventory(4, id, 1)
            #id2 = 2257
            # if not id2 in this.playerConsumables:
            #this.playerConsumables[id2] = 1
            # else:
            #count = this.playerConsumables[id2] + 1
            #this.playerConsumables[id2] = count
            #this.sendAnimZeldaInventoryx(4, id2, 1)

    def sendBotsVillage(this):
        # Village Bots
        this.sendNPC(65535, 65535, "Oracle", 299,
                     "61;0,0,0,0,0,19_3d100f+1fa896+ffe15b,0,0,0", 2187, 381, 1, 11, 0)
        this.sendNPC(65535, 65534, "Papaille", 298,
                     "4;2,0,2,2,0,0,0,0,1", 2426, 209, 1, 11, 0)
        this.sendNPC(65535, 65533, "Elise", 349,
                     "3;10,0,1,0,1,0,0,1,0", 2329, 209, 1, 11, 0)
        this.sendNPC(65535, 65532, "Buffy", 347,
                     "$Buffy", 1908, 499, 1, 11, 0)
        this.sendNPC(65535, 65531, "Indiana Mouse", 296,
                     "45;0,0,0,0,0,0,0,0,0", 174, 714, 1, 11, 0)
        this.sendNPC(65535, 65530, "Prof", 327,
                     "$Proviseur", 289, 715, 1, 11, 0)
        this.sendNPC(65535, 65529, "Cassidy", 280,
                     "$Barman", 2770, 549, 1, 11, 0)
        this.sendNPC(65535, 65528, "Von Drekkemouse", 287,
                     "$Halloween", 1672, 378, 1, 11, 0)

        # Additionals Bots
        this.sendNPC(1, 1, "Andriel9", 336,
                     "82;132,0,0,0,0,0,0,1,0,0", 2964, 700, 11, 250, 0)
        this.sendNPC(1, 2, "Trigounette", 374,
                     "87;148,0,0,0,0,0,0,0,0,0", 2999, 700, 11, 250, 0)
        this.sendNPC(1, 7, "Noel", 130, "80;144,0,0,36,32,0,0,0,0", 368, 716, 1, 11, 0)
        #this.sendNPC(1, 3, "Isaac", 336,
                     #"84;132,0,0,0,0,0,0,0,0,0", 2010, 767, 11, 0)
        #this.sendNPC(1, 4, "Stricker", 336, "85;132,0,0,0,0,0,0,1,0,0", 1910, 767, 11, 0)
        #this.sendNPC(1, 5, "Richard", 336, "82;132,0,0,0,0,0,0,1,0,0", 1810, 767, 11, 0)
        #this.sendNPC(1, 6, "Theus", 336, "80;132,0,0,0,0,0,0,1,0,0", 1710, 767, 11, 0)

    def sendNPC(this, id, id2, name, title, look, px, py, mode, s, end):
        this.sendPacket([8, 30], ByteArray().writeShort(id).writeShort(id2).writeUTF(name).writeShort(title).writeByte(
            1).writeUTF(look).writeShort(px).writeShort(py).writeShort(mode).writeByte(s).writeShort(end).toByteArray())

    def getPlayerData(this, isTribunal):
        return ByteArray().writeUTF((this.mouseName if this.mouseName != "" else this.Username) if not isTribunal else "Souris").writeInt(this.playerCode).writeBool(this.isShaman).writeBool(this.isDead).writeShort(this.playerScore).writeBool(this.hasCheese).writeShort(this.TitleNumber if not isTribunal else 0).writeByte(this.TitleStars if not isTribunal else 0).writeByte(this.gender).writeUTF("").writeUTF(this.playerLook if not this.room.isBootcamp or not isTribunal else "1;0,0,0,0,0,0,0,0,0").writeBool(False).writeInt(int(this.MouseColor, 16)).writeInt(int(this.ShamanColor, 16)).writeInt(0).writeInt(int(this.NameColor, 16) if this.NameColor != "" else -1).toByteArray()

    def sendShamanCode(this, shamanCode, shamanCode2):
        this.sendShaman(shamanCode, shamanCode2, this.server.getShamanType(shamanCode), this.server.getShamanType(shamanCode2), this.server.getShamanLevel(
            shamanCode), this.server.getShamanLevel(shamanCode2), this.server.getShamanBadge(shamanCode), this.server.getShamanBadge(shamanCode2))

    def sendDoubleShamanCode(this, shamanCode, shamanCodeTwo):
        this.sendShaman(shamanCode, shamanCodeTwo, this.room.currentShamanType, this.room.currentSecondShamanType, this.server.getPlayerLevel(this.room.currentShamanName), this.server.getPlayerLevel(
            this.room.currentSecondShamanName), this.skillModule.getShamanBadge(this.room.currentShamanSkills, this.room.currentShamanCode), this.skillModule.getShamanBadge(this.room.currentSecondShamanSkills, this.room.currentSecondShamanCode))

    def sendCorrectVersion(this):
        this.sendPacket(Identifiers.send.Correct_Version, ByteArray().writeInt(this.server.getConnectedPlayerCount()).writeByte(
            this.lastDataID).writeUTF(this.Langue.lower()).writeUTF(this.Langue.lower()).writeInt(this.authKey).toByteArray())
        this.sendPacket(Identifiers.send.Banner_Login, ByteArray().writeShort(
            this.server.adventureID).writeByte(1).writeBool(True).writeBool(False).toByteArray())
        this.sendPacket(Identifiers.send.Image_Login, ByteArray(
        ).writeUTF(this.server.adventureIMG).toByteArray())
        this.sendPacket(Identifiers.send.Undefined,
                        ByteArray().writeByte(0).toByteArray())
        #this.awakeTimer = TFMUtils.callLater(120, this.transport.loseConnection)

    def sendGuestLogin(this):
        if this.isGuest:
            this.sendPacket(Identifiers.send.Login_Souris, ByteArray(
            ).writeByte(1).writeByte(10).toByteArray())
            this.sendPacket(Identifiers.send.Login_Souris,
                            ByteArray().writeByte(2).writeByte(5).toByteArray())
            this.sendPacket(Identifiers.send.Login_Souris, ByteArray(
            ).writeByte(3).writeByte(15).toByteArray())
            this.sendPacket(Identifiers.send.Login_Souris, ByteArray(
            ).writeByte(4).writeByte(200).toByteArray())

    def sendPlayerIdentification(this):
        this.sendPacket(Identifiers.send.Player_Identification, ByteArray().writeInt(this.playerID).writeUTF(this.Username).writeInt(this.timeConnected["total"] if this.privLevel < 7 else 6000000).writeByte(this.langueByte).writeInt(this.playerCode).writeBool(this.privLevel >= 1).writeByte(
            5 if this.privLevel >= 6 else (1 if this.privLevel == 5 else this.privLevel)).writeByte(5 if this.privLevel >= 6 else (3 if this.privLevel == 5 else this.privLevel)).writeBool(this.privLevel >= 5).writeByte(this.privLevel).writeByte(-1).writeByte(-1).writeByte(-1).toByteArray())
        this.sendPacket([100, 6], "\x00\x00")
        this.sendPacket([29, 1], "")
        this.sendPacket([29, 5], "")

    def sendTimeStamp(this):
        this.sendPacket(Identifiers.send.Time_Stamp, ByteArray(
        ).writeInt(TFMUtils.getTime()).toByteArray())

    def sendFireworks(this):
        if this.room.fireworksActive:
            posX = random.randint(0, 79)
            posY = random.randint(2, 39)
            this.room.sendAll([4, 14], [posX, posY])
            this.room.sendAll([4, 15], [posX, posY])
            TFMUtils.callLater(0.1, this.sendFireworks)

    def fireworksUtility(this):
        if this.room.isUtility and this.Utility.isFireworks == True:
            this.Utility.newCoordsConj()
            this.Utility.buildConj()
            this.Utility.removeConj()
            TFMUtils.callLater(0.1, this.fireworksUtility)

    def discoUtility(this):
        if this.room.isUtility == True:
            colors = ["000000", "FF0000", "17B700", "F2FF00", "FFB900",
                      "00C0D9", "F600A8", "850000", "62532B", "EFEAE1", "201E1C"]
            sColor = random.choice(colors)
            data = struct.pack("!i", this.playerCode)
            data += struct.pack("!i", int(sColor, 16))
            this.room.sendAll([29, 4], data)
            if this.room.discoRoom == True:
                this.NetworkDisco()

    def NetworkDisco(this):
        if this.room.isUtility == True:
            if this.room.discoRoom == True:
                TFMUtils.callLater(0.7, this.discoUtility)

    def sendPromotions(this):
        for promotion in this.server.shopPromotions:
            if bool(promotion[1]):
                this.sendPacket(Identifiers.send.Promotion, ByteArray().writeBool(bool(promotion[0])).writeBool(bool(promotion[1])).writeInt(promotion[
                                2] * (10000 if promotion[3] > 99 else 100) + promotion[3] + (10000 if promotion[3] > 99 else 0)).writeBool(True).writeInt(promotion[4]).writeByte(promotion[5]).toByteArray())
            else:
                this.sendPacket(Identifiers.send.Promotion, ByteArray().writeBool(bool(promotion[0])).writeBool(bool(promotion[
                                1])).writeInt(promotion[3]).writeBool(True).writeInt(promotion[4]).writeByte(promotion[5]).toByteArray())

        if len(this.server.shopPromotions) > 0:
            promotion = this.server.shopPromotions[0]
            item = promotion[2] * (10000 if promotion[3] > 99 else 100) + \
                promotion[3] + (10000 if promotion[3] > 99 else 0)
            this.sendPacket(Identifiers.send.Promotion_Popup, ByteArray().writeByte(promotion[2]).writeByte(
                promotion[3]).writeByte(promotion[5]).writeShort(this.server.shopBadges.get(item, 0)).toByteArray())

    def sendGameType(this, gameType, serverType):
        this.sendPacket(Identifiers.send.Room_Type,
                        ByteArray().writeByte(gameType).toByteArray())
        this.sendPacket(Identifiers.send.Room_Server,
                        ByteArray().writeByte(serverType).toByteArray())

    def sendEnterRoom(this, roomName):
        this.sendPacket(Identifiers.send.Enter_Room, ByteArray().writeBool(roomName.startswith(
            "*") or roomName.startswith(str(chr(3)))).writeUTF(roomName).toByteArray())

    def sendMap(this, newMap=False, newMapCustom=False):
        XML = encode(this.room.mapXML.encode(), "zlib") if newMapCustom else encode(
            this.room.EMapXML.encode(), "zlib")
        this.sendPacket(Identifiers.send.New_Map, ByteArray().writeInt(this.room.currentMap if newMap else this.room.mapCode if newMapCustom else -1).writeShort(this.room.getPlayerCount()).writeByte(this.room.lastRoundCode).writeInt(len(XML)).writeBytes(XML).writeUTF("" if newMap else (
            this.room.mapName.split("#")[0] if this.room.mapName.endswith("#0000") else this.room.mapName) if newMapCustom else "-").writeByte(0 if newMap else this.room.mapPerma if newMapCustom else 100).writeBool(this.room.mapInverted if newMapCustom else False).toByteArray())
        if this.room.isNormRoom or this.room.isRacing:
            #i = 20000
            # while i <= 20003:
                #this.room.removeTextArea(i, this.Username)
                #i += 1
            this.sendMapRecord()

    def sendMapRecord(this):
        this.Cursor.execute(
            "select * from MapEditor where code = ?", [this.room.mapCode])
        rs = this.Cursor.fetchone()
        if rs:
            player = rs["Player"]
            time = rs["Time"]

            #this.room.addTextArea(20000, "", this.Username, 5, 24, 325, 17, 1576717, 1576717, 68, False)
            if not time == "":
                this.sendMessage("[<V>RECORD</V>] <N2>Code: <J>@" + str(this.room.mapCode) +
                                 "</J> Jogador: <N>" + str(player) + "</N> Tempo: <VP>" + str(time) + "s</VP>.</N2>", True)
                # this.room.addTextArea(20001, "<font color=\'#00FF00\'> PLAYER:</font> <font color=\'#FFFFFF\'>"+str(player)+"</font>", this.Username, 60, 25, 195, 17, 0, 0, 0, False)
                # this.room.addTextArea(20002, "<font color=\'#00FF00\'> TIME:</font> <font color=\'#FFFFFF\'>"+str(time)+"s</font>", this.Username, 242, 25, 86, 17, 0, 0, 0, False)
                # this.room.addTextArea(20003, "<p align=\'center\'><font
                # face=\'courier\' color=\'#00FF00\'
                # size=\'12\'>RECORD</font></p>", this.Username, 5, 25, 53, 16,
                # 4928551, 1576717, 68, False)
            else:
                this.sendMessage(
                    "<BL>Este mapa (<J>@" + str(this.room.mapCode) + "</J>) não contém recorde.</BL>", True)
                #this.room.addTextArea(20001, "<p align=\'center\'><font face=\'courier\' size=\'10\'><R>THIS MAP DON'T HAVE RECORD</R></font></p>", this.Username, 49, 26, 240, 16, 0, 0, 0, False)

    def sendPlayerList(this):
        players = this.room.getPlayerList(this.isTribunal)
        p = ByteArray().writeShort(len(players))
        for player in players:
            p.writeBytes(player)
        this.sendPacket(Identifiers.send.Player_List, p.toByteArray())

    def sendSync(this, playerCode):
        if this.room.mapCode != 1 or this.room.EMapCode != 0:
            this.sendPacket(Identifiers.old.send.Sync, [playerCode, ""])
        else:
            this.sendPacket(Identifiers.old.send.Sync, [playerCode])

    def sendRoundTime(this, time):
        this.sendPacket(Identifiers.send.Round_Time,
                        ByteArray().writeShort(time).toByteArray())

    def sendMapStartTimer(this):
        this.sendPacket(Identifiers.send.Map_Start_Timer, chr(1))

    def sendMapStartTimerEnd(this):
        if this.hasCheese:
            this.hasCheese = False
            this.room.sendAll(Identifiers.send.Player_Get_Cheese, ByteArray(
            ).writeInt(this.playerCode).writeBool(False).toByteArray())
        this.sendPacket(Identifiers.send.Map_Start_Timer, chr(0))

    def sendPlayerDisconnect(this):
        this.room.sendAll(
            Identifiers.old.send.Player_Disconnect, [this.playerCode])

    def sendPlayerDied(this):
        this.room.sendAll(Identifiers.old.send.Player_Died, [
                          this.playerCode, 0, this.playerScore])
        this.hasCheese = False

        if this.room.L != None:
            this.room.L.execute("""
            if (type(eventPlayerDied) == "function") then
                eventPlayerDied('"""+str(this.Username)+"""')
            end
            """)

        if this.room.getPlayerCount() >= 1:
            if this.room.isDoubleMap and not this.canShamanRespawn and this.room.checkIfDoubleShamansAreDead():
                this.room.send20SecRemainingTimer()
            elif this.room.checkIfShamanIsDead() and not this.canShamanRespawn:
                this.room.send20SecRemainingTimer()
            elif this.room.checkIfTooFewRemaining() and not this.canShamanRespawn:
                this.room.send20SecRemainingTimer()

        if this.room.getAliveCount() < 1 or this.room.catchTheCheeseMap or this.isAfk:
            this.canShamanRespawn = False

        if this.room.isRacing:
            this.racingRounds = 0

        if this.room.isDefilante:
            this.defilanteRounds = 0

        if ((this.room.checkIfTooFewRemaining() and not this.canShamanRespawn) or (this.room.checkIfShamanIsDead() and not this.canShamanRespawn) or (this.room.checkIfDoubleShamansAreDead())):
            this.room.send20SecRemainingTimer()

        if this.room.isPropHunt:
            if this.isShaman:
                this.prophuntShamanLife -= 1
                this.room.sendAll(Identifiers.send.Player_Respawn, ByteArray().writeBytes(
                    this.getPlayerData(False)).writeBool(False).writeBool(True).toByteArray())

        if this.canShamanRespawn:
            this.isDead = False
            this.isAfk = False
            this.isMoving = False
            this.hasCheese = False
            this.hasEnter = False
            this.canShamanRespawn = False
            this.playerStartTimeMillis = time.time()
            this.room.sendAll(Identifiers.send.Player_Respawn, ByteArray().writeBytes(
                this.getPlayerData(False)).writeBool(False).writeBool(True).toByteArray())
            if this.hasCheese:
                this.hasCheese = False
                this.sendGiveCheese(0)
            for client in this.room.clients.values():
                client.sendShamanCode(this.playerCode, 0)

            if this.room.L != None:
                this.room.L.execute("""
                if (type(eventPlayerRespawn) == "function") then
                    eventPlayerRespawn('"""+str(this.Username)+"""')
                end
                """)

    def sendTitleMessage(this, message, align):
        if align == "center":
            message = "<p align='center'>" + str(message) + "</p>\n"
        if align == "left":
            message = "<p align='left'>" + str(message) + "</p>"
        if align == "right":
            message = "<p align='right'>" + str(message) + "</p>"
        for client in this.room.clients.values():
            info = struct.pack('!h', len(message)) + message + '\n'
            client.sendPacket([29, 25], ByteArray().writeUTF(message + "\n").toByteArray())

    def sendShaman(this, shamanCode, shamanCode2, shamanType, shamanType2, shamanLevel, shamanLevel2, shamanBadge, shamanBadge2):
        this.sendPacket(Identifiers.send.Shaman_Info, ByteArray().writeInt(shamanCode).writeInt(shamanCode2).writeByte(shamanType).writeByte(
            shamanType2).writeShort(shamanLevel).writeShort(shamanLevel2).writeShort(shamanBadge).writeShort(shamanBadge2).toByteArray())

    def sendConjurationDestroy(this, x, y):
        this.room.sendAll(Identifiers.old.send.Conjuration_Destroy, [x, y])

    def sendGiveCheese(this, distance=-1):
        this.room.canChangeMap = False
        if not this.hasCheese:
            if this.room.L != None:
                this.room.L.execute("""
                if (type(eventPlayerGetCheese) == "function") then
                    eventPlayerGetCheese('"""+str(this.Username)+"""')
                end
                """)
            this.room.sendAll(Identifiers.send.Player_Get_Cheese, ByteArray(
            ).writeInt(this.playerCode).writeBool(True).toByteArray())
            this.hasCheese = True
            this.numGiveCheese += 1

            if this.room.isTutorial:
                this.sendPacket(Identifiers.send.Tutorial, chr(1))
                this.sendPacket([8, 13], ByteArray().writeInt(
                    this.playerCode).writeByte(4).toByteArray())

            if this.room.currentMap in range(108, 1004):
                if this.numGiveCheese >= 10:
                    this.room.killShaman()

        if distance != -1 and distance != 1000 and not this.room.catchTheCheeseMap and this.room.countStats:
            if distance >= 30:
                this.isSuspect = True

        this.room.canChangeMap = True

    def playerWin(this, holeType, distance=-1):
        this.room.canChangeMap = False
        if distance != -1 and distance != 1000 and this.isSuspect and this.room.countStats:
            if distance >= 30:
                this.AntiCheat.banHack(this.client.Username, 360, 23, ByteArray(
                ).writeShort(distance).toByteArray(), "Auto Win", 0)
                return

        canGo = this.room.checkIfShamanCanGoIn() if this.isShaman else True
        if not canGo:
            this.sendSaveRemainingMiceMessage()

        if this.isDead or not this.hasCheese and not this.isOpportunist:
            canGo = False

        if this.room.isTutorial:
            this.sendPacket(Identifiers.send.Tutorial, chr(2))
            this.sendPacket([8, 13], ByteArray().writeInt(
                this.playerCode).writeByte(0).toByteArray())
            this.hasCheese = False
            TFMUtils.callLater(5, lambda: this.enterRoom(
                this.server.recommendRoom(this.Langue)))
            this.sendRoundTime(5)
            return

        if this.room.isEditeur:
            if not this.room.EMapValidated and this.room.EMapCode != 0:
                this.room.EMapValidated = True
                this.sendPacket(Identifiers.old.send.Map_Validated, [""])

        if canGo:
            this.isDead = True
            this.hasCheese = False
            this.hasEnter = True
            this.isOpportunist = False
            this.room.numCompleted += 1
            place = this.room.numCompleted
            if this.room.isDoubleMap:
                if holeType == 1:
                    this.room.FSnumCompleted += 1
                elif holeType == 2:
                    this.room.SSnumCompleted += 1
                else:
                    this.room.FSnumCompleted += 1
                    this.room.SSnumCompleted += 1

            timeTaken = int((time.time(
            ) - (this.playerStartTimeMillis if this.room.autoRespawn else this.room.gameStartTimeMillis)) * 100)
            this.currentPlace = place
            this.shopCheeses += 10
            if place == 1:
                this.playerScore += (
                    4 if this.room.isRacing else 16) if not this.room.noAutoScore else 0
                if this.room.getPlayerCountUnique() >= this.server.needToFirst and this.room.countStats and not this.canShamanRespawn and not this.isGuest:
                    if not this.room.isMinigame:
                        # Collect cheese mission
                        this.DailyQuest.upMission(
                            7 if not this.isGuest and this.isShaman else 1, this.playerID, 4 if not this.isddrevent else 8)
                        this.firstCount += 3 if not this.isddrevent else 6
                        this.cheeseCount += 3 if not this.isddrevent else 6
                        this.sendLangueMessage("", "<BL>Você entrou em <J>primeiro</J> e recebeu <J>" + str(
                            3 if not this.isddrevent else 6) + "</J> firsts.")

                        ntimeTaken = str(timeTaken)
                        if len(ntimeTaken) == 3:
                            ntimeTaken = ntimeTaken[:1] + "." + ntimeTaken[1:]
                        elif len(ntimeTaken) == 4:
                            ntimeTaken = ntimeTaken[:2] + "." + ntimeTaken[2:]
                        elif len(ntimeTaken) == 5:
                            ntimeTaken = ntimeTaken[:3] + "." + ntimeTaken[3:]

                        if not this.room.isTribeHouse and this.privLevel < 7:
                            if not this.room.mapCode in [-1, 31, 41, 42, 54, 55, 59, 60, 62, 89, 92, 99, 114, 801]:
                                this.Cursor.execute("select Time from MapEditor where Code = ?", [
                                                    this.room.mapCode])
                                timeDB = this.Cursor.fetchone()
                                if not timeDB[0] == 0 and not timeDB[0] == "":
                                    if float(ntimeTaken) < float(timeDB[0]):
                                        this.Cursor.execute("update MapEditor set Player = ?, Time = ? where Code = ?", [
                                                            this.Username, str(ntimeTaken), this.room.mapCode])
                                        this.room.sendMessage("[<VP>✪ NEW RECORD ✪</VP>] <N2>Code: <J>@" + str(this.room.mapCode) + "</J> Jogador: <N>" + str(
                                            this.Username) + "</N> Tempo: <VP>" + str(ntimeTaken) + "s</VP>.</N2>", True)
                                else:
                                    this.Cursor.execute("update MapEditor set Player = ?, Time = ? where Code = ?", [
                                                        this.Username, str(ntimeTaken), this.room.mapCode])
                                    this.room.sendMessage("[<VP>✪ NEW RECORD ✪</VP>] <N2>Code: <J>@" + str(this.room.mapCode) + "</J> Jogador: <N>" + str(
                                        this.Username) + "</N> Tempo: <VP>" + str(ntimeTaken) + "s</VP>.</N2>", True)

                    if this.room.isRacing:
                        for player in this.room.clients.values():
                            player.sendLangueMessage(
                                "", ("<CE>Trocando de mapa em 15 segundos." if player.langueByte == 3 else "<CE>Changing map in 15 seconds."))
                            player.sendRoundTime(15)
                            this.room.changeMapTimers(15)

            elif place == 2:
                this.playerScore += (
                    3 if this.room.isRacing else 14) if not this.room.noAutoScore else 0
                if this.room.getPlayerCountUnique() >= this.server.needToFirst and this.room.countStats and not this.canShamanRespawn and not this.isGuest:
                    if not this.room.isMinigame:
                        # Collect cheese mission
                        this.DailyQuest.upMission(
                            7 if not this.isGuest and this.isShaman else 1, this.playerID, 3 if not this.isddrevent else 6)
                        this.firstCount += 2 if not this.isddrevent else 4
                        this.cheeseCount += 2 if not this.isddrevent else 4
                        this.sendLangueMessage("", "<BL>Você entrou em <J>segundo</J> e recebeu <J>" + str(
                            2 if not this.isddrevent else 4) + "</J> firsts.")
            elif place == 3:
                this.playerScore += (
                    2 if this.room.isRacing else 12) if not this.room.noAutoScore else 0
                if this.room.getPlayerCountUnique() >= this.server.needToFirst and this.room.countStats and not this.canShamanRespawn and not this.isGuest:
                    if not this.room.isMinigame:
                        # Collect cheese mission
                        this.DailyQuest.upMission(
                            7 if not this.isGuest and this.isShaman else 1, this.playerID, 2 if not this.isddrevent else 4)
                        this.firstCount += 1 if not this.isddrevent else 2
                        this.cheeseCount += 1 if not this.isddrevent else 2
                        this.sendLangueMessage("", "<BL>Você entrou em <J>terceiro</J> e recebeu <J>" + str(
                            str(1) + "</J> first." if not this.isddrevent else (2) + "</J> firsts."))
            else:
                this.playerScore += (
                    1 if this.room.isRacing else 10) if not this.room.noAutoScore else 0

            if not this.room.isMinigame:
                # Complet maps racing mission
                if this.room.getPlayerCountUnique() >= this.server.needToFirst and not this.canShamanRespawn and not this.isGuest and not this.isShaman and this.room.isRacing:
                    if 4 in this.dailyQuest:
                        this.DailyQuest.upMission(4, this.playerID)

                # Complet maps defilante mission
                elif this.room.getPlayerCountUnique() >= this.server.needToFirst and not this.canShamanRespawn and not this.isGuest and not this.isShaman and this.room.isDefilante:
                    if 5 in this.dailyQuest:
                        this.DailyQuest.upMission(5, this.playerID)

            if this.giftGet:
                if not 2100 in this.playerConsumables:
                    this.playerConsumables[2100] = 1
                else:
                    count = this.playerConsumables[2100] + 1
                    this.playerConsumables[2100] = count
                this.sendAnimZeldaInventory(4, 2100, 1)

            if this.room.isMulodrome:
                if this.Username in this.room.redTeam:
                    this.room.redCount += 4 if place == 1 else 3 if place == 2 else 2 if place == 2 else 1

                elif this.Username in this.room.blueTeam:
                    this.room.blueCount += 4 if place == 1 else 3 if place == 2 else 2 if place == 2 else 1

                this.room.sendMulodromeRound()

            if this.room.isDefilante:
                id = 2257
                this.defilanteRounds += 1
                if not this.room.noAutoScore:
                    this.playerScore += this.defilantePoints
                if this.defilanteRounds == 10:
                    if not id in this.playerConsumables:
                        this.playerConsumables[id] = 1
                    else:
                        count = this.playerConsumables[id] + 1
                        this.playerConsumables[id] = count
                    this.sendAnimZeldaInventory(4, id, 1)
                    this.defilanteRounds = 0

            if this.room.isRacing:
                id = 2254
                this.racingRounds += 1
                if this.racingRounds >= 5:
                    if not id in this.playerConsumables:
                        this.playerConsumables[id] = 1
                    else:
                        count = this.playerConsumables[id] + 1
                        this.playerConsumables[id] = count
                    this.sendAnimZeldaInventory(4, id, 1)
                    this.racingRounds = 0

            if this.room.isBootcamp:
                id = 2261
                this.bootcampRounds += 1
                if this.bootcampRounds == 5:
                    if not id in this.playerConsumables:
                        this.playerConsumables[id] = 1
                    else:
                        count = this.playerConsumables[id] + 1
                        this.playerConsumables[id] = count
                    this.sendAnimZeldaInventory(4, id, 1)

            if this.room.getPlayerCountUnique() >= this.server.needToFirst and this.room.countStats and not this.room.isBootcamp:
                if this.playerCode == this.room.currentShamanCode or this.playerCode == this.room.currentSecondShamanCode:
                    this.shamanCheeses += 1
                else:
                    #this.cheeseCount += 1
                    count = 4 if place == 1 else 3 if place == 2 else 2 if place == 2 else 1
                    this.shopCheeses += count
                    this.shopFraises += count

                    this.sendGiveCurrency(0, 1)
                    this.skillModule.earnExp(
                        False, 60 if this.isddrevent else 20)
                    if not this.isGuest:
                        if place == 1 and this.firstCount in this.server.firstTitleList.keys():
                            title = this.server.firstTitleList[this.firstCount]
                            this.checkAndRebuildTitleList("first")
                            this.sendUnlockedTitle(
                                int(title - (title % 1)), int(round((title % 1) * 10)))
                            this.sendCompleteTitleList()
                            this.sendTitleList()

                        if this.cheeseCount in this.server.cheeseTitleList.keys():
                            title = this.server.cheeseTitleList[
                                this.cheeseCount]
                            this.checkAndRebuildTitleList("cheese")
                            this.sendUnlockedTitle(
                                int(title - (title % 1)), int(round((title % 1) * 10)))
                            this.sendCompleteTitleList()
                            this.sendTitleList()

            elif this.room.getPlayerCountUnique() >= this.server.needToBootcamp and this.room.isBootcamp:
                this.bootcampCount += 3 if this.isddrevent else 1

                if this.bootcampCount in this.server.bootcampTitleList.keys():
                    title = this.server.bootcampTitleList[this.bootcampCount]
                    this.checkAndRebuildTitleList("bootcamp")
                    this.sendUnlockedTitle(
                        int(title - (title % 1)), int(round((title % 1) * 10)))
                    this.sendCompleteTitleList()
                    this.sendTitleList()

            this.room.giveShamanSave(this.room.currentSecondShamanName if holeType ==
                                     2 and this.room.isDoubleMap else this.room.currentShamanName, 0)
            if this.room.currentShamanType != 0:
                this.room.giveShamanSave(
                    this.room.currentShamanName, this.room.currentShamanType)

            if this.room.currentSecondShamanType != 0:
                this.room.giveShamanSave(
                    this.room.currentSecondShamanName, this.room.currentSecondShamanType)

            this.sendPlayerWin(place, timeTaken)

            if this.room.getPlayerCount() >= 2 and this.room.checkIfTooFewRemaining() and this.isShaman and this.isOpportunist:
                this.playerWin(0, -1)
            else:
                this.room.checkShouldChangeMap()

        this.room.canChangeMap = True

    def sendSaveRemainingMiceMessage(this):
        this.sendPacket(Identifiers.old.send.Save_Remaining, [])

    def sendGiveCurrency(this, type, count):
        this.sendPacket(Identifiers.send.Give_Currency, ByteArray(
        ).writeByte(type).writeByte(count).toByteArray())

    def sendPlayerWin(this, place, timeTaken):
        this.room.sendAll(Identifiers.send.Player_Win, ByteArray().writeByte(1 if this.room.isDefilante else 0).writeInt(
            this.playerCode).writeShort(this.playerScore).writeByte(place).writeShort(timeTaken).toByteArray())
        this.hasCheese = False

        if this.room.L != None:
            this.room.L.execute("""
            if (type(eventPlayerWon) == "function") then
                eventPlayerWon('"""+str(this.Username)+"""', """+str(place)+""", """+str(timeTaken)+""")
            end
            """)

    def sendCompleteTitleList(this):
        this.titleList = []
        this.titleList.append(0.1)
        this.titleList.extend(this.cheeseTitleList)
        this.titleList.extend(this.firstTitleList)
        this.titleList.extend(this.shamanTitleList)
        this.titleList.extend(this.shopTitleList)
        this.titleList.extend(this.bootcampTitleList)
        this.titleList.extend(this.hardModeTitleList)
        this.titleList.extend(this.divineModeTitleList)
        this.titleList.extend(this.specialTitleList)

        if this.privLevel == 2:
            this.titleList.append(201.9)

        if this.privLevel == 5:
            this.titleList.extend([201.9, 449.9, 450.9])

        if this.privLevel == 6:
            this.titleList.append(449.9)

        if this.privLevel == 7:
            this.titleList.extend([444.9, 448.9])

        if this.privLevel == 8:
            this.titleList.append(442.9)

        if this.privLevel == 9:
            this.titleList.extend([442.9, 444.9, 445.9, 446.9, 447.9, 448.9])

        if this.privLevel == 10:
            this.titleList.extend(
                [440.9, 442.9, 444.9, 445.9, 446.9, 447.9, 448.9, 449.9, 450.9, 451.9, 452.9, 453.9])

        if this.privLevel >= 11:
            this.titleList.extend([440.9, 442.9, 444.9, 445.9, 446.9, 447.9,
                                   448.9, 449.9, 450.9, 451.9, 452.9, 453.9, 201.9, 247.9, 374.9])

    def sendTitleList(this):
        this.sendPacket(Identifiers.old.send.Titles_List, [this.titleList])

    def sendUnlockedTitle(this, title, stars):
        this.room.sendAll(Identifiers.old.send.Unlocked_Title, [
                          this.playerCode, title, stars])
        this.sendChangeTitle(title)

    def sendChangeTitle(this, titleID):
        for title in this.titleList:
            if str(title).split(".")[0] != titleID:
                continue
            if not this.TitleNumber == int(titleID):
                this.TitleNumber = int(titleID)
                this.TitleStars = int(str(title).split(".")[1])
                this.sendPacket(Identifiers.send.Change_Title, ByteArray().writeByte(
                    this.gender).writeShort(titleID).toByteArray())

    def sendMessage(this, message, tab=False, *args):
        p = ByteArray().writeBool(tab).writeUTF(message).writeByte(len(args))
        for arg in args:
            p.writeUTF(arg)
        this.sendPacket(Identifiers.send.Recv_Message, p.toByteArray())

    def sendProfile(this, playerName):
        player = this.server.players.get(playerName)
        if player != None and not player.isGuest:
            packet = ByteArray().writeUTF(player.Username).writeInt(player.playerID).writeInt(player.regDate).writeByte(
                {1: 1, 2: 1, 3: 13, 4: 13, 5: 11, 6: 11, 7: 5, 8: 5, 9: 10, 10: 10, 11: 10, 12: 12}[player.privLevel]).writeByte(player.gender).writeUTF(player.tribeName).writeUTF(player.marriage)
            for stat in [player.shamanSaves, player.shamanCheeses, player.firstCount, player.cheeseCount, player.hardModeSaves, player.bootcampCount, player.divineModeSaves]:
                packet.writeInt(stat)

            packet.writeShort(player.TitleNumber).writeShort(
                len(player.titleList))
            for title in player.titleList:
                packet.writeShort(int(title - title % 1))
                packet.writeByte(int(round(title % 1 * 10)))

            packet.writeUTF(player.playerLook + ';' + player.MouseColor)
            packet.writeShort(player.shamanLevel)
            packet.writeShort(len(list(player.shopBadges)) * 2)
            badges = map(int, player.shopBadges)
            for badge in [120, 121, 122, 123, 124, 125, 126, 127, 145, 42, 54, 55, 0, 1, 6, 7, 9, 16, 17, 18, 28, 29, 30, 33, 34, 35, 46, 47, 50, 51, 57, 58, 59, 64, 65, 69, 71, 73, 129, 130, 131, 132, 133, 134, 139, 142, 144, 147, 153, 154, 158, 161, 162, 169, 170]:
                if badge in badges:
                    packet.writeShort(badge).writeShort(player.racingStats[0] / 1500 if badge == 124 else (player.racingStats[1] / 10000 if badge == 125 else (player.racingStats[2] / 10000 if badge == 127 else (player.racingStats[3] / 10000 if badge == 126 else (
                        player.survivorStats[0] / 1000 if badge == 120 else (player.survivorStats[1] / 800 if badge == 121 else (player.survivorStats[2] / 20000 if badge == 122 else (player.survivorStats[3] / 10000 if badge == 123 else 0))))))))
                    badges.remove(int(badge))

            for badge in badges:
                packet.writeShort(badge).writeShort(player.racingStats[0] / 1500 if badge == 124 else (player.racingStats[1] / 10000 if badge == 125 else (player.racingStats[2] / 10000 if badge == 127 else (player.racingStats[3] / 10000 if badge == 126 else (
                    player.survivorStats[0] / 1000 if badge == 120 else (player.survivorStats[1] / 800 if badge == 121 else (player.survivorStats[2] / 20000 if badge == 122 else (player.survivorStats[3] / 10000 if badge == 123 else 0))))))))

            stats = [[30, player.racingStats[0], 1500, 124], [31, player.racingStats[1], 10000, 125], [33, player.racingStats[2], 10000, 127], [32, player.racingStats[3], 10000, 126], [
                26, player.survivorStats[0], 1000, 120], [27, player.survivorStats[1], 800, 121], [28, player.survivorStats[2], 20000, 122], [29, player.survivorStats[3], 10000, 123]]
            packet.writeByte(len(stats))
            for stat in stats:
                packet.writeByte(stat[0]).writeInt(
                    stat[1]).writeInt(stat[2]).writeByte(stat[3])

            #shamanBadges = range(1, 31)
            shamanBadges = []
            packet.writeByte(player.equipedShamanBadge).writeByte(
                len(shamanBadges))
            for shamanBadge in shamanBadges:
                packet.writeByte(shamanBadge)

            count = 0
            for c in player.aventurePoints.values():
                count += c
            packet.writeBool(True).writeInt(count)

            this.sendPacket(Identifiers.send.Profile, packet.toByteArray())

    def sendPlayerBan(this, hours, reason, silent):
        this.sendPacket(Identifiers.old.send.Player_Ban,
                        [3600000 * hours, reason])
        if not silent and this.room != None:
            for player in this.room.clients.values():
                player.sendLangueMessage(
                    "", "<ROSE>$Message_Ban", this.Username, str(hours), reason)

        if hours >= 1081:
            this.server.disconnectIPAddress(this.ipAddress)

    def sendPlayerEmote(this, emoteID, flag, others, lua):
        p = ByteArray().writeInt(this.playerCode).writeByte(emoteID)
        if not flag == "":
            p.writeUTF(flag)
        result = p.writeBool(lua).toByteArray()

        this.room.sendAllOthers(this, Identifiers.send.Player_Emote, result) if others else this.room.sendAll(
            Identifiers.send.Player_Emote, result)

    def sendEmotion(this, emotion):
        this.room.sendAllOthers(this, Identifiers.send.Emotion, ByteArray(
        ).writeInt(this.playerCode).writeByte(emotion).toByteArray())

    def sendPlaceObject(this, objectID, code, px, py, angle, vx, vy, dur, sendAll):
        p = ByteArray().writeInt(objectID).writeShort(code).writeShort(px).writeShort(
            py).writeShort(angle).writeByte(vx).writeByte(vy).writeBool(dur)
        p.writeByte(0) if this.isGuest or sendAll else p.writeBytes(
            this.shopModule.getShamanItemCustom(code))

        if not sendAll:
            this.room.sendAllOthers(
                this, Identifiers.send.Spawn_Object, p.toByteArray())
            this.room.objectID = objectID
        else:
            this.room.sendAll(Identifiers.send.Spawn_Object, p.toByteArray())

    def sendAllModerationChat(this, type, message):
        playerName = "" if type == 0 else "Message Serveur" if type == 1 else this.Username
        this.server.sendStaffChat(type, this.Langue, Identifiers.send.Staff_Chat, ByteArray().writeByte(
            1 if type == -1 else type).writeUTF(playerName).writeUTF(message).writeShort(0).writeShort(0).toByteArray())

    def sendTotem(this, totem, x, y, playerCode):
        this.sendPacket(Identifiers.old.send.Totem, [
                        str(playerCode) + "#" + str(x) + "#" + str(y) + totem])

    def sendTotemItemCount(this, number):
        if this.room.isTotemEditeur:
            this.sendPacket(Identifiers.old.send.Totem_Item_Count, ByteArray(
            ).writeShort(number * 2).writeShort(0).toByteArray())

    def initTotemEditeur(this):
        if this.RTotem:
            this.sendTotemItemCount(0)
            this.RTotem = False
        else:
            if not this.STotem[1] == "":
                this.Totem[0] = this.STotem[0]
                this.Totem[1] = this.STotem[1]
                this.sendTotemItemCount(int(this.STotem[0]))
                this.sendTotem(this.STotem[1], 400, 202, this.playerCode)
            else:
                this.sendTotemItemCount(0)

    def sendShamanType(this, mode, canDivine):
        this.sendPacket(Identifiers.send.Shaman_Type, ByteArray().writeByte(
            mode).writeBool(canDivine).writeInt(int(this.ShamanColor, 16)).toByteArray())

    def sendBanConsideration(this):
        this.sendPacket(Identifiers.old.send.Ban_Consideration, ["0"])

    def sendShamanPosition(this, direction):
        this.room.sendAll(Identifiers.send.Shaman_Position, ByteArray().writeInt(
            this.playerCode).writeBool(direction).toByteArray())

    def getJson(this, mode, objects):
        if mode in 'dumps':
            return json.dumps(objects)

    def getLookUser(this, name):
        for room in this.server.rooms.values():
            for client in room.clients.values():
                if client.Username == name:
                    return client.playerLook
        this.Cursor.execute(
            'SELECT Look FROM users WHERE Username = ?', [name])
        return this.Cursor.fetchone()[0]

    def loadCafeMode(this):
        can = not this.isGuest
        #can = this.privLevel >= 5 or (this.Langue.upper(
        #) == this.realLangue and this.privLevel != 0 and this.cheeseCount >= 100)
        if not can:
            this.sendLangueMessage("", "<ROSE>$PasAutoriseParlerSurServeur")
        this.sendPacket(Identifiers.send.Open_Cafe,
                        ByteArray().writeBool(can).toByteArray())

        p = ByteArray()
        this.Cursor.execute(
            "select * from CafeTopics where Langue = ? order by Date desc limit 0, 20", [this.Langue])
        for rs in this.Cursor.fetchall():
            p.writeInt(rs["TopicID"]).writeUTF(rs["Title"]).writeInt(this.server.getPlayerID(rs["Author"])).writeInt(
                rs["Posts"]).writeUTF(rs["LastPostName"]).writeInt(TFMUtils.getSecondsDiff(rs["Date"]))
        this.sendPacket(Identifiers.send.Cafe_Topics_List, p.toByteArray())

    def openCafeTopic(this, topicID):
        p = ByteArray().writeBool(True).writeInt(topicID)
        this.Cursor.execute(
            "select * from CafePosts where TopicID = ? order by PostID asc", [topicID])
        for rs in this.Cursor.fetchall():
            p.writeInt(rs["PostID"]).writeInt(this.server.getPlayerID(rs["Name"])).writeInt(TFMUtils.getSecondsDiff(rs["Date"])).writeUTF(
                rs["Name"]).writeUTF(rs["Post"]).writeBool(str(this.playerCode) not in rs["Votes"].split(",")).writeShort(rs["Points"])
        this.sendPacket(Identifiers.send.Open_Cafe_Topic, p.toByteArray())

    def createNewCafeTopic(this, title, message):
        this.server.lastTopicID += 1
        this.Cursor.execute("insert into CafeTopics values (?, ?, ?, '', 0, ?, ?)", [
                            this.server.lastTopicID, "* Mensagem suspeita oculta *" if this.server.checkMessage(this, title) else title, this.Username, TFMUtils.getTime(), this.Langue])
        this.server.updateConfig()
        this.createNewCafePost(
            this.server.lastTopicID, "* Mensagem suspeita oculta *" if this.server.checkMessage(this, message) else message)
        this.loadCafeMode()

    def createNewCafePost(this, topicID, message):
        commentsCount = 0
        this.server.lastPostID += 1
        this.Cursor.execute("insert into CafePosts values (?, ?, ?, ?, ?, 0, ?)", [
                            this.server.lastPostID, topicID, this.Username, "* Mensagem suspeita oculta *" if this.server.checkMessage(this, message) else message, TFMUtils.getTime(), str(this.playerCode)])
        this.Cursor.execute("update CafeTopics set Posts = Posts + 1, LastPostName = ?, Date = ? where TopicID = ?", [
                            this.Username, TFMUtils.getTime(), topicID])
        this.Cursor.execute(
            "select count(*) as count from CafePosts where TopicID = ?", [topicID])
        rs = this.Cursor.fetchone()
        commentsCount = rs["count"]
        this.openCafeTopic(topicID)
        for client in this.server.players.values():
            if client.isCafe:
                client.sendPacket(Identifiers.send.Cafe_New_Post, ByteArray().writeInt(
                    topicID).writeUTF(this.Username).writeInt(commentsCount).toByteArray())

    def voteCafePost(this, topicID, postID, mode):
        this.Cursor.execute("update cafeposts set Points = Points %s 1, Votes = (case when Votes = '' then ? else (Votes || ?) end) where TopicID = ? and PostID = ?" % (
            "+" if mode else "-"), [this.playerCode, ","+str(this.playerCode), topicID, postID])
        this.openCafeTopic(topicID)

    def deleteCafePost(this, topicID, postID):
        this.Cursor.execute(
            "delete from CafePosts where TopicID = ? and PostID = ?", [topicID, postID])
        this.sendPacket(Identifiers.send.Delete_Cafe_Message, ByteArray(
        ).writeInt(topicID).writeInt(postID).toByteArray())
        this.openCafeTopic(topicID)

    def deleteAllCafePost(this, topicID, playerName):
        this.Cursor.execute("delete from CafePosts where TopicID = ? and Name = ?", [
                            topicID, playerName])
        this.Cursor.execute(
            "delete from CafeTopics where TopicID = ?", [topicID])
        this.loadCafeMode()
        this.openCafeTopic(topicID)

    def sendLangueMessage(this, message1, message2, *args):
        p = ByteArray().writeUTF(message1).writeUTF(message2).writeByte(len(args))
        for arg in args:
            p.writeUTF(arg)
        this.sendPacket(Identifiers.send.Message_Langue, p.toByteArray())

    def sendVampireMode(this, others):
        this.isVampire = True

        if this.room.L != None:
            this.room.L.execute("""
            if (type(eventPlayerVampire) == "function") then
                eventPlayerVampire('"""+str(this.Username)+"""')
            end
            """)

        d = ByteArray().writeInt(this.playerCode)
        if others:
            this.room.sendAllOthers(
                this, Identifiers.send.Vampire_Mode, d.toByteArray())
        else:
            this.room.sendAll(Identifiers.send.Vampire_Mode, d.toByteArray())

    def sendRemoveCheese(this):
        this.room.sendAll(Identifiers.send.Player_Get_Cheese, ByteArray(
        ).writeInt(this.playerCode).writeBool(False).toByteArray())

    def sendLuaMessage(this, message: str):
        this.sendPacket(Identifiers.send.Lua_Message,
                        ByteArray().writeUTF(str(message)).toByteArray())

    def sendLuaMessageAdmin(this, message: str):
        for client in this.server.players.values():
            if client.privLevel >= 10:
                client.sendPacket(Identifiers.send.Lua_Message,
                                  ByteArray().writeUTF(str(message)).toByteArray())

    def sendGameMode(this, mode):
        mode = 1 if mode == 0 else mode
        types = [1, 3, 8, 9, 2, 10, 16]
        p = ByteArray().writeByte(len(types))
        for roomType in types:
            p.writeByte(roomType)

        p.writeByte(mode)
        modeInfo = this.server.getPlayersCountMode(mode)
        if not modeInfo[0] == "" and not mode == 18:
            roomsCount = 0
            p.writeByte(1).writeByte(this.langueByte).writeUTF(
                str(modeInfo[0])).writeUTF(str(modeInfo[1])).writeUTF("mjj").writeUTF("1")
            for checkRoom in this.server.rooms.values():
                if ((checkRoom.isNormRoom or not checkRoom.isNormRoom) and not checkRoom.isTutorial if mode == 1 else checkRoom.isVanilla if mode == 3 else checkRoom.isSurvivor if mode == 8 else checkRoom.isRacing or checkRoom.isFastRacing if mode == 9 else checkRoom.isMusic if mode == 11 else checkRoom.isBootcamp if mode == 2 else checkRoom.isDefilante if mode == 10 else checkRoom.isVillage):
                    roomsCount += 1
                    p.writeByte(0).writeByte(0).writeUTF(checkRoom.roomName).writeShort(
                        checkRoom.getPlayerCount()).writeByte(checkRoom.maxPlayers).writeBool(checkRoom.isFuncorp)

            if roomsCount == 0:
                p.writeByte(0).writeByte(0).writeUTF(("" if mode == 1 else str(
                    modeInfo[0].split(" ")[1])) + "1").writeShort(0).writeByte(200).writeBool(False)
                if mode == 9:
                    p.writeByte(0).writeByte(0).writeUTF("fastracing1").writeShort(
                        0).writeByte(200).writeBool(False)

        if mode == 18:
            minigamesList = {}
            minigames = ["ffarace", "deathmatch", "tribewar", "invocation",
                         "explosion", "ballonrace", "fly", "pokelua", "utility"]
            roomsList = {}
            for minigame in minigames:
                minigame = "#" + minigame
                minigamesList[minigame] = 0
                for checkRoom in this.server.rooms.values():
                    if checkRoom.roomName.startswith(minigame) and checkRoom.community == this.Langue.lower():
                        minigamesList[minigame] += checkRoom.getPlayerCount()
                        roomsList[checkRoom.roomName] = [
                            checkRoom.getPlayerCount(), checkRoom.maxPlayers, checkRoom.isFuncorp]

            for minigame, count in minigamesList.items():
                p.writeByte(1).writeByte(0).writeUTF(str(minigame)).writeUTF(str(count)).writeUTF("mjj").writeUTF(
                    (minigame + "00" + this.Username.lower() if minigame == "#utility" or minigame == "#pokelua" else minigame))

            for minigame, count in roomsList.items():
                p.writeByte(0).writeByte(0).writeUTF(minigame).writeShort(
                    count[0]).writeByte(count[1]).writeBool(count[2])

        this.sendPacket(Identifiers.send.Game_Mode, p.toByteArray())

    def sendMusicVideo(this, id, sendAll=True):
        if id != 0:
            music = this.room.musicVideos[id - 1]
            p = ByteArray().writeUTF(str(music["id"].encode("UTF-8"))).writeUTF(str(music["title"].encode(
                "UTF-8"))).writeShort(this.room.musicTime).writeUTF(str(music["by"].encode("UTF-8")))
            if sendAll:
                this.room.musicSkipVotes = 0
                this.room.sendAll(
                    Identifiers.send.Music_Video, p.toByteArray())
            else:
                this.sendPacket(Identifiers.send.Music_Video, p.toByteArray())

    def checkMusicSkip(this):
        if this.room.isMusic and this.room.currentMusicID != 0:
            count = this.room.getPlayersCount()
            count = count if count % 2 == 0 else count + 1
            if this.room.musicSkipVotes == count / 2:
                this.room.musicVideos.remove(this.room.currentMusicID)
                this.sendMusicVideo(this.room.currentMusicID + 1, True)

    def sendStaffMessage(this, message, othersLangues, tab=False):
        for player in this.server.players.values():
            if othersLangues or player.Langue == this.Langue:
                player.sendMessage(message, tab)

    def sendStaffMessageGlobal(this, message, othersLangues):
        for player in this.server.players.values():
            if othersLangues or player.Langue == this.Langue:
                player.sendLangueMessage("", message)

    def sendBulle(this):
        this.sendPacket(Identifiers.send.Bulle, ByteArray().writeInt(
            2).writeUTF("").writeInt(5).toByteArray())

    def checkVip(this, vipTime):
        days = TFMUtils.getDiffDays(vipTime)
        if days <= 0:
            this.privLevel = 1
            if this.TitleNumber == 1100:
                this.TitleNumber = 0

            this.sendMessage("O seu VIP se estogou.")
            this.Cursor.execute(
                "update users set VipTime = 0 where Username = ?", [this.Username])
        else:
            this.sendMessage("Você ainda tem <V>" + str(days) +
                             "</V> dias de privilégio VIP!")

    def updateTribePoints(this):
        this.Cursor.execute(
            "update Tribe set Points = Points + ? where Code = ?", [this.tribePoints, this.tribeCode])
        this.tribePoints = 0

    def sendLogMessage(this, message):
        this.sendPacket(Identifiers.send.Log_Message, ByteArray().writeByte(0).writeUTF("").writeByte((len(message) >> 16) & 0xFF).writeByte(
            (len(message) >> 8) & 0xFF).writeByte(len(message) & 0xFF).writeBytes(message).toByteArray())

    def addConjuration(this, x, y, time):
        this.room.sendAll(Identifiers.old.send.Add_Conjuration, [int(x), int(y)])
        TFMUtils.callLater(int(time), this.sendConjurationDestroy, int(x), int(y))

    def disableAfkDeath(this, v):
        if isinstance(v, bool):
            this.room.disableAfkKill = v
            
    def disableAllShamanSkills(this, v):
        if isinstance(v, bool):
            this.room.noShamanSkills = v
            
    def disableAutoNewGame(this, v):
        if isinstance(v, bool):
            this.room.specificMap = v
            
    def disableAutoScore(this, v):
        if isinstance(v, bool):
            this.room.noAutoScore = v
            
    def disableAutoShaman(this, v):
        if isinstance(v, bool):
            this.room.noShaman = v
            
    def disableAutoTimeLeft(this, v):
        if isinstance(v, bool):
            this.room.never20secTimer = v

    def explosionPlayer(this, posX, posY):
        this.sendPacket([5, 17], ByteArray().writeShort(int(posX)).writeByte(0).writeShort(33842).writeShort(int(posY)).writeBool(True).toByteArray())
        
    def killPlayer(this, player):
        for client in this.server.players.values():
            if client.Username == player and this.room == client.room:
                if not client.isDead:
                    client.isDead = True
                    if not client.room.noAutoScore: client.playerScore += 1
                    client.sendPlayerDied()
                    
    def giveMeep(this, player):
        for client in this.server.players.values():
            if client.Username == player and this.room == client.room:
                client.sendPacket(Identifiers.send.Can_Meep, chr(1))
                
    def giveCheese(this, player):
        for client in this.server.players.values():
            if client.Username == player and this.room == client.room:
                client.room.sendAll(Identifiers.send.Player_Get_Cheese, ByteArray(
                    ).writeInt(client.playerCode).writeBool(True).toByteArray())
                client.hasCheese = True

    def newGame(this, v='@0'):
        if v.startswith('#'):
            this.room.mapPerma = int(v[1:])
            
            if this.room.changeMapTimer != None:
                this.room.changeMapTimer.cancel()
            this.room.mapChange()
        elif str(v).replace(' ','').startswith('<C>'):
            this.room.mapCode = 0
            this.room.mapName = "#Module"
            this.room.mapXML = v
            this.room.mapYesVotes = 0
            this.room.mapNoVotes = 0
            this.room.mapPerma = 1
            this.room.mapInverted = False
            
            if this.room.changeMapTimer != None:
                this.room.changeMapTimer.cancel()
            this.room.mapChange()
        else:
            try:
                if v.isdigit():
                    v='@'+str(v)
            except:
                if type(v) in int:
                    v='@'+str(v)
                    
            if v.startswith("@"):
                mapInfo = this.room.getMapInfo(int(v[1:]))
                if mapInfo[0] == None:
                    this.sendLangueMessage("", "$CarteIntrouvable")
                else:
                    this.room.forceNextMap = v
                    if this.room.changeMapTimer != None:
                        this.room.changeMapTimer.cancel()
                    this.room.mapChange()
                                        
    def sendChatMessage(this, message, player=None):
        if player != None:
            for client in this.server.players.values():
                if client.Username == player and this.room == client.room:
                    client.sendMessage(message)
        else:
            for client in this.server.players.values():
                if this.room == client.room:
                    client.sendMessage(message)

    def LuaExit(this):
        this.parseCommands.parseCommand("module stop")

    def updateLua(this):
        if not this.room.L is None:
            if not this._G is None:
                for client in this.room.clients.values():
                    this._G['tfm']['get']['room'].playerList[client.Username.replace('#','_')] = this.room.L.eval("{}")
                    this._G['tfm']['get']['room'].playerList[client.Username.replace('#','_')].community = client.Langue
                    this._G['tfm']['get']['room'].playerList[client.Username.replace('#','_')].hasCheese = client.hasCheese
                    this._G['tfm']['get']['room'].playerList[client.Username.replace('#','_')].id = client.playerID
                    this._G['tfm']['get']['room'].playerList[client.Username.replace('#','_')].tag = client.Username.split('#')[1]
                    this._G['tfm']['get']['room'].playerList[client.Username.replace('#','_')].isDead = client.isDead
                    this._G['tfm']['get']['room'].playerList[client.Username.replace('#','_')].isJumping = (client.isJumping)
                    this._G['tfm']['get']['room'].playerList[client.Username.replace('#','_')].isShaman = (client.isShaman)
                    this._G['tfm']['get']['room'].playerList[client.Username.replace('#','_')].isVampire = (client.isJumping)
                    this._G['tfm']['get']['room'].playerList[client.Username.replace('#','_')].look = client.playerLook
                    this._G['tfm']['get']['room'].playerList[client.Username.replace('#','_')].movingLeft = client.isMovingLeft
                    this._G['tfm']['get']['room'].playerList[client.Username.replace('#','_')].movingLeft = client.isMovingRight
                    this._G['tfm']['get']['room'].playerList[client.Username.replace('#','_')].playerName = client.Username.split('#')[0]
                    this._G['tfm']['get']['room'].playerList[client.Username.replace('#','_')].registrationDate = client.regDate
                    this._G['tfm']['get']['room'].playerList[client.Username.replace('#','_')].score = client.playerScore
                    this._G['tfm']['get']['room'].playerList[client.Username.replace('#','_')].shamanMode = client.Totem[0]
                    this._G['tfm']['get']['room'].playerList[client.Username.replace('#','_')].title = client.TitleNumber
                    this._G['tfm']['get']['room'].playerList[client.Username.replace('#','_')].x = client.posX
                    this._G['tfm']['get']['room'].playerList[client.Username.replace('#','_')].y = client.posY
            this.room.L.execute("""
            if (type(eventLoop) == "function") then
                eventLoop("""+str((time.time()-this.room.gameStartTimeMillis)*1000)+""", """+str((this.room.roundTime*1000)-(time.time()-this.room.gameStartTimeMillis)*1000)+""")
            end
            """)
            TFMUtils.callLater(0.2, this.updateLua)
        else:
            this.room.disableAfkKill = this._MapDefinitions['disableAfkKill']
            this.room.noShamanSkills = this._MapDefinitions['noShamanSkills']
            this.room.specificMap = this._MapDefinitions['specificMap']
            this.room.noAutoScore = this._MapDefinitions['noAutoScore']
            this.room.noShaman = this._MapDefinitions['noShaman']
            this.room.never20secTimer = this._MapDefinitions['never20secTimer']
            
            this._MapDefinitions = None
            this._G = None

    def runLuaScript(this, script, roomLoad = False):
        try:
            if not this.isLuaAdmin:
                this.parseCommands.parseCommand("module stop")
                this.room.L = LuaRuntime()
                this._G = this.room.L.globals()
                if this._G != None:
                    this._G['io'] = None
                    this._G['print'] = this.sendLuaMessage
                    this._G['system'] = this.room.L.eval('{}')
                    this._G['system'].disableChatCommandDisplay = this.room.bindKeyBoard
                    this._G['system'].bindKeyboard = this.room.bindKeyBoard
                    this._G['system'].bindMouse = this.room.bindMouse
                    this._G['system'].exit = this.LuaExit

                    this._G['os'] = this.room.L.eval('{}')
                    this._G['os']['time'] = TFMUtils.getTime
                    this._G['os']['date'] = TFMUtils.getDate

                    this._G['debug'] = this.room.L.eval('{}')
                    this._G['debug']['disableEventLog'] = not this.room.disableEventLog
                    this._G['debug']['disableTimerLog'] = this.room.L.eval('{}')

                    this._G['ui'] = this.room.L.eval('{}')
                    this._G['ui']['addPopup'] = this.room.addPopup
                    this._G['ui']['addTextArea'] = this.room.addTextArea

                    this._G['ui']['updateTextArea'] = this.room.updateTextArea

                    this._G['ui']['removeTextArea'] = this.room.removeTextArea

                    this._G['ui']['setMapName'] = this.room.setMapName
                    this._G['ui']['setShamanName'] = this.room.setShamanName

                    this._G['ui']['showColorPicker'] = this.room.showColorPicker

                    this._MapDefinitions = dict()
                    this._MapDefinitions['disableAfkKill'] = this.room.disableAfkKill
                    this._MapDefinitions['specificMap'] = this.room.specificMap
                    this._MapDefinitions['never20secTimer'] = this.room.never20secTimer

                    this._MapDefinitions['noShamanSkills'] = this.room.noShamanSkills
                    this._MapDefinitions['noAutoScore'] = this.room.noAutoScore
                    this._MapDefinitions['noShaman'] = this.room.noShaman

                    this._G['tfm'] = this.room.L.eval('{}')                
                    this._G['tfm']['exec'] = this.room.L.eval('{}')
                    this._G['tfm']['exec'].addConjuration = this.addConjuration
                    this._G['tfm']['exec'].addPhysicObject = this.room.addPhysicObject
                    this._G['tfm']['exec'].addShamanObject = this.sendPlaceObject

                    this._G['tfm']['exec'].disableAfkDeath = this.disableAfkDeath
                    this._G['tfm']['exec'].disableAllShamanSkills = this.disableAllShamanSkills
                    this._G['tfm']['exec'].disableAutoNewGame = this.disableAutoNewGame
                    this._G['tfm']['exec'].disableAutoScore = this.disableAutoScore
                    this._G['tfm']['exec'].disableAutoShaman = this.disableAutoShaman
                    this._G['tfm']['exec'].disableAutoTimeLeft = this.disableAutoTimeLeft

                    this._G['tfm']['exec'].giveMeep = this.giveMeep
                    this._G['tfm']['exec'].giveCheese = this.giveCheese

                    this._G['tfm']['exec'].setNameColor = this.room.setNameColor
                    this._G['tfm']['exec'].setGameTime = this.room.setGameTime

                    this._G['tfm']['exec'].explosion = this.explosionPlayer
                    this._G['tfm']['exec'].killPlayer = this.killPlayer
                    this._G['tfm']['exec'].movePlayer = this.room.movePlayer
                    this._G['tfm']['exec'].newGame = this.newGame

                    if this.privLevel >= 3 or roomLoad:
                        this._G['tfm']['exec'].chatMessage = this.sendChatMessage
                        this._G['tfm']['exec'].addImage = this.room.addImageLUA
                        this._G['tfm']['exec'].removeImage = this.room.removeImage

                    this._G['tfm']['get'] = this.room.L.eval('{}')
                    this._G['tfm']['get']['misc'] = this.room.L.eval('{}')
                    this._G['tfm']['get']['misc'].apiVersion = 0.2
                    this._G['tfm']['get']['misc'].transformiceVersion = int(this.server.Version)
                    this._G['tfm']['get']['misc'].playerWhoLoadedScript = this.Username

                    this._G['tfm']['get']['room'] = this.room.L.eval('{}')
                    this._G['tfm']['get']['room'].community = this.room.community
                    this._G['tfm']['get']['room'].currentMap = this.room.currentMap
                    this._G['tfm']['get']['room'].maxPlayers = this.room.maxPlayers
                    this._G['tfm']['get']['room'].mirroredMap = this.room.mapInverted
                    this._G['tfm']['get']['room'].name = this.room.name
                    this._G['tfm']['get']['room'].passwordProtected = (this.room.roomPassword != "")
                    this._G['tfm']['get']['room'].objectList = this.room.L.eval("{}")
                    this._G['tfm']['get']['room'].playerList = this.room.L.eval("{}")

                    this._G['tfm']['enum'] = this.room.L.eval('{}')
                    this._G['tfm']['enum']['emote'] = this.room.L.eval('{}')
                    this._G['tfm']['enum']['emote'].dance = 0
                    this._G['tfm']['enum']['emote'].laugh = 1
                    this._G['tfm']['enum']['emote'].cry = 2
                    this._G['tfm']['enum']['emote'].kiss = 3
                    this._G['tfm']['enum']['emote'].angry = 4
                    this._G['tfm']['enum']['emote'].clap = 5
                    this._G['tfm']['enum']['emote'].sleep = 6
                    this._G['tfm']['enum']['emote'].facepaw = 7
                    this._G['tfm']['enum']['emote'].sit = 8
                    this._G['tfm']['enum']['emote'].confetti = 9
                    this._G['tfm']['enum']['emote'].flag = 10
                    this._G['tfm']['enum']['emote'].marshmallow = 11
                    this._G['tfm']['enum']['emote'].selfie = 12

                    this._G['tfm']['enum']['shamanObject'] = this.room.L.eval('{}')
                    this._G['tfm']['enum']['shamanObject'].arrow = 0
                    this._G['tfm']['enum']['shamanObject'].littleBox = 1
                    this._G['tfm']['enum']['shamanObject'].box = 2
                    this._G['tfm']['enum']['shamanObject'].littleBoard = 3
                    this._G['tfm']['enum']['shamanObject'].board = 4
                    this._G['tfm']['enum']['shamanObject'].ball = 6
                    this._G['tfm']['enum']['shamanObject'].trampoline = 7
                    this._G['tfm']['enum']['shamanObject'].anvil = 10
                    this._G['tfm']['enum']['shamanObject'].cannon = 17
                    this._G['tfm']['enum']['shamanObject'].bomb = 23
                    this._G['tfm']['enum']['shamanObject'].bluePortal = 26
                    this._G['tfm']['enum']['shamanObject'].orangePortal = 27
                    this._G['tfm']['enum']['shamanObject'].balloon = 28
                    this._G['tfm']['enum']['shamanObject'].blueBalloon = 28
                    this._G['tfm']['enum']['shamanObject'].redBalloon = 29
                    this._G['tfm']['enum']['shamanObject'].greenBalloon = 30
                    this._G['tfm']['enum']['shamanObject'].yellowBalloon = 31
                    this._G['tfm']['enum']['shamanObject'].rune = 32
                    this._G['tfm']['enum']['shamanObject'].chicken = 33
                    this._G['tfm']['enum']['shamanObject'].snowBall = 34
                    this._G['tfm']['enum']['shamanObject'].cupidonArrow = 35
                    this._G['tfm']['enum']['shamanObject'].apple = 39
                    this._G['tfm']['enum']['shamanObject'].sheep = 40
                    this._G['tfm']['enum']['shamanObject'].littleBoardIce = 45
                    this._G['tfm']['enum']['shamanObject'].littleBoardChocolate = 46
                    this._G['tfm']['enum']['shamanObject'].iceCube = 54
                    this._G['tfm']['enum']['shamanObject'].cloud = 57
                    this._G['tfm']['enum']['shamanObject'].bubble = 59
                    this._G['tfm']['enum']['shamanObject'].tinyBoard = 60
                    this._G['tfm']['enum']['shamanObject'].companionCube = 61
                    this._G['tfm']['enum']['shamanObject'].stableRune = 62
                    this._G['tfm']['enum']['shamanObject'].balloonFish = 65
                    this._G['tfm']['enum']['shamanObject'].longBoard = 67
                    this._G['tfm']['enum']['shamanObject'].triangle = 68
                    this._G['tfm']['enum']['shamanObject'].sBoard = 69
                    this._G['tfm']['enum']['shamanObject'].paperPlane = 80
                    this._G['tfm']['enum']['shamanObject'].rock = 85
                    this._G['tfm']['enum']['shamanObject'].pumpkinBall = 89
                    this._G['tfm']['enum']['shamanObject'].tombstone = 90
                    this._G['tfm']['enum']['shamanObject'].paperBall = 95

                    this._G['tfm']['enum']['ground'] = this.room.L.eval('{}')
                    this._G['tfm']['enum']['ground'].wood = 0
                    this._G['tfm']['enum']['ground'].ice = 1
                    this._G['tfm']['enum']['ground'].trampoline = 2
                    this._G['tfm']['enum']['ground'].lava = 3
                    this._G['tfm']['enum']['ground'].chocolate = 4
                    this._G['tfm']['enum']['ground'].earth = 5
                    this._G['tfm']['enum']['ground'].grass = 6
                    this._G['tfm']['enum']['ground'].sand = 7
                    this._G['tfm']['enum']['ground'].cloud = 8
                    this._G['tfm']['enum']['ground'].water = 9
                    this._G['tfm']['enum']['ground'].stone = 10
                    this._G['tfm']['enum']['ground'].snow = 11
                    this._G['tfm']['enum']['ground'].rectangle = 12
                    this._G['tfm']['enum']['ground'].circle = 13
                    this._G['tfm']['enum']['ground'].invisible = 14
                    this._G['tfm']['enum']['ground'].web = 15

                    this._G['tfm']['enum']['particle'] = this.room.L.eval('{}')
                    this._G['tfm']['enum']['particle'].whiteGlitter = 0
                    this._G['tfm']['enum']['particle'].blueGlitter = 1
                    this._G['tfm']['enum']['particle'].orangeGlitter = 2
                    this._G['tfm']['enum']['particle'].cloud = 3
                    this._G['tfm']['enum']['particle'].dullWhiteGlitter = 4
                    this._G['tfm']['enum']['particle'].heart = 5
                    this._G['tfm']['enum']['particle'].bubble = 6
                    this._G['tfm']['enum']['particle'].tealGlitter = 9
                    this._G['tfm']['enum']['particle'].spirit = 10
                    this._G['tfm']['enum']['particle'].yellowGlitter = 11
                    this._G['tfm']['enum']['particle'].ghostSpirit = 12
                    this._G['tfm']['enum']['particle'].redGlitter = 13
                    this._G['tfm']['enum']['particle'].waterBubble = 14
                    this._G['tfm']['enum']['particle'].plus1 = 15
                    this._G['tfm']['enum']['particle'].plus10 = 16
                    this._G['tfm']['enum']['particle'].plus12 = 17
                    this._G['tfm']['enum']['particle'].plus14 = 18
                    this._G['tfm']['enum']['particle'].plus16 = 19
                    this._G['tfm']['enum']['particle'].meep = 20
                    this._G['tfm']['enum']['particle'].redConfetti = 21
                    this._G['tfm']['enum']['particle'].greenConfetti = 22
                    this._G['tfm']['enum']['particle'].blueConfetti = 23
                    this._G['tfm']['enum']['particle'].yellowConfetti = 24
                    this._G['tfm']['enum']['particle'].diagonalRain = 25
                    this._G['tfm']['enum']['particle'].curlyWind = 26
                    this._G['tfm']['enum']['particle'].wind = 27
                    this._G['tfm']['enum']['particle'].rain = 28
                    this._G['tfm']['enum']['particle'].star = 29
                    this._G['tfm']['enum']['particle'].littleRedHeart = 30
                    this._G['tfm']['enum']['particle'].littlePinkHeart = 31
                    this._G['tfm']['enum']['particle'].daisy = 32
                    this._G['tfm']['enum']['particle'].bell = 33
                    this._G['tfm']['enum']['particle'].egg = 34
                    this._G['tfm']['enum']['particle'].projection = 35
                    this._G['tfm']['enum']['particle'].mouseTeleportation = 36
                    this._G['tfm']['enum']['particle'].shamanTeleportation = 37
                    this._G['tfm']['enum']['particle'].lollipopConfetti = 38
                    this._G['tfm']['enum']['particle'].yellowCandyConfetti = 39
                    this._G['tfm']['enum']['particle'].pinkCandyConfetti = 40
                    
                this.room.L.execute(script.replace('while', '_while'))
                this.updateLua()
            else:
                exec(compile(str(script), "<string>", "exec"))

            startTime = int(time.time())
            endTime = int(time.time())
            totalTime = endTime - startTime

            if totalTime > 4000:
                this.sendLuaMessage("<V>["+this.room.roomName+"]<BL> ["+this.Username+"] Lua script not loaded. ("+str(totalTime)+" ms - 4000 max)")
            else:
                this.sendLuaMessage("<V>["+this.room.roomName+"]<BL> ["+this.Username+"] Lua script loaded in "+str(totalTime)+" ms (4000 max)")
        except Exception as error:
            this.sendLuaMessage("<V>["+this.room.roomName+"]<BL> ["+this.Username+"][Exception]: "+str(error))

    def reloadModule(this, module):
        try:
            for mod in sys.modules:
                if mod == module:
                    print(mod, module)
                    # reload(sys.modules[module])
                    if module == "ParseCommands":
                        reload(ParseCommands)
                        this.parseCommands = ParseCommands(this, this.server)
                        return True
            return False
        except Exception as ERROR:
            print(ERROR)

    def sendMBox(this, text, x, y, width, height, alpha, bgcolor, bordercolor, boxid, fixed=True):
        text = str(text)
        x, y, width, height = int(x), int(y), int(width), int(height)

        alpha = str(alpha).split("%")[0]
        alpha = int(alpha)

        if "#" in str(bgcolor):
            bgcolor = str(bgcolor[1:])
        else:
            pass
        if "#" in str(bordercolor):
            bordercolor = str(bordercolor[1:])
        else:
            pass
        bgcolor, bordercolor = int(bgcolor, 16), int(bordercolor, 16)

        this.sendPacket([29, 20], ByteArray().writeInt(int(boxid)).writeUTF(text).writeShort(x).writeShort(y).writeShort(
            width).writeShort(height).writeInt(bgcolor).writeInt(bordercolor).writeByte(alpha).writeShort(fixed).toByteArray())

    def sendAnimZelda(this, type, item):
        if type == 7:
            this.room.sendAll(Identifiers.send.Anim_Zelda, ByteArray().writeInt(
                this.playerCode).writeByte(type).writeUTF("$De6").writeByte(item).toByteArray())
        else:
            this.room.sendAll(Identifiers.send.Anim_Zelda, ByteArray().writeInt(
                this.playerCode).writeByte(type).writeInt(item).toByteArray())

    def sendAnimZeldaInventory(this, id1, id2, count):
        if id1 == 4:
            this.sendPacket([100, 67], ByteArray().writeByte(
                0).writeShort(id2).writeShort(count).toByteArray())
        this.room.sendAll([8, 44], ByteArray().writeInt(
            this.playerCode).writeByte(id1).writeInt(id2).toByteArray())

    def sendAnimZeldaInventoryx(this, id1, id2, count):
        if id1 == 4:
            this.sendPacket([100, 67], ByteArray().writeByte(
                0).writeShort(id2).writeShort(count).toByteArray())

    def premioVillage(this, coisa):
        if coisa[0] == 1:
            medal = coisa[1]
            if this.playerConsumables[coisa[4]] >= coisa[5]:
                if not int(medal) in this.shopBadges:
                    this.shopModule.sendUnlockedBadge(medal)
                    this.shopBadges.append(str(medal))
                    this.playerConsumables[coisa[4]] -= coisa[5]
        elif coisa[0] == 2:
            symbol = str(coisa[1])
            if not symbol in this.shamanBadges:
                if this.shamanBadges[0] == '':
                    this.shamanBadges = [symbol]
                else:
                    test = [symbol]
                    this.shamanBadges = this.shamanBadges + test
                this.playerConsumables[coisa[4]] -= coisa[5]
                this.sendAnimZeldaInventory(6, coisa[1], 1)
        elif coisa[0] == 3:
            titles = [str(coisa[1]) + ".1"]
            #titles = ["387.1"]
            title = random.choice(titles)
            while title in this.titleList:
                try:
                    titles.remove(title)
                    title = random.choice(titles)
                except:
                    break
            if not title in this.titleList:
                stitle = title.split(".")
                this.specialTitleList = this.specialTitleList + [title]
                this.sendUnlockedTitle(stitle[0], stitle[1])

                this.sendCompleteTitleList()
                this.sendTitleList()
        elif coisa[0] == 4:
            if this.playerConsumables[coisa[4]] >= coisa[5]:
                id = coisa[1]
                if not id in this.playerConsumables:
                    this.playerConsumables[id] = coisa[2]
                else:
                    count = this.playerConsumables[id] + coisa[2]
                    this.playerConsumables[id] = count
                this.playerConsumables[coisa[4]] -= coisa[5]
                this.sendAnimZeldaInventory(4, id, coisa[2])
        this.BotsVillage(this.botVillage)

    def BotsVillage(this, bot):
        itens = list()
        for item in this.itensBots[bot]:
            if item[0] == 1 and str(item[1]) in this.shopBadges:
                itens.append(item)
            elif item[0] == 2 and str(item[1]) in this.shamanBadges:
                itens.append(item)
            elif item[0] == 3 and str(item[1]) + ".1" in this.titleList:
                itens.append(item)
        for item in itens:
            this.itensBots[bot].remove(item)
        p = ByteArray()
        for items in this.itensBots[bot]:
            count = items[5]
            if items[4] in this.playerConsumables:
                one = 0 if this.playerConsumables[items[4]] >= count else 1
            else:
                one = 1
            p.writeByte(one).writeByte(items[0]).writeShort(items[1]).writeShort(
                items[2]).writeByte(items[3]).writeShort(items[4]).writeShort(items[5]).writeInt(0)
        this.sendPacket([26, 38], ByteArray().writeUTF(bot).writeByte(
            len(this.itensBots[bot])).toByteArray() + p.toByteArray())

    def sendInventoryConsumables(this):
        p = ByteArray().writeShort(len(this.playerConsumables))
        for id, count in this.playerConsumables.items():
            p.writeShort(int(id)).writeByte(250 if count > 250 else count).writeByte(0).writeBool(True).writeBool(False if id in this.server.inventory else True).writeBool(
                True).writeBool(True).writeBool(True).writeBool(False).writeBool(False).writeByte(this.equipedConsumables.index(int(id)) + 1 if int(id) in this.equipedConsumables else 0)
        this.sendPacket(Identifiers.send.Inventory, p.toByteArray())

    def updateInventoryConsumable(this, id, count):
        this.sendPacket(Identifiers.send.Update_Inventory_Consumable, ByteArray(
        ).writeShort(id).writeByte(250 if count > 250 else count).toByteArray())

    def useInventoryConsumable(this, id):
        if id == 29 or id == 30 or id == 2241:
            this.sendPacket(Identifiers.send.Use_Inventory_Consumable, ByteArray(
            ).writeInt(this.playerCode).writeShort(id).toByteArray())
        else:
            this.room.sendAll(Identifiers.send.Use_Inventory_Consumable, ByteArray(
            ).writeInt(this.playerCode).writeShort(id).toByteArray())

    def sendTradeResult(this, playerName, result):
        this.sendPacket(Identifiers.send.Trade_Result, ByteArray().writeUTF(
            playerName).writeByte(result).toByteArray())

    def sendTradeInvite(this, playerCode):
        this.sendPacket(Identifiers.send.Trade_Invite,
                        ByteArray().writeInt(playerCode).toByteArray())

    def sendTradeStart(this, playerCode):
        this.sendPacket(Identifiers.send.Trade_Start,
                        ByteArray().writeInt(playerCode).toByteArray())

    def tradeInvite(this, playerName):
        player = this.room.clients.get(playerName)
        if player != None and this.privLevel != 0 and player.privLevel != 0:
            if not player.isTrade:
                if not player.room.name == this.room.name:
                    this.sendTradeResult(playerName, 5)
                elif player.isTrade:
                    this.sendTradeResult(playerName, 0)
                else:
                    this.sendLangueMessage("", "$Demande_Envoyée")
                    player.sendTradeInvite(this.playerCode)

                this.tradeName = playerName
                this.isTrade = True
            else:
                this.tradeName = playerName
                this.isTrade = True
                this.sendTradeStart(player.playerCode)
                player.sendTradeStart(this.playerCode)

    def cancelTrade(this, playerName):
        player = this.room.clients.get(playerName)
        if player != None:
            this.tradeName = ""
            this.isTrade = False
            this.tradeConsumables = {}
            this.tradeConfirm = False
            player.tradeName = ""
            player.isTrade = False
            player.tradeConsumables = {}
            player.tradeConfirm = False
            player.sendTradeResult(this.Username, 2)

    def tradeAddConsumable(this, id, isAdd):
        player = this.room.clients.get(this.tradeName)
        if player != None and player.isTrade and player.tradeName == this.Username:
            if isAdd:
                if id in this.tradeConsumables.keys():
                    this.tradeConsumables[id] += 1
                else:
                    this.tradeConsumables[id] = 1
            else:
                count = this.tradeConsumables[id] - 1
                if count > 0:
                    this.tradeConsumables[id] = count
                else:
                    del this.tradeConsumables[id]

            player.sendPacket(Identifiers.send.Trade_Add_Consumable, ByteArray().writeBool(
                False).writeShort(id).writeBool(isAdd).writeByte(1).writeBool(False).toByteArray())
            this.sendPacket(Identifiers.send.Trade_Add_Consumable, ByteArray().writeBool(
                True).writeShort(id).writeBool(isAdd).writeByte(1).writeBool(False).toByteArray())

    def tradeResult(this, isAccept):
        player = this.room.clients.get(this.tradeName)
        if player != None and player.isTrade and player.tradeName == this.Username:
            this.tradeConfirm = isAccept
            player.sendPacket(Identifiers.send.Trade_Confirm, ByteArray(
            ).writeBool(False).writeBool(isAccept).toByteArray())
            this.sendPacket(Identifiers.send.Trade_Confirm, ByteArray(
            ).writeBool(True).writeBool(isAccept).toByteArray())
            if this.tradeConfirm and player.tradeConfirm:
                for consumable in player.tradeConsumables.items():
                    if consumable[0] in this.playerConsumables.keys():
                        this.playerConsumables[consumable[0]] += consumable[1]
                    else:
                        this.playerConsumables[consumable[0]] = consumable[1]

                    consumable = list(consumable)
                    count = player.playerConsumables[
                        consumable[0]] - consumable[1]
                    if count <= 0:
                        del player.playerConsumables[consumable[0]]
                        if consumable[0] in player.equipedConsumables:
                            player.equipedConsumables.remove(consumable[0])
                    else:
                        player.playerConsumables[consumable[0]] = consumable[1]

                for consumable in this.tradeConsumables.items():
                    if consumable[0] in player.playerConsumables.keys():
                        player.playerConsumables[
                            consumable[0]] += consumable[1]
                    else:
                        player.playerConsumables[consumable[0]] = consumable[1]

                    consumable = list(consumable)
                    count = this.playerConsumables[
                        consumable[0]] - consumable[1]
                    if count <= 0:
                        del this.playerConsumables[consumable[0]]
                        if consumable[0] in player.equipedConsumables:
                            this.equipedConsumables.remove(consumable[0])
                    else:
                        this.playerConsumables[consumable[0]] = consumable[1]

                player.tradeName = ""
                player.isTrade = False
                player.tradeConsumables = {}
                player.tradeConfirm = False
                player.sendPacket(Identifiers.send.Trade_Close)
                player.sendInventoryConsumables()
                this.tradeName = ""
                this.isTrade = False
                this.tradeConsumables = {}
                this.tradeConfirm = False
                this.sendPacket(Identifiers.send.Trade_Close)
                this.sendInventoryConsumables()

    def winEventMap(this):
        if 2245 in this.playerConsumables.keys():
            if this.playerConsumables[2245] == 5:
                this.sendGiveConsumable(2257, 1)
            elif this.playerConsumables[2245] == random.randint(1, 80):
                this.sendGiveConsumable(2240, 1)
            elif this.playerConsumables[2245] == random.randint(1, 80):
                this.sendGiveConsumable(800, 1)
            elif this.playerConsumables[2245] == 10:
                this.winTitleEvent(386)
            elif this.playerConsumables[2245] == 25:
                this.winBadgeEvent(134)
            elif this.playerConsumables[2245] == 35:
                this.winTitleEvent(297)
            elif this.playerConsumables[2245] == 45:
                this.sendGiveConsumable(801, 5)
            elif this.playerConsumables[2245] == 40:
                this.winBadgeEvent(131)
            elif this.playerConsumables[2245] == 70:
                this.winTitleEvent(417)
                this.sendGiveConsumable(2257, 20)
            elif this.playerConsumables[2245] == 80:
                this.winTitleEvent(418)
        # if 2238 in this.playerConsumables.keys():
            # if this.playerConsumables[2238] == 6:
                #this.sendGiveConsumable(2257, 1)
            # elif this.playerConsumables[2238] == 11:
                # this.winTitleEvent(386)

    def winBadgeEvent(this, badge):
        if not badge in this.shopBadges:
            this.sendAnimZelda(3, badge)
            this.shopBadges.append(badge)
            this.shopModule.checkAndRebuildBadges()
            this.shopModule.sendUnlockedBadge(badge)

    def winTitleEvent(this, title):
        if not title in this.specialTitleList:
            this.specialTitleList.append(title + 0.1)
            this.sendUnlockedTitle(title, 1)
            this.sendCompleteTitleList()
            this.sendTitleList()
            this.sendPacket([100, 72], ByteArray().writeByte(
                this.gender).writeShort(title).toByteArray())

    def sendGiveConsumable(this, consumable, count):
        this.sendAnimZelda(4, consumable)
        this.sendNewConsumable(consumable, count)
        if consumable in this.playerConsumables.keys():
            this.playerConsumables[consumable] += count
        else:
            this.playerConsumables[consumable] = count
        this.updateInventoryConsumable(consumable, count)

    def winConsumables(this):
        consumables = [2252, 2239, 2246, 2234, 35,
                       33, 28, 31, 34, 2240, 2247, 2262, 21]
        for x in consumables:
            this.sendGiveConsumable(x, 1)

    def giveConsumable(this, id, amount=80, limit=80):
        this.sendAnimZelda(4, id)
        sum = (this.playerConsumables[
               id] if id in this.playerConsumables.keys() else 0) + amount
        if limit != -1 and sum > limit:
            sum = limit
        if id in this.playerConsumables.keys():
            this.playerConsumables[id] = sum
        else:
            this.playerConsumables[id] = sum

        this.updateInventoryConsumable(id, sum)

    def sendNewConsumable(this, consumable, count):
        this.sendPacket(Identifiers.send.New_Consumable, ByteArray().writeByte(
            0).writeShort(consumable).writeShort(count).toByteArray())

    def checkLetters(this, playerLetters):
        needUpdate = False
        letters = playerLetters.split("/")
        for letter in letters:
            if not letter == "":
                values = letter.split("|")
                this.sendPacket(Identifiers.send.Letter, ByteArray().writeUTF(values[0]).writeUTF(
                    values[1]).writeByte(int(values[2])).writeBytes(binascii.unhexlify(values[3])).toByteArray())
                needUpdate = True

        if needUpdate:
            this.Cursor.execute(
                "update users set Letters = '' where PlayerID = ?", [this.playerID])

    def getFullItemID(this, category, itemID):
        return (itemID + 10000 + 10000 * category) if (itemID >= 100) else itemID + 100 * category

    def getSimpleItemID(this, category, itemID):
        return itemID - 10000 - 10000 * category if (itemID >= 10000) else itemID - 100 * category

    def getItemInfo(this, category, itemID):
        shop = list(list(map(int, item.split(","))) for item in this.server.shopList)

        for item in shop:
            if item[0] == category and item[1] == itemID:
                return item + ([20] if (category != 22) else [0])

class Server:

    def __init__(this):
        # Settings
        # Boolean
        this.DEBUG = bool(int(this.config("Boolean", "DEBUG")))
        this.isNowEvent = bool(int(this.config("Boolean", "Now Event")))
        this.resetMaps = bool(int(this.config("Boolean", "Reset Maps")))

        # Integer
        this.lastPlayerID = int(this.configInt("Last Player ID"))
        this.lastMapEditeurCode = int(this.configInt("Last Map Editeur Code"))
        this.needToFirst = int(this.configInt("Need To First"))
        this.needToBootcamp = int(this.configInt("Need To Bootcamp"))
        this.lastTribeID = int(this.configInt("Last Tribe ID"))
        this.lastChatID = int(this.configInt("Last Chat ID"))
        this.initialCheeses = int(this.configInt("Initial Cheeses"))
        this.initialFraises = int(this.configInt("Initial Fraises"))
        this.lastTopicID = int(this.configInt("Last Topic ID"))
        this.lastPostID = int(this.configInt("Last Post ID"))
        this.adventureID = int(this.configInt("Adventure ID"))
        this.timeEvent = int(this.configInt("Time Event"))
        this.electionDays = int(this.configInt("Election Days"))
        this.electionHours = int(this.configInt("Election Hours"))
        this.captchaLetters = int(this.configInt("Captcha Letters"))
        this.projectVersion = float(this.configInt("Project Version"))

        # String
        this.Version = str(this.configStr("Version"))
        this.CKEY = str(this.configStr("CKEY"))
        this.adventureIMG = str(this.configStr("Adventure IMG"))
        this.adminAllow = this.configStr("admin Allow").split(", ")
        this.miceName = str(this.configStr("Mice Name"))
        this.miceURL = str(this.configStr("Mice URL"))
        this.shopURL = str(this.configStr("Shop URL"))
        this.fbURL = str(this.configStr("Facebook URL"))
        this.standURL = str(this.configStr("Standalone URL"))
        this.discordURL = str(this.configStr("Discord URL"))

        this.ftpHOST = str(this.configStr("FTP Host"))
        this.ftpUSER = str(this.configStr("FTP Username"))
        this.ftpPASS = str(this.configStr("FTP Password"))
        this.ftpDIRECTORY = str(this.configStr("FTP Directory"))
        this.dftAvatar = str(this.configStr("Default Avatar"))

        # Eval
        this.calendarioSystem = eval(this.configEval("Calendario"))
        this.calendarioCount = eval(this.configEval("Calendario Count"))

        # List
        this.packetKeys = [int(key) for key in this.configList("Packet Keys").split(
            "[")[1].split("]")[0].split(", ")]
        this.loginKeys = [int(key) for key in this.configList("Login Keys").split(
            "[")[1].split("]")[0].split(", ")]

        # ShopList
        this.shopList = Config.get("ConfigShop", "Shop List").split(";")
        this.shamanShopList = Config.get(
            "ConfigShop", "Shaman Shop List").split(";")
        this.newVisuList = eval(Config.get("ConfigShop", "New Visu List"))

        # Commands
        this.allowedCommands = eval(Config.get("Commands", "Allowed"))
        this.unllowedCommands = eval(Config.get("Commands", "Unllowed"))

        # Integer
        this.lastPlayerCode = 0
        this.lastGiftID = 0
        this.serverBR = 0
        this.serverES = 0
        this.serverEN = 0
        this.startServerTime = 0

        # Boolean
        this.whisperLogging = True

        # Nonetype
        this.rebootTimer = None

        # List
        this.userMuteCache = []
        this.tempIPBanList = []
        this.userMuteCache = []
        this.shopPromotions = []
        this.ipPermaBanCache = []
        this.userTempBanCache = []
        this.userPermaBanCache = []
        this.staffChat = []
        this.activeStaffChat = []

        # Dict
        this.reports = {}
        this.rooms = {}
        this.players = {}
        this.shopListCheck = {}
        this.shamanShopListCheck = {}
        this.shopGifts = {}
        this.chatMessages = {}
        this.connectedCounts = {}
        this.cheeseTitleList = {5: 5.1, 20: 6.1, 100: 7.1, 200: 8.1, 300: 35.1, 400: 36.1, 500: 37.1, 600: 26.1, 700: 27.1, 800: 28.1, 900: 29.1, 1000: 30.1, 1100: 31.1, 1200: 32.1, 1300: 33.1, 1400: 34.1, 1500: 38.1, 1600: 39.1, 1700: 40.1, 1800: 41.1, 2000: 72.1, 2300: 73.1, 2700: 74.1, 3200: 75.1,
                                3800: 76.1, 4600: 77.1, 6000: 78.1, 7000: 79.1, 8000: 80.1, 9001: 81.1, 10000: 82.1, 14000: 83.1, 18000: 84.1, 22000: 85.1, 26000: 86.1, 30000: 87.1, 34000: 88.1, 38000: 89.1, 42000: 90.1, 46000: 91.1, 50000: 92.1, 55000: 234.1, 60000: 235.1, 65000: 236.1, 70000: 237.1, 75000: 238.1, 80000: 93.1}
        this.firstTitleList = {1: 9.1, 10: 10.1, 100: 11.1, 200: 12.1, 300: 42.1, 400: 43.1, 500: 44.1, 600: 45.1, 700: 46.1, 800: 47.1, 900: 48.1, 1000: 49.1, 1100: 50.1, 1200: 51.1, 1400: 52.1, 1600: 53.1, 1800: 54.1, 2000: 55.1, 2200: 56.1, 2400: 57.1, 2600: 58.1, 2800: 59.1, 3000: 60.1,
                               3200: 61.1, 3400: 62.1, 3600: 63.1, 3800: 64.1, 4000: 65.1, 4500: 66.1, 5000: 67.1, 5500: 68.1, 6000: 69.1, 7000: 231.1, 8000: 232.1, 9000: 233.1, 10000: 70.1, 12000: 224.1, 14000: 225.1, 16000: 226.1, 18000: 227.1, 20000: 202.1, 25000: 228.1, 30000: 229.1, 35000: 230.1, 40000: 71.1}
        this.shamanTitleList = {10: 1.1, 100: 2.1, 1000: 3.1, 2000: 4.1, 3000: 13.1, 4000: 14.1, 5000: 15.1, 6000: 16.1, 7000: 17.1, 8000: 18.1, 9000: 19.1, 10000: 20.1, 11000: 21.1, 12000: 22.1, 13000: 23.1, 14000: 24.1, 15000: 25.1, 16000: 94.1, 18000: 95.1, 20000: 96.1,
                                22000: 97.1, 24000: 98.1, 26000: 99.1, 28000: 100.1, 30000: 101.1, 35000: 102.1, 40000: 103.1, 45000: 104.1, 50000: 105.1, 55000: 106.1, 60000: 107.1, 65000: 108.1, 70000: 109.1, 75000: 110.1, 80000: 111.1, 85000: 112.1, 90000: 113.1, 100000: 114.1, 140000: 115.1}
        this.shopTitleList = {1: 115.1, 2: 116.1, 4: 117.1, 6: 118.1, 8: 119.1, 10: 120.1, 12: 121.1, 14: 122.1, 16: 123.1, 18: 124.1, 20: 125.1, 22: 126.1, 23: 115.2, 24: 116.2, 26: 117.2, 28: 118.2, 30: 119.2, 32: 120.2, 34: 121.2, 36: 122.2, 38: 123.2, 40: 124.2, 42: 125.2, 44: 126.2, 45: 115.3, 46: 116.3, 48: 117.3, 50: 118.3, 52: 119.3, 54: 120.3, 56: 121.3, 58: 122.3, 60: 123.3, 62: 124.3, 64: 125.3, 66: 126.3, 67: 115.4, 68: 116.4, 70: 117.4, 72: 118.4, 74: 119.4, 76: 120.4, 78: 121.4, 80: 122.4, 82: 123.4, 84: 124.4, 86: 125.4, 88: 126.4, 89: 115.5, 90: 116.5, 92: 117.5, 94: 118.5, 96: 119.5, 98: 120.5, 100: 121.5, 102: 122.5,
                              104: 123.5, 106: 124.5, 108: 125.5, 110: 126.5, 111: 115.6, 112: 116.6, 114: 117.6, 116: 118.6, 118: 119.6, 120: 120.6, 122: 121.6, 124: 122.6, 126: 123.6, 128: 124.6, 130: 125.6, 132: 126.6, 133: 115.7, 134: 116.7, 136: 117.7, 138: 118.7, 140: 119.7, 142: 120.7, 144: 121.7, 146: 122.7, 148: 123.7, 150: 124.7, 152: 125.7, 154: 126.7, 155: 115.8, 156: 116.8, 158: 117.8, 160: 118.8, 162: 119.8, 164: 120.8, 166: 121.8, 168: 122.8, 170: 123.8, 172: 124.8, 174: 125.8, 176: 126.8, 177: 115.9, 178: 116.9, 180: 117.9, 182: 118.9, 184: 119.9, 186: 120.9, 188: 121.9, 190: 122.9, 192: 123.9, 194: 124.9, 196: 125.9, 198: 126.9}
        this.bootcampTitleList = {1: 256.1, 3: 257.1, 5: 258.1, 7: 259.1, 10: 260.1, 15: 261.1, 20: 262.1, 25: 263.1, 30: 264.1, 40: 265.1, 50: 266.1, 60: 267.1, 70: 268.1, 80: 269.1, 90: 270.1, 100: 271.1, 120: 272.1, 140: 273.1, 160: 274.1, 180: 275.1, 200: 276.1, 250: 277.1, 300: 278.1, 350: 279.1, 400: 280.1, 500: 281.1, 600: 282.1, 700: 283.1, 800: 284.1, 900: 285.1, 1000: 286.1, 1001: 256.2, 1003: 257.2, 1005: 258.2, 1007: 259.2, 1010: 260.2, 1015: 261.2, 1020: 262.2, 1025: 263.2, 1030: 264.2, 1040: 265.2, 1050: 266.2, 1060: 267.2, 1070: 268.2, 1080: 269.2, 1090: 270.2, 1100: 271.2, 1120: 272.2, 1140: 273.2, 1160: 274.2, 1180: 275.2, 1200: 276.2, 1250: 277.2, 1300: 278.2, 1350: 279.2, 1400: 280.2, 1500: 281.2, 1600: 282.2, 1700: 283.2, 1800: 284.2, 1900: 285.2, 2000: 286.2, 2001: 256.3, 2003: 257.3, 2005: 258.3, 2007: 259.3, 2010: 260.3, 2015: 261.3, 2020: 262.3, 2025: 263.3, 2030: 264.3, 2040: 265.3, 2050: 266.3, 2060: 267.3, 2070: 268.3, 2080: 269.3, 2090: 270.3, 2100: 271.3, 2120: 272.3, 2140: 273.3, 2160: 274.3, 2180: 275.3, 2200: 276.3, 2250: 277.3, 2300: 278.3, 2350: 279.3, 2400: 280.3, 2500: 281.3, 2600: 282.3, 2700: 283.3, 2800: 284.3, 2900: 285.3, 3000: 286.3, 3001: 256.4, 3003: 257.4, 3005: 258.4, 3007: 259.4, 3010: 260.4, 3015: 261.4, 3020: 262.4, 3025: 263.4, 3030: 264.4, 3040: 265.4, 3050: 266.4, 3060: 267.4, 3070: 268.4, 3080: 269.4, 3090: 270.4, 3100: 271.4, 3120: 272.4, 3140: 273.4, 3160: 274.4, 3180: 275.4, 3200: 276.4, 3250: 277.4, 3300: 278.4, 3350: 279.4, 3400: 280.4, 3500: 281.4, 3600: 282.4, 3700: 283.4, 3800: 284.4, 3900: 285.4, 4000: 286.4, 4001: 256.5, 4003: 257.5, 4005: 258.5, 4007: 259.5, 4010: 260.5, 4015: 261.5, 4020: 262.5, 4025: 263.5, 4030: 264.5, 4040: 265.5, 4050: 266.5, 4060: 267.5, 4070: 268.5, 4080: 269.5, 4090: 270.5, 4100: 271.5,
                                  4120: 272.5, 4140: 273.5, 4160: 274.5, 4180: 275.5, 4200: 276.5, 4250: 277.5, 4300: 278.5, 4350: 279.5, 4400: 280.5, 4500: 281.5, 4600: 282.5, 4700: 283.5, 4800: 284.5, 4900: 285.5, 5000: 286.5, 5001: 256.6, 5003: 257.6, 5005: 258.6, 5007: 259.6, 5010: 260.6, 5015: 261.6, 5020: 262.6, 5025: 263.6, 5030: 264.6, 5040: 265.6, 5050: 266.6, 5060: 267.6, 5070: 268.6, 5080: 269.6, 5090: 270.6, 5100: 271.6, 5120: 272.6, 5140: 273.6, 5160: 274.6, 5180: 275.6, 5200: 276.6, 5250: 277.6, 5300: 278.6, 5350: 279.6, 5400: 280.6, 5500: 281.6, 5600: 282.6, 5700: 283.6, 5800: 284.6, 5900: 285.6, 6000: 286.6, 6001: 256.7, 6003: 257.7, 6005: 258.7, 6007: 259.7, 6010: 260.7, 6015: 261.7, 6020: 262.7, 6025: 263.7, 6030: 264.7, 6040: 265.7, 6050: 266.7, 6060: 267.7, 6070: 268.7, 6080: 269.7, 6090: 270.7, 6100: 271.7, 6120: 272.7, 6140: 273.7, 6160: 274.7, 6180: 275.7, 6200: 276.7, 6250: 277.7, 6300: 278.7, 6350: 279.7, 6400: 280.7, 6500: 281.7, 6600: 282.7, 6700: 283.7, 6800: 284.7, 6900: 285.7, 7000: 286.7, 7001: 256.8, 7003: 257.8, 7005: 258.8, 7007: 259.8, 7010: 260.8, 7015: 261.8, 7020: 262.8, 7025: 263.8, 7030: 264.8, 7040: 265.8, 7050: 266.8, 7060: 267.8, 7070: 268.8, 7080: 269.8, 7090: 270.8, 7100: 271.8, 7120: 272.8, 7140: 273.8, 7160: 274.8, 7180: 275.8, 7200: 276.8, 7250: 277.8, 7300: 278.8, 7350: 279.8, 7400: 280.8, 7500: 281.8, 7600: 282.8, 7700: 283.8, 7800: 284.8, 7900: 285.8, 8000: 286.8, 8001: 256.9, 8003: 257.9, 8005: 258.9, 8007: 259.9, 8010: 260.9, 8015: 261.9, 8020: 262.9, 8025: 263.9, 8030: 264.9, 8040: 265.9, 8050: 266.9, 8060: 267.9, 8070: 268.9, 8080: 269.9, 8090: 270.9, 8100: 271.9, 8120: 272.9, 8140: 273.9, 8160: 274.9, 8180: 275.9, 8200: 276.9, 8250: 277.9, 8300: 278.9, 8350: 279.9, 8400: 280.9, 8500: 281.9, 8600: 282.9, 8700: 283.9, 8800: 284.9, 8900: 285.9, 9000: 286.9}
        this.hardModeTitleList = {500: 213.1, 2000: 214.1, 4000: 215.1, 7000: 216.1, 10000: 217.1,
                                  14000: 218.1, 18000: 219.1, 22000: 220.1, 26000: 221.1, 30000: 222.1, 40000: 223.1}
        this.divineModeTitleList = {500: 324.1, 2000: 325.1, 4000: 326.1, 7000: 327.1, 10000: 328.1,
                                    14000: 329.1, 18000: 330.1, 22000: 331.1, 26000: 332.1, 30000: 333.1, 40000: 334.1}
        this.shopBadges = {2227: 2, 2208: 3, 2202: 4, 2209: 5, 2228: 8, 2218: 10, 2206: 11, 2219: 12, 2229: 13, 2230: 14, 2231: 15, 2211: 19, 2232: 20, 2224: 21, 2217: 22, 2214: 23, 2212: 24, 2220: 25, 2223: 26, 2234: 27, 2203: 31, 2205: 38, 2220: 25, 2221: 32, 2215: 37, 2222: 39, 2236: 36, 2204: 40, 2238: 41, 2239: 43, 2241: 44, 2243: 45, 2244: 48, 2207: 49, 2246: 52, 2247: 53, 210: 54, 2225: 56, 2213: 60, 2248: 61, 2226: 62,
                           2249: 63, 2250: 66, 2252: 67, 2253: 68, 2254: 69, 2254: 70, 10132: 71, 2255: 72, 2256: 128, 10133: 129, 422: 130, 124: 73, 2257: 135, 2258: 136, 2259: 137, 2260: 138, 2262: 140, 2263: 143, 2264: 146, 2265: 148, 2267: 149, 2268: 150, 2269: 151, 2270: 152, 2271: 155, 2272: 156, 2273: 157, 2274: 160, 2276: 165, 2277: 167, 2278: 171, 2279: 173, 2280: 175, 2281: 176, 2282: 177, 2283: 178, 2284: 179, 2285: 180, 2286: 183, 2287: 185}
        this.inventory = [2202, 2203, 2204, 2227, 2235, 2257, 2261, 2253, 2254, 2260, 2261, 2263, 2264, 2265, 2266, 2267, 2268, 2269, 2270, 2271, 2272, 2273, 2274, 2275, 2276, 2277, 2278, 2279, 2280, 2281, 2282, 2283, 2284, 2285, 2286, 2287,
                          2288, 2289, 2290, 2291, 2292, 2293, 2294, 2295, 2296, 2297, 2298, 2299, 2300, 2301, 2302, 2303, 2304, 2305, 2306, 2310, 2311, 2312, 2313, 2314, 2315, 2316, 2317, 2318, 2319, 2320, 2321, 2322, 2323, 2324, 2325, 2326, 2327, 2328]
        # Others
        this.Cursor = Cursor
        this.parseShop()
        this.parseBanList()
        this.parseShamanShop()
        this.serverList = this.parseJson("./include/json/serverList.json")
        this.promotions = this.parseJson("./include/json/promotions.json")
        this.parsePromotions()

    def updateConfig(this):
        this.configsStr("Admin Allow", str(this.adminAllow).replace(
            "'", "").split("[")[1].split("]")[0])
        this.configsInt("Last Player ID", str(this.lastPlayerID))
        this.configsInt("Last Map Editeur Code", str(this.lastMapEditeurCode))
        this.configsInt("Last Tribe ID", str(this.lastTribeID))
        this.configsInt("Last Chat ID", str(this.lastChatID))
        this.configsInt("Last Topic ID", str(this.lastTopicID))
        this.configsInt("Last Post ID", str(this.lastPostID))
        this.configsInt("Time Event", str(this.timeEvent))
        this.configsBool("Reset Maps", str(1 if this.resetMaps else 0))

    def getPointsColor(this, playerName, aventure, itemID, itemType, itemNeeded):
        for client in this.players.values():
            if client.Username == playerName:
                if int(itemID) in client.aventureCounts.keys():
                    if client.aventureCounts[int(itemID)] >= int(itemNeeded):
                        return 1
        return 0

    def getAventureCounts(this, playerName, aventure, itemID, itemType):
        for client in this.players.values():
            if client.Username == playerName:
                if int(itemID) in client.aventureCounts.keys():
                    return client.aventureCounts[int(itemID)]
        return 0

    def getAventureItems(this, playerName, aventure, itemType, itemID):
        c = 0
        for client in this.players.values():
            if client.Username == playerName:
                if aventure == 52:
                    if int(itemID) in client.aventureCounts.keys():
                        return client.aventureCounts[itemID]
                if aventure == 24:
                    if itemType == 0 and itemID == 2:
                        for item in client.aventureCounts.keys():
                            if int(str(item)) >= 38 and int(str(item)) <= 44:
                                c += client.aventureCounts[item]
                        return c

        return 0

    def parseShop(this):
        for item in this.shopList:
            values = item.split(",")
            this.shopListCheck[values[0] + "|" + values[1]
                               ] = [int(values[5]), int(values[6])]

    def parseShamanShop(this):
        for item in this.shamanShopList:
            values = item.split(",")
            this.shamanShopListCheck[values[0]] = [
                int(values[4]), int(values[5])]

    def sendOutput(this, message):
        print("[" + (str(time.strftime("%H:%M:%S"))) + "] " + message)

    def config(this, part, setting):
        return Config.get(part, setting)

    def configStr(this, setting):
        return Config.get("String", setting)

    def configInt(this, setting):
        return Config.get("Integer", setting)

    def configEval(this, setting):
        return Config.get("Eval", setting)

    def configList(this, setting):
        return Config.get("List", setting)

    def configsBool(this, setting, value):
        Config.set("Boolean", setting, value)
        with open("./include/Config.properties", "w") as f:
            Config.write(f)

    def configsStr(this, setting, value):
        Config.set("String", setting, value)
        with open("./include/Config.properties", "w") as f:
            Config.write(f)

    def configsInt(this, setting, value):
        Config.set("Integer", setting, value)
        with open("./include/Config.properties", "w") as f:
            Config.write(f)

    def parseJson(this, directory):
        with open(directory, "r") as f:
            return eval(f.read())

    def updateServerList(this):
        with open("./include/json/serverList.json", "w") as f:
            json.dump(this.serverList, f)

    def updateCommands(this):
        Config.set("Commands", "Allowed", this.allowedCommands)
        with open("./include/Config.properties", "w") as f:
            Config.write(f)
        Config.set("Commands", "Unllowed", this.unllowedCommands)
        with open("./include/Config.properties", "w") as f:
            Config.write(f)

    def sendServerRestart(this, no, sec):
        if sec > 0 or no != 5:
            this.sendServerRestartSEC(120 if no == 0 else 60 if no == 1 else 30 if no ==
                                      2 else 20 if no == 3 else 10 if no == 4 else sec)
            if this.rebootTimer != None:
                this.rebootTimer.cancel()
            this.rebootTimer = TFMUtils.callLater(60 if no == 0 else 30 if no == 1 else 10 if no == 2 or no == 3 else 1, lambda: this.sendServerRestart(
                no if no == 5 else no + 1, 9 if no == 4 else sec - 1 if no == 5 else 0))

    def sendServerRestartSEC(this, seconds):
        this.sendPanelRestartMessage(seconds)
        this.sendWholeServer(Identifiers.send.Server_Restart,
                             ByteArray().writeInt(seconds * 1000).toByteArray())

    def sendPanelRestartMessage(this, seconds):
        if seconds == 120:
            this.sendOutput("[SERVER] The server will restart in 2 minutes.")
        elif seconds < 120 and seconds > 1:
            this.sendOutput(
                "[SERVER] The server will restart in " + str(seconds) + " seconds.")
        else:
            this.sendOutput("[SERVER] The server will restart in 1 second.")
            os._exit(12)

    def closeServer(this):
        this.updateConfig()
        for client in this.players.values():
            client.loseConnection()
            del this.players[client.Username]

        os._exit(0)

    def getConnectedPlayerCount(this):
        return len(this.players)

    def getRoomsCount(this):
        return len(this.rooms)

    def checkAlreadyExistingGuest(this, playerName):
        found = False
        result = ""

        if not this.checkConnectedAccount(playerName):
            found = True
            result = playerName

        while not found:
            tempName = playerName + "_" + TFMUtils.getRandomChars(4).lower()
            if not this.checkConnectedAccount(tempName):
                found = True
                result = tempName
        return result

    def checkConnectedAccount(this, playerName):
        return playerName in this.players.keys()

    def disconnectIPAddress(this, ip):
        for client in this.players.values():
            if client.ipAddress == ip:
                client.transport.loseConnection()

    def checkExistingUser(this, playerName):
        this.Cursor.execute(
            "select * from Users where Username = ?", [playerName])
        if this.Cursor.fetchone():
            return True
        return False

    def resetMapsServer(this):
        day = date.today()
        days = ('seg', 'ter', 'qua', 'quin', 'sex', 'sab', 'dom')
        dds = str(days[day.weekday()])
        if not this.resetMaps and dds == 'sab':
            # for client in this.players.values():
                #client.sendLangueMessage("", "<CH>Os <J>recordes dos mapas</J> foram resetados!")
            this.Cursor.execute(
                "update MapEditor set Player = '', Time = ''")
            this.resetMaps = 1
            this.updateConfig()
        if not dds == 'sab':
            this.resetMaps = 0
            this.updateConfig()

    def recommendRoom(this, langue):
        found = False
        x = 0
        result = ""
        while not found:
            x += 1
            if (langue + "-" + str(x)) in this.rooms.keys():
                if this.rooms[langue + "-" + str(x)].getPlayerCount() < 25:
                    found = True
                    result = str(x)
            else:
                found = True
                result = str(x)
        return result

    def checkRoom(this, roomName, langue):
        found = False
        x = 0
        result = roomName
        if (langue + "-" + roomName if not roomName.startswith("*") and roomName[0] != chr(3) else roomName) in this.rooms.keys():
            room = this.rooms.get(langue + "-" + roomName if not roomName.startswith(
                "*") and roomName[0] != chr(3) else roomName)
            if room.getPlayerCount() < room.maxPlayers if room.maxPlayers != -1 else True:
                found = True
        else:
            found = True

        while not found:
            x += 1
            if (langue + "-" + roomName if not roomName.startswith("*") and roomName[0] != chr(3) else roomName) in this.rooms.keys():
                room = this.rooms.get((langue + "-" + roomName if not roomName.startswith(
                    "*") and roomName[0] != chr(3) else roomName) + str(x))
                if room.getPlayerCount() < room.maxPlayers if room.maxPlayers != -1 else True:
                    found = True
                    result += str(x)
            else:
                found = True
                result += str(x)
        return result

    def addClientToRoom(this, client, roomName):
        if roomName in this.rooms.keys():
            this.rooms[roomName].addClient(client)
        else:
            room = Room(this, roomName)
            this.rooms[roomName] = room
            room.addClient(client)

    def getIPPermaBan(this, ip):
        return ip in this.ipPermaBanCache

    def checkReport(this, array, playerName):
        return playerName in array

    def banPlayer(this, playerName, bantime, reason, modname, silent):
        found = False

        client = this.players.get(playerName)
        player = this.players.get(modname)
        if client != None:
            found = True
            if not modname == "Server":
                client.banHours += bantime
                ban = str(time.time())
                bandate = ban[:len(ban) - 4]
                this.Cursor.execute("insert into BanLog values (?, ?, ?, ?, ?, 'Online', ?, ?)", [
                                    playerName, modname, str(bantime), reason, bandate, client.roomName, client.ipAddress])
            else:
                if this.client.langueByte == 3:
                    this.sendStaffMessage(5, "<V>O servidor <BL>baniu o jogador <V>" +
                                          playerName + "<BL> por <V>1 <BL> hora. Motivo: <V>Voto popular<BL>.")
                else:
                    this.sendStaffMessage(5, "<V>Server <BL>banned player <V>" + playerName +
                                          "<BL> for <V>1 <BL> hour. Reason: <V>Vote Populaire<BL>.")

            this.Cursor.execute("update Users SET BanHours = ? WHERE PlayerID = ?", [
                                bantime, client.playerID])

            if bantime >= 2161 or client.banHours >= 2161:
                this.userPermaBanCache.append(playerName)
                this.Cursor.execute("insert into UserPermaBan values (?, ?, ?)", [
                                    playerName, modname, reason])

            if client.banHours >= 2161:
                this.ipPermaBanCache.append(client.ipAddress)
                this.Cursor.execute("insert into IPPermaBan values (?, ?, ?)", [
                                    client.ipAddress, modname, reason])

            if bantime >= 1081 and bantime <= 2160:
                this.tempBanUser(playerName, bantime, reason)
                if not client.ipAddress in this.tempIPBanList:
                    this.tempIPBanList.append(client.ipAddress)
                    TFMUtils.callLater(
                        bantime * 60, lambda: this.tempIPBanList.remove(client.ipAddress))

            if bantime >= 1 and bantime <= 1080:
                this.tempBanUser(playerName, bantime, reason)

            if this.checkReport(this.reports, playerName):
                this.modopwetBan(playerName, modname, bantime, reason)

            client.sendPlayerBan(bantime, reason, silent)

        if not found and this.checkExistingUser(playerName) and not modname == "Server" and bantime >= 1:
            found = True
            totalBanTime = this.getTotalBanHours(playerName) + bantime
            if (totalBanTime >= 1081 and bantime <= 360) or bantime >= 1081:
                this.userPermaBanCache.append(playerName)
                this.Cursor.execute("insert into UserPermaBan values (?, ?, ?, ?)", [
                                    playerName, reason, modname, totalBanTime])

            if bantime >= 1 and bantime <= 360:
                this.tempBanUser(playerName, bantime, reason)

            this.Cursor.execute("update Users SET BanHours = ? WHERE PlayerID = ?", [
                                bantime, client.playerID])

            ban = str(time.time())
            bandate = ban[:len(ban) - 4]
            this.Cursor.execute("insert into BanLog values (?, ?, ?, ?, ?, 'Offline', '', 'Offline')", [
                                playerName, modname, str(bantime), reason, bandate])

        return found

    def checkTempBan(this, playerName):
        this.Cursor.execute(
            "select * from UserTempBan where Name = ?", [playerName])
        if this.Cursor.fetchone():
            return True
        return False

    def removeTempBan(this, playerName):
        try:
            if playerName in this.userTempBanCache:
                this.userTempBanCache.remove(playerName)
            this.Cursor.execute(
                "delete from UserTempBan where Name = ?", [playerName])
        except:
            pass

    def tempBanUser(this, playerName, bantime, reason):
        if this.checkTempBan(playerName):
            this.removeTempBan(playerName)

        this.userTempBanCache.append(playerName)
        this.Cursor.execute("insert into UserTempBan values (?, ?, ?)", [
                            playerName, str(TFMUtils.getTime() + (bantime * 3600)), reason])

    def getTempBanInfo(this, playerName):
        this.Cursor.execute(
            "select Time, Reason from UserTempBan where Name = ?", [playerName])
        r = this.Cursor.fetchall()
        for rs in r:
            return [rs["Time"], rs["Reason"]]
        return [0, "Without a reason"]

    def getPermBanInfo(this, playerName):
        Cursor.execute(
            "select Reason from UserPermaBan where Name = ?", [playerName])
        for rs in Cursor.fetchall():
            return rs["Reason"]
        else:
            return "Without a reason"

    def checkPermaBan(this, playerName):
        this.Cursor.execute(
            "select * from UserPermaBan where Name = ?", [playerName])
        if this.Cursor.fetchone():
            return True
        return False

    def removePermaBan(this, playerName):
        try:
            if playerName in this.userPermaBanCache:
                this.userPermaBanCache.remove(playerName)
            this.Cursor.execute(
                "delete from UserPermaBan where Name = ?", [playerName])
        except:
            pass

    def getTotalBanHours(this, playerName):
        this.Cursor.execute(
            "select BanHours from Users where Username = ?", [playerName])
        rs = this.Cursor.fetchone()
        if rs:
            return rs["BanHours"]
        return 0

    def parseBanList(this):
        this.Cursor.execute("select IP from IPPermaBan")
        for rs in this.Cursor.fetchall():
            this.ipPermaBanCache.append(rs[0])

        this.Cursor.execute("select Name from UserPermaBan")
        for rs in this.Cursor.fetchall():
            this.userPermaBanCache.append(rs[0])

        this.Cursor.execute("select Name from UserTempBan")
        for rs in this.Cursor.fetchall():
            this.userTempBanCache.append(rs[0])

        this.Cursor.execute("select Name from UserMute")
        for rs in this.Cursor.fetchall():
            this.userMuteCache.append(rs[0])

    def modopwetBan(this, playerName, modname, bantime, reason):
        this.reports[playerName]["status"] = "banned"
        this.reports[playerName]["banhours"] = str(bantime)
        this.reports[playerName]["bannedby"] = str(modname)
        this.reports[playerName]["banreason"] = str(reason)
        reporters = []
        offline_reporters = []
        for report in this.reports[playerName]["reporters"]:
            if not report in reporters:
                reporters.append(report)
                player = this.players.get(report)
                if player != None:
                    player.karma += 1
                    if player.langueByte == 3:
                        player.sendMessage(
                            str(playerName) + " foi banido. Karma +1 (" + str(player.karma) + ")")
                    else:
                        player.sendMessage(
                            str(playerName) + " has banned. Karma +1 (" + str(player.karma) + ")")
                else:
                    offline_reporters.append(report)

    def voteBanPopulaire(this, playerName, ip):
        client = this.players.get(playerName)
        if client != None and client.privLevel == 1 and not ip in client.voteBan:
            client.voteBan.append(ip)
            if len(client.voteBan) == 10:
                this.banPlayer(playerName, 1, "Vote Populaire",
                               "Server", False, False)

    def muteUser(this, playerName, modname, mutetime, reason):
        this.userMuteCache.append(playerName)
        this.Cursor.execute("insert into UserMute values (?, ?, ?, ?)", [
                            playerName, str(TFMUtils.getTime() + (mutetime * 3600)), reason, modname])

    def removeModMute(this, playerName):
        try:
            this.userMuteCache.remove(playerName)
            this.Cursor.execute(
                "delete from UserMute where Name = ?", [playerName])
        except:
            pass

    def getModMuteInfo(this, playerName):
        this.Cursor.execute(
            "select Time, Reason, Mutedby from UserMute where Name = ?", [playerName])
        rs = this.Cursor.fetchone()
        if rs:
            return [rs["Time"], rs["Reason"], rs["Mutedby"]]
        return [0, "Without a reason", "Server"]

    def mutePlayer(this, playerName, time, reason, modname):
        client = this.players.get(playerName)
        if client != None:
            this.sendStaffMessage(5, "<V>" + str(modname) + "<BL> deixou <V>" + playerName + "<BL> sem falar por <V>" + str(
                time) + "<BL> " + str("hora" if time == 1 else "horas") + ". Motivo: <V>" + str(reason))
            if playerName in this.userMuteCache:
                this.removeModMute(playerName)

            for player in client.room.clients.values():
                if player.Username != playerName:
                    player.sendLangueMessage(
                        "", "<ROSE>$MuteInfo2", playerName, str(time), reason)

            client.isMute = True
            client.sendLangueMessage("", "<ROSE>$MuteInfo1", str(time), reason)
            this.muteUser(playerName, modname, time, reason)

    def desmutePlayer(this, playerName, modname):
        client = this.players.get(playerName)
        if client != None:
            this.sendStaffMessage(
                5, "<V>" + str(modname) + "<N> desmutou <V>" + playerName + "<BL>.")
            this.removeModMute(playerName)
            client.isMute = False

    def sendStaffChat(this, type, langue, identifiers, packet):
        minLevel = 0 if type == -1 or type == 0 else 1 if type == 1 else 7 if type == 3 or type == 4 else 5 if type == 2 or type == 5 else 6 if type == 7 or type == 6 else 3 if type == 8 else 4 if type == 9 else 0
        for client in this.players.values():
            if client.privLevel >= minLevel and client.Langue == langue or type == 1 or type == 4 or type == 5:
                client.sendPacket(identifiers, packet)

    def getTotemData(this, playerName):
        if playerName.startswith("*"):
            return []
        else:
            this.Cursor.execute(
                "select ItemCount, Totem from Totem where Name = ?", [playerName])
            rs = this.Cursor.fetchone()
            if rs:
                itemCount = rs["ItemCount"]
                totem = rs["Totem"]
                totem = totem.replace("%", chr(1))
                return [str(itemCount), totem]
        return []

    def setTotemData(this, playerName, ItemCount, totem):
        if playerName.startswith("*"):
            pass
        else:
            totem = totem.replace(chr(1), "%")

            if len(this.getTotemData(playerName)) != 0:
                this.Cursor.execute("update Totem set ItemCount = ?, Totem = ? where Name = ?", [
                                    ItemCount, totem, playerName])
            else:
                this.Cursor.execute("insert into Totem values (?, ?, ?)", [
                                    playerName, ItemCount, totem])

    def getShamanType(this, playerCode):
        for player in this.players.values():
            if player.playerCode == playerCode:
                return player.shamanType

        return 0

    def getShamanLevel(this, playerCode):
        for player in this.players.values():
            if player.playerCode == playerCode:
                return player.shamanLevel
        return 0

    def getShamanBadge(this, playerCode):
        for player in this.players.values():
            if player.playerCode == playerCode:
                return player.skillModule.getShamanBadge()

        return 0

    def getPlayerID(this, playerName):
        if playerName.startswith("*"):
            return 0

        elif playerName in this.players.keys():
            return this.players[playerName].playerID
        else:
            this.Cursor.execute(
                "select PlayerID from Users where Username = ?", [playerName])
            rs = this.Cursor.fetchone()
            if rs:
                return rs["PlayerID"]
        return 0

    def getPlayerPrivlevel(this, playerName):
        if playerName.startswith("*"):
            return 0

        elif playerName in this.players.keys():
            return this.players[playerName].privLevel
        else:
            this.Cursor.execute(
                "select PrivLevel from Users where Username = ?", [playerName])
            rs = this.Cursor.fetchone()
            if rs:
                return rs["PrivLevel"]
        return 0

    def getPlayerName(this, playerID):
        this.Cursor.execute(
            "select Username from Users where PlayerID = ?", [playerID])
        rs = this.Cursor.fetchone()
        if rs:
            return rs["Username"]
        return ""

    def getPlayerRoomName(this, playerName):
        if playerName in this.players.keys():
            return this.players[playerName].roomName
        return ""

    def getTribeInfo(this, tribeCode):
        tribeRankings = {}
        this.Cursor.execute("select * from tribe where Code = ?", [tribeCode])
        rs = this.Cursor.fetchone()
        if rs:
            return [rs["Name"], rs["Message"], rs["House"], rs["Chat"], rs["Rankings"]]
        return ["", "", 0, 0, tribeRankings]

    def getTribeHouse(this, tribeName):
        this.Cursor.execute(
            "select House from Tribe where Name = ?", [tribeName])
        rs = this.Cursor.fetchone()
        if rs:
            return rs["House"]
        return -1

    def checkDuplicateEmail(this, email):
        Cursor.execute("select Username from Users where Email = ?", [email])
        if Cursor.fetchone():
            return True
        return False

    def getPlayersCountMode(this, mode):
        modeName = {1: "", 3: "vanilla", 8: "survivor", 9: "racing", 11: "music",
                    2: "bootcamp", 10: "defilante", 18: "", 16: "village"}[mode]
        playerCount = 0
        for room in this.rooms.values():
            if ((room.isNormRoom or not room.isNormRoom if mode == 1 else room.isVanilla if mode == 3 else room.isSurvivor if mode == 8 else room.isRacing or room.isFastRacing if mode == 9 else room.isMusic if mode == 11 else room.isBootcamp if mode == 2 else room.isDefilante if mode == 10 else room.isVillage if mode == 16 else False)):
                playerCount += room.getPlayerCount()
        return ["%s %s" % (this.miceName, modeName), playerCount]

    def parsePromotions(this):
        needUpdate = False
        i = 0
        while i < len(this.promotions):
            item = this.promotions[i]
            if item[4] < 1000:
                item[4] = TFMUtils.getTime() + item[4] * 86400 + 30
                needUpdate = True

            this.shopPromotions.append(
                [item[0], item[1], item[2], item[3], item[4], item[5]])
            i += 1

        if needUpdate:
            with open("./include/json/promotions.json", "w") as f:
                json.dump(this.promotions, f)

        this.checkPromotionsEnd()

    def checkPromotionsEnd(this):
        needUpdate = False
        for promotion in this.shopPromotions:
            if TFMUtils.getHoursDiff(promotion[4]) <= 0:
                this.shopPromotions.remove(promotion)
                needUpdate = True
                i = 0
                while i < len(this.promotions):
                    if this.promotions[i][2] == promotion[2] and this.promotions[i][3] == promotion[3]:
                        del this.promotions[i]
                    i += 1

        if needUpdate:
            with open("./include/json/promotions.json", "w") as f:
                json.dump(this.promotions, f)

    def sendWholeServer(this, identifiers, result):
        for client in this.players.values():
            client.sendPacket(identifiers, result)

    def checkMessage(this, client, message, whisper=False):
        blackList = this.serverList["blacklist"]
        suspectWords = this.serverList["suspectwords"]
        whiteList = this.serverList["whitelist"]
        isSuspect = False
        if client.privLevel < 9:
            i = 0
            while i < len(blackList):
                if re.search("[^a-zA-Z]*".join(blackList[i]), message.lower() or client.banforMessage.keys()):
                    if message in client.banforMessage:
                        client.banforMessage[message] += 1
                    else:
                        client.banforMessage[message] = 1
                    if int(client.banforMessage[message]) >= 3:
                        this.banPlayer(client.Username, 360,
                                       "Disclosure", "ANT-DV", False)
                        this.sendStaffMessage(7, "[<V>ANT-DV</V>][<V>" + str(client.Username) + "</V>][<J>" + str(
                            message) + "</J>] It was banned for divulging even though it was warned of the ban.")
                        return True
                    client.sendMessage(
                        "Ooops <V>%s</V>, Make fingered a forbidden url.. <R>Be careful!</R> If you continue to send this type of message you will be banned." % (client.Username))
                    this.sendStaffMessage(7, "[<V>ANT-DV</V>][<V>" + str(client.Username) + "</V>][<J>" + str(message) + "</J>] Is releasing a link from the blacklist" + str(
                        " on whisper" if whisper else "") + ", this message does not appear to other players.")
                    isSuspect = True
                    return True
                i += 1

            if not isSuspect:
                if filter(lambda word: word in message.lower(), suspectWords) and not filter(lambda white: white in message.lower(), whiteList):
                    this.sendStaffMessage(7, "[<V>ANT-DV</V>][<V>" + str(client.Username) + "</V>][<J>" + str(message) + "</J>] Enter a suspicious link" + str(
                        " on whisper" if whisper else "") + ", type <V>/appendblack link</V> to add it to the blacklist.")
        return False

    def setVip(this, playerName, days):
        player = this.players.get(playerName)
        if ((player != None and player.privLevel == 1) or this.getPlayerPrivlevel(playerName) == 1):
            this.Cursor.execute("update users set VipTime = ? where Username = ?" if player !=
                                None else "update users SET VipTime = ?, PrivLevel = 2 where Username = ?", [TFMUtils.getTime() + (days * 24 * 3600), playerName])
            if player != None:
                player.realLevel = 2
                player.privLevel = 2

                if player.langueByte == 3:
                    this.sendStaffMessage(
                        7, "<V>" + playerName + "</V> se tornou VIP por <V>" + str(days) + "</V> dias.")
                else:
                    this.sendStaffMessage(
                        7, "<V>" + playerName + "</V> became VIP for <V>" + str(days) + "</V> days.")
            return True
        return False

    def getPlayerCode(this, playerName):
        client = this.players.get(TFMUtils.parsePlayerName(playerName))
        return client.playerCode if player != None else 0

    def sendStaffMessage(this, minLevel, message, tab=False):
        for client in this.players.values():
            if client.privLevel >= minLevel:
                client.sendMessage(message, tab)


class Room:

    def __init__(this, server, name):

        # String
        this.currentSyncName = ""
        this.currentShamanName = ""
        this.currentSecondShamanName = ""
        this.forceNextMap = "-1"
        this.mapName = ""
        this.mapXML = ""
        this.EMapXML = ""
        this.roomPassword = ""
        this.deathWin = ""

        # Integer
        this.maxPlayers = 200
        this.currentMap = 0
        this.lastRoundCode = 0
        this.mapCode = -1
        this.mapYesVotes = 0
        this.mapNoVotes = 0
        this.mapPerma = -1
        this.mapStatus = 0
        this.currentSyncCode = -1
        this.roundTime = 120
        this.gameStartTime = 0
        this.currentShamanCode = -1
        this.currentSecondShamanCode = -1
        this.currentShamanType = -1
        this.currentSecondShamanType = -1
        this.forceNextShaman = -1
        this.numCompleted = 0
        this.FSnumCompleted = 0
        this.SSnumCompleted = 0
        this.receivedNo = 0
        this.receivedYes = 0
        this.EMapLoaded = 0
        this.EMapCode = 0
        this.objectID = 0
        this.tempTotemCount = -1
        this.addTime = 0
        this.cloudID = -1
        this.companionBox = -1
        this.mulodromeRoundCount = 0
        this.redCount = 0
        this.blueCount = 0
        this.musicMapStatus = 0
        this.roundsCount = -1
        this.survivorMapStatus = 0
        this.lastImageID = 0
        this.changeMapAttemps = 0
        this.musicSkipVotes = 0
        this.musicTime = 0
        this.gameStartTimeMillis = 0
        this.eventMap = 0
        this.deathRemaining = 0
        this.currentMusicID = 0
        this.mapTime = 0
        this.luaStartTimeMillis = 0

        # Bool
        this.discoRoom = False
        this.isClosed = False
        this.isCurrentlyPlay = False
        this.isDoubleMap = False
        this.isNoShamanMap = False
        this.isVotingMode = False
        this.initVotingMode = True
        this.isVotingBox = False
        this.EMapValidated = False
        this.countStats = True
        this.never20secTimer = False
        this.isVanilla = False
        this.isVanillaP41 = False
        this.isEditeur = False
        this.changed20secTimer = False
        this.specificMap = False
        this.noShaman = False
        this.isTutorial = False
        this.isTotemEditeur = False
        this.autoRespawn = False
        this.noAutoScore = False
        this.catchTheCheeseMap = False
        this.isTribeHouse = False
        this.isTribeHouseMap = False
        this.isMulodrome = False
        this.isRacing = False
        this.isMusic = False
        this.isPlayingMusic = False
        this.isRacingP17 = False
        this.isBootcamp = False
        this.isBootcampP13 = False
        this.isSurvivor = False
        this.isSurvivorVamp = False
        this.isDefilante = False
        this.isNormRoom = False
        this.isSnowing = False
        this.canChangeMap = True
        this.disableAfkKill = False
        this.isFixedMap = False
        this.noShamanSkills = False
        this.is801Room = False
        this.mapInverted = False
        this.isFuncorp = False
        this.isVillage = False
        this.isEventMap = False
        this.isEventMap2 = False
        this.discoRoom = False
        this.canCannon = False
        this.isCloseRoom = False
        this.fireworksActive = False
        this.disableEventLog = False

        # Minigames
        this.isMinigame = False
        this.isLuaMinigame = False
        this.isUtility = False
        this.isTribeWar = False
        this.isPokeLua = False
        this.isExplosion = False
        this.isInvocation = False
        this.isBallonRace = False
        this.isFly = False
        this.isPropHunt = False
        this.isUnoTFM = False
        this.isFastRacing = False

        # None
        this.changeMapTimer = None
        this.closeRoomRoundJoinTimer = None
        this.voteCloseTimer = None
        this.killAfkTimer = None
        this.autoRespawnTimer = None
        this.endSnowTimer = None
        this.startTimerLeft = None
        this.contagemDeath = None
        this.L = None
        this.minigame = MiniGame()

        # List Arguments
        this.MapList = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82,
                        83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 136, 137, 138, 139, 140, 141, 142, 143, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210]
        this.noShamanMaps = [7, 8, 14, 22, 23, 28, 29, 54, 55, 57, 58, 59, 60, 61, 70, 77, 78, 87, 88,
                             92, 122, 123, 124, 125, 126, 1007, 888, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210]
        this.anchors = []
        this.lastHandymouse = [-1, -1]

        # List
        this.musicVideos = []
        this.redTeam = []
        this.blueTeam = []
        this.roomTimers = []
        this.adminsRoom = []
        this.playersBan = []
        this.Minigames = []

        # Dict
        this.clients = {}
        this.currentShamanSkills = {}
        this.currentSecondShamanSkills = {}
        this.currentTimers = {}

        # Uno
        this.modeUNO = "inicio"
        this.playersUNO = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0}
        this.playersIDUNO = {}

        # Others
        this.name = name
        this.server = server
        this.Cursor = Cursor
        this.prophuntInfo = this.server.parseJson(
            "./include/json/minigames/prophunt.json")

        if this.name.startswith("*"):
            this.community = "xx"
            this.roomName = this.name
        else:
            this.community = this.name.split("-")[0].lower()
            this.roomName = this.name.split("-")[1]

        roomNameCheck = this.roomName[
            1:] if this.roomName.startswith("*") else this.roomName
        if this.roomName.startswith(chr(3) + "[Editeur] "):
            this.countStats = False
            this.isEditeur = True
            this.maxPlayers = 1
            this.never20secTimer = True

        elif this.roomName.startswith(chr(3) + "[Tutorial] "):
            this.countStats = False
            this.currentMap = 900
            this.maxPlayers = 1
            this.specificMap = True
            this.noShaman = True
            this.never20secTimer = True
            this.isTutorial = True

        elif this.roomName.startswith(chr(3) + "[Totem] "):
            this.countStats = False
            this.specificMap = True
            this.currentMap = 444
            this.maxPlayers = 1
            this.isTotemEditeur = True
            this.never20secTimer = True

        elif this.roomName.startswith("*" + chr(3)):
            this.countStats = False
            this.isTribeHouse = True
            this.autoRespawn = True
            this.never20secTimer = True
            this.noShaman = True
            this.disableAfkKill = True
            this.isFixedMap = True
            this.roundTime = 0

        elif this.roomName.startswith("#tribewar") or this.roomName.startswith("*#tribewar"):
            this.isMinigame = True
            this.isTribeWar = True
            this.roundTime = 63
            this.noShaman = True

        elif this.roomName.startswith("#utility") or this.roomName.startswith("*#utility"):
            this.isMinigame = True
            this.isUtility = True
            this.roundTime = 0
            this.never20secTimer = True
            this.autoRespawn = True
            this.countStats = False
            this.noShaman = True
            this.isFixedMap = True

        elif this.roomName.startswith("#invocation") or this.roomName.startswith("*#invocation"):
            this.isMinigame = True
            this.isInvocation = True
            this.never20secTimer = True
            this.countStats = False
            this.noShaman = True

        elif this.roomName.startswith("#explosion") or this.roomName.startswith("*#explosion"):
            this.isMinigame = True
            this.isExplosion = True
            this.never20secTimer = True
            this.countStats = False
            this.noShaman = True

        elif this.roomName.startswith("#ballonrace") or this.roomName.startswith("*#ballonrace"):
            this.isMinigame = True
            this.isBallonRace = True
            this.never20secTimer = True
            this.countStats = False
            this.noShaman = True

        elif this.roomName.startswith("#pokelua") or this.roomName.startswith("*#pokelua"):
            this.isMinigame = True
            this.isPokeLua = True
            this.never20secTimer = True
            this.countStats = False
            this.noShaman = True

        elif this.roomName.startswith("#fly") or this.roomName.startswith("*#fly"):
            this.isMinigame = True
            this.isFly = True
            this.never20secTimer = True
            this.countStats = False
            this.noShaman = True

        elif this.roomName.startswith("#prophunt") or this.roomName.startswith("*#prophunt"):
            this.isMinigame = True
            this.isPropHunt = True
            this.never20secTimer = True
            this.countStats = False

        elif this.roomName.startswith("#"):
            minigameName = this.roomName[2:] if this.roomName.startswith(
                "*") else this.roomName[1:]
            this.isMinigame = True
            if minigameName.startswith("ffarace"):
                this.minigame = FFARace(this.Cursor, this)
            elif minigameName.startswith("deathmatch"):
                this.minigame = DeathMatch(this.Cursor, this)
            elif minigameName.startswith("unotfm"):
                this.minigame = UnoTFM()
            this.minigame.createRoom(this)

        elif this.roomName.startswith("music") or this.roomName.startswith("*music"):
            this.isMusic = True

        elif this.roomName.startswith("racing") or this.roomName.startswith("*racing"):
            this.isRacing = True
            this.noShaman = True
            this.noAutoScore = False
            this.never20secTimer = True
            this.roundTime = 63

        elif this.roomName.startswith("fastracing") or this.roomName.startswith("*fastracing"):
            this.isRacing = True
            this.isFastRacing = True
            this.noShaman = True
            this.noAutoScore = False
            this.never20secTimer = True
            this.roundTime = 33

        elif this.roomName.startswith("bootcamp") or this.roomName.startswith("*bootcamp"):
            this.isBootcamp = True
            this.countStats = False
            this.roundTime = 360
            this.never20secTimer = True
            this.autoRespawn = True
            this.noShaman = True

        elif this.roomName.startswith("vanilla") or this.roomName.startswith("*vanilla"):
            this.isVanilla = True

        elif this.roomName.startswith("survivor") or this.roomName.startswith("*survivor"):
            this.isSurvivor = True
            this.roundTime = 90

        elif this.roomName.startswith("defilante") or this.roomName.startswith("*defilante"):
            this.isDefilante = True
            this.noShaman = True
            this.countStats = False
            this.noAutoScore = False

        elif this.roomName.startswith("801") or this.roomName.startswith("*801") or this.roomName.startswith("village") or this.roomName.startswith("*village"):
            if "village" in this.roomName:
                this.isVillage = True
            else:
                this.is801Room = True
            this.roundTime = 0
            this.never20secTimer = True
            this.autoRespawn = True
            this.countStats = False
            this.noShaman = True
            this.isFixedMap = True
            this.disableAfkKill = True
        else:
            this.isNormRoom = True
        this.mapChange()

    def startTimer(this):
        for client in this.clients.values():
            client.sendMapStartTimerEnd()

    def mapChange(this):
        this.isEventMap = False
        if this.changeMapTimer != None:
            this.changeMapTimer.cancel()

        if not this.canChangeMap:
            this.changeMapAttemps += 1
            if this.changeMapAttemps < 5:
                this.changeMapTimer = TFMUtils.callLater(1, this.mapChange)
                return

        for timer in this.roomTimers:
            timer.cancel()

        this.roomTimers = []

        for timer in [this.voteCloseTimer, this.killAfkTimer, this.autoRespawnTimer, this.startTimerLeft]:
            if timer != None:
                timer.cancel()

        if this.getPlayerCount() >= this.server.needToFirst:
            this.eventMap += 1

        if this.initVotingMode:
            if not this.isVotingBox and (this.mapPerma == 0 and this.mapCode != -1) and this.getPlayerCount() >= 2:
                this.isVotingMode = True
                this.isVotingBox = True
                this.voteCloseTimer = TFMUtils.callLater(8, this.closeVoting)
                for client in this.clients.values():
                    client.sendPacket(Identifiers.old.send.Vote_Box, [
                                      this.mapName, this.mapYesVotes, this.mapNoVotes])
            else:
                this.votingMode = False
                this.closeVoting()

        elif this.isTribeHouse and this.isTribeHouseMap:
            pass
        else:
            if this.isVotingMode:
                TotalYes = this.mapYesVotes + this.receivedYes
                TotalNo = this.mapNoVotes + this.receivedNo
                isDel = False

                if TotalYes + TotalNo >= 100:
                    TotalVotes = TotalYes + TotalNo
                    Rating = (1.0 * TotalYes / TotalNo) * 100
                    rate = str(Rating).split(".")
                    if int(rate[0]) < 50:
                        isDel = True
                this.Cursor.execute("update MapEditor set YesVotes = ?, NoVotes = ?, Perma = 44 where Code = ?", [TotalYes, TotalNo, this.mapCode]) if isDel else this.Cursor.execute(
                    "update MapEditor set YesVotes = ?, NoVotes = ? where Code = ?", [TotalYes, TotalNo, this.mapCode])
                this.isVotingMode = False
                this.receivedNo = 0
                this.receivedYes = 0
                for client in this.clients.values():
                    client.qualifiedVoted = False
                    client.isVoted = False

            this.initVotingMode = True

            this.lastRoundCode += 1
            this.lastRoundCode %= 127

            if this.isSurvivor:
                for client in this.clients.values():
                    if not client.isDead and (not client.isVampire if this.isSurvivorVamp else not client.isShaman):
                        if not this.noAutoScore:
                            client.playerScore += 10

            if this.catchTheCheeseMap:
                this.catchTheCheeseMap = False
            else:
                numCom = this.FSnumCompleted - 1 if this.isDoubleMap else this.numCompleted - 1
                numCom2 = this.SSnumCompleted - 1 if this.isDoubleMap else 0
                if numCom < 0:
                    numCom = 0
                if numCom2 < 0:
                    numCom2 = 0

                player = this.clients.get(this.currentShamanName)
                if player != None:
                    this.sendAll(Identifiers.old.send.Shaman_Perfomance, [
                                 this.currentShamanName, numCom])
                    if not this.noAutoScore:
                        player.playerScore = numCom
                    if numCom > 0:
                        player.skillModule.earnExp(True, numCom)

                player2 = this.clients.get(this.currentSecondShamanName)
                if player2 != None:
                    this.sendAll(Identifiers.old.send.Shaman_Perfomance, [
                                 this.currentSecondShamanName, numCom2])
                    if not this.noAutoScore:
                        player2.playerScore = numCom2
                    if numCom2 > 0:
                        player2.skillModule.earnExp(True, numCom2)

            if this.isSurvivor and this.getPlayerCount() >= this.server.needToFirst:
                this.giveSurvivorStats()
            elif this.isRacing and this.getPlayerCount() >= this.server.needToFirst:
                this.giveRacingStats()

            this.currentSyncCode = -1
            this.currentSyncName = ""
            this.currentShamanCode = -1
            this.currentSecondShamanCode = -1
            this.currentShamanName = ""
            this.currentSecondShamanName = ""
            this.currentShamanType = -1
            this.currentSecondShamanType = -1
            this.currentShamanSkills = {}
            this.currentSecondShamanSkills = {}
            this.changed20secTimer = False
            this.isDoubleMap = False
            this.isNoShamanMap = False
            this.FSnumCompleted = 0
            this.SSnumCompleted = 0
            this.objectID = 0
            this.tempTotemCount = -1
            this.addTime = 0
            this.cloudID = -1
            this.companionBox = -1
            this.lastHandymouse = [-1, -1]
            this.isTribeHouseMap = False
            this.canChangeMap = True
            this.changeMapAttemps = 0

            this.getSyncCode()

            this.anchors = []

            this.mapStatus += 1
            this.mapStatus %= 13
            this.musicMapStatus += 1
            this.musicMapStatus %= 6
            this.survivorMapStatus += 1
            this.survivorMapStatus %= 11

            this.isRacingP17 = not this.isRacingP17
            this.isBootcampP13 = not this.isBootcampP13
            this.isVanillaP41 = not this.isVanillaP41

            this.numCompleted = 0
            this.mapTime = 30 if this.mapCode == 42 and (this.mapXML == "" or this.mapName == "Transformice") else 0

            this.currentMap = this.selectMap()
            this.checkVanillaXML()

            if not this.noShamanSkills:
                player = this.clients.get(this.currentShamanName)
                if player != None:
                    if this.currentShamanName != None:
                        player.skillModule.getTimeSkill()

                    if this.currentSecondShamanName != None:
                        player.skillModule.getTimeSkill()

            if this.currentMap in [range(44, 54), range(138, 144)] or this.mapPerma == 8 and this.getPlayerCount() >= 2:
                this.isDoubleMap = True

            if this.mapPerma == 7 or this.mapPerma == 42 or this.isSurvivorVamp:
                this.isNoShamanMap = True

            if this.currentMap in range(108, 114):
                this.catchTheCheeseMap = True

            this.gameStartTime = TFMUtils.getTime()
            this.gameStartTimeMillis = time.time()
            this.isCurrentlyPlay = False

            for player in this.clients.values():
                player.resetPlay()

            for player in this.clients.values():
                player.startPlay()
                if player.isHidden:
                    player.sendPlayerDisconnect()

            if this.getPlayerCountUnique() >= this.server.needToFirst and this.server.adventureID == 52:
                localGift = random.randint(0, 30)
                if not this.isDefilante and not this.isSurvivor and not this.isTutorial and not this.isTotemEditeur and not this.isTribeHouse and not this.isMulodrome and not this.isMusic and not this.isEditeur and not this.isMinigame and not this.isEventMap:
                    for player in this.clients.values():
                        player.sendPacket([5, 51], ByteArray().writeByte(52).writeByte(
                            1).writeShort(1).writeShort(localGift).writeShort(-100).toByteArray())
                        player.sendPacket([100, 101], "\x01\x01")

            for player in this.clients.values():
                if player.pet != 0:
                    if TFMUtils.getSecondsDiff(player.petEnd) >= 0:
                        player.pet = 0
                        player.petEnd = 0
                    else:
                        this.sendAll(Identifiers.send.Pet, ByteArray().writeInt(
                            player.playerCode).writeByte(player.pet).toByteArray())

            if this.isSurvivorVamp:
                TFMUtils.callLater(5, this.sendVampireMode)

            if this.isMulodrome:
                this.mulodromeRoundCount += 1
                this.sendMulodromeRound()

                if this.mulodromeRoundCount <= 10:
                    for client in this.clients.values():
                        if client.Username in this.blueTeam:
                            this.setNameColor(
                                client.Username, int("979EFF", 16))
                        else:
                            this.setNameColor(
                                client.Username, int("FF9396", 16))
            else:
                this.sendAll(Identifiers.send.Mulodrome_End)

            if this.isMinigame:
                this.minigame.mapChange(this)

            if this.isRacing or this.isDefilante:
                this.roundsCount = (this.roundsCount + 1) % 10
                player = this.clients.get(this.getHighestScore())
                this.sendAll(Identifiers.send.Rounds_Count, ByteArray().writeByte(
                    this.roundsCount).writeInt(player.playerCode if player != None else 0).toByteArray())
                if this.roundsCount == 9:
                    for client in this.clients.values():
                        client.playerScore = 0

            this.startTimerLeft = TFMUtils.callLater(3, this.startTimer)
            this.closeRoomRoundJoinTimer = TFMUtils.callLater(
                3, setattr, this, "isCurrentlyPlay", True)
            if not this.isFixedMap and not this.isTribeHouse and not this.isTribeHouseMap:
                this.changeMapTimer = TFMUtils.callLater(
                    this.roundTime + this.addTime, this.mapChange)

            this.killAfkTimer = TFMUtils.callLater(30, this.killAfk)
            if this.autoRespawn or this.isTribeHouseMap:
                this.autoRespawnTimer = TFMUtils.callLater(2, this.respawnMice)

    def getPlayerCount(this):
        count = 0
        for client in this.clients.values():
            if not client.isHidden and not client.isTribunal:
                count += 1
        return count

    def getPlayerCountUnique(this):
        ipList = []
        for client in this.clients.values():
            if not client.ipAddress in ipList:
                ipList.append(client.ipAddress)
        return len(ipList)

    def getPlayerList(this, isTribunal):
        result = []
        for client in this.clients.values():
            if not client.isHidden and not client.isTribunal:
                result.append(client.getPlayerData(isTribunal))
        return result

    def addClient(this, client):
        this.clients[client.Username] = client

        client.room = this
        client.isDead = this.isCurrentlyPlay
        #this.sendAllOthers(client, Identifiers.old.send.Player_Respawn, [client.getPlayerData()])
        if not client.isHidden and not client.isTribunal:
            this.sendAllOthers(client, Identifiers.send.Player_Respawn, ByteArray().writeBytes(
                client.getPlayerData(False)).writeBool(False).writeBool(True).toByteArray())
        client.startPlay()

    def removeClient(this, client):
        if client.Username in this.clients:
            del this.clients[client.Username]
            client.resetPlay()
            client.playerScore = 0
            client.sendPlayerDisconnect()

            if this.isMulodrome:
                if client.Username in this.redTeam:
                    this.redTeam.remove(client.Username)
                if client.Username in this.blueTeam:
                    this.blueTeam.remove(client.Username)

                if len(this.redTeam) == 0 and len(this.blueTeam) == 0:
                    this.mulodromeRoundCount = 10
                    this.sendMulodromeRound()

            if len(this.clients) == 0:
                for timer in [this.autoRespawnTimer, this.changeMapTimer, this.closeRoomRoundJoinTimer, this.endSnowTimer, this.killAfkTimer, this.voteCloseTimer]:
                    if timer != None:
                        timer.cancel()

                this.isClosed = True
                del this.server.rooms[this.name]
            else:
                if client.playerCode == this.currentSyncCode:
                    this.currentSyncCode = -1
                    this.currentSyncName = ""
                    this.getSyncCode()
                    for clientOnline in this.clients.values():
                        clientOnline.sendSync(this.currentSyncCode)
                this.checkShouldChangeMap()

    def checkShouldChangeMap(this):
        if (not (this.isBootcamp or this.autoRespawn or (this.isTribeHouse and this.isTribeHouseMap) or this.isFixedMap)):
            for client in this.clients.values():
                if not client.isDead:
                    alivePeople = True
                    break
                else:
                    alivePeople = False
            if not alivePeople:
                this.mapChange()

    def sendAll(this, identifiers, packet=""):
        for client in this.clients.values():
            client.sendPacket(identifiers, packet)

    def sendAllOthers(this, senderClient, identifiers, packet=""):
        for client in this.clients.values():
            if not client == senderClient:
                client.sendPacket(identifiers, packet)

    def sendAllChat(this, playerCode, playerName, message, LangueByte, isOnly):
        p = ByteArray().writeInt(playerCode).writeUTF(
            playerName).writeByte(LangueByte).writeUTF(message)
        if not isOnly:
            for client in this.clients.values():
                client.sendPacket(
                    Identifiers.send.Chat_Message, p.toByteArray())
        else:
            client = this.clients.get(playerName)
            if client != None:
                client.sendPacket(
                    Identifiers.send.Chat_Message, p.toByteArray())

    def addImage(this, id, image, targetID, playerCode, x, y, targetPlayer):
        p = ByteArray().writeInt(id).writeUTF(image).writeByte(
            targetID).writeInt(playerCode).writeShort(x).writeShort(y)
        if targetPlayer == "":
            this.sendAll([29, 19], p.toByteArray())
        else:
            client = this.clients.get(targetPlayer)
            if client != None:
                client.sendPacket([29, 19], p.toByteArray())

    def addImageLUA(this, imageName, target, x, y, targetPlayer):
        this.lastImageID += 1
        p = ByteArray().writeInt(this.lastImageID).writeUTF(imageName).writeByte(
            1 if target.startswith("#") else 2 if target.startswith("$") else 3 if target.startswith("%") else 4 if target.startswith("?") else 5 if target.startswith("_") else 6 if target.startswith("!") else 7 if target.startswith("&") else 0).writeInt(int(target) if target.isdigit() else this.server.getPlayerCode(TFMUtils.parsePlayerName(target))).writeShort(x).writeShort(y)
        if targetPlayer == "":
            this.sendAll([29, 19], p.toByteArray())
        else:
            client = this.clients.get(targetPlayer)
            if client != None:
                client.sendPacket([29, 19], p.toByteArray())

    def removeImage(this, id, targetPlayer):
        p = ByteArray().writeInt(id)
        if targetPlayer == "":
            this.sendAll([29, 18], p.toByteArray())
        else:
            client = this.clients.get(targetPlayer)
            if client != None:
                client.sendPacket([29, 18], p.toByteArray())

    def getSyncCode(this):
        if this.getPlayerCount() > 0:
            if this.currentSyncCode == -1:
                players = this.clients
                values = players.values()
                client = random.choice(list(values))
                this.currentSyncCode = client.playerCode
                this.currentSyncName = client.Username
        else:
            if this.currentSyncCode == -1:
                this.currentSyncCode = 0
                this.currentSyncName = ""

        return this.currentSyncCode

    def selectMap(this):
        if not this.forceNextMap == "-1":
            force = this.forceNextMap
            this.forceNextMap = "-1"
            this.mapCode = -1

            if force.isdigit():
                return this.selectMapSpecificic(force, "Vanilla")
            elif force.startswith("@"):
                return this.selectMapSpecificic(force[1:], "Custom")
            elif force.startswith("#"):
                return this.selectMapSpecificic(force[1:], "Perm")
            elif force.startswith("<"):
                return this.selectMapSpecificic(force, "Xml")
            else:
                return 0

        elif this.specificMap:
            this.mapCode = -1
            return this.currentMap
        else:
            if this.isEditeur:
                return this.EMapCode

            elif this.isTribeHouse:
                tribeName = this.roomName[2:]
                runMap = this.server.getTribeHouse(tribeName)

                if runMap == 0:
                    this.mapCode = 0
                    this.mapName = "Tigrounette"
                    this.mapXML = "<C><P /><Z><S><S Y=\"360\" T=\"0\" P=\"0,0,0.3,0.2,0,0,0,0\" L=\"800\" H=\"80\" X=\"400\" /></S><D><P Y=\"0\" T=\"34\" P=\"0,0\" X=\"0\" C=\"719b9f\" /><T Y=\"320\" X=\"49\" /><P Y=\"320\" T=\"16\" X=\"224\" P=\"0,0\" /><P Y=\"319\" T=\"17\" X=\"311\" P=\"0,0\" /><P Y=\"284\" T=\"18\" P=\"1,0\" X=\"337\" C=\"57703e,e7c3d6\" /><P Y=\"284\" T=\"21\" X=\"294\" P=\"0,0\" /><P Y=\"134\" T=\"23\" X=\"135\" P=\"0,0\" /><P Y=\"320\" T=\"24\" P=\"0,1\" X=\"677\" C=\"46788e\" /><P Y=\"320\" T=\"26\" X=\"588\" P=\"1,0\" /><P Y=\"193\" T=\"14\" P=\"0,0\" X=\"562\" C=\"95311e,bde8f3,faf1b3\" /></D><O /></Z></C>"
                    this.mapYesVotes = 0
                    this.mapNoVotes = 0
                    this.mapPerma = 22
                    this.mapInverted = False
                else:
                    run = this.selectMapSpecificic(runMap, "Custom")
                    if run != -1:
                        this.mapCode = 0
                        this.mapName = "Tigrounette"
                        this.mapXML = "<C><P /><Z><S><S Y=\"360\" T=\"0\" P=\"0,0,0.3,0.2,0,0,0,0\" L=\"800\" H=\"80\" X=\"400\" /></S><D><P Y=\"0\" T=\"34\" P=\"0,0\" X=\"0\" C=\"719b9f\" /><T Y=\"320\" X=\"49\" /><P Y=\"320\" T=\"16\" X=\"224\" P=\"0,0\" /><P Y=\"319\" T=\"17\" X=\"311\" P=\"0,0\" /><P Y=\"284\" T=\"18\" P=\"1,0\" X=\"337\" C=\"57703e,e7c3d6\" /><P Y=\"284\" T=\"21\" X=\"294\" P=\"0,0\" /><P Y=\"134\" T=\"23\" X=\"135\" P=\"0,0\" /><P Y=\"320\" T=\"24\" P=\"0,1\" X=\"677\" C=\"46788e\" /><P Y=\"320\" T=\"26\" X=\"588\" P=\"1,0\" /><P Y=\"193\" T=\"14\" P=\"0,0\" X=\"562\" C=\"95311e,bde8f3,faf1b3\" /></D><O /></Z></C>"
                        this.mapYesVotes = 0
                        this.mapNoVotes = 0
                        this.mapPerma = 22
                        this.mapInverted = False

            elif this.is801Room or this.isVillage:
                return 801

            elif "#unotfm" in this.roomName:
                this.mapCode = 0
                this.mapName = "UNO!"
                color = random.randint(0, 7)
                if color == 0:
                    this.mapXML = str('<C><P /><Z><S><S P="0,0,0.3,0.2,0,0,0,0" L="1200" o="442600" X="400" c="3" Y="135" T="12" H="40" /><S L="166" H="10" X="-129" Y="79" T="3" P="0,0,0,9999,90,0,0,0" /><S c="4" L="800" o="442600" H="60" X="400" N="" Y="370" T="12" P="0,0,0.3,0.2,0,0,0,0" /><S H="40" L="1200" o="442600" N="" X="400" c="4" Y="126" T="12" P="0,0,0.3,0.2,0,0,0,0" /><S L="166" X="930" H="10" Y="79" T="3" P="0,0,0,9999,90,0,0,0" /><S P="0,0,0,0.2,0,0,0,0" L="200" o="6a7495" H="3000" c="4" N="" Y="200" T="12" X="-100" /><S P="0,0,0,0.2,0,0,0,0" L="200" o="6a7495" X="900" c="4" N="" Y="200" T="12" H="3000" /><S P="0,0,0,0.2,0,0,0,0" L="800" o="6a7495" H="100" c="4" N="" Y="-41" T="12" X="400" /></S><D><P C="1e005b" P="0,0" T="34" Y="115" X="0" /><DS Y="99" X="402" /></D><O /></Z></C>')
                elif color == 1:
                    this.mapXML = str('<C><P /><Z><S><S L="166" H="10" X="-129" Y="79" T="3" P="0,0,0,9999,90,0,0,0" /><S P="0,0,0.3,0.2,0,0,0,0" L="1200" o="5589d4" X="400" c="3" N="" Y="133" T="12" H="40" /><S H="60" L="800" o="5589d4" X="400" c="4" N="" Y="370" T="12" P="0,0,0.3,0.2,0,0,0,0" /><S L="166" X="930" H="10" Y="79" T="3" P="0,0,0,9999,90,0,0,0" /><S P="0,0,0,0.2,0,0,0,0" L="200" o="6a7495" H="3000" c="4" N="" Y="200" T="12" X="-100" /><S P="0,0,0,0.2,0,0,0,0" L="200" o="6a7495" X="900" c="4" N="" Y="200" T="12" H="3000" /><S P="0,0,0,0.2,0,0,0,0" L="800" o="6a7495" H="100" c="4" N="" Y="-41" T="12" X="400" /><S P="0,0,0.3,0.2,0,0,0,0" L="800" o="47ad" X="400" c="4" N="" Y="248" T="12" H="190" /></S><D><DS Y="100" X="400" /><P C="867f7f" Y="142" T="19" X="350" P="0,0" /><P C="867f7f" Y="142" T="19" P="0,0" X="50" /><P C="867f7f" Y="142" T="19" X="150" P="0,0" /><P C="867f7f" Y="142" T="19" P="0,0" X="250" /><P C="867f7f" Y="142" T="19" P="0,0" X="450" /><P C="867f7f" Y="142" T="19" X="750" P="0,0" /><P C="867f7f" Y="142" T="19" P="0,0" X="650" /><P C="867f7f" Y="142" T="19" X="550" P="0,0" /></D><O /></Z></C>')
                elif color == 2:
                    this.mapXML = str('<C><P /><Z><S><S L="166" X="-129" H="10" Y="79" T="3" P="0,0,0,9999,90,0,0,0" /><S H="40" L="1200" o="6f091e" X="400" c="3" N="" Y="133" T="12" P="0,0,0.3,0.2,0,0,0,0" /><S P="0,0,0.3,0.2,0,0,0,0" L="800" o="6f091e" X="400" c="4" N="" Y="370" T="12" H="60" /><S L="166" H="10" X="930" Y="79" T="3" P="0,0,0,9999,90,0,0,0" /><S X="-100" L="200" o="6a7495" H="3000" c="4" N="" Y="200" T="12" P="0,0,0,0.2,0,0,0,0" /><S H="3000" L="200" o="6a7495" X="901" c="4" N="" Y="200" T="12" P="0,0,0,0.2,0,0,0,0" /><S X="400" L="800" o="6a7495" H="100" c="4" N="" Y="-41" T="12" P="0,0,0,0.2,0,0,0,0" /><S H="190" L="800" o="8f0b28" X="400" c="4" N="" Y="248" T="12" P="0,0,0.3,0.2,0,0,0,0" /></S><D><DS Y="100" X="400" /><P P="0,0" C="867f7f" Y="142" T="19" X="350" /><P C="867f7f" Y="142" T="19" X="50" P="0,0" /><P C="867f7f" Y="142" T="19" P="0,0" X="150" /><P C="867f7f" Y="142" T="19" X="250" P="0,0" /><P C="867f7f" Y="142" T="19" X="450" P="0,0" /><P C="867f7f" Y="142" T="19" P="0,0" X="750" /><P C="867f7f" Y="142" T="19" X="650" P="0,0" /><P C="867f7f" Y="142" T="19" P="0,0" X="550" /></D><O /></Z></C>')
                elif color == 3:
                    this.mapXML = str('<C><P /><Z><S><S L="166" H="10" X="-129" Y="79" T="3" P="0,0,0,9999,90,0,0,0" /><S P="0,0,0.3,0.2,0,0,0,0" L="1200" o="152216" X="400" c="3" N="" Y="133" T="12" H="40" /><S H="60" L="800" o="152216" X="400" c="4" N="" Y="370" T="12" P="0,0,0.3,0.2,0,0,0,0" /><S L="166" X="930" H="10" Y="79" T="3" P="0,0,0,9999,90,0,0,0" /><S P="0,0,0,0.2,0,0,0,0" L="200" o="6a7495" H="3000" c="4" N="" Y="200" T="12" X="-100" /><S P="0,0,0,0.2,0,0,0,0" L="200" o="6a7495" X="900" c="4" N="" Y="200" T="12" H="3000" /><S P="0,0,0,0.2,0,0,0,0" L="800" o="6a7495" H="100" c="4" N="" Y="-41" T="12" X="400" /><S P="0,0,0.3,0.2,0,0,0,0" L="800" o="355535" X="400" c="4" N="" Y="248" T="12" H="190" /></S><D><DS Y="100" X="400" /><P C="867f7f" Y="142" T="19" X="350" P="0,0" /><P C="867f7f" Y="142" T="19" P="0,0" X="50" /><P C="867f7f" Y="142" T="19" X="150" P="0,0" /><P C="867f7f" Y="142" T="19" P="0,0" X="250" /><P C="867f7f" Y="142" T="19" P="0,0" X="450" /><P C="867f7f" Y="142" T="19" X="750" P="0,0" /><P C="867f7f" Y="142" T="19" P="0,0" X="650" /><P C="867f7f" Y="142" T="19" X="550" P="0,0" /></D><O /></Z></C>')
                elif color == 4:
                    this.mapXML = str('<C><P /><Z><S><S L="166" X="-129" H="10" Y="79" T="3" P="0,0,0,9999,90,0,0,0" /><S H="40" L="1200" o="423223" X="400" c="3" N="" Y="133" T="12" P="0,0,0.3,0.2,0,0,0,0" /><S P="0,0,0.3,0.2,0,0,0,0" L="800" o="423223" X="400" c="4" N="" Y="370" T="12" H="60" /><S L="166" H="10" X="930" Y="79" T="3" P="0,0,0,9999,90,0,0,0" /><S X="-100" L="200" o="6a7495" H="3000" c="4" N="" Y="200" T="12" P="0,0,0,0.2,0,0,0,0" /><S H="3000" L="200" o="6a7495" X="900" c="4" N="" Y="200" T="12" P="0,0,0,0.2,0,0,0,0" /><S X="400" L="800" o="6a7495" H="100" c="4" N="" Y="-41" T="12" P="0,0,0,0.2,0,0,0,0" /><S H="190" L="800" o="785a40" X="400" c="4" N="" Y="248" T="12" P="0,0,0.3,0.2,0,0,0,0" /></S><D><DS Y="100" X="400" /><P C="867f7f" Y="142" T="19" P="0,0" X="350" /><P C="867f7f" Y="142" T="19" X="50" P="0,0" /><P C="867f7f" Y="142" T="19" P="0,0" X="150" /><P C="867f7f" Y="142" T="19" X="250" P="0,0" /><P C="867f7f" Y="142" T="19" X="450" P="0,0" /><P C="867f7f" Y="142" T="19" P="0,0" X="750" /><P C="867f7f" Y="142" T="19" X="650" P="0,0" /><P C="867f7f" Y="142" T="19" P="0,0" X="550" /></D><O /></Z></C>')
                elif color == 5:
                    this.mapXML = str('<C><P /><Z><S><S L="166" X="-129" H="10" Y="79" T="3" P="0,0,0,9999,90,0,0,0" /><S H="40" L="1200" o="392774" X="400" c="3" N="" Y="133" T="12" P="0,0,0.3,0.2,0,0,0,0" /><S P="0,0,0.3,0.2,0,0,0,0" L="800" o="392774" X="400" c="4" N="" Y="370" T="12" H="60" /><S L="166" H="10" X="930" Y="79" T="3" P="0,0,0,9999,90,0,0,0" /><S X="-100" L="200" o="6a7495" H="3000" c="4" N="" Y="200" T="12" P="0,0,0,0.2,0,0,0,0" /><S H="3000" L="200" o="6a7495" X="900" c="4" N="" Y="200" T="12" P="0,0,0,0.2,0,0,0,0" /><S X="400" L="800" o="6a7495" H="100" c="4" N="" Y="-41" T="12" P="0,0,0,0.2,0,0,0,0" /><S H="190" L="800" o="f0262" X="400" c="4" N="" Y="248" T="12" P="0,0,0.3,0.2,0,0,0,0" /></S><D><DS Y="100" X="400" /><P C="867f7f" Y="142" T="19" P="0,0" X="350" /><P C="867f7f" Y="142" T="19" X="50" P="0,0" /><P C="867f7f" Y="142" T="19" P="0,0" X="150" /><P C="867f7f" Y="142" T="19" X="250" P="0,0" /><P C="867f7f" Y="142" T="19" X="450" P="0,0" /><P C="867f7f" Y="142" T="19" P="0,0" X="750" /><P C="867f7f" Y="142" T="19" X="650" P="0,0" /><P C="867f7f" Y="142" T="19" P="0,0" X="550" /></D><O /></Z></C>')
                elif color == 6:
                    this.mapXML = str('<C><P /><Z><S><S L="166" X="-129" H="10" Y="79" T="3" P="0,0,0,9999,90,0,0,0" /><S H="40" L="1200" o="34292a" X="400" c="3" N="" Y="133" T="12" P="0,0,0.3,0.2,0,0,0,0" /><S P="0,0,0.3,0.2,0,0,0,0" L="800" o="34292a" X="400" c="4" N="" Y="370" T="12" H="60" /><S L="166" H="10" X="930" Y="79" T="3" P="0,0,0,9999,90,0,0,0" /><S X="-100" L="200" o="6a7495" H="3000" c="4" N="" Y="200" T="12" P="0,0,0,0.2,0,0,0,0" /><S H="3000" L="200" o="6a7495" X="900" c="4" N="" Y="200" T="12" P="0,0,0,0.2,0,0,0,0" /><S X="400" L="800" o="6a7495" H="100" c="4" N="" Y="-41" T="12" P="0,0,0,0.2,0,0,0,0" /><S H="190" L="800" o="423535" X="400" c="4" N="" Y="248" T="12" P="0,0,0.3,0.2,0,0,0,0" /></S><D><DS Y="100" X="400" /><P C="867f7f" Y="142" T="19" P="0,0" X="350" /><P C="867f7f" Y="142" T="19" X="50" P="0,0" /><P C="867f7f" Y="142" T="19" P="0,0" X="150" /><P C="867f7f" Y="142" T="19" X="250" P="0,0" /><P C="867f7f" Y="142" T="19" X="450" P="0,0" /><P C="867f7f" Y="142" T="19" P="0,0" X="750" /><P C="867f7f" Y="142" T="19" X="650" P="0,0" /><P C="867f7f" Y="142" T="19" P="0,0" X="550" /></D><O /></Z></C>')
                elif color == 7:
                    this.mapXML = str('<C><P /><Z><S><S L="166" X="-129" H="10" Y="79" T="3" P="0,0,0,9999,90,0,0,0" /><S H="40" L="1200" o="2e4417" X="400" c="3" N="" Y="133" T="12" P="0,0,0.3,0.2,0,0,0,0" /><S P="0,0,0.3,0.2,0,0,0,0" L="800" o="2e4417" X="400" c="4" N="" Y="370" T="12" H="60" /><S L="166" H="10" X="930" Y="79" T="3" P="0,0,0,9999,90,0,0,0" /><S X="-100" L="200" o="6a7495" H="3000" c="4" N="" Y="200" T="12" P="0,0,0,0.2,0,0,0,0" /><S H="3000" L="200" o="6a7495" X="900" c="4" N="" Y="200" T="12" P="0,0,0,0.2,0,0,0,0" /><S X="400" L="800" o="6a7495" H="100" c="4" N="" Y="-41" T="12" P="0,0,0,0.2,0,0,0,0" /><S H="190" L="800" o="3e4932" X="400" c="4" N="" Y="248" T="12" P="0,0,0.3,0.2,0,0,0,0" /></S><D><DS Y="100" X="400" /><P C="867f7f" Y="142" T="19" P="0,0" X="350" /><P C="867f7f" Y="142" T="19" X="50" P="0,0" /><P C="867f7f" Y="142" T="19" P="0,0" X="150" /><P C="867f7f" Y="142" T="19" X="250" P="0,0" /><P C="867f7f" Y="142" T="19" X="450" P="0,0" /><P C="867f7f" Y="142" T="19" P="0,0" X="750" /><P C="867f7f" Y="142" T="19" X="650" P="0,0" /><P C="867f7f" Y="142" T="19" P="0,0" X="550" /></D><O /></Z></C>')
                this.mapYesVotes = 0
                this.mapNoVotes = 0
                this.mapPerma = -1
                this.mapInverted = False

            elif this.eventMap >= 3 and this.server.adventureID == 52:
                this.getMapNatal()
                this.eventMap = 0
                if this.mapCode == 1:
                    this.isEventMap = True
                    this.isEventMap2 = False
                    for room in this.server.rooms.values():
                        if room.name == this.name:
                            for playerCode, client in room.clients.items():
                                client.sendLangueMessage("", "<ROSE>Vá atras dos presentes e ganhe prêmios!")
                else:
                    this.isEventMap2 = True
                    this.isEventMap = False

            else:
                this.mapCode = -1
                this.mapName = "Invalid"
                this.mapXML = "<C><P /><Z><S /><D /><O /></Z></C>"
                this.mapYesVotes = 0
                this.mapNoVotes = 0
                this.mapPerma = -1
                this.mapInverted = False
                return this.selectMapStatus(this.mapStatus)
        return -1

    def selectMapStatus(this, mapStatus):
        customMaps = [0, -1, 4, 9, 5, 0, -1, 8, 6, 7]
        mapList = []

        if this.isVanilla:
            if this.isVanillaP41:
                this.Cursor.execute(
                    "select Code from MapEditor where Perma = 41 ORDER BY RANDOM() LIMIT 1")
                r = this.Cursor.fetchall()
                for rs in r:
                    mapList.append(rs[0])
            else:
                map = random.choice(this.MapList)
                while map == this.currentMap:
                    map = random.choice(this.MapList)
                return map

        elif this.isMusic:
            if this.musicMapStatus == 5:
                this.Cursor.execute(
                    "select Code from MapEditor where Perma = 19 ORDER BY RANDOM() LIMIT 1")
                r = this.Cursor.fetchall()
                for rs in r:
                    mapList.append(rs[0])

        elif this.isUtility:
            this.Cursor.execute(
                "select Code from MapEditor where Perma = 45 ORDER BY RANDOM() LIMIT 1")
            r = this.Cursor.fetchall()
            for rs in r:
                mapList.append(rs[0])

        elif this.isPropHunt:
            this.Cursor.execute(
                "select Code from MapEditor where Perma = 47 ORDER BY RANDOM() LIMIT 1")
            r = this.Cursor.fetchall()
            for rs in r:
                mapList.append(rs[0])

        elif this.isRacing or this.isTribeWar:
            this.Cursor.execute(
                "select Code from MapEditor where Perma = 17 ORDER BY RANDOM() LIMIT 1")
            r = this.Cursor.fetchall()
            for rs in r:
                mapList.append(rs[0])

        elif this.isBootcamp:
            P3List = []
            P13List = []

            this.Cursor.execute(
                "select Code, Perma from MapEditor where Perma = 3 or Perma = 13 ORDER BY RANDOM() LIMIT 1")
            r = this.Cursor.fetchall()
            for rs in r:
                perma = rs[1]
                if perma == 3:
                    P3List.append(rs[0])
                else:
                    P13List.append(rs[0])

            if this.isBootcampP13:
                mapList = P3List if len(P13List) == 0 else P13List
            else:
                mapList = P13List if len(P3List) == 0 else P3List

        elif this.isSurvivor:
            this.isSurvivorVamp = this.survivorMapStatus == 10

            this.Cursor.execute("select Code from MapEditor where Perma = ?", [
                                11 if this.isSurvivorVamp else 10])
            r = this.Cursor.fetchall()
            for rs in r:
                mapList.append(rs[0])

        elif this.isDefilante:
            this.Cursor.execute(
                "select Code from MapEditor where Perma = 18 ORDER BY RANDOM() LIMIT 1")
            r = this.Cursor.fetchall()
            for rs in r:
                mapList.append(rs[0])

        elif mapStatus in customMaps:
            multiple = False
            selectCode = 0

            if mapStatus == 1 or mapStatus == 9:
                multiple = True
            elif mapStatus == 2:
                selectCode = 5
            elif mapStatus == 3:
                selectCode = 9
            elif mapStatus == 5 or mapStatus == 11:
                selectCode = 6
            elif mapStatus == 6:
                selectCode = 7
            elif mapStatus == 7:
                selectCode = 8
            elif mapStatus == 10:
                selectCode = 4

            if multiple:
                this.Cursor.execute(
                    "select Code from MapEditor where Perma = 0 ORDER BY RANDOM() LIMIT 1")
                r = this.Cursor.fetchall()
                for rs in r:
                    mapList.append(rs[0])

                this.Cursor.execute(
                    "select Code from MapEditor where Perma = 1 ORDER BY RANDOM() LIMIT 1")
                r = this.Cursor.fetchall()
                for rs in r:
                    mapList.append(rs[0])
            else:
                this.Cursor.execute(
                    "select Code from MapEditor where Perma = ? ORDER BY RANDOM() LIMIT 1", [selectCode])
                r = this.Cursor.fetchall()
                for rs in r:
                    mapList.append(rs[0])
        else:
            P41 = random.randint(0, 10) < 3
            if P41:
                this.Cursor.execute(
                    "select Code from MapEditor where Perma = 41 ORDER BY RANDOM() LIMIT 1")
                r = this.Cursor.fetchall()
                for rs in r:
                    mapList.append(rs[0])
            else:
                map = random.choice(this.MapList)
                while map == this.currentMap:
                    map = random.choice(this.MapList)
                return map

        if len(mapList) >= 1:
            runMap = random.choice(mapList)
        else:
            runMap = 0

        if len(mapList) >= 2:
            while runMap == this.currentMap:
                runMap = random.choice(mapList)

        if runMap == 0:
            map = random.choice(this.MapList)
            while map == this.currentMap:
                map = random.choice(this.MapList)
            return map
        else:
            mapInfo = this.getMapInfo(runMap)
            this.mapCode = runMap
            this.mapName = str(mapInfo[0])
            this.mapXML = str(mapInfo[1])
            this.mapYesVotes = int(mapInfo[2])
            this.mapNoVotes = int(mapInfo[3])
            this.mapPerma = int(mapInfo[4])
            this.mapInverted = random.randint(0, 100) > 85
            return -1

    def selectMapSpecificic(this, code, type):
        if type == "Vanilla":
            return int(code)

        elif type == "Custom":
            mapInfo = this.getMapInfo(int(code))
            if mapInfo[0] == None:
                return 0
            else:
                this.mapCode = int(code)
                this.mapName = str(mapInfo[0])
                this.mapXML = str(mapInfo[1])
                this.mapYesVotes = int(mapInfo[2])
                this.mapNoVotes = int(mapInfo[3])
                this.mapPerma = int(mapInfo[4])
                this.mapInverted = False
                return -1

        elif type == "Perm":
            mapList = []
            this.Cursor.execute(
                "select Code from MapEditor where Perma = ? ORDER BY RANDOM() LIMIT 1", [int(str(code))])
            r = this.Cursor.fetchall()
            for rs in r:
                mapList.append(rs["Code"])

            if len(mapList) >= 1:
                runMap = random.choice(mapList)
            else:
                runMap = 0

            if len(mapList) >= 2:
                while runMap == this.currentMap:
                    runMap = random.choice(mapList)

            if runMap == 0:
                map = random.choice(this.MapList)
                while map == this.currentMap:
                    map = random.choice(this.MapList)
                return map
            else:
                mapInfo = this.getMapInfo(runMap)
                this.mapCode = runMap
                this.mapName = str(mapInfo[0])
                this.mapXML = str(mapInfo[1])
                this.mapYesVotes = int(mapInfo[2])
                this.mapNoVotes = int(mapInfo[3])
                this.mapPerma = int(mapInfo[4])
                this.mapInverted = False
                return -1

        elif type == "Xml":
            this.mapCode = 0
            this.mapName = "#Module"
            this.mapXML = str(code)
            this.mapYesVotes = 0
            this.mapNoVotes = 0
            this.mapPerma = 22
            this.mapInverted = False
            return -1

    def getMapInfo(this, mapCode):
        mapInfo = ["", "", 0, 0, 0]
        this.Cursor.execute(
            "select Name, XML, YesVotes, NoVotes, Perma from MapEditor where Code = ? ORDER BY RANDOM() LIMIT 1", [mapCode])
        rs = this.Cursor.fetchone()
        if rs:
            mapInfo = rs["Name"], rs["XML"], rs[
                "YesVotes"], rs["NoVotes"], rs["Perma"]

        return mapInfo

    def checkIfDeathMouse(this):
        count = 0
        for client in this.clients.values():
            if not client.isDead:
                count += 1
        return count <= 1

    def checkIfTooFewRemaining(this):
        count = 0
        for client in this.clients.values():
            if not client.isDead:
                count += 1
        return count <= 2

    def getAliveCount(this):
        count = 0
        for client in this.clients.values():
            if not client.isDead:
                count += 1
        return count

    def getDeathCountNoShaman(this):
        return len(filter(lambda player: not player.isShaman and not player.isDead and not player.isNewPlayer, this.clients.values()))

    def getHighestScore(this):
        scores = []

        for client in this.clients.values():
            scores.append(client.playerScore)

        try:
            for client in this.clients.values():
                if client.playerScore == max(scores):
                    return client.playerCode
        except:
            pass
        return 0

    def getSecondHighestScore(this):
        scores = []

        for client in this.clients.values():
            scores.append(client.playerScore)

        scores.remove(max(scores))

        try:
            for client in this.clients.values():
                if client.playerScore == max(scores):
                    return client.playerCode
        except:
            pass
        return 0

    def getShamanCode(this):
        if this.currentShamanCode == -1:
            if this.currentMap in this.noShamanMaps or this.isNoShamanMap:
                pass
            elif this.noShaman or (this.survivorMapStatus == 7 and this.isSurvivor):
                pass
            else:
                if this.forceNextShaman > 0:
                    this.currentShamanCode = this.forceNextShaman
                    this.forceNextShaman = 0
                else:
                    this.currentShamanCode = this.getHighestScore()

            if this.currentShamanCode == -1:
                this.currentShamanName = ""
            else:
                for client in this.clients.values():
                    if client.playerCode == this.currentShamanCode:
                        this.currentShamanName = client.Username
                        this.currentShamanType = client.shamanType
                        this.currentShamanSkills = client.playerSkills
                        break
        return this.currentShamanCode

    def getDoubleShamanCode(this):
        if this.currentShamanCode == -1 and this.currentSecondShamanCode == -1:
            if this.forceNextShaman > 0:
                this.currentShamanCode = this.forceNextShaman
                this.forceNextShaman = 0
            else:
                this.currentShamanCode = this.getHighestScore()

            if this.currentSecondShamanCode == -1:
                this.currentSecondShamanCode = this.getSecondHighestScore()

            if this.currentSecondShamanCode == this.currentShamanCode:
                values = this.clients.values()
                tempClient = random.choice(values)
                this.currentSecondShamanCode = tempClient.playerCode

            for client in this.clients.values():
                if client.playerCode == this.currentShamanCode:
                    this.currentShamanName = client.Username
                    this.currentShamanType = client.shamanType
                    this.currentShamanSkills = client.playerSkills
                    break

                if client.playerCode == this.currentSecondShamanCode:
                    this.currentSecondShamanName = client.Username
                    this.currentSecondShamanType = client.shamanType
                    this.currentSecondShamanSkills = client.playerSkills
                    break

        return [this.currentShamanCode, this.currentSecondShamanCode]

    def closeVoting(this):
        this.initVotingMode = False
        this.isVotingBox = False
        if this.voteCloseTimer != None:
            this.voteCloseTimer.cancel()
        this.mapChange()

    def killAllNoDie(this):
        for client in this.clients.values():
            if not client.isDead:
                client.isDead = True
        this.checkShouldChangeMap()

    def killAll(this):
        for client in this.clients.values():
            if not client.isDead:
                client.sendPlayerDied()
                client.isDead = True
        this.checkShouldChangeMap()

    def killShaman(this):
        for client in this.clients.values():
            if client.playerCode == this.currentShamanCode:
                client.isDead = True
                client.sendPlayerDied()
        this.checkShouldChangeMap()

    def killAfk(this):
        if not this.isEditeur or not this.isTotemEditeur or not this.isBootcamp or not this.isTribeHouseMap or not this.disableAfkKill:
            if ((TFMUtils.getTime() - this.gameStartTime) < 32 and (TFMUtils.getTime() - this.gameStartTime) > 28):
                for client in this.clients.values():
                    if not client.isDead and client.isAfk:
                        client.isDead = True
                        if not this.noAutoScore:
                            client.playerScore += 1
                        client.sendPlayerDied()
                this.checkShouldChangeMap()

    def checkIfDoubleShamansAreDead(this):
        client1 = this.clients.get(this.currentShamanName)
        client2 = this.clients.get(this.currentSecondShamanName)
        return (False if client1 == None else client1.isDead) and (False if client2 == None else client2.isDead)

    def checkIfShamanIsDead(this):
        client = this.clients.get(this.currentShamanName)
        return False if client == None else client.isDead

    def checkIfShamanCanGoIn(this):
        for client in this.clients.values():
            if client.playerCode != this.currentShamanCode and client.playerCode != this.currentSecondShamanCode and not client.isDead:
                return False
        return True

    def giveShamanSave(this, shamanName, type):
        if not this.countStats:
            return

        client = this.clients.get(shamanName)
        if client != None:
            if type == 0:
                client.shamanSaves += 1
                if 2 in client.dailyQuest:
                    missionType = client.DailyQuest.getMission(
                        2, client.playerID)[1]
                    if int(missionType) == 1:
                        client.DailyQuest.upMission(2, client.playerID)
            elif type == 1:
                client.hardModeSaves += 1
                if 2 in client.dailyQuest:
                    missionType = client.DailyQuest.getMission(
                        2, client.playerID)[1]
                    if int(missionType) == 2:
                        client.DailyQuest.upMission(2, client.playerID)
            elif type == 2:
                client.divineModeSaves += 1
                if 2 in client.dailyQuest:
                    missionType = client.DailyQuest.getMission(
                        2, client.playerID)[1]
                    if int(missionType) == 3:
                        client.DailyQuest.upMission(2, client.playerID)
            if client.privLevel != 0:
                counts = [client.shamanSaves,
                          client.hardModeSaves, client.divineModeSaves]
                titles = [this.server.shamanTitleList,
                          this.server.hardModeTitleList, this.server.divineModeTitleList]
                rebuilds = ["shaman", "hardmode", "divinemode"]
                if counts[type] in titles[type].keys():
                    title = titles[type][counts[type]]
                    client.checkAndRebuildTitleList(rebuilds[type])
                    client.sendUnlockedTitle(
                        int(title - (title % 1)), int(round((title % 1) * 10)))
                    client.sendCompleteTitleList()
                    client.sendTitleList()

    def respawnMice(this):
        for client in this.clients.values():
            if client.isDead:
                client.isDead = False
                client.playerStartTimeMillis = time.time()
                this.sendAll(Identifiers.send.Player_Respawn, ByteArray().writeBytes(
                    client.getPlayerData(False)).writeBool(False).writeBool(not this.isBootcamp).toByteArray())

            if client.room.isPropHunt:
                if client.isShaman:
                    if client.prophuntShamanLife >= 1:
                        client.room.addImage(
                            1, "155f60f85dc.png", 2, client.playerCode, -19, -48, "")
                    if client.prophuntShamanLife >= 2:
                        client.room.addImage(
                            2, "155f60f85dc.png", 2, client.playerCode, -9, -48, "")
                    if client.prophuntShamanLife >= 3:
                        client.room.addImage(
                            3, "155f60f85dc.png", 2, client.playerCode, 1, -48, "")

        if this.autoRespawn or this.isTribeHouseMap:
            this.autoRespawnTimer = TFMUtils.callLater(2, this.respawnMice)

    def respawnSpecific(this, playerName, isResetPlay=False):
        client = this.clients.get(playerName)
        if client != None and client.isDead:
            client.resetPlay(isResetPlay)
            client.isAfk = False
            client.isMoving = False
            client.playerStartTimeMillis = time.time()
            this.sendAll(Identifiers.send.Player_Respawn, ByteArray().writeBytes(
                client.getPlayerData(False)).writeBool(False).writeBool(not this.isBootcamp).toByteArray())

    def sendMessage(this, message, tab=False):
        for client in this.clients.values():
            client.sendMessage(message, tab)

    def sendMulodromeRound(this):
        this.sendAll(Identifiers.send.Mulodrome_Result, ByteArray().writeByte(
            this.mulodromeRoundCount).writeShort(this.blueCount).writeShort(this.redCount).toByteArray())
        if this.mulodromeRoundCount > 10:
            this.sendAll(Identifiers.send.Mulodrome_End, "")
            this.sendAll(Identifiers.send.Mulodrome_Winner, ByteArray().writeByte(2 if this.blueCount == this.redCount else (
                1 if this.blueCount < this.redCount else 0)).writeShort(this.blueCount).writeShort(this.redCount).toByteArray())
            this.isMulodrome = False
            this.mulodromeRoundCount = 0
            this.redCount = 0
            this.blueCount = 0
            this.redTeam = []
            this.blueTeam = []
            this.isRacing = False
            this.mapStatus = 1
            this.never20secTimer = False
            this.noShaman = False

    def checkVanillaXML(this):
        try:
            with open("./include/maps/vanilla/" + str(this.currentMap) + ".xml", "r") as f:
                XML = f.read()
                f.close()

                this.mapCode = int(this.currentMap)
                this.mapName = "Transformice"
                this.mapXML = str(XML)
                this.mapYesVotes = 0
                this.mapNoVotes = 0
                this.mapPerma = 2
                this.currentMap = -1
                this.mapInverted = False
        except:
            pass

    def getMapNatal(this):
        try:
            mapID = random.randint(1, 2)
            with open("./include/maps/natal/" + str(mapID) + ".xml", "r") as f:
                XML = f.read()
                f.close()

                this.mapCode = 0 + int(mapID)
                this.mapName = "Transformice"
                this.mapXML = str(XML)
                this.mapYesVotes = 0
                this.mapNoVotes = 0
                this.mapPerma = 2
                this.currentMap = -1
                this.mapInverted = False
        except:
            pass

    def sendVampireMode(this):
        client = this.clients.get(this.currentSyncName)
        if client != None:
            client.sendVampireMode(False)

    def bindKeyBoard(this, playerName: str, key: int, down: bool, yes: bool):
        client = this.clients.get(playerName)
        if client != None:
            client.sendPacket(Identifiers.send.Bind_Key_Board, ByteArray().writeShort(
                key).writeBool(down).writeBool(yes).toByteArray())

    def addPhysicObject(this, id, x, y, bodyDef):
        this.sendAll(Identifiers.send.Add_Physic_Object, ByteArray().writeShort(id).writeBool(bool(bodyDef["dynamic"]) if "dynamic" in bodyDef.keys() else False).writeByte(int(bodyDef["type"]) if "type" in bodyDef.keys() else 0).writeShort(x).writeShort(y).writeShort(int(bodyDef["width"]) if "width" in bodyDef.keys() else 0).writeShort(int(bodyDef["height"]) if "height" in bodyDef.keys() else 0).writeBool(bool(bodyDef["foreground"]) if "foreground" in bodyDef.keys() else False).writeShort(int(bodyDef["friction"]) if "friction" in bodyDef.keys() else 0).writeShort(int(bodyDef["restitution"]) if "restitution" in bodyDef.keys() else 0).writeShort(int(bodyDef["angle"]) if "angle" in bodyDef.keys() else 0).writeBool("color" in bodyDef.keys()).writeInt(int(bodyDef["color"]) if "color" in bodyDef.keys() else 0).writeBool(bool(bodyDef["miceCollision"]) if "miceCollision" in bodyDef.keys() else True).writeBool(bool(bodyDef["groundCollision"]) if "groundCollision" in bodyDef.keys() else True).writeBool(bool(bodyDef["fixedRotation"]) if "fixedRotation" in bodyDef.keys() else False).writeShort(int(bodyDef["mass"]) if "mass" in bodyDef.keys() else 0).writeShort(int(bodyDef["linearDamping"]) if "linearDamping" in bodyDef.keys() else 0).writeShort(int(bodyDef["angularDamping"]) if "angularDamping" in bodyDef.keys() else 0).writeBool(False).writeUTF("").toByteArray())

    def chatMessage(this, message, playerName):
        p = ByteArray().writeUTF(message)
        if playerName == "":
            this.sendAll(Identifiers.send.Message, p.toByteArray())
        else:
            client = this.clients.get(playerName)
            if client != None:
                client.sendPacket(Identifiers.send.Message, p.toByteArray())

    def removeObject(this, objectId):
        this.sendAll(Identifiers.send.Remove_Object, ByteArray(
        ).writeInt(objectId).writeBool(True).toByteArray())

    def movePlayer(this, playerName, xPosition, yPosition, pOffSet, xSpeed, ySpeed, sOffSet):
        client = this.clients.get(playerName)
        if client != None:
            client.sendPacket(Identifiers.send.Move_Player, ByteArray().writeShort(xPosition).writeShort(
                yPosition).writeBool(pOffSet).writeShort(xSpeed).writeShort(ySpeed).writeBool(sOffSet).toByteArray())

    def setNameColor(this, playerName, color):
        if playerName in this.clients.keys():
            this.sendAll(Identifiers.send.Set_Name_Color, ByteArray().writeInt(
                this.clients.get(playerName).playerCode).writeInt(color).toByteArray())

    def setGameTime(this, time, init = False):
        if init or (this.mapTime if this.mapTime > 0 else (this.roundTime + this.addTime)) + (this.gameStartTime - TFMUtils.getTime()) > time:
            for client in this.clients.values():
                client.sendRoundTime(time)

            this.roundTime = time * 1000
            this.luaStartTimeMillis = _time.time()
            this.changeMapTimers(time)

    def bindMouse(this, playerName: str, yes: bool):
        client = this.clients.get(playerName)
        if client != None:
            client.sendPacket(Identifiers.send.Bind_Mouse,
                              ByteArray().writeBool(yes).toByteArray())

    def addPopup(this, id, type, text, targetPlayer, x, y, width, fixedPos = False):
        p = ByteArray().writeInt(id).writeByte(type).writeUTF(
            text).writeShort(x).writeShort(y).writeShort(width).writeBool(fixedPos)
        if targetPlayer == "":
            this.sendAll(Identifiers.send.Add_Popup, p.toByteArray())
        else:
            player = this.clients.get(targetPlayer)
            if player != None:
                player.sendPacket(Identifiers.send.Add_Popup, p.toByteArray())

    def addTextArea(this, id, text, targetPlayer, x, y, width, height, backgroundColor, borderColor, backgroundAlpha, fixedPos):
        p = ByteArray().writeInt(id).writeUTF(text).writeShort(x).writeShort(y).writeShort(width).writeShort(height).writeInt(
            backgroundColor).writeInt(borderColor).writeByte(100 if backgroundAlpha > 100 else backgroundAlpha).writeBool(fixedPos)
        if targetPlayer == "":
            this.sendAll(Identifiers.send.Add_Text_Area, p.toByteArray())
        else:
            client = this.clients.get(targetPlayer)
            if client != None:
                client.sendPacket(
                    Identifiers.send.Add_Text_Area, p.toByteArray())

    def removeTextArea(this, id, targetPlayer):
        p = ByteArray().writeInt(id)
        if targetPlayer == "":
            this.sendAll(Identifiers.send.Remove_Text_Area, p.toByteArray())
        else:
            client = this.clients.get(targetPlayer)
            if client != None:
                client.sendPacket(
                    Identifiers.send.Remove_Text_Area, p.toByteArray())

    def updateTextArea(this, id, text, targetPlayer):
        p = ByteArray().writeInt(id).writeUTF(text)
        if targetPlayer == "":
            this.sendAll(Identifiers.send.Update_Text_Area, p.toByteArray())
        else:
            client = this.clients.get(targetPlayer)
            if client != None:
                client.sendPacket(
                    Identifiers.send.Update_Text_Area, p.toByteArray())

    def setMapName(this, name):
        this.sendAll(Identifiers.send.Set_Map_Name, ByteArray().writeUTF(name).toByteArray())

    def setShamanName(this, name):
        this.sendAll(Identifiers.send.Set_Shaman_Name, ByteArray().writeUTF(name).toByteArray())

    def showColorPicker(this, id, targetPlayer, defaultColor, title):
        p = ByteArray().writeInt(id).writeInt(defaultColor).writeUTF(title)
        if targetPlayer == "":
            this.sendAll(Identifiers.send.Show_Color_Picker, p.toByteArray())
        else:
            client = this.clients.get(targetPlayer)
            if client != None:
                client.sendPacket(
                    Identifiers.send.Show_Color_Picker, p.toByteArray())

    def startSnowSchedule(this, power):
        if this.isSnowing:
            this.startSnow(0, power, False)

    def startSnow(this, millis, power, enabled):
        this.isSnowing = enabled
        this.sendAll(Identifiers.send.Snow, ByteArray().writeBool(
            enabled).writeShort(power).toByteArray())
        if enabled:
            this.endSnowTimer = TFMUtils.callLater(
                millis, lambda: this.startSnowSchedule(power))

    def giveSurvivorStats(this):
        for client in this.clients.values():
            if not client.isNewPlayer:
                client.survivorStats[0] += 1
                if client.isShaman:
                    client.survivorStats[1] += 1
                    client.survivorStats[2] += this.getDeathCountNoShaman()
                elif not client.isDead:
                    client.survivorStats[3] += 1

                if client.survivorStats[0] >= 1000 and not str(120) in client.shopBadges:
                    client.shopModule.sendUnlockedBadge(str(120))
                    client.shopBadges.append(str(120))
                    client.shopModule.checkAndRebuildBadges()

                if client.survivorStats[1] >= 800 and not str(121) in client.shopBadges:
                    client.shopModule.sendUnlockedBadge(str(121))
                    client.shopBadges.append(str(121))
                    client.shopModule.checkAndRebuildBadges()

                if client.survivorStats[2] >= 20000 and not str(122) in client.shopBadges:
                    client.shopModule.sendUnlockedBadge(str(122))
                    client.shopBadges.append(str(122))
                    client.shopModule.checkAndRebuildBadges()

                if client.survivorStats[3] >= 10000 and not str(123) in client.shopBadges:
                    client.shopModule.sendUnlockedBadge(str(123))
                    client.shopBadges.append(str(123))
                    client.shopModule.checkAndRebuildBadges()

    def giveRacingStats(this):
        for client in this.clients.values():
            if not client.isNewPlayer:
                client.racingStats[0] += 1
                if client.hasCheese or client.hasEnter:
                    client.racingStats[1] += 1

                if client.hasEnter:
                    if client.currentPlace <= 3:
                        client.racingStats[2] += 1

                    if client.currentPlace == 1:
                        client.racingStats[3] += 1

                if client.racingStats[0] >= 1500 and not str(124) in client.shopBadges:
                    client.shopModule.sendUnlockedBadge(str(124))
                    client.shopBadges.append(str(124))
                    client.shopModule.checkAndRebuildBadges()

                if client.racingStats[1] >= 10000 and not str(125) in client.shopBadges:
                    client.shopModule.sendUnlockedBadge(str(125))
                    client.shopBadges.append(str(125))
                    client.shopModule.checkAndRebuildBadges()

                if client.racingStats[2] >= 10000 and not str(127) in client.shopBadges:
                    client.shopModule.sendUnlockedBadge(str(127))
                    client.shopBadges.append(str(127))
                    client.shopModule.checkAndRebuildBadges()

                if client.racingStats[3] >= 10000 and not str(126) in client.shopBadges:
                    client.shopModule.sendUnlockedBadge(str(126))
                    client.shopBadges.append(str(126))
                    client.shopModule.checkAndRebuildBadges()

    def send20SecRemainingTimer(this):
        if not this.changed20secTimer:
            if not this.never20secTimer and this.roundTime + (this.gameStartTime - TFMUtils.getTime()) > 21:
                this.changed20secTimer = True
                this.changeMapTimers(20)
                for client in this.clients.values():
                    client.sendRoundTime(20)

    def changeMapTimers(this, seconds):
        if this.changeMapTimer != None:
            this.changeMapTimer.cancel()
        this.changeMapTimer = TFMUtils.callLater(seconds, this.mapChange)

    def newConsumableTimer(this, code):
        this.roomTimers.append(TFMUtils.callLater(10, lambda: this.sendAll(
            Identifiers.send.Remove_Object, ByteArray().writeInt(code).writeBool(False).toByteArray())))

class Network(asyncore.dispatcher):

    def __init__(this, server, host: str, port: int):
        this.server = server
        asyncore.dispatcher.__init__(this)
        this.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        this.set_reuse_addr()
        this.bind((host, port))
        this.listen(100)

    def handle_accepted(this, client: socket, address: object):
        ipAddress = address[0]
        if this.server.getIPPermaBan(ipAddress) or ipAddress in this.server.tempIPBanList:
            return

        if ipAddress in this.server.connectedCounts.keys():
            this.server.connectedCounts[ipAddress] += 1
        else:
            this.server.connectedCounts[ipAddress] = 1

        if this.server.connectedCounts[ipAddress] >= 5 or int(address[1]) in [80, 443, 448, 8080]:
            this.server.tempIPBanList.append(ipAddress)
            #this.server.sendStaffMessage(10, "[<V>ANT-DDOS</V>] BLOCKED ATTACK! IP: [<R>"+str(ipAddress)+"</R>]")
            this.server.disconnectIPAddress(ipAddress)
            del this.server.connectedCounts[ipAddress]
            this.close()
            return
        else:
            c = Client(client)
            
            c.server = this.server
            c.TFMUtils = TFMUtils
            c.apiToken = c.TFMUtils.getRandomChars(50, True)
            #c.Langue = c.TFMUtils.getCountryCode(ipAddress)

            c.parsePackets = ParsePackets(c, this.server)
            c.parseCommands = ParseCommands(c, this.server)
            c.shopModule = ShopModule(c, this.server)
            c.ModoPwet = ModoPwet(c, this.server)
            c.skillModule = SkillModule(c, this.server)
            c.tribulle = Tribulle(c, this.server)
            c.config = config(c, this.server)
            c.ranking = ranking(c, this.server)
            c.email = email(c, this.server)
            c.radios = radios(c, this.server)
            c.AntiCheat = AntiCheat(c, this.server)
            c.Utility = Utility(c, this.server)
            c.DailyQuest = DailyQuest(c, this.server)
            c.PokeLua = PokeLua(c, this.server)
            c.Cryptography = Cryptography(this.server)
            c.downloadCenter = DownloadCenter(c, this.server)

            c.ipAddress = ipAddress

if __name__ == "__main__":
    print("[" + (str(time.strftime("%H:%M:%S"))) +
          "] Initializing game server...")
    startServer = int(round(time.time() * 1000))

    # Connection Settings
    print("[" + (str(time.strftime("%H:%M:%S"))) +
          "] Loading configuration...")
    start = int(round(time.time() * 1000))
    try:
        Config = configparser.ConfigParser()
        Config.read("./include/Config.properties")
        print("[" + (str(time.strftime("%H:%M:%S"))) +
              "] Configuration loaded in " + str(int(round(time.time() * 1000)) - start) + "ms.")
    except Exception as e:
        print("[" + (str(time.strftime("%H:%M:%S"))) +
              "] Error when load configuration.")
        print("ERROR: " + str(e))

    # Connection Database
    print("[" + (str(time.strftime("%H:%M:%S"))) +
          "] Loading database...")
    start = int(round(time.time() * 1000))
    Database, Cursor = None, None
    try:
        print("[" + (str(time.strftime("%H:%M:%S"))) +
              "] Connecting the database...")
        startC = int(round(time.time() * 1000))
        Database = sqlite3.connect(
            "./database/Transformice.db", check_same_thread=False)
        print("[" + (str(time.strftime("%H:%M:%S"))) +
              "] Database connected in " + str(int(round(time.time() * 1000)) - startC) + "ms.")
        Database.text_factory = str
        Database.isolation_level = None
        Database.row_factory = sqlite3.Row
        Cursor = Database.cursor()
        Cursor.execute("select * from Users")
        print("[" + (str(time.strftime("%H:%M:%S"))) +
              "] Database loaded in " + str(int(round(time.time() * 1000)) - start) + "ms.")
    except Exception as e:
        print("[" + (str(time.strftime("%H:%M:%S"))) +
              "] Error when load database.")
        print("ERROR: " + str(e))

    # Connection Server
    print("[" + (str(time.strftime("%H:%M:%S"))) +
          "] Loading server...")
    TFM = Server()
    os.system("title Transformice emulator v"+str(TFM.projectVersion))
    validPorts = []
    invalidPorts = []
    for port in [11801, 12801, 13801, 14801]:
        try:
            server = Network(TFM, '', port)
            validPorts.append(port)
        except Exception as e:
            print(e)
            invalidPorts.append(port)
    if len(validPorts) > 0:
        TFM.startServerTime = TFMUtils.getTime()
        print("[" + (str(time.strftime("%H:%M:%S"))) + "] Server loaded in " +
              str(int(round(time.time() * 1000)) - startServer) + "ms.")
        print("[" + (str(time.strftime("%H:%M:%S"))) +
              "] Server running on ports " + str(validPorts) + "\n")
    else:
        print("[" + (str(time.strftime("%H:%M:%S"))) + "] Error when load server.")
        print("[" + (str(time.strftime("%H:%M:%S"))) +
              "] Server error on ports " + str(invalidPorts) + "\n")

    asyncore.loop(timeout=30.0, use_poll=False, map=None, count=None)
