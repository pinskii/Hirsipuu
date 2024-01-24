"""
COMP.CS.100 Ohjelmointi 1
Nimi: Pinja Rontu
Opiskelijanumero: H299834
Hirsipuupeli

Kyseessä on perinteinen hirsipuupeli. Pelaajalle arpoutuu satunnaisesti
sana, ja pelaajan tehtävänä on arvata tämä sana kirjain kerrallaan.
Näytöllä näkyy viivoina sanan kirjainmäärä.
Helpossa vaikeustasossa sanat ovat 9-kirjaimisia ja vaikeassa 13-kirjaimisia.
Vaikeustaso päätetään pelin alussa napilla.
Arvatessaan tiettyä kirjainta pelaaja painaa kyseisen kirjaimen nappia.
Jos tämä kirjain esiintyy sanassa, se näkyy ruudulla niissä kohdissa,
missä se sanassa sijaitsee. Yhdellä arvauksella paljastuu siis kaikki ne kohdat,
joissa arvattu kirjain esiintyy. Jos pelaaja arvaa väärin, ruudulle tulostuu piirros.
Piirroksen ensimmäinen osa ensimmäisen virheen jälkeen on kumpu, toisen virheen
jälkeen kummun päälle piirtyy lankku jne., kunnes on muodostunut hirsipuu.
Yhteensä pelissä voi tehdä virheen eli arvata väärää kirjainta viisi kertaa
ennen kuin häviää. Pelaaja voittaa, jos hän arvaa sanan ennen piirroksen
valmistumista. Uusi peli -napilla pelin voi aloittaa aina alusta.
"""

from tkinter import *
import random

# 9-kirjaimisten sanojen lista
HELPOT_SANAT = ["yököttävä", "mörökölli", "kalaruoka", "jätesanko", "ahdistelu",
                "harjoitus", "lähtöarvo", "mehulinko", "hiuslakka", "aamukahvi",
                "murtovesi", "lesbopari", "kopiokone", "kuntosali", "keskiarvo",
                "keräkaali", "muinainen", "hevosrotu", "bassoääni", "elinkeino",
                "feminismi", "korkkipuu", "maaliskuu", "autotalli", "desilitra"]

# 13-kirjaimisten sanojen lista
VAIKEAT_SANAT = ["ympäristöalue", "rouvashenkilö", "henkilökuvaus",
                 "funktiolaskin", "absoluuttinen", "epätavallinen",
                 "harjoittelija", "joulukynttilä", "korvatulehdus",
                 "mustikkamaito", "riidanalainen", "suitsutusaine",
                 "goottilaisuus", "ilmatyynyalus", "mezzosopraano",
                 "jäätelötuutti", "aamunsarastus", "cashewpähkinä"]

# Aakkoslista
AAKKOSET = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q",
            "R","S","T","U","V","W","X","Y","Z","Å","Ä","Ö"]

