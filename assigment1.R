###### uvoz knjiznic ######
#C:\Users\Robert\Documents\GitHub\NBApredictions
source("/home/matic/Dropbox/Inteligentni Sistemi/Assigment1/myfunctions.R") #funkcije za ocenjevanje natancnosti modela
#source("C:/Users/Robert/Documents/GitHub/NBApredictions/myfunctions.R") #funkcije za ocenjevanje natancnosti modela
install.packages(c("kknn","pROC","ipred", "prodlim", "CORElearn", "e1071", "randomForest", "kernlab", "nnet"))
library(rpart)
library(CORElearn)
library(pROC)
library(randomForest)
library(e1071)
library(nnet)
library(kknn)


###### uvoz podatkov ######
vseIgre <- read.table("/home/matic/Dropbox/Inteligentni Sistemi/Assigment1/games.csv", header=T, sep=",")
#vseIgre <- read.table("C:/Users/Robert/Documents/GitHub/NBApredictions/games.csv", header=T, sep=",")

###### pregled podatkov ######
head(vseIgre)
summary(vseIgre)
str(vseIgre)
names(vseIgre)

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

###### model: rekurzivno particioniranje - odlocitveno drevo ######
model <- rpart(HOME_win ~ .,data=ucnaMnozicaKlasifikacija)
#izris modela recursive partitioning v obliki odlocitvenega drevesa
plot(model)
text(model, pretty=0)
#ocena natancnosti modela 
resnicneVrednosti <- testnaMnozicaKlasifikacija$HOME_win
napovedi <- predict(model,testnaMnozicaKlasifikacija,type="class")  #ce zelimo res odgovoriti na vprasanja iz navodil naloge namesto "class" nastavi na "prob"
t <- table(resnicneVrednosti,napovedi)
#klasifikacijska natancnost
sprintf("Natancnost rekurzivnega particioniranja: %f",CA(resnicneVrednosti,napovedi))
#brier score
predMat <- predict(model, testnaMnozicaKlasifikacija, type="prob")
obsMat <- model.matrix(~ HOME_win-1,testnaMnozicaKlasifikacija)
sprintf("Brier score rekurzivnega particioniranja: %f",brier.score(obsMat,predMat))
#obcutljivost
sprintf("Obcutljivost rekurzivnega particioniranja: %f",Sensitivity(resnicneVrednosti,napovedi,"True"))
#specificnost
sprintf("Obcutljivost rekurzivnega particioniranja: %f",Specificity(resnicneVrednosti,napovedi,"True"))
#krivulja ROC
rocobjKlasifikacija_rpart <- roc(resnicneVrednosti, predMat[,"True"])
plot(rocobjKlasifikacija_rpart)
names(rocobjKlasifikacija_rpart)
#cutoffs <- rocobj$thresholds
#tp = rocobj$sensitivities
#fp = 1 - rocobj$specificities
#dist <- (1-tp)^2 + fp^2
#dist
#which.min(dist)
#best.cutoff <- cutoffs[which.min(dist)]
# the selected cut-off value has impact on the model's performance
#predicted.label <- factor(ifelse(predMat[,"YES"] >= best.cutoff, "YES", "NO"))
#table(observed, predicted.label)
#CA(bin.observed, predicted.label)
#Sensitivity(resnicneVrednosti, predicted.label, "YES")
#Specificity(resnicneVrednosti, predicted.label, "YES")

##### model: odlocitveno drevo #####
model <- CoreModel(HOME_win ~ .,data=ucnaMnozicaKlasifikacija, model="tree")
#ocena natancnosti modela 
resnicneVrednosti <- testnaMnozicaKlasifikacija$HOME_win
napovedi <- predict(model,testnaMnozicaKlasifikacija,type="class")  #ce zelimo res odgovoriti na vprasanja iz navodil naloge namesto "class" nastavi na "prob"
t <- table(resnicneVrednosti,napovedi)
#klasifikacijska natancnost
sprintf("Natancnost odlocitvenega drevesa: %f",CA(resnicneVrednosti,napovedi))
#brier score
predMat <- predict(model, testnaMnozicaKlasifikacija, type="prob")
obsMat <- model.matrix(~ HOME_win-1,testnaMnozicaKlasifikacija)
sprintf("Brier score odlocitvenega drevesa: %f",brier.score(obsMat,predMat))
#obcutljivost
sprintf("Obcutljivost odlocitvenega drevesa: %f",Sensitivity(resnicneVrednosti,napovedi,"True"))
#specificnost
sprintf("Obcutljivost odlocitvenega drevesa: %f",Specificity(resnicneVrednosti,napovedi,"True"))
#krivulja ROC
rocobjKlasifikacija_dt <- roc(resnicneVrednosti, predMat[,"True"])
plot(rocobjKlasifikacija_dt)
#names(rocobjKlasifikacija_dt)

