# coding: utf-8
import time as thetime
import random
import time
import json
import re
import base64
import xml.etree.ElementTree as xml
import xml.parsers.expat

from datetime import datetime
from urllib.request import Request
from urllib.request import urlopen
from threading import Timer


class TFMUtils:

    @staticmethod
    def callLater(time, target, *args):
        t = Timer(time, target, args)
        t.start()
        return t

    @staticmethod
    def getTFMLangues(langueID):
        return {-1: "XX", 0: "EN", 1: "FR", 2: "FR", 3: "BR", 4: "ES", 5: "CN", 6: "TR", 7: "VK", 8: "PL", 9: "HU", 10: "NL", 11: "RO", 12: "ID", 13: "DE", 14: "E2", 15: "AR", 16: "PH", 17: "LT", 18: "JP", 19: "CH", 20: "FI", 21: "CZ", 22: "SK", 23: "HR", 24: "BU", 25: "LV", 26: "HE", 27: "IT", 29: "ET", 30: "AZ", 31: "PT"}[langueID]

    @staticmethod
    def getCountryCode(ip):
        """try:
            data = json.load(urlopen("http://ipinfo.io/json"))
            if data["country"] != None:
                if data["country"] in ["PT", "BR"]:
                    return "BR"
                elif data["country"] in ["ES", "VE", "UY", "DO", "PE", "PA", "PY", "NI", "HN", "GT", "SV", "CU", "CR", "CO", "CL", "BO", "AR", "MX", "TR", "TM", "TC", "BG"]:
                    return "ES"
        except:
            pass"""
        return "EN"

    @staticmethod
    def getTime():
        return int(time.time())

    @staticmethod
    def getDate():
        return datetime.now().strftime("%e %m %d %H:%M:%S %Y")

    @staticmethod
    def checkValidXML(XML):
        if re.search("ENTITY", XML) and re.search("<html>", XML):
            return False
        else:
            try:
                parser = xml.parsers.expat.ParserCreate()
                parser.Parse(XML)
                return True
            except Exception as e:
                return False

    @staticmethod
    def getHoursDiff(endTimeMillis):
        startTime = TFMUtils.getTime()
        startTime = datetime.fromtimestamp(float(startTime))
        endTime = datetime.fromtimestamp(float(endTimeMillis))
        result = endTime - startTime
        seconds = (result.microseconds + (result.seconds +
                                          result.days * 24 * 3600) * 10 ** 6) / float(10 ** 6)
        hours = int(int(seconds) / 3600) + 1
        return hours

    @staticmethod
    def getDiffDays(time):
        return time - TFMUtils.getTime() / (24 * 60 * 60)

    @staticmethod
    def getSecondsDiff(endTimeMillis):
        return int(thetime.time() - endTimeMillis)

    @staticmethod
    def getRandomChars(size, numbers=False):
        return "".join((random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ" + ("123456789" if numbers else "")) for x in range(size)))

    @staticmethod
    def calculateTime(time):
        diff = int(time) - TFMUtils.getTime()
        diffSeconds = diff // 1000 % 60
        diffMinutes = diff // (60 * 1000) % 60
        diffHours = diff // (60 * 60 * 1000) % 24
        diffDays = diff // (24 * 60 * 60 * 1000)
        return diffDays <= 0 and diffHours <= 0 and diffMinutes <= 0 and diffSeconds <= 0

    @staticmethod
    def parsePlayerName(playerName):
        if "@" in playerName:
            return playerName
        else:
            return (playerName[0] + playerName[1:].lower().capitalize()) if playerName.startswith("*") or playerName.startswith("+") else playerName.lower().capitalize()

    @staticmethod
    def joinWithQuotes(list):
        return "\"" + "\", \"".join(list) + "\""

    @staticmethod
    def getValue(*array):
        return random.choice(array)

    @staticmethod
    def getYoutubeID(url):
        matcher = re.compile(
            ".*(?:youtu.be\\/|v\\/|u\\/\\w\\/|embed\\/|watch\\?v=)([^#\\&\\?]*).*").match(url)
        return matcher.group(1) if matcher else None

    @staticmethod
    def Duration(duration):
        time = re.compile('P''(?:(?P<years>\d+)Y)?''(?:(?P<months>\d+)M)?''(?:(?P<weeks>\d+)W)?''(?:(?P<days>\d+)D)?''(?:T''(?:(?P<hours>\d+)H)?''(?:(?P<minutes>\d+)M)?''(?:(?P<seconds>\d+)S)?'')?').match(duration).groupdict()
        for key in time.items():
            time[key[0]] = 0 if key[1] is None else time[key[0]]
        return (int(time["weeks"]) * 7 * 24 * 60 * 60) + (int(time["days"]) * 24 * 60 * 60) + (int(time["hours"]) * 60 * 60) + (int(time["minutes"]) * 60) + (int(time["seconds"]) - 1)

    @staticmethod
    def decryptXML(cryptedXML, key):
        c = int()
        finalXML = ""
        XML = base64.b64decode(cryptedXML)
        i = 0
        while i < len(XML):
            c = int(ord(XML[i]))
            c = (c - int(ord(key[(i + 1) % len(key)])))
            finalXML += chr(abs(c) & 0xFF)
            i += 1
        return finalXML

    @staticmethod
    def getMap(player, mapCode):
        mapID = 0
        if mapCode > 0:
            url = urlopen(Request("http://api.micetigri.fr/maps/xmlnew/{0}".format(mapCode), headers={
                          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.75 Safari/537.36'})).read()
            Code = int(str(url).split('CODE="')[1].split('"')[0])
            Perm = int(str(url).split('PERM="')[1].split('"')[0])
            Creator = str(str(url).split('CREATOR="')[1].split('"')[0])
            XML = TFMUtils.decryptXML(
                str(str(url).split('XML="')[1].split('"')[0]), "59A[XG^znsqsq8v{`Xhp3P9G")
            if not XML == "" and not Creator == "" and not Perm in [44, 22, 0]:
                try:
                    player.server.lastMapEditeurCode += 1
                    mapID = player.server.lastMapEditeurCode
                    player.Cursor.execute("insert into MapEditor values (?, ?, ?, 0, 0, ?, ?, '', '')", [
                                          mapID, Creator, XML, Perm, TFMUtils.getTime()])
                    player.server.updateConfig()
                except Exception as e:
                    return 0
        return mapID
