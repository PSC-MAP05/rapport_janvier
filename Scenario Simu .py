# Libraries Included:
# Numpy, Scipy, Scikit, Pandas

print("Hello, world!")
print(1/4)
import numpy as np

n_utilisateurs = 10000

n_jours = 10

n_periodes = 24

n_plats = 3

# tab pour savoir si un tuilsaeur a achete ou non
# tab qui donne les indices des utilisateurs qui peuvent encore acheter

tab_consom_potentiel = [i for i in range(n_utilisateurs)]


# fonction qui à une période donnée retourne le paramètre de la loi de poisson
# vérifier que ce paramètre ne déborde pas
def tiragePoisson(periode):
   # coeff =  # je comprends pas ce que tu fais ....
    # je suppose que lambda est tiré selon une loi uniforme entre des bornes variables
    # pour que lambda soit plus grand à 22H qu'à 20H.
    # OOK
    a = -periode*(periode-24)
    b= 1

    pam_lambd = np.random.uniform(low=a , high=a + b)
    return pam_lambd





# tab_notes est composée d'une matrice pour chaque plat. Donc pour accéder à la matrice d'un plat on fera tab_notes[plat][utilisateurs][prix]

# tab_prix sera la matrice qui pour un plat donné donne le vecteur ligne des prix pour un jour donné. Par exemple [[1 3 4 5 6 7 9] [10 10 10 10 10 10]] veut dire que pour le plat 1, on a mis les prix 1 à 20H, 3 à 20H10, 4 à 20H20. et 10 pour le plat 2

def genererNote(propension, prix):
    # cette fonction sert à générer la note de l'utilsateurs à partir de la propension a payer
    note = (propension - prix)  /propension * 5
    return note


def argmaxCritere(propension, tab_prix, periode):
    argmax = -1
    maximu = -1
    for plat in range(len(tab_prix)):
        if propension[plat] - tab_prix[plat][periode] > maximu:
            argmax = plat
            maximu = propension[plat]-tab_prix[plat][periode]

    return argmax


def f(i, n):
    if i <= n / 3:
        return 0, 0, n/3
    elif i >= 2 * n / 3:
        return 2, 2*n/3,n
    else:
        return 1, n/3, 2*n/3


def g(i, e_low, e_high,p):
    i = i-e_low
    e_high = e_high - e_low
    e_low = 0
    resultat = 0
    if i <= e_high / 3:
        resultat = 0
    elif i >= 2 * e_high / 3:
        resultat =  2
    else:
        resultat = 1

    if p ==1:
        resultat+=1
        resultat %= 3
    if p==2:
        resultat +=2
        resultat%=3
    return resultat


def z(classe, gout_plat):


    return classe + gout_plat

def remplir_prix(tab_prix,jr):
    for i in range(len(tab_prix[0])):
        tab_prix[0][i] = 1
        tab_prix[1][i] = 2
        tab_prix[2][i] = 3
    return tab_prix

tab_prix = [[0 for i in range(n_periodes)] for j in range(n_plats)]

for jr in range(n_jours):
    tab_prix = remplir_prix(tab_prix, jr)
    tab_ventes = [[0 for j in range(n_periodes)] for i in range(n_plats)]
    n_util_restant = n_utilisateurs
    tab_lambda = [0 for i in range(n_periodes)]
    tab_consom_potentiel = [i for i in range(n_utilisateurs)]

    for per in range(n_periodes):
        n_util_restant = len(tab_consom_potentiel)
        tab_lambda[per] = tiragePoisson(per)
        # np = lambda
        p = tab_lambda[per] / n_util_restant
        temp = []
        # pour chaque personne restante, tirer une loi de bernoulli et voir si elle consomme ou pas. Si c'est le cas, on l'enlève de la liste des consommateurs potentiels
        for indice in tab_consom_potentiel:
            if (np.random.rand() < p):
                temp.append(indice)
        tab_consom_potentiel = np.array(tab_consom_potentiel)
        tab_consom_potentiel = np.delete(tab_consom_potentiel, temp)
        # ici, on a la liste actualisée de tous les individus susceptibles de consommer
        for i in temp:

            propension = [0 for i in range(n_plats)]
            # np.random.exponential(scale= parametre)
            # maintenant on peut découper notre population selon la classe sociale et le gout pour chaque produit. L'attributino se fait en fonction de l'indice de la personne
            classe, extremite_low, extremite_high = f(i, n_utilisateurs)
            gout_plat = g(i,extremite_low,extremite_high,p)
            for p in range(n_plats):
                gout_plat = g(i, extremite_low, extremite_high, p)
                propension[p] = np.random.exponential(scale=1/(z(classe, gout_plat+0.5)))
            plat = argmaxCritere(propension, tab_prix, per)
            tab_ventes[plat][per] += 1

            # on a 2 possibilités: il achete le plat qui maximise un critère, ou bien il n'achète pas


    print("Jour ",jr ,tab_ventes)


