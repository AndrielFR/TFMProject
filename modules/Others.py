# coding: utf-8
import time
import random
import urllib
import smtplib
import json
import time as _time

# Modules
from modules.ByteArray import ByteArray

# Utils
from utils.TFMUtils import TFMUtils


class config:

    def __init__(this, client, server):
        this.client = client
        this.server = client.server
        currentPage = 1

    def close(this):
        i = 10000
        while i <= 12000:
            this.client.room.removeTextArea(i, this.client.Username)
            i += 1

    def close2(this):
        i = 10000
        while i <= 12000:
            this.client.room.removeTextArea(i, this.client.Username)
            i += 1

    def closeoption(this):
        this.client.room.removeTextArea(10004, this.client.Username)
        this.client.room.removeTextArea(10005, this.client.Username)

    def open(this):
        this.close2()
        text = "<p align=\'center\'><font size=\'20\' color=\'#990000\'>Configurações do seu jogo</font></p>"
        text += "\n<font size=\'18\'>-</font> <font size=\'13\'><a href=\'event:config:personalizacao\'>Personalização</a></font>"
        this.client.room.addTextArea(10002, str(
            text), this.client.Username, 64, 46, 680, 320, 0x000000, 0x313131, 95, False)
        this.client.room.addTextArea(10003, "<font size=\'28\' color=\'#990000\'><a href=\'event:config:close\'>X</a></font>",
                                     this.client.Username, 754, 40, 50, 50, 0, 0, 0, False)

    def options(this, id=0, option1="", option2="", option3="", option4="", option5=""):
        id = "Cor do nome <J>(VIP)</J>" if id == 1 else "Música" if id == 2 else ""
        opt = "Escolha uma das opções abaixo: " + str(id) + "\n"
        opt += "\n<font size=\'18\'>-</font> <font size=\'13\'>" + \
            str(option1) + "</font>" if option1 != "" else ""
        opt += "\n<font size=\'18\'>-</font> <font size=\'13\'>" + \
            str(option2) + "</font>" if option2 != "" else ""
        opt += "\n<font size=\'18\'>-</font> <font size=\'13\'>" + \
            str(option3) + "</font>" if option3 != "" else ""
        opt += "\n<font size=\'18\'>-</font> <font size=\'13\'>" + \
            str(option4) + "</font>" if option4 != "" else ""
        opt += "\n<font size=\'18\'>-</font> <font size=\'13\'>" + \
            str(option5) + "</font>" if option5 != "" else ""
        this.client.room.addTextArea(10004, str(
            opt), this.client.Username, 280, 150, 260, 140, 0x000000, 0xFFFFFF, 95, False)
        this.client.room.addTextArea(10005, "<font size=\'28\' color=\'#990000\'><a href=\'event:config:closeoption\'>X</a></font>",
                                     this.client.Username, 548, 146, 50, 50, 0, 0, 0, False)

    def personalizationopen(this):
        text = "<p align=\'center\'><font size=\'20\' color=\'#990000\'>Personalize seu jogo</font></p>"
        text += "\n<font size=\'18\'>-</font> <font size=\'13\'><a href=\'event:config:colormouse\'>Cor do rato</a></font>"
        text += "\n<font size=\'18\'>-</font> <font size=\'13\'><a href=\'event:config:colornick\'>Cor do nome <J>(VIP)</J></a></font>"
        this.client.room.addTextArea(10006, str(
            text), this.client.Username, 420, 94, 300, 240, 0x000000, 0x313131, 95, False)

    def musicName(this, enable=1):
        music = ""
        if enable == 0:
            this.client.room.removeTextArea(15000, this.client.Username)
            this.client.musicName = 0
        else:
            if this.client.musicOn == 1:
                if this.client.musicNameLink != "" and this.client.musicName == 1:
                    try:
                        this.client.room.removeTextArea(
                            15000, this.client.Username)
                        if ".json" in this.client.musicNameLink:
                            music = json.loads(urllib.request.urlopen(this.client.musicNameLink).read())[
                                "playing"]["current"].replace("=", "-")
                        else:
                            music = urllib.request.urlopen(
                                this.client.musicNameLink).read().decode("utf-8")
                        this.client.room.addTextArea(15000, "<font face=\'Arial\'>" + str(
                            music).replace("WWW.MUNDODOFUNK.COM", "") + "</font>", this.client.Username, 6, 379, 274, 18, 0x000000, 0x313131, 68, False)
                        TFMUtils.callLater(30, this.musicName)
                    except Exception as e:
                        print(e)
                        this.client.sendLangueMessage(
                            "", "<R>Conexão fraca ou erro no sistema...")
                else:
                    this.client.room.removeTextArea(
                        15000, this.client.Username)
                    this.client.musicNameLink = ""
                    this.client.musicName = 0
                    this.musicName(0)
            else:
                pass
                #this.client.sendMessage("<R>Ligue a rádio para usar essa função.")