##### model: naivni Bayes #####
model <- CoreModel(HOME_win ~ .,data=ucnaMnozicaKlasifikacija, model="bayes")
#ocena natancnosti modela 
resnicneVrednosti <- testnaMnozicaKlasifikacija$HOME_win
napovedi <- predict(model,testnaMnozicaKlasifikacija,type="class")  #ce zelimo res odgovoriti na vprasanja iz navodil naloge namesto "class" nastavi na "prob"
t <- table(resnicneVrednosti,napovedi)
#klasifikacijska natancnost
sprintf("Natancnost naivnega bayesa: %f",CA(resnicneVrednosti,napovedi))
#brier score
predMat <- predict(model, testnaMnozicaKlasifikacija, type="prob")
obsMat <- model.matrix(~ HOME_win-1,testnaMnozicaKlasifikacija)
sprintf("Brier score naivnega bayesa: %f",brier.score(obsMat,predMat))
#obcutljivost
sprintf("Obcutljivost naivnega bayesa: %f",Sensitivity(resnicneVrednosti,napovedi,"True"))
#specificnost
sprintf("Obcutljivost naivnega bayesa: %f",Specificity(resnicneVrednosti,napovedi,"True"))
#krivulja ROC
rocobjKlasifikacija_bayes <- roc(resnicneVrednosti, predMat[,"True"])
plot(rocobjKlasifikacija_bayes)
#names(rocobjKlasifikacija_bayes)

##### model: k-najblizjih sosedov - CoreModel#####
model <- CoreModel(HOME_win ~ .,data=ucnaMnozicaKlasifikacija, model="knn",kInNN=20)
#ocena natancnosti modela 
resnicneVrednosti <- testnaMnozicaKlasifikacija$HOME_win
napovedi <- predict(model,testnaMnozicaKlasifikacija,type="class")  #ce zelimo res odgovoriti na vprasanja iz navodil naloge namesto "class" nastavi na "prob"
t <- table(resnicneVrednosti,napovedi)
#klasifikacijska natancnost
sprintf("Natancnost nevronske mreze (KNN): %f",CA(resnicneVrednosti,napovedi))
#brier score
predMat <- predict(model, testnaMnozicaKlasifikacija, type="prob")
obsMat <- model.matrix(~ HOME_win-1,testnaMnozicaKlasifikacija)
sprintf("Brier score nevronske mreze (KNN): %f",brier.score(obsMat,predMat))
#obcutljivost
sprintf("Obcutljivost nevronske mreze (KNN): %f",Sensitivity(resnicneVrednosti,napovedi,"True"))
#specificnost
sprintf("Obcutljivost nevronske mreze (KNN): %f",Specificity(resnicneVrednosti,napovedi,"True"))
#krivulja ROC
rocobjKlasifikacija_dt <- roc(resnicneVrednosti, predMat[,"True"])
plot(rocobjKlasifikacija_dt)
#names(rocobjKlasifikacija_dt)


##### model: nakljucni gozdovi #####
model <- randomForest(HOME_win ~ .,data=ucnaMnozicaKlasifikacija)
#ocena natancnosti modela 
resnicneVrednosti <- testnaMnozicaKlasifikacija$HOME_win
napovedi <- predict(model,testnaMnozicaKlasifikacija,type="class")  #ce zelimo res odgovoriti na vprasanja iz navodil naloge namesto "class" nastavi na "prob"
t <- table(resnicneVrednosti,napovedi)
#klasifikacijska natancnost
sprintf("Natancnost nakljucnih gozdov: %f",CA(resnicneVrednosti,napovedi))
#brier score
predMat <- predict(model, testnaMnozicaKlasifikacija, type="prob")
obsMat <- model.matrix(~ HOME_win-1,testnaMnozicaKlasifikacija)
sprintf("Brier score nakljucnih gozdov: %f",brier.score(obsMat,predMat))
#obcutljivost
sprintf("Obcutljivost nakljucnih gozdov: %f",Sensitivity(resnicneVrednosti,napovedi,"True"))
#specificnost
sprintf("Obcutljivost nakljucnih gozdov: %f",Specificity(resnicneVrednosti,napovedi,"True"))
#krivulja ROC
rocobjKlasifikacija_rf <- roc(resnicneVrednosti, predMat[,"True"])
plot(rocobjKlasifikacija_rf)

