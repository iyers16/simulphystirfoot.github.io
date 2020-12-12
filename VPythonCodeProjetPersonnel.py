from vpython import *
#GlowScript 3.0 VPython


scene.width = 1520
scene.height = 600
print_options(width = 1520, height = 350)
#Données de l'utilisateur
dist = input("Distance entre le tireur et le but (de 0 à 84.00m) : ")
hei = input("Hauteur du ballon lorsqu'il entre dans le but (hauteur du but maximale de 2.44m) : ")
usermass = input("Indiquez votre masse (en kgs) : ")
#Vérification de validité des entrées
while True : 
    try :
       distance = float(dist)
       height = float(hei)
       umass = float(usermass)
       break;
    except ValueError :
      print("Entrées invalides, réesssayez encore une fois")

#Constantes présentes dans le logiciel
g = -9.8
maxspeed = 30.0
viz = 0.00
dt = 0.001
t = 0
tempsmax = 3.5
averageballmass = 0.45
bodytolegpercentage = 17.555 / 100
averagelegmass = umass * bodytolegpercentage
coeffofrestitution = 0.8

#Algorithme de réception, optimization et classification des résultats
vixlist = []
viylist = []
count = 1.0
vix = count
while vix <= maxspeed:
    viy = (2 * pow(vix, 2) * height - g * pow(distance, 2)) / (2*vix*distance)
    if ((pow(vix, 2) + pow(viy, 2)) <= pow(maxspeed, 2)):
        vixlist.append(vix)
        viylist.append(viy)
    vix += count

#Formation de mes objets 3D
ball = sphere(pos = vector(0,0,0), radius = 0.22, color = color.red, make_trail = True, trail_radius = 0.07, interval = 10)
goal = box(pos = vector(distance + 0.25,1.05,0), length = 0.5, height = 2.44, width = 7.32, color = color.white)
field = box(pos = vector(distance/2,-(ball.radius),0), length = distance, height = 0.1, width = 60, color = color.green)

#Calcul de variables utilisables par l'utilisateur
airtime = distance/vixlist[-1]
angle = degrees(atan(viylist[-1] / vixlist[-1]))
launchvelocity = sqrt(pow(viylist[-1], 2) + pow(vixlist[-1], 2))
possibletrajectories = len(vixlist)
accelball = launchvelocity *100
kicknetforce = averageballmass * accelball
kickmass = kicknetforce / 9.8
legvelocity = (launchvelocity * (averagelegmass + averageballmass)) / ((1 + coeffofrestitution) * averagelegmass)
kickpoint = angle * ball.radius

#def whichquintile(T,A) : 
#  rep = T / A
#  return rep

#q1 = whichquintile(tempsmax, airtime)


#if (q1 > 0 and q1 <= 0.7):
#    print("Probabilité de réussite entre 81% et 100%")
#    q2 = q1 * 100 / 0.7
#    q3 = 80 + (20*q2/100)
#    print("Probabilité de réussite : ",q3, "%")
#elif (q1 > 0.7 and q1 <= 1.4):
#    print("Probabilité de réussite entre 61% et 80%")
#    q2 = (q1 - 0.7) * 100 / 0.7
#    q3 = 60 + (20*q2/100)
#    print("Probabilité de réussite : ",q3, "%")
#elif (q1 > 1.4 and q1 <= 2.1):
#    print("Probabilité de réussite entre 41% et 60%")
#    q2 = (q1 - 1.4) * 100 / 0.7
#    q3 = 40 + (20*q2/100)
#    print("Probabilité de réussite : ",q3, "%")
#elif (q1 > 2.1 and q1 <= 2.8) :
#    print("Probabilité de réussite entre 21% et 40%")
#    q2 = (q1 - 2.1) * 100 / 0.7
#    q3 = 20 + (20*q2/100)
#    print("Probabilité de réussite : ",q3, "%")
#elif (q1 > 2.8 and q1 <= 3.5) :
#    print("Probabilité de réussite entre 0% et 20%")
#    q2 = (q1 - 2.8) * 100 / 0.7
#    q3 = 0 + (20*q2/100)
#    print("Probabilité de réussite : ",q3, "%")
#else :
#    print("Improbable de réussir ce tir réellement avec un gardien dans le but")
            

#Données à retourner vers l'utilisateur
if (len(vixlist) > 0):
    print("Shift + clique + bouger souris = changement de perspective de vue   et   Ctrl + clique + bouger souris = rotation de perspective\n\n")
    print("Nombre de trajectoires possibles : ", possibletrajectories,"\n\n")
    print("Infos sur la trajectoire optimale : \n")
    print("Temps de vol : ", airtime, "secondes.")
    print("Angle de lancée : ", angle, "degres.")
    print("Vélocité initiale du ballon : ", launchvelocity, "m/s.")
    print("Force nécessaire pour effectuer la frappe : ", kicknetforce, "N")
    print("Au moment du contact avec le ballon, votre jambe doit voyager à une vitesse de : ", legvelocity, "m/s.")
    print("Vous ressentirez une masse de", kickmass,"kg sur votre pied au moment de contact avec le ballon.\nSuggestion d'entrainement musculaire : Lorsque vous vous entrainez les jambes essayez de vous rapprocher le plus possible le masse inscrite ci-dessus pour faciliter le tir.")
    print("Vous devriez frapper la balle aussi exactement que possible à", kickpoint,"cm en bas du milieu horizontal du ballon.")
    
    
    
#Initialisation d'un vecteur de mouvement mutlidimmensionnel du ballon
ball.velocity = vector(vix, viy, viz)

#Algorithme de mouvement du ballon
while ball.pos.x <= distance - ball.radius:    
    rate (1000)
    
    ball.pos.y = ball.pos.y + ball.velocity.y*dt
    ball.pos.x = ball.pos.x + ball.velocity.x*dt
    ball.pos.z = ball.pos.z + ball.velocity.z*dt
    
    if ball.pos.y < ball.radius:
      ball.velocity.y = abs(ball.velocity.y)
    else:
      ball.velocity.y = ball.velocity.y + g*dt
    
    
    if ball.pos.x > distance - ball.radius or ball.pos.x < 0 :
      ball.velocity.x = 0
      ball.velocity.y = 0
    else : 
      ball.velocity.x = ball.velocity.x


print("\nPosition du ballon final : (", str(ball.pos.x), ";", str(ball.pos.y), ")")
print("***Incertitude de + ou - 0.9 m***")