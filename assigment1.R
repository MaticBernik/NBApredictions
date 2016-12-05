###### uvoz knjiznic ######
#C:\Users\Robert\Documents\GitHub\NBApredictions
#source("/home/matic/Dropbox/Inteligentni Sistemi/Assigment1/myfunctions.R") #funkcije za ocenjevanje natancnosti modela
source("C:/Users/Robert/Documents/GitHub/NBApredictions/myfunctions.R") #funkcije za ocenjevanje natancnosti modela
library(rpart)
library(CORElearn)

###### uvoz podatkov ######
#vseIgre <- read.table("/home/matic/Dropbox/Inteligentni Sistemi/Assigment1/games.csv", header=T, sep=",")
vseIgre <- read.table("C:/Users/Robert/Documents/GitHub/NBApredictions/games.csv", header=T, sep=",")


###### izracun izhodiscne natancnosti - vecinskega klasifikatorja
domacaZmagaIgre=vseIgre[vseIgre$HOME_win == "True",] #vse igre, kjer je zmagala domaca ekipa
tujaZmagaIgre=vseIgre[vseIgre$HOME_win == "False",] #vse igre, kjer je zmagala tuja ekipa
domacaEkipaNatancnost=nrow(domacaZmagaIgre)/nrow(vseIgre) #klasifikacijska tocnost, ce vsakic napovemo, da bo zmagala domaca ekipa
tujaEkipaNatancnost=nrow(tujaZmagaIgre)/nrow(vseIgre) #klasifikacijska tocnost, ce vsakic napovemo, da bo zmagala tuja ekipa
sprintf("Natancnost klasifikatorja 'zmagala bo domaca ekipa': %f",domacaEkipaNatancnost)
sprintf("Natancnost klasifikatorja 'zmagala bo tuja ekipa': %f",tujaEkipaNatancnost)
sprintf("Nas model bo torej moral biti v napovedovanju boljsi kot vecinski klasifikator z natancnostjo: %f",if(domacaEkipaNatancnost>tujaEkipaNatancnost)domacaEkipaNatancnost else tujaEkipaNatancnost)

###### delitev na ucno in tesno mnozico ######
#Za potrebe internega preverjanja modela kot testno mnozico izberemo zadnjih nekaj(30%) tekem (t.j. tekem, ki so bile odigrane kasneje kot tekme vsebovane v ucni mnozici).
#Kakrsna koli drugacna delitev podatkov, ki vrstice najprej premesa, da unici urejenost v podatki (npr. nekatere ekipe so morda bolje odrezejo proti koncu ali na zacetku sezone),
#bi tako dopustila moznost, da v nekem delu preverjanja napovedujemo izid tekme z modelom, ki je bil naucen tudi na podatkih tekem, ki so se zgodile po opazovani tekmi (torej tisti, katere izid napovedujemo).
#Atributi take tekme (tekme, ki so se zgodile po tekmi, katere izid zelimo napovedati) pa zajemajo tudi statistiko tekme, ki jo napovedujemo,
#---> kar pomeni da ucna in testna mnozica nista neodvisni.  
stVrstic=nrow(vseIgre)
indx=as.integer(stVrstic*0.7 +0.5)
ucnaMnozica=vseIgre[c(0:indx),]
testnaMnozica=vseIgre[c(indx:stVrstic),]

###### primerjava natancnosti vecinskega klasifikatorja nad ucno in testno mnozico z natancnostjo nad vsemi podatki ######
#Testiranje nad ucno mnozico
domacaZmagaIgreUCNA=ucnaMnozica[ucnaMnozica$HOME_win == "True",] #UCNA MNOZICA:vse igre, kjer je zmagala domaca ekipa
tujaZmagaIgreUCNA=ucnaMnozica[ucnaMnozica$HOME_win == "False",] #UCNA MNOZICA:vse igre, kjer je zmagala tuja ekipa
domacaEkipaNatancnostUCNA=nrow(domacaZmagaIgreUCNA)/nrow(ucnaMnozica) #UCNA MNOZICA:klasifikacijska tocnost, ce vsakic napovemo, da bo zmagala domaca ekipa
tujaEkipaNatancnostUCNA=nrow(tujaZmagaIgre)/nrow(vseIgre) #UCNA MNOZICA: klasifikacijska tocnost, ce vsakic napovemo, da bo zmagala tuja ekipa
sprintf("UCNA MNOZICA: Natancnost klasifikatorja 'zmagala bo domaca ekipa': %f",domacaEkipaNatancnostUCNA)
sprintf("UCNA MNOZICA: Natancnost klasifikatorja 'zmagala bo tuja ekipa': %f",tujaEkipaNatancnostUCNA)
#Testiranje nad testno mnozico
domacaZmagaIgreTESTNA=testnaMnozica[testnaMnozica$HOME_win == "True",] #TESTNA MNOZICA:vse igre, kjer je zmagala domaca ekipa
tujaZmagaIgreTESTNA=testnaMnozica[testnaMnozica$HOME_win == "False",] #TESTNA MNOZICA:vse igre, kjer je zmagala tuja ekipa
domacaEkipaNatancnostTESTNA=nrow(domacaZmagaIgreTESTNA)/nrow(testnaMnozica) #TESTNA MNOZICA:klasifikacijska tocnost, ce vsakic napovemo, da bo zmagala domaca ekipa
tujaEkipaNatancnostTESTNA=nrow(tujaZmagaIgreTESTNA)/nrow(testnaMnozica) #TESTNA MNOZICA:klasifikacijska tocnost, ce vsakic napovemo, da bo zmagala tuja ekipa
sprintf("TESTNA MNOZICA: Natancnost klasifikatorja 'zmagala bo domaca ekipa': %f",domacaEkipaNatancnostTESTNA)
sprintf("TESTNA MNOZICA: Natancnost klasifikatorja 'zmagala bo tuja ekipa': %f",tujaEkipaNatancnostTESTNA)