##### model: SVM #####
model <- svm(HOME_win ~ .,data=ucnaMnozicaKlasifikacija)
#ocena natancnosti modela 
resnicneVrednosti <- testnaMnozicaKlasifikacija$HOME_win
napovedi <- predict(model,testnaMnozicaKlasifikacija,type="class")  #ce zelimo res odgovoriti na vprasanja iz navodil naloge namesto "class" nastavi na "prob"
t <- table(resnicneVrednosti,napovedi)
#klasifikacijska natancnost
sprintf("Natancnost SVM: %f",CA(resnicneVrednosti,napovedi))
#brier score
predMat <- predict(model, testnaMnozicaKlasifikacija, type="prob")
obsMat <- model.matrix(~ HOME_win-1,testnaMnozicaKlasifikacija)
sprintf("Brier score SVM: %f",brier.score(obsMat,predMat))
#obcutljivost
sprintf("Obcutljivost SVM: %f",Sensitivity(resnicneVrednosti,napovedi,"True"))
#specificnost
sprintf("Obcutljivost SVM: %f",Specificity(resnicneVrednosti,napovedi,"True"))
#krivulja ROC
rocobjKlasifikacija_rf <- roc(resnicneVrednosti, predMat[,"True"])
plot(rocobjKlasifikacija_rf)

##### model: nevronske mreze - nnet #####
#norm.data <- scale.data(rbind(ucnaMnozicaKlasifikacija,testnaMnozicaKlasifikacija))
#norm.learn <- norm.data[1:nrow(learn),]
#norm.test <- norm.data[-(1:nrow(learn)),]
#model <- nnet(Class ~ ., data = norm.learn, size = 5, decay = 0.0001, maxit = 10000)
#ocena natancnosti modela 
#resnicneVrednosti <- testnaMnozicaKlasifikacija$HOME_win
#napovedi <- predict(model,testnaMnozicaKlasifikacija,type="class")  #ce zelimo res odgovoriti na vprasanja iz navodil naloge namesto "class" nastavi na "prob"
#t <- table(resnicneVrednosti,napovedi)
#klasifikacijska natancnost
#sprintf("Natancnost nevronske mreze (KNN) nnet: %f",CA(resnicneVrednosti,napovedi))
#brier score
#predMat <- predict(model, testnaMnozicaKlasifikacija, type="prob")
#obsMat <- model.matrix(~ HOME_win-1,testnaMnozicaKlasifikacija)
#sprintf("Brier score nevronske mreze (KNN) nnet: %f",brier.score(obsMat,predMat))
#obcutljivost
#sprintf("Obcutljivost nevronske mreze (KNN) nnet: %f",Sensitivity(resnicneVrednosti,napovedi,"True"))
#specificnost
#sprintf("Obcutljivost nevronske mreze (KNN) nnet: %f",Specificity(resnicneVrednosti,napovedi,"True"))
#krivulja ROC
#rocobjKlasifikacija_dt <- roc(resnicneVrednosti, predMat[,"True"])
#plot(rocobjKlasifikacija_dt)
#names(rocobjKlasifikacija_dt)

######!!! REGRESIJA !!!######
#iz podatkov odstranimo atribut HOME_win, ki je sicer ciljni atribut klasifikacije
ucnaMnozicaRegresija=ucnaMnozica
ucnaMnozicaRegresija$HOME_win <- NULL
testnaMnozicaRegresija=testnaMnozica
testnaMnozicaRegresija$HOME_win <- NULL