class ranking:

    def __init__(this, client, server):
        this.client = client
        this.server = client.server
        currentPage = 1

    def close(this):
        i = 10000
        while i <= 12000:
            this.client.room.removeTextArea(i, this.client.Username)
            i += 1

    def close2(this):
        i = 10000
        while i <= 12000:
            this.client.room.removeTextArea(i, this.client.Username)
            i += 1

    def open(this):
        this.close()
        this.client.room.addTextArea(
            10002, "", this.client.Username, 5, 20, 790, 390, 0, 1, 85, False)
        this.client.room.addTextArea(10003, "<p align=\'center\'><font size=\'22\' family=\'Arial\' color=\'#BEBB56\'><a><b>Ranking " + str(
            this.server.miceName) + "</b></a></font></p>", this.client.Username, 235, 27, 340, 45, 0, 0, 100, False)
        this.client.room.addTextArea(10016, "<font size=\'23\' color=\'#990000\'><a href=\'event:ranking:close\'>X</a></font>",
                                     this.client.Username, 762, 34, 50, 50, 0, 0, 0, False)

        # Firsts
        this.client.room.addTextArea(10004, "<p align=\'center\'><font size=\'11\'><BV><b>Firsts</b></BV></font></p>",
                                     this.client.Username, -82, 81, 340, 45, 0, 0, 100, False)
        this.client.Cursor.execute(
            "select Username, FirstCount from Users where PrivLevel < 3 ORDER By FirstCount DESC LIMIT 22")
        rs = this.client.Cursor.fetchall()
        pos = 1
        text = ""
        count = ""
        for rrf in rs:
            posfirsts = "0" + str(pos) if pos <= 9 else pos
            playerName = str(rrf[0])
            firstCount = rrf[1]
            if pos == 1:
                text += "<font size=\'11\' color=\'#FADE55\'>" + \
                    str(posfirsts) + "</font> <V>-</V> " + \
                    str(playerName) + "</font>"
                text += "<br />"
            elif pos == 2:
                text += "<font size=\'11\' color=\'#EFEBE0\'>" + \
                    str(posfirsts) + "</font> <V>-</V> " + \
                    str(playerName) + "</font>"
                text += "<br />"
            elif pos == 3:
                text += "<font size=\'11\' color=\'#B44F0D\'>" + \
                    str(posfirsts) + "</font> <V>-</V> " + \
                    str(playerName) + "</font>"
                text += "<br />"
            else:
                text += "<font size=\'11\'><CH>" + \
                    str(posfirsts) + "</CH> <V>-</V> " + \
                    str(playerName) + "</font>"
                text += "<br />"
            count += "<V>" + str(firstCount) + "</V>\n"
            this.client.room.addTextArea(10005, str(
                text), this.client.Username, 8, 107, 340, 420, 0, 0, 100, False)
            this.client.room.addTextArea(10006, str(
                count), this.client.Username, 158, 107, 340, 420, 0, 0, 100, False)
            pos += 1

        # Queijos
        this.client.room.addTextArea(10007, "<p align=\'center\'><font size=\'11\'><BV><b>Cheeses</b></BV></font></p>",
                                     this.client.Username, 117, 81, 340, 45, 0, 0, 100, False)
        this.client.Cursor.execute(
            "select Username, CheeseCount from Users where PrivLevel < 3 ORDER By CheeseCount DESC LIMIT 22")
        rs = this.client.Cursor.fetchall()
        pos = 1
        text = ""
        count = ""
        for rrf in rs:
            poscheeses = "0" + str(pos) if pos <= 9 else pos
            playerName = str(rrf[0])
            cheeseCount = rrf[1]
            if pos == 1:
                text += "<font size=\'11\' color=\'#FADE55\'>" + \
                    str(poscheeses) + "</font> <V>-</V> " + \
                    str(playerName) + "</font>"
                text += "<br />"
            elif pos == 2:
                text += "<font size=\'11\' color=\'#EFEBE0\'>" + \
                    str(poscheeses) + "</font> <V>-</V> " + \
                    str(playerName) + "</font>"
                text += "<br />"
            elif pos == 3:
                text += "<font size=\'11\' color=\'#B44F0D\'>" + \
                    str(poscheeses) + "</font> <V>-</V> " + \
                    str(playerName) + "</font>"
                text += "<br />"
            else:
                text += "<font size=\'11\'><CH>" + \
                    str(poscheeses) + "</CH> <V>-</V> " + \
                    str(playerName) + "</font>"
                text += "<br />"
            count += "<V>" + str(cheeseCount) + "</V>\n"
            this.client.room.addTextArea(10008, str(
                text), this.client.Username, 203, 107, 340, 420, 0, 0, 100, False)
            this.client.room.addTextArea(10009, str(
                count), this.client.Username, 353, 107, 340, 420, 0, 0, 100, False)
            pos += 1

        # Saves
        this.client.room.addTextArea(10010, "<p align=\'center\'><font size=\'11\'><BV><b>Saves</b></BV></font></p>",
                                     this.client.Username, 333, 81, 340, 45, 0, 0, 100, False)
        this.client.Cursor.execute(
            "select Username, ShamanSaves from Users where PrivLevel < 3 ORDER By ShamanSaves DESC LIMIT 22")
        rs = this.client.Cursor.fetchall()
        pos = 1
        text = ""
        count = ""
        for rrf in rs:
            possaves = "0" + str(pos) if pos <= 9 else pos
            playerName = str(rrf[0])
            savesCount = rrf[1]
            if pos == 1:
                text += "<font size=\'11\' color=\'#FADE55\'>" + \
                    str(possaves) + "</font> <V>-</V> " + \
                    str(playerName) + "</font>"
                text += "<br />"
            elif pos == 2:
                text += "<font size=\'11\' color=\'#EFEBE0\'>" + \
                    str(possaves) + "</font> <V>-</V> " + \
                    str(playerName) + "</font>"
                text += "<br />"
            elif pos == 3:
                text += "<font size=\'11\' color=\'#B44F0D\'>" + \
                    str(possaves) + "</font> <V>-</V> " + \
                    str(playerName) + "</font>"
                text += "<br />"
            else:
                text += "<font size=\'11\'><CH>" + \
                    str(possaves) + "</CH> <V>-</V> " + \
                    str(playerName) + "</font>"
                text += "<br />"
            count += "<V>" + str(savesCount) + "</V>\n"
            this.client.room.addTextArea(10011, str(
                text), this.client.Username, 427, 107, 340, 420, 0, 0, 100, False)
            this.client.room.addTextArea(10012, str(
                count), this.client.Username, 575, 107, 340, 420, 0, 0, 100, False)
            pos += 1

        # Bootcamps
        this.client.room.addTextArea(10013, "<p align=\'center\'><font size=\'11\'><BV><b>Bootcamps</b></BV></font></p>",
                                     this.client.Username, 517, 81, 340, 45, 0, 0, 100, False)
        this.client.Cursor.execute(
            "select Username, BootcampCount from Users where PrivLevel < 3 ORDER By BootcampCount DESC LIMIT 22")
        rs = this.client.Cursor.fetchall()
        pos = 1
        text = ""
        count = ""
        for rrf in rs:
            posbootcamps = "0" + str(pos) if pos <= 9 else pos
            playerName = str(rrf[0])
            bootcampCount = rrf[1]
            if pos == 1:
                text += "<font size=\'11\' color=\'#FADE55\'>" + \
                    str(posbootcamps) + "</font> <V>-</V> " + \
                    str(playerName) + "</font>"
                text += "<br />"
            elif pos == 2:
                text += "<font size=\'11\' color=\'#EFEBE0\'>" + \
                    str(posbootcamps) + "</font> <V>-</V> " + \
                    str(playerName) + "</font>"
                text += "<br />"
            elif pos == 3:
                text += "<font size=\'11\' color=\'#B44F0D\'>" + \
                    str(posbootcamps) + "</font> <V>-</V> " + \
                    str(playerName) + "</font>"
                text += "<br />"
            else:
                text += "<font size=\'11\'><CH>" + \
                    str(posbootcamps) + "</CH> <V>-</V> " + \
                    str(playerName) + "</font>"
                text += "<br />"
            count += "<V>" + str(bootcampCount) + "</V>\n"
            this.client.room.addTextArea(10014, str(
                text), this.client.Username, 613, 107, 340, 420, 0, 0, 100, False)
            this.client.room.addTextArea(10015, str(
                count), this.client.Username, 762, 107, 340, 420, 0, 0, 100, False)
            pos += 1