######!!! KLASIFIKACIJA !!!######
#iz podatkov odstranimo atribut finalScoreDifferential, ki je sicer ciljni atribut regresije
ucnaMnozicaKlasifikacija=ucnaMnozica
ucnaMnozicaKlasifikacija$finalScoreDifferential <- NULL
testnaMnozicaKlasifikacija=testnaMnozica
testnaMnozicaKlasifikacija$finalScoreDifferenetial <- NULL
#od ucne mnozice locimo ciljni atribut (da ju lahko loceno podamo algoritmu za gradnjo napovednega modela)
#ucnaMnozicaKlasifikacija_ciljni = ucnaMnozicaKlasifikacija$HOME_win 
#ucnaMnozicaKlasifikacija_opisni = ucnaMnozicaKlasifikacija[-ucnaMnozicaKlasifikacija$HOME_win]
#od testne mnozice locimo ciljni atribut
#testnaMnozicaKlasifikacija_ciljni = testnaMnozicaKlasifikacija$HOME_win 
#testnaMnozicaKlasifikacija_opisni = testnaMnozicaKlasifikacija[-testnaMnozicaKlasifikacija$HOME_win]

###### model: rekurzivno particioniranje ######

model <- rpart(HOME_win ~ .,data=ucnaMnozicaKlasifikacija)
#izris modela recursive partitioning v obliki odlocitvenega drevesa
plot(model)
#text(dtmpretty=0)
#ocena natancnosti modela 
resnicneVrednosti <- testnaMnozicaKlasifikacija$HOME_win
napovedi <- predict(model,testnaMnozicaKlasifikacija,type="class")  #ce zelimo res odgovoriti na vprasanja iz navodil naloge namesto "class" nastavi na "prob"
t <- table(resnicneVrednosti,napovedi)
#klasifikacijska natancnost
sprintf("Natancnost rekurzivnega particioniranja: %f",CA(resnicneVrednosti,napovedi))
#brier score
sprintf("Brier score rekurzivnega particioniranja: %f",brier.score(resnicneVrednosti,napovedi))
#obcutljivost
sprintf("Obcutljivost rekurzivnega particioniranja: %f",Sensitivity(resnicneVrednosti,napovedi,HOME_win))
#specificnost
sprintf("Obcutljivost rekurzivnega particioniranja: %f",Specificity(resnicneVrednosti,napovedi,HOME_win))
#krivulja ROC
#install.packages("pROC") #namesti paket pROC
rocobjKlasifikacija_rpart <- (bin.resnicneVrednosti, bin.napovedi)

##### model: odlocitveno drevo
model <- CoreModel(HOME_win ~ .,data=ucnaMnozicaKlasifikacija, model="tree")

##### model: naivni Bayes
model <- CoreModel(HOME_win ~ .,data=ucnaMnozicaKlasifikacija, model="bayes")

##### model: nevronske mreze (KNN)
model <- CoreModel(HOME_win ~ .,data=ucnaMnozicaKlasifikacija, model="knn",kInNN=5)

######!!! REGRESIJA !!!######
#iz podatkov odstranimo atribut HOME_win, ki je sicer ciljni atribut klasifikacije
ucnaMnozicaRegresija=ucnaMnozica
ucnaMnozicaRegresija$HOME_win <- NULL
testnaMnozicaRegresija=testnaMnozica
testnaMnozicaRegresija$HOME_win <- NULL
#od ucne mnozice locimo ciljni atribut (da ju lahko loceno podamo algoritmu za gradnjo napovednega modela)
#ucnaMnozicaRegresija_ciljni = ucnaMnozicaRegresija$finalScoreDifferential 
#ucnaMnozicaRegresija_opisni = ucnaMnozicaRegresija[-ucnaMnozicaRegresija$finalScoreDifferential]
#od testne mnozice locimo ciljni atribut
#testnaMnozicaRegresija_ciljni = testnaMnozicaRegresija$finalScoreDifferential 
#testnaMnozicaRegresija_opisni = testnaMnozicaRegresija[-testnaMnozicaRegresija$finalScoreDifferential]