class Game:
    def __init__(self):
        self.__game = Tk()

        # Määrätään ruudun koko
        self.__game.geometry("1500x700")

        # Lisätään kuvat
        self.__kuva_1 = PhotoImage(file="eka.gif")
        self.__kuva_2 = PhotoImage(file="toinen.gif")
        self.__kuva_3 = PhotoImage(file="kolmas.gif")
        self.__kuva_4 = PhotoImage(file="neljas.gif")
        self.__kuva_5 = PhotoImage(file="viides.gif")
        self.__kuva_6 = PhotoImage(file="kuudes.gif")

        # Muodostetaan otsikko
        self.__otsikko = Label(self.__game, text="Hirsipuu",
                             width=20, font="none 24 bold underline")
        self.__otsikko.grid(column=19, row=0, sticky=E+W)

        # Vaikeustasonapit
        self.__vaikea = Button(self.__game, text="Vaikea", font="none 18",
                               command=self.vaikea, width=6)
        self.__vaikea.grid(column=21, row=0, sticky=N+E)

        self.__helppo = Button(self.__game, text="Helppo", font="none 18",
                               command=self.helppo, width=6)
        self.__helppo.grid(column=21, row=1, sticky=N + E)

        # Label, johon arvatessa väärää kirjainta, tulostuu kuva
        self.__kuva_label = Label(self.__game, image=None)
        self.__kuva_label.grid(row=9, column=1, sticky=N, columnspan=15)

        # Label, jossa pelin päättyessä näkyy joko "hävisit pelin"
        # tai "voitit pelin"
        self.__pelin_loppu = Label(self.__game, text=None, font="none 18")
        self.__pelin_loppu.grid(row=1, column=19)

        # Nappi, josta peli alkaa alusta
        self.__uusi_peli = Button(self.__game, text="Uusi peli",
                                  command=self.uusi_peli, state=DISABLED,
                                  background="gray", font="none 15")
        self.__uusi_peli.grid(row=3, column=19)

        # Muodostetaan aakkoslistasta kirjainnapit
        self.__napit = []
        for kirjain in AAKKOSET:
            nappi = Button(self.__game, text=kirjain,
                           command=lambda x=kirjain: self.painallus(x),
                           width=7, height=2, font="none 10", state=DISABLED,
                           background="gray")
            self.__napit.append(nappi)

        # Määrätään kirjainnappien paikat
        for i in range(len(self.__napit)):
            if i < 5:
                self.__napit[i].grid(row=4, column=i+20, sticky=N)
            elif 4 < i < 10:
                self.__napit[i].grid(row=5, column=i + 20 -5, sticky=N)
            elif 9 < i < 15:
                self.__napit[i].grid(row=6, column=i + 20-10, sticky=N)
            elif 14 < i < 20:
                self.__napit[i].grid(row=7, column=i + 20-15, sticky=N)
            elif 19 < i < 25:
                self.__napit[i].grid(row=8, column=i + 20-20, sticky=N)
            elif 24 < i < 30:
                self.__napit[i].grid(row=9,column=i + 20-25, sticky=N)

        # Laskuri, joka laskee pelaajan virheet
        self.__fail_laskuri = 0

        self.__game.mainloop()

    def vaikea(self):
        """
        Valittu vaikea vaikeustaso. Sanat ovat siis 13-kirjaimisia.
        """
        # Arvotaan sana
        self.__sana = random.choice(VAIKEAT_SANAT)
        self.sanan_muodostus()
        # Muutetaan nappien päälläoloa
        self.__vaikea.configure(state=DISABLED, background="gray")
        self.__helppo.configure(state=DISABLED, background="gray")
        for nappi in self.__napit:
            nappi.configure(state=NORMAL, background="SystemButtonFace")


    def helppo(self):
        """
        Valittu helppo vaikeustaso. Sanat ovat siis 9-kirjaimisia.
        """
        # Arvotaan sana
        self.__sana = random.choice(HELPOT_SANAT)
        self.sanan_muodostus()
        # Muutetaan nappien päälläoloa
        self.__helppo.configure(state=DISABLED, background="gray")
        self.__vaikea.configure(state=DISABLED, background="gray")
        for nappi in self.__napit:
            nappi.configure(state=NORMAL, background="SystemButtonFace")

    def sanan_muodostus(self):
        """
        Funktio muodostaa alaviivat ja labelit, johon sana paljastuu
        """
        # Sanan pituus
        self.__kirjain_maara = len(self.__sana)

        # Arvattavan sanan kirjaimille labelit, johon ne paljastuvat
        # Ennen kuin kirjain arvataan, paikassa on alaviiva
        kolumni_kohta = 4
        self.__kirjain_lista = []
        for k in range(self.__kirjain_maara):
            self.__arvattava = Label(self.__game, text=" _", font="none 20 bold",
                                     width=3)
            self.__kirjain_lista.append(self.__arvattava)

        for i in range(len(self.__kirjain_lista)):
            self.__kirjain_lista[i].grid(row=2, column=kolumni_kohta, sticky=W)
            kolumni_kohta += 1

    def painallus(self, kirjain):
        """
        Pelaajan painaessa kirjainnappia tapahtuu tämän funktion toiminta,
        eli joko kirjainten tai kuvan tulostuminen ruudulle
        :param kirjain: str, pelaajan painamaa nappia vastaava kirjain
        """
        # Kirjaimet pitää muuttaa pieniksi vertailuja varten
        kirjain_pieni = kirjain.lower()

        # Jos arvattu kirjain on sanassa, saadaan kirjainten paikat tietoon
        # kirjaimen_indeksi-funktiolla ja paikkatiedon avulla ne voidaan
        # configuroida näkymään pelaajalle
        if kirjain_pieni in self.__sana:
            indeksit = self.kirjaimen_indeksi(kirjain_pieni)
            for k in self.__sana:
                if k == kirjain_pieni:
                    for indeksi in indeksit:
                        self.__kirjain_lista[indeksi].configure(text=kirjain)

        # Jos arvattu kirjain ei ole sanassa,
        # virhelaskurin arvoon lisätään yksi virhe lisää
        else:
            self.__fail_laskuri += 1

        # Kun nappia on painettu kerran, sitä ei voi enää painaa uudestaan
        haluttu_nappi = self.__napit[AAKKOSET.index(kirjain)]
        haluttu_nappi.configure(state=DISABLED, background="gray")

        # Tarkistetaan, voittiko pelaaja
        self.pelin_voittaminen()

        # Funktio kasvattaa piirrosta virheiden määrän mukaan
        self.piirros_kasvaa()

    def piirros_kasvaa(self):
        """
        Kuva muuttuu sitä mukaa, kun virheiden määrä kasvaa ja
        häviö tulee kuudesta virheestä
        """
        if self.__fail_laskuri == 1:
            self.__kuva_label.configure(image=self.__kuva_1)
        elif self.__fail_laskuri == 2:
            self.__kuva_label.configure(image=self.__kuva_2)
        elif self.__fail_laskuri == 3:
            self.__kuva_label.configure(image=self.__kuva_3)
        elif self.__fail_laskuri == 4:
            self.__kuva_label.configure(image=self.__kuva_4)
        elif self.__fail_laskuri == 5:
            self.__kuva_label.configure(image=self.__kuva_5)
        elif self.__fail_laskuri == 6:
            self.__kuva_label.configure(image=self.__kuva_6)

            # Fail_laskurin täyttyessä pelaaja häviää ja uusi_peli -nappi
            # aktivoituu
            self.__pelin_loppu.configure(text="Hävisit pelin!")
            for nappi in self.__napit:
                nappi.configure(state=DISABLED, background="gray")
            self.__uusi_peli.configure(state=NORMAL,
                                       background="SystemButtonFace")
            # Myös sana paljastuu kokonaan hävitessä
            kirjaimet = list(self.__sana.upper())
            for indeksi in range(len(self.__kirjain_lista)):
                self.__kirjain_lista[indeksi].configure(text=kirjaimet[indeksi])

    def pelin_voittaminen(self):
        """
        Tämä funktio tarkistaa, onko pelaaja voittanut. Jos on, tulostuu
        näytölle "voitit pelin!" ja uusi_peli -nappi aktivoituu
        """
        # Kootaan pelaajan arvaama sana sen kirjainlabeleista
        arvatut_kirjaimet = ""
        for indeksi in range(len(self.__kirjain_lista)):
            arvatut_kirjaimet += self.__kirjain_lista[indeksi].cget("text")

        teksti = arvatut_kirjaimet.lower()

        # Jos koottu sana on sama kuin arvottu sana, pelaaja voittaa
        if teksti == self.__sana:
            self.__pelin_loppu.configure(text="Voitit pelin!")
            for nappi in self.__napit:
                nappi.configure(state=DISABLED, background="gray")
            self.__uusi_peli.configure(state=NORMAL,
                                       background="SystemButtonFace")

    def kirjaimen_indeksi(self,kirjain):
        """
        Käydään läpi kaikki sanassa esiintyvät kirjaimet ja jos sanassa on
        pelaajan arvaama kirjain, sen indeksi tallentuu listaan
        :param kirjain: str, se kirjain, jonka nappia painettu
        :return: list, lista kirjainten indekseistä sanassa
        """
        self.__indeksilista = []
        for k in range(len(self.__sana)):
            if self.__sana[k] == kirjain.lower():
                self.__indeksilista.append(k)

        return self.__indeksilista

    def uusi_peli(self):
        """
        Uusi peli -nappia painessa pelin kaikki elementit resetoidaan
        """
        for nappi in self.__napit:
            nappi.configure(state=DISABLED, background="gray")
        self.__kuva_label.configure(image="")
        self.__pelin_loppu.configure(text="")
        for kirjain in self.__kirjain_lista:
            kirjain.configure(text="")
        self.__vaikea.configure(state=NORMAL, background="SystemButtonFace")
        self.__helppo.configure(state=NORMAL, background="SystemButtonFace")
        self.__uusi_peli.configure(state=DISABLED, background="gray")
        self.__kirjain_lista.clear()
        self.__indeksilista.clear()
        self.__fail_laskuri = 0



def main():
    Game()


main()