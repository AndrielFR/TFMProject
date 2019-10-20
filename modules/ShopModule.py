import binascii

from modules.ByteArray import ByteArray
from modules.Identifiers import Identifiers


class ShopModule:

    def __init__(this, player, server):
        this.client = player
        this.server = player.server
        this.Cursor = player.Cursor

    def getShopLength(this):
        return 0 if this.client.shopItems == "" else len(this.client.shopItems.split(","))

    def checkUnlockShopTitle(this):
        if this.getShopLength() in this.server.shopTitleList.keys():
            title = this.server.shopTitleList[this.getShopLength()]
            this.client.checkAndRebuildTitleList("shop")
            this.client.sendUnlockedTitle(
                int(title - (title % 1)), int(round((title % 1) * 10)))
            this.client.sendCompleteTitleList()
            this.client.sendTitleList()

    def checkAndRebuildBadges(this):
        rebuild = False
        for badge in this.server.shopBadges.items():
            if not badge[0] in this.client.shopBadges and this.checkInShop(badge[0]):
                this.client.shopBadges.append(str(badge[1]))
                rebuild = True

        if rebuild:
            tempBadges = []
            tempBadges.extend(this.client.shopBadges)
            this.client.shopBadges = []
            for badge in tempBadges:
                if not badge in this.client.shopBadges:
                    this.client.shopBadges.append(badge)

    def checkUnlockShopBadge(this, itemID):
        if not this.client.isGuest:
            if itemID in this.server.shopBadges.keys():
                unlockedBadge = this.server.shopBadges[itemID]
                this.sendUnlockedBadge(unlockedBadge)
                this.checkAndRebuildBadges()

    def checkInShop(this, checkItem):
        if this.client.shopItems == "":
            return False
        else:
            splitedItems = this.client.shopItems.split(",")
            for shopItem in splitedItems:
                item = shopItem.split("_")[0] if "_" in shopItem else shopItem
                if checkItem == int(item):
                    return True
        return False

    def checkInShamanShop(this, checkItem):
        if this.client.shamanItems == "":
            return False
        else:
            splitedItems = this.client.shamanItems.split(",")
            for shopItem in splitedItems:
                item = shopItem.split("_")[0] if "_" in shopItem else shopItem
                if checkItem == int(item):
                    return True
        return False

    def checkInPlayerShop(this, type, playerName, checkItem):
        this.Cursor.execute("select " + type +
                            " from Users where Username = ?", [playerName])
        r = this.Cursor.fetchall()
        for rs in r:
            items = rs[type]
            if items == "":
                return False
            else:
                for shopItem in items.split(","):
                    if checkItem == int(shopItem.split("_")[0] if "_" in shopItem else shopItem):
                        return True
        return False

    def getItemCustomization(this, checkItem, isShamanShop):
        items = this.client.shamanItems if isShamanShop else this.client.shopItems
        if items == "":
            return ""
        else:
            splitedItems = items.split(",")
            for shopItem in splitedItems:
                itemSplited = shopItem.split("_")
                custom = itemSplited[1] if len(itemSplited) >= 2 else ""
                if int(itemSplited[0]) == checkItem:
                    return "" if custom == "" else ("_" + custom)
        return ""

    def getShamanItemCustom(this, code):
        item = this.client.shamanItems.split(",")
        if "_" in item:
            itemSplited = item.split("_")
            custom = (itemSplited[1] if len(
                itemSplited) >= 2 else "").split("+")
            if int(itemSplited[0]) == code:
                p = ByteArray().writeByte(len(custom))
                x = 0
                while x < len(custom):
                    p.writeInt(int(custom[x], 16))
                    x += 1
                return p.toByteArray()
        return chr(0)

    def getShopItemPrice(this, fullItem):
        itemCat = (0 if fullItem // 10000 == 1 else fullItem //
                   10000) if fullItem > 9999 else fullItem // 100
        item = fullItem % 1000 if fullItem > 9999 else fullItem % 100 if fullItem > 999 else fullItem % (
            100 * itemCat) if fullItem > 99 else fullItem
        return this.getItemPromotion(itemCat, item, this.server.shopListCheck[str(itemCat) + "|" + str(item)][1])

    def getShamanShopItemPrice(this, fullItem):
        return this.server.shamanShopListCheck[str(fullItem)][1]

    def getItemPromotion(this, itemCat, item, price):
        for promotion in this.server.shopPromotions:
            if promotion[2] == itemCat and promotion[3] == item:
                return int(price * (100 - promotion[5]) // 100.0)
        return price

    def sendShopInfo(this):
        this.client.sendPacket(Identifiers.send.Shop_Info, ByteArray().writeInt(
            this.client.shopCheeses).writeInt(this.client.shopFraises).toByteArray())

    def sendShopList(this, sendItems=True):
        shopItems = [] if this.client.shopItems == "" else this.client.shopItems.split(
            ",")

        packet = ByteArray().writeInt(this.client.shopCheeses).writeInt(
            this.client.shopFraises).writeUTF(this.client.playerLook).writeInt(len(shopItems))
        for item in shopItems:
            if "_" in item:
                itemSplited = item.split("_")
                realItem = itemSplited[0]
                custom = itemSplited[1] if len(itemSplited) >= 2 else ""
                realCustom = [] if custom == "" else custom.split("+")

                packet.writeByte(len(realCustom) + 1).writeInt(int(realItem))

                x = 0
                while x < len(realCustom):
                    packet.writeInt(int(realCustom[x], 16))
                    x += 1
            else:
                packet.writeByte(0).writeInt(int(item))

        shop = this.server.shopList if sendItems else []
        packet.writeInt(len(shop))

        for item in shop:
            value = item.split(",")
            packet.writeShort(int(value[0])).writeShort(int(value[1])).writeByte(int(value[2])).writeByte(
                int(value[3])).writeByte(int(value[4])).writeInt(int(value[5])).writeInt(int(value[6])).writeShort(0)

        visuais = this.server.newVisuList
        packet.writeByte(len(visuais))
        i = len(visuais)
        for visual in visuais.items():
            packet.writeShort(visual[0])
            a = visual[1]
            packet.writeUTF(''.join(a))
            packet.writeByte(0 if visual[0] in [46, 47, 54, 55, 204, 216, 243, 244] else 1 if visual[0] in [
                             18, 19, 53, 205, 217] else 2 if visual[0] in [52] else 3 if visual[0] in [203] else 4 if visual[0] in [20, 21, 56] else 2)
            i -= 1

        packet.writeShort(len(list(this.client.clothes)))

        for clothe in this.client.clothes:
            clotheSplited = clothe.split("/")
            packet.writeUTF(
                clotheSplited[1] + ";" + clotheSplited[2] + ";" + clotheSplited[3])

        shamanItems = [
        ] if this.client.shamanItems == "" else this.client.shamanItems.split(",")
        packet.writeShort(len(shamanItems))

        for item in shamanItems:
            if "_" in item:
                itemSplited = item.split("_")
                realItem = itemSplited[0]
                custom = itemSplited[1] if len(itemSplited) >= 2 else ""
                realCustom = [] if custom == "" else custom.split("+")

                packet.writeShort(int(realItem))

                packet.writeBool(item in this.client.shamanLook.split(
                    ",")).writeByte(len(realCustom) + 1)

                x = 0
                while x < len(realCustom):
                    packet.writeInt(int(realCustom[x], 16))
                    x += 1
            else:
                packet.writeShort(int(item)).writeBool(
                    item in this.client.shamanLook.split(",")).writeByte(0)

        shamanShop = this.server.shamanShopList if sendItems else []
        packet.writeShort(len(shamanShop))

        for item in shamanShop:
            value = item.split(",")
            packet.writeInt(int(value[0])).writeByte(int(value[1])).writeByte(int(value[
                2])).writeByte(int(value[3])).writeInt(int(value[4])).writeShort(int(value[5]))

        this.client.sendPacket(
            Identifiers.send.Shop_List, packet.toByteArray())

    def sendShamanItems(this):
        p = ByteArray()

        shamanItems = [
        ] if this.client.shamanItems == "" else this.client.shamanItems.split(",")
        p.writeShort(len(shamanItems))

        for item in shamanItems:
            if "_" in item:
                itemSplited = item.split("_")
                realItem = itemSplited[0]
                custom = itemSplited[1] if len(itemSplited) >= 2 else ""
                realCustom = [] if custom == "" else custom.split("+")
                p.writeShort(int(realItem)).writeBool(
                    item in this.client.shamanLook.split(",")).writeByte(len(realCustom) + 1)
                x = 0
                while x < len(realCustom):
                    p.writeInt(int(realCustom[x], 16))
                    x += 1
            else:
                p.writeShort(int(item)).writeBool(
                    item in this.client.shamanLook.split(",")).writeByte(0)

        this.client.sendPacket(Identifiers.send.Shaman_Items, p.toByteArray())

    def sendLookChange(this):
        try:
            p = ByteArray()
            look = this.client.playerLook.split(";")
            p.writeShort(int(look[0]))

            for item in look[1].split(","):
                if "_" in item:
                    itemSplited = item.split("_")
                    realItem = itemSplited[0]
                    custom = itemSplited[1] if len(itemSplited) >= 2 else ""
                    realCustom = [] if custom == "" else custom.split("+")
                    p.writeInt(int(realItem)).writeByte(len(realCustom))
                    x = 0
                    while x < len(realCustom):
                        p.writeInt(int(realCustom[x], 16))
                        x += 1
                else:
                    p.writeInt(int(item)).writeByte(0)

            p.writeInt(int(this.client.MouseColor, 16))
            this.client.sendPacket(
                Identifiers.send.Look_Change, p.toByteArray())
        except:
            pass

    def sendShamanLook(this):
        p = ByteArray()
        items = ByteArray()
        shamanLook = this.client.shamanLook.split(",")
        count = 0

        for item in shamanLook:
            realItem = int(item.split("_")[0]) if "_" in item else int(item)
            if realItem != 0:
                items.writeShort(realItem)
                count += 1

        this.client.sendPacket(Identifiers.send.Shaman_Look, p.writeShort(
            count).writeBytes(items.toByteArray()).toByteArray())

    def sendItemBuy(this, fullItem):
        this.client.sendPacket(Identifiers.send.Item_Buy, ByteArray(
        ).writeInt(fullItem).writeByte(int(0)).toByteArray())

    def sendUnlockedBadge(this, badge):
        this.client.room.sendAll(Identifiers.send.Unlocked_Badge, ByteArray().writeInt(
            this.client.playerCode).writeShort(badge).toByteArray())

    def sendGiftResult(this, type, playerName):
        this.client.sendPacket(Identifiers.send.Gift_Result, ByteArray().writeByte(
            type).writeByte(0).writeUTF(playerName).writeByte(0).writeShort(0).toByteArray())

    def buyItem(this, packet):
        fullItem, withFraises = packet.readInt(), packet.readBool()
        fullItem = 230100 + (32044 + fullItem) if fullItem < 0 else fullItem
        itemCat = (0 if fullItem // 10000 == 1 else fullItem //
                   10000 - 1) if fullItem > 9999 else fullItem // 100
        item = fullItem % 1000 if fullItem > 9999 else fullItem % 100 if fullItem > 999 else fullItem % (
            100 * itemCat) if fullItem > 99 else fullItem
        price = this.getItemPromotion(itemCat, item, this.server.shopListCheck[
                                      str(itemCat) + "|" + str(item)][1 if withFraises else 0])
        this.client.shopItems += str(
            fullItem) if this.client.shopItems == "" else "," + str(fullItem)
        if withFraises:
            this.client.shopFraises -= price
        else:
            this.client.shopCheeses -= price

        #print("[NORMAL] Cat: "+str(itemCat)+", ID: "+str(item)+", Price: "+str(price)+", Type Price: "+str("cheese" if not withFraises else "fraise"))

        # Buy one item mission
        if 6 in this.client.dailyQuest:
            this.client.DailyQuest.upMission(6, this.client.playerID)

        this.sendItemBuy(fullItem)
        this.sendShopList(False)
        this.client.sendAnimZelda(0, fullItem)
        this.checkUnlockShopTitle()
        this.checkUnlockShopBadge(fullItem)

    def equipItem(this, packet):
        fullItem = packet.readInt()
        fullItem = 230100 + (32044 + fullItem) if fullItem < 0 else fullItem
        itemCat = (0 if fullItem // 10000 == 1 else fullItem //
                   10000 - 1) if fullItem > 9999 else fullItem // 100
        item = fullItem % 1000 if fullItem > 9999 else fullItem % 100 if fullItem > 999 else fullItem % (
            100 * itemCat) if fullItem > 99 else fullItem
        lookList = this.client.playerLook.split(";")
        lookItems = lookList[1].split(",")
        lookCheckList = lookItems[:]
        i = 0
        while i < len(lookCheckList):
            lookCheckList[i] = lookCheckList[i].split("_")[0] if "_" in lookCheckList[
                i] else lookCheckList[i]
            i += 1

        if itemCat <= 10:
            lookItems[itemCat] = "0" if lookCheckList[itemCat] == str(
                item) else str(item) + this.getItemCustomization(fullItem, False)
        elif itemCat == 21:
            lookList[0] = "1"
            color = "bd9067" if item == 0 else "593618" if item == 1 else "8c887f" if item == 2 else "dfd8ce" if item == 3 else "4e443a" if item == 4 else "e3c07e" if item == 5 else "272220" if item == 6 else "78583a"
            this.client.MouseColor = "78583a" if this.client.MouseColor == color else color
        else:
            lookList[0] = "1" if lookList[0] == str(item) else str(item)
            this.client.MouseColor = "78583a"

        this.client.playerLook = lookList[
            0] + ";" + ",".join(map(str, lookItems))
        this.sendLookChange()

    def customItemBuy(this, packet):
        fullItem, withFraises = packet.readInt(), packet.readBool()

        items = this.client.shopItems.split(",")
        for shopItem in items:
            item = shopItem.split("_")[0] if "_" in shopItem else shopItem
            if fullItem == int(item):
                items[items.index(shopItem)] = shopItem + "_"
                break

        this.client.shopItems = ",".join(items)
        if withFraises:
            this.client.shopFraises -= 20
        else:
            this.client.shopCheeses -= 2000

        this.sendShopList(False)

    def customItem(this, packet):
        fullItem, length = packet.readInt(), packet.readByte()
        custom = length
        customs = []

        i = 0
        while i < length:
            customs.append(packet.readInt())
            i += 1

        items = this.client.shopItems.split(",")
        for shopItem in items:
            sItem = shopItem.split("_")[0] if "_" in shopItem else shopItem
            if fullItem == int(sItem):
                newCustoms = map(lambda color: "%06X" %
                                 (0xffffff & color), customs)

                items[items.index(shopItem)] = sItem + \
                    "_" + "+".join(newCustoms)
                this.client.shopItems = ",".join(items)

                itemCat = (0 if fullItem // 10000 == 1 else fullItem //
                           10000) if fullItem > 9999 else fullItem // 100
                item = fullItem % 1000 if fullItem > 9999 else fullItem % 100 if fullItem > 999 else fullItem % (
                    100 * itemCat) if fullItem > 99 else fullItem
                equip = str(item) + this.getItemCustomization(fullItem, False)
                lookList = this.client.playerLook.split(";")
                lookItems = lookList[1].split(",")

                if "_" in lookItems[itemCat]:
                    if lookItems[itemCat].split("_")[0] == str(fullItem):
                        lookItems[itemCat] = equip

                elif lookItems[itemCat] == str(fullItem):
                    lookItems[itemCat] = equip

                this.client.playerLook = lookList[
                    0] + ";" + ",".join(lookItems)
                this.sendShopList(False)
                this.sendLookChange()
                break

    def buyShamanItem(this, packet):
        fullItem, withFraises = packet.readShort(), packet.readBool()
        price = this.server.shamanShopListCheck[
            str(fullItem)][1 if withFraises else 0]
        this.client.shamanItems += str(
            fullItem) if this.client.shamanItems == "" else "," + str(fullItem)

        if withFraises:
            this.client.shopFraises -= price
        else:
            this.client.shopCheeses -= price

        #print("[SHAMAN] ID: "+str(fullItem)+", Price: "+str(price)+", Type Price: "+str("cheese" if not withFraises else "fraise"))

        this.sendShopList(False)
        this.client.sendAnimZelda(1, fullItem)

    def equipShamanItem(this, packet):
        fullItem = packet.readInt()
        item = str(fullItem) + this.getItemCustomization(fullItem, True)
        itemStr = str(fullItem)
        itemCat = int(itemStr[:len(itemStr) - 2])
        index = itemCat if itemCat <= 4 else itemCat - \
            1 if itemCat <= 7 else 7 if itemCat == 10 else 8 if itemCat == 17 else 9
        index -= 1
        lookItems = this.client.shamanLook.split(",")

        if "_" in lookItems[index]:
            if lookItems[index].split("_")[0] == itemStr:
                lookItems[index] = "0"
            else:
                lookItems[index] = item

        elif lookItems[index] == itemStr:
            lookItems[index] = "0"
        else:
            lookItems[index] = item

        this.client.shamanLook = ",".join(lookItems)
        this.sendShamanLook()

    def customShamanItemBuy(this, packet):
        fullItem, withFraises = packet.readShort(), packet.readBool()

        items = this.client.shamanItems.split(",")
        for shopItem in items:
            item = shopItem.split("_")[0] if "_" in shopItem else shopItem
            if fullItem == int(item):
                items[items.index(shopItem)] = shopItem + "_"
                break

        this.client.shamanItems = ",".join(items)
        if withFraises:
            this.client.shopFraises -= 150
        else:
            this.client.shopCheeses -= 4000

        this.sendShopList(False)

    def customShamanItem(this, packet):
        fullItem, length = packet.readShort(), packet.readByte()
        customs = []
        i = 0
        while i < length:
            customs.append(packet.readInt())
            i += 1

        items = this.client.shamanItems.split(",")
        for shopItem in items:
            sItem = shopItem.split("_")[0] if "_" in shopItem else shopItem
            if fullItem == int(sItem):
                newCustoms = map(lambda color: "%06X" %
                                 (0xFFFFFF & color), customs)

                items[items.index(shopItem)] = sItem + \
                    "_" + "+".join(newCustoms)
                this.client.shamanItems = ",".join(items)

                item = str(fullItem) + \
                    this.getItemCustomization(fullItem, True)
                itemStr = str(fullItem)
                itemCat = int(itemStr[len(itemStr) - 2:])
                index = itemCat if itemCat <= 4 else itemCat - \
                    1 if itemCat <= 7 else 7 if itemCat == 10 else 8 if itemCat == 17 else 9
                index -= 1
                lookItems = this.client.shamanLook.split(",")

                if "_" in lookItems[index]:
                    if lookItems[index].split("_")[0] == itemStr:
                        lookItems[index] = item

                elif lookItems[index] == itemStr:
                    lookItems[index] = item

                this.client.shamanLook = ",".join(lookItems)
                this.sendShopList(False)
                this.sendShamanLook()
                break

    def buyClothe(this, packet):
        clotheID, withFraises = packet.readByte(), packet.readBool()
        this.client.clothes.append("%02d/%s/%s/%s" % (clotheID, "1;0,0,0,0,0,0,0,0,0",
                                                      "78583a", "fade55" if this.client.shamanSaves >= 1000 else "95d9d6"))
        if withFraises:
            this.client.shopFraises -= 5 if clotheID == 0 else 50 if clotheID == 1 else 100
        else:
            this.client.shopFraises -= 40 if clotheID == 0 else 1000 if clotheID == 1 else 2000 if clotheID == 2 else 4000

        this.sendShopList(False)

    def equipClothe(this, packet):
        clotheID = packet.readByte()
        for clothe in this.client.clothes:
            values = clothe.split("/")
            if values[0] == "%02d" % (clotheID):
                this.client.playerLook = values[1]
                this.client.MouseColor = values[2]
                this.client.ShamanColor = values[3]
                break

        this.sendLookChange()
        this.sendShopList(False)

    def saveClothe(this, packet):
        clotheID = packet.readByte()
        for clothe in this.client.clothes:
            values = clothe.split("/")
            if values[0] == "%02d" % (clotheID):
                values[1] = this.client.playerLook
                values[2] = this.client.MouseColor
                values[3] = this.client.ShamanColor
                this.client.clothes[this.client.clothes.index(
                    clothe)] = "/".join(values)
                break

        this.sendShopList(False)

    def sendGift(this, packet):
        playerName, isShamanItem, fullItem, message = packet.readUTF(
        ), packet.readBool(), packet.readInt(), packet.readUTF()
        if not this.server.checkExistingUser(playerName):
            this.sendGiftResult(1, playerName)
        else:
            player = this.server.players.get(playerName)
            if player != None:
                if (player.shopModule.checkInShamanShop(fullItem) if isShamanItem else player.shopModule.checkInShop(fullItem)):
                    this.sendGiftResult(2, playerName)
                else:
                    this.server.lastGiftID += 1
                    player.sendPacket(Identifiers.send.Shop_Gift, ByteArray().writeInt(this.server.lastGiftID).writeUTF(this.client.Username).writeUTF(
                        this.client.playerLook).writeBool(isShamanItem).writeInt(fullItem).writeUTF(message).writeBool(False).toByteArray())
                    this.sendGiftResult(0, playerName)
                    this.server.shopGifts[this.server.lastGiftID] = [
                        this.client.Username, isShamanItem, fullItem]
                    this.client.shopFraises -= this.getShamanShopItemPrice(
                        fullItem) if isShamanItem else this.getShopItemPrice(fullItem)
                    this.sendShopList(False)
            else:
                gifts = ""
                if (this.checkInPlayerShop("ShamanItems" if isShamanItem else "ShopItems", playerName, fullItem)):
                    this.sendGiftResult(2, playerName)
                else:
                    this.Cursor.execute(
                        "select Gifts from Users where Username = ?", [playerName])
                    rs = this.Cursor.fetchone()
                    gifts = rs["Gifts"]

                gifts += ("" if gifts == "" else "/") + binascii.hexlify("|".join(map(str, [
                    this.client.Username, this.client.playerLook, isShamanItem, fullItem, message])))
                this.Cursor.execute("update Users set Gifts = ? where Username = ?", [
                                    gifts, playerName])

                this.sendGiftResult(0, playerName)

    def giftResult(this, packet):
        giftID, isOpen, message, isMessage = packet.readInt(
        ), packet.readBool(), packet.readUTF(), packet.readBool()
        if isOpen:
            values = this.server.shopGifts[int(giftID)]
            player = this.server.players.get(str(values[0]))
            if player != None:
                player.sendLangueMessage(
                    "", "$DonItemRecu", this.client.Username)

            isShamanItem = bool(values[1])
            fullItem = int(values[2])
            if isShamanItem:
                this.client.shamanItems += str(
                    fullItem) if this.client.shamanItems == "" else "," + str(fullItem)
                this.sendShopList(False)
                this.client.sendAnimZelda(1, fullItem)
            else:
                this.client.shopItems += str(
                    fullItem) if this.client.shopItems == "" else "," + str(fullItem)
                this.client.sendAnimZelda(0, fullItem)
                this.checkUnlockShopTitle()
                this.checkUnlockShopBadge(fullItem)

        elif not message == "":
            values = this.server.shopGifts[int(giftID)]
            player = this.server.players.get(str(values[0]))
            if player != None:
                player.sendPacket(Identifiers.send.Shop_Gift, ByteArray().writeInt(giftID).writeUTF(this.client.Username).writeUTF(
                    this.client.playerLook).writeBool(bool(values[1])).writeInt(int(values[2])).writeUTF(message).writeBool(True).toByteArray())
            else:
                messages = ""
                this.Cursor.execute(
                    "select Messages from Users where Username = ?", [str(values[0])])
                rs = this.Cursor.fetchone()
                messages = rs["Messages"]

                messages += ("" if messages == "" else "/") + binascii.hexlify("|".join(map(
                    str, [this.client.Username, this.client.playerLook, values[1], values[2], message])))
                this.Cursor.execute("update Users set Messages = ? where Username = ?", [
                                    messages, str(values[0])])

    def checkGiftsAndMessages(this, lastReceivedGifts, lastReceivedMessages):
        needUpdate = False
        gifts = lastReceivedGifts.split("/")
        for gift in gifts:
            if not gift == "":
                values = binascii.unhexlify(gift).split("|", 4)
                this.server.lastGiftID += 1
                this.client.sendPacket(Identifiers.send.Shop_Gift, ByteArray().writeInt(this.server.lastGiftID).writeUTF(values[0]).writeUTF(values[
                                       1]).writeBool(bool(values[2])).writeShort(int(values[3])).writeUTF(values[4] if len(values) > 4 else "").writeBool(False).toByteArray())
                this.server.shopGifts[this.server.lastGiftID] = [
                    values[0], bool(values[2]), int(values[3])]
                needUpdate = True

        messages = lastReceivedMessages.split("/")
        for message in messages:
            if not message == "":
                values = binascii.unhexlify(message).split("|", 4)
                this.client.sendPacket(Identifiers.send.Shop_GIft_Message, ByteArray().writeShort(0).writeShort(0).writeUTF(values[0]).writeBool(
                    bool(values[1])).writeShort(int(values[2])).writeUTF(values[4]).writeUTF(values[3]).writeBool(True).toByteArray())
                needUpdate = True

        if needUpdate:
            this.Cursor.execute("update Users set Gifts = '', Messages = '' where Username = ?", [
                                this.client.Username])