class email:

    def __init__(this, client, server):
        this.client = client
        this.server = client.server
        currentPage = 1

    def close(this):
        i = 10000
        while i <= 12000:
            this.client.room.removeTextArea(i, this.client.Username)
            i += 1

    def openConfirmationBox(this):
        this.close()
        text = "<p align=\'center\'><font size=\'20\' color=\'#990000\'>Confirme seu endereço de email</font></p>"
        text += "\n<font size=\'15\'>Clique <a href=\'event:email:resend\'>aqui</a> para reenviar o código para seu endereço de email.</font>"
        text += "\n<font size=\'15\'>Para confirmar seu endereço de email:</font>"
        text += "\n<font size=\'13\'>1. Entre no email que você usou para criar sua conta.</font>"
        text += "\n<font size=\'13\'>2. Copie o código enviado para o seu email e digite na caixa de texto abaixo.</font>"
        text += "\n<font size=\'13\'>3. Pronto, desfrute dos nossos sistemas e seja feliz!</font>"
        this.client.room.addTextArea(10002, str(
            text), this.client.Username, 64, 46, 680, 128, 0x000000, 0x313131, 95, False)
        this.client.room.addPopup(
            10004, 2, "Digite o código recebido em seu email!\n <center>Ex: B2HGDA87Y.</center>", this.client.Username, 280, 181, 240, True)
        this.client.room.addTextArea(10003, "<font size=\'28\' color=\'#990000\'><a href=\'event:email:close\'>X</a></font>",
                                     this.client.Username, 754, 40, 50, 50, 0, 0, 0, False)

    def sendCode(this):
        code = TFMUtils.getRandomChars(random.randint(8, 10))
        this.client.codeEmailConfirmation = str(code)

        # Credenciais
        remetente = 'andrielkogama@gmail.com'
        senha = 'andriel2004'

        # Informações da mensagem
        destinatario = str(this.client.emailAddress)
        assunto = "Confirme sua conta do " + str(this.server.miceName)
        texto = "Caro " + str(this.client.Username) + ", confirme sua conta do " + str(this.server.miceName) + \
            " usando o seguinte código abaixo: \n" + \
                str(code) + " \nDivirta-se desfrutando de nossos sistemas!"

        # Preparando a mensagem
        msg = "\r\n".join([
            'From: %s' % remetente,
            'To: %s' % destinatario,
            'Subject: %s' % assunto,
            '',
            '%s' % texto
        ])

        # Enviando o email
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.starttls()
        server.login(remetente, senha)
        server.sendmail(remetente, destinatario, msg)
        server.quit()

        this.client.sendMessage("<BL>Verifique seu endereço de email!")
        this.client.updateDatabase()