##### model: linearna regresija ##### 
lm.model <- lm(finalScoreDifferential ~ ., data = ucnaMnozicaRegresija)
#ocena natancnosti modela
observed <- testnaMnozicaRegresija$finalScoreDifferential
predicted <- predict(lm.model, testnaMnozicaRegresija)
#povprecna absolutna napaka (RME)
sprintf("MAE za linearno regresijo: %f",mae(observed, predicted)
#relativna povprecna absolutna napaka (RMAE)
sprintf("RMAE za linearno regresijo: %f",rmae(observed, predicted, mean(ucnaMnozicaRegresija$finalScoreDifferential))
#srednja kvadrirana napaka
sprintf("MSE za linearno regresijo: %f",mse(observed, predicted))
#relativna srednja kvadrirana napaka
sprintf("RMSE za linearno regresijo: %f",rmse(observed, predicted, mean(ucnaMnozicaRegresija$finalScoreDifferential)))

##### model: regresijsko drevo #####
rt.model <- rpart(finalScoreDifferential ~ ., ucnaMnozicaRegresija, maxdepth = 2,minsplit=3,cp=0)
plot(rt.model);text(rt.model, pretty = 0)
# the minsplit parameter determines the minimum number of observations that must 
# exist in a node in order for a split to be attempted
# cp parameter controls a compomise between predictive accuracy and tree size
# a table of optimal prunings based on a complexity parameter
printcp(rt.model)
# prune the tree using the complexity parameter associated with minimum error (eg xerror)
rt.model2 <- prune(rt.model, cp = 0.02)
plot(rt.model2)
#ocena natancnosti modela
observed <- testnaMnozicaRegresija$finalScoreDifferential
predicted <- predict(rt.model2, testnaMnozicaRegresija)
#povprecna absolutna napaka (RME)
sprintf("MAE za regresijsko drevo: %f",mae(observed, predicted)
#relativna povprecna absolutna napaka (RMAE)
sprintf("RMAE za regresijsko drevo: %f",rmae(observed, predicted, mean(ucnaMnozicaRegresija$finalScoreDifferential))
#srednja kvadrirana napaka
sprintf("MSE za regresijsko drevo: %f",mse(observed, predicted))
#relativna srednja kvadrirana napaka
sprintf("RMSE za regresijsko drevo: %f",rmse(observed, predicted, mean(ucnaMnozicaRegresija$finalScoreDifferential)))

##### model: nakljucni gozdovi ######
rf.model <- randomForest(finalScoreDifferential ~ ., ucnaMnozicaRegresija)
#ocena natancnosti modela
observed <- testnaMnozicaRegresija$finalScoreDifferential
predicted <- predict(rf.model, testnaMnozicaRegresija)
#povprecna absolutna napaka (RME)
sprintf("MAE za SVM: %f",mae(observed, predicted)
#relativna povprecna absolutna napaka (RMAE)
sprintf("RMAE za nakljucne gozdove: %f",rmae(observed, predicted, mean(ucnaMnozicaRegresija$finalScoreDifferential))
#srednja kvadrirana napaka
sprintf("MSE za nakljucne gozdove: %f",mse(observed, predicted))
#relativna srednja kvadrirana napaka
sprintf("RMSE za nakljucne gozdove: %f",rmse(observed, predicted, mean(ucnaMnozicaRegresija$finalScoreDifferential)))

##### model: SVM ######
svm.model <- svm(finalScoreDifferential ~ ., ucnaMnozicaRegresija)
#ocena natancnosti modela
observed <- testnaMnozicaRegresija$finalScoreDifferential
predicted <- predict(svm.model, testnaMnozicaRegresija)
#povprecna absolutna napaka (RME)
sprintf("MAE za SVM: %f",mae(observed, predicted)
#relativna povprecna absolutna napaka (RMAE)
sprintf("RMAE za SVM: %f",rmae(observed, predicted, mean(ucnaMnozicaRegresija$finalScoreDifferential))
#srednja kvadrirana napaka
sprintf("MSE za SVM: %f",mse(observed, predicted))
#relativna srednja kvadrirana napaka
sprintf("RMSE za SVM: %f",rmse(observed, predicted, mean(ucnaMnozicaRegresija$finalScoreDifferential)))

##### model: K-najblizjih sosedov ###### installation of package ‘kknn’ had non-zero exit status
#knn.model <- kknn(finalScoreDifferential ~ ., ucnaMnozicaRegresija)
#ocena natancnosti modela
#observed <- testnaMnozicaRegresija$finalScoreDifferential
#predicted <- predict(svm.model, testnaMnozicaRegresija)
#povprecna absolutna napaka (RME)
#mae(observed, predicted)
#relativna povprecna absolutna napaka (RMAE)
#rmae(observed, predicted, mean(ucnaMnozicaRegresija$finalScoreDifferential))

##### model: neural network ######
set.seed(6789)
nn.model <- nnet(finalScoreDifferential ~ ., ucnaMnozicaRegresija, size = 10, decay = 1e-4, maxit = 10000, linout = T)
#ocena natancnosti modela
observed <- testnaMnozicaRegresija$finalScoreDifferential
predicted <- predict(svm.model, testnaMnozicaRegresija)
#povprecna absolutna napaka (RME)
sprintf("MAE za nevronsko mrezo: %f",mae(observed, predicted)
#relativna povprecna absolutna napaka (RMAE)
sprintf("RMAE za nevronsko mrezo: %f",rmae(observed, predicted, mean(ucnaMnozicaRegresija$finalScoreDifferential))
#srednja kvadrirana napaka
sprintf("MSE za nevronsko mrezo: %f",mse(observed, predicted))
#relativna srednja kvadrirana napaka
sprintf("RMSE za nevronsko mrezo: %f",rmse(observed, predicted, mean(ucnaMnozicaRegresija$finalScoreDifferential)))