class radios:

    def __init__(this, client, server):
        this.client = client
        this.server = client.server
        this.Cursor = client.Cursor
        currentPage = 1

    def close(this):
        i = 13000
        while i <= 13019:
            this.client.room.removeTextArea(i, this.client.Username)
            i += 1

    def open(this):
        this.client.room.addTextArea(13000, "<p align=\'center\'><img src=\'https://i.imgur.com/feG3iCj.png\' hspace=\'0\' vspace=\'-2\'>",
                                     this.client.Username, 180, 15, 455, 370, 0, 0, 0, False)
        this.client.room.addTextArea(13001, "<p align=\'center\'><N>Olá <J>" + str(this.client.Username) +
                                     "</J>, bem-vindo ao reprodutor de músicas do " + str(this.server.miceName) + "!", this.client.Username, 200, 85, 430, 100, 0, 0, 0, False)
        this.client.room.addTextArea(13002, "<p align=\'center\'><N>Todas as rádios estão em Português.",
                                     this.client.Username, 220, 104, 350, 100, 0, 0, 0, False)
        this.client.room.addTextArea(13003, "<p align=\'center\'><N>Desfrute do nosso sistema abaixo!",
                                     this.client.Username, 220, 120, 350, 100, 0, 0, 0, False)
        this.client.room.addTextArea(13004, "<p align=\'center\'><N>Escolha uma das opções de rádio acima.",
                                     this.client.Username, 220, 345, 350, 100, 0, 0, 0, False)
        this.client.room.addTextArea(13005, "<p align=\'center\'><img src=\'https://i.imgur.com/eQmi5zW.png\'>",
                                     this.client.Username, 335, 130, 350, 100, 0, 0, 0, False)
        this.client.room.addTextArea(13006, "<p align=\'center\'><img src=\'https://i.imgur.com/eQmi5zW.png\'>",
                                     this.client.Username, 335, 165, 350, 100, 0, 0, 0, False)
        this.client.room.addTextArea(13007, "<p align=\'center\'><img src=\'https://i.imgur.com/eQmi5zW.png\'>",
                                     this.client.Username, 335, 200, 350, 100, 0, 0, 0, False)
        this.client.room.addTextArea(13008, "<p align=\'center\'><img src=\'https://i.imgur.com/eQmi5zW.png\'>",
                                     this.client.Username, 335, 235, 350, 100, 0, 0, 0, False)
        this.client.room.addTextArea(13009, "<p align=\'center\'><img src=\'https://i.imgur.com/eQmi5zW.png\'>",
                                     this.client.Username, 335, 270, 350, 100, 0, 0, 0, False)
        this.client.room.addTextArea(13010, "<p align=\'center\'><img src=\'https://i.imgur.com/eQmi5zW.png\'>",
                                     this.client.Username, 335, 305, 350, 100, 0, 0, 0, False)
        this.client.room.addTextArea(13011, "<p align=\'center\'><img src=\'https://i.imgur.com/eQmi5zW.png\'>",
                                     this.client.Username, 465, 285, 350, 100, 0, 0, 0, False)
        this.client.room.addTextArea(13012, "<N><a href=\'event:config:music:funk\'>FUNK</a>",
                                     this.client.Username, 377, 145, 50, 20, 0, 0, 0, False)
        this.client.room.addTextArea(13013, "<N><a href=\'event:config:music:eletronica\'>ELETRÔNICA</a>",
                                     this.client.Username, 356, 180, 100, 20, 0, 0, 0, False)
        this.client.room.addTextArea(13014, "<N><a href=\'event:config:music:sertaneja\'>SERTANEJA</a>",
                                     this.client.Username, 360, 215, 100, 20, 0, 0, 0, False)
        this.client.room.addTextArea(13015, "<N><a href=\'event:config:music:rap\'>RAP</a>",
                                     this.client.Username, 381, 250, 100, 20, 0, 0, 0, False)
        this.client.room.addTextArea(13016, "<N><a href=\'event:config:music:pop\'>POP</a>",
                                     this.client.Username, 381, 285, 100, 20, 0, 0, 0, False)
        this.client.room.addTextArea(13017, "<N><a href=\'event:config:music:mix\'>MIX</a>",
                                     this.client.Username, 381, 320, 100, 20, 0, 0, 0, False)
        this.client.room.addTextArea(13018, "<N><a href=\'event:config:music:off\'>DESLIGAR</a>",
                                     this.client.Username, 494, 300, 100, 23, 0, 0, 0, False)
        this.client.room.addTextArea(13019, "<R><font size=\'14\'><b><a href=\'event:config:music:close\'>X</a></b></font></R>",
                                     this.client.Username, 192, 54, 34, 34, 0, 0, 0, False)

class DownloadCenter:

    def __init__(this, client, server):
        this.client = client
        this.server = client.server
        currentPage = 1

        this.files = []
        this.changelog = []

        this.newVersion = 0

    def close(this):
        i = 30000
        while i <= 32000:
            this.client.room.removeTextArea(i, this.client.Username)
            i += 1

    def open(this):
        this.close()
        this.client.room.addTextArea(
            30000, "", this.client.Username, 5, 20, 790, 390, 0, 1, 85, False)
        this.client.room.addTextArea(
            30001, "<p align=\'center\'><font size=\'22\' family=\'Arial\' color=\'#BEBB56\'><a><b>Download Center</b></a></font></p>", this.client.Username, 235, 27, 340, 45, 0, 0, 100, False)
        this.client.room.addTextArea(30002, "<font size=\'23\' color=\'#990000\'><a href=\'event:downloadCenter:close\'>X</a></font>",
                                 this.client.Username, 762, 34, 50, 50, 0, 0, 0, False)
        this.client.room.addTextArea(30003, "<p align=\'center\'><font size=\'22\' family=\'Arial\' color=\'#BEBB56\'><a><b>Loading...</b></a></font></p>",
                                 this.client.Username, 320, 208, 150, 50, 0, 0, 0, False)
        this.getUpdates()

    def getUpdates(this):
        up = json.loads(urllib.request.urlopen("https://raw.githubusercontent.com/AndrielGame/TFMProject/master/Updates.json").read())
        for v in up:
            this.files = up[str(v)]["files"]
            this.changelog = up[str(v)]["changelog"]
            this.newVersion = float(v)
            if float(v) > float(this.server.projectVersion):
                this.client.room.addTextArea(30003, "<font size=\'19\' face=\'Arial\'>- " + str(
                            v) + "</font>", this.client.Username, 40, 72, 50, 50, 0x000000, 0x000000, 68, False)
                this.client.room.addTextArea(30004, "<font size=\'17\' face=\'Arial\'>Changelog:</font>", this.client.Username, 51, 92, 100, 50, 0x000000, 0x000000, 68, False)
                i = 0
                for cg in this.changelog:
                    this.client.room.addTextArea(30010+i, "<font size=\'15\' face=\'Arial\'>- " + str(
                            cg) + "</font>", this.client.Username, 139, 92+(90*i//5), 500, 25, 0x000000, 0x000000, 68, False)
                    i += 1
                this.client.room.addTextArea(30005, "<font size=\'17\' face=\'Arial\'>Files:</font>", this.client.Username, 52, 220, 100, 50, 0x000000, 0x000000, 68, False)
                i = 0
                for cg in this.files:
                    this.client.room.addTextArea(30019+i, "<font size=\'15\' face=\'Arial\'>- " + str(
                            cg[0]) + "</font>", this.client.Username, 95, 220+(90*i//5), 500, 25, 0x000000, 0x000000, 68, False)
                    i += 1
                this.client.room.addTextArea(30006, "<a href=\'event:downloadCenter:downloadUpdate\'><font size=\'17\' face=\'Arial\'>Download</font></a>", this.client.Username, 689, 370, 75, 22, 0x000000, 0x313131, 100, False)
            else:
                this.client.room.addTextArea(30003, "<p align=\'center\'><font size=\'22\' family=\'Arial\' color=\'#990000\'><a><b>No have updates :(</b></a></font></p>",
                                 this.client.Username, 218, 208, 380, 50, 0, 0, 0, False)

    def downloadUpdate(this):
        this.client.room.removeTextArea(30002, this.client.Username)
        this.client.room.addTextArea(30006, "<p align=\'center\'><font size=\'17\' face=\'Arial\'>0%</font></p>", this.client.Username, 689, 370, 75, 22, 0x000000, 0x313131, 100, False)
        for file in this.files:
            this.client.room.addTextArea(30007, "<p align=\'center\'><font size=\'14\' face=\'Arial\'>"+(file[0] if file[1] == "init" else file[0]+" > "+file[1]+"/"+file[0])+"</font></p>", this.client.Username, 257, 342, 300, 20, 0x000000, 0x313131, 100, False)
            urllib.request.urlretrieve("https://raw.githubusercontent.com/AndrielGame/TFMProject/master/modules/"+file[0], (file[0] if file[1] == "init" else file[1]+"/"+file[0]), reporthook=this.downloadProgress)
            this.client.room.addTextArea(30009, "]", this.client.Username, 673, 373, 650, 20, 0, 0, 100, False)
        this.client.room.updateTextArea(30007, "<p align=\'center\'><font size=\'14\' face=\'Arial\'>Updated! :)</font></p>", this.client.Username)
        this.server.projectVersion = this.newVersion
        this.server.updateConfig()
        this.server.sendServerRestart(0, 0)
        this.client.room.addTextArea(30002, "<font size=\'23\' color=\'#990000\'><a href=\'event:downloadCenter:close\'>X</a></font>",
                                 this.client.Username, 762, 34, 50, 50, 0, 0, 0, False)

    def downloadProgress(this, count, blockSize, totalSize):
        percent = int(count*blockSize*100/totalSize)
        this.client.room.updateTextArea(30006, "<p align=\'center\'><font size=\'17\' face=\'Arial\'>"+str(100 if percent > 100 else percent)+"%</font></p>", this.client.Username)
        percent = int(percent*(69/100))
        this.client.room.addTextArea(30008, "["+("="*(69 if percent > 69 else percent)), this.client.Username, 47, 373, 650, 20, 0, 0, 100, False)