# Projet-Vanna-Volga 

Ce script reconstruit une surface de volatilité FX en utilisant la méthode Vanna-Volga, qui est une méthode semi-analytique utilisée en trading FX pour interpoler (ou extrapoler) des volatilités implicites. 

# Pourquoi on fait ça ? 

En FX, le marché ne cote pas toutes les volatilités : il cote seulement : 

- la volatilité ATM
- le 25D Risk Reversal (différence call – put)
- le 25D Butterfly (symétrie du smile)

Mais pour pricer une option exotique ou faire du hedging, il faut : 

→ une volatilité à TOUT strike Donc on reconstruit la "nappe" complète : 

Strike × Ténor → Volatilité implicite 

La méthode Vanna-Volga utilise trois points : vol_put25 , vol_atm , vol_call25 et reconstitue une vol pour n’importe quel strike. 

# TAUX D'INTÉRÊT DOMESTIQUE ET FOREIGN 

Pour convertir un delta en strike ou un forward en strike, il faut connaître les taux domestique et étranger : 

rd : taux domestique 
rf : taux étranger 

# À quoi servent les discount factors en FX ? 

En FX, une option est un produit à deux taux d’intérêt : 

rd = taux domestique (devise dans laquelle tu payes ton payoff) 
rf = taux étranger (taux de l’actif sous-jacent, car l’underlying = spot FX) 

Comme l’actif est dans une autre devise, il porte un taux étranger, exactement comme une action qui verserait un dividende. Donc dans FX : 

👉 rf joue le rôle d’un taux de dividende 
👉 rd joue le rôle du taux sans risque 

C’est un pilier essentiel du pricing FX. 

# ARBITRAGE FORWARD FX 

# Principe fondamental 

Un contrat forward FX fixe aujourd’hui un prix 𝐹 pour échanger une devise étrangère contre une devise domestique à une date future 𝑇. 

Pour qu’il n’y ait pas d’arbitrage, ce forward doit être cohérent avec : le spot 𝑆 le taux domestique 𝑟𝑑 le taux étranger 𝑟𝑓 

Si 𝐹 n’est pas cohérent, alors tu peux construire une stratégie qui donne un profit certain, sans risque de change. Toute la théorie du forward FX repose sur cette condition. 

# Domestic vs Foreign (règle absolument essentielle) 

Dans une paire FX BASE/QUOTE, on a : 

Foreign currency = BASE 
Domestic currency = QUOTE 

Exemples : 
EUR/USD → foreign = EUR, domestic = USD 
USD/JPY → foreign = USD, domestic = JPY 
GBP/CHF → foreign = GBP, domestic = CHF 

Donc : 
𝑟𝑑 = taux d’intérêt de la devise domestique 
𝑟𝑓 = taux d’intérêt de la devise étrangère 

Ça n’a rien à voir avec le pays où tu te trouves.
<img width="535" height="225" alt="Capture d’écran 2025-12-01 à 17 22 13" src="https://github.com/user-attachments/assets/b38787ba-87e4-44ea-aba3-c0c6fae8a3f1" /> 

# Stratégie A (synthetic forward) 

Données : 

- Paire : EUR/USD Spot = 1.10 USD pour 1 EUR 
- rd (USD) = 5 % 
- rf (EUR) = 2 % 
- Maturité = 1 an 
- Montant = 100 000 EUR 

# Objectif de la stratégie A : 

Créer artificiellement un “achat de 100 000 EUR forward”, sans utiliser de forward officiel. 

On veut copier le payoff du forward, mais à partir d’opérations cash + money market. 

Si le forward officiel est mal pricé → arbitrage gratuit. 

# Étape 1 — Emprunter en devise domestique 

Tu veux acheter 100 000 EUR aujourd’hui. Spot = 1.10 
→ tu as besoin de : 100 000 × 1.10 = 110 000 USD 

Donc tu empruntes 110 000 USD pendant 1 an au taux rd = 5 %. 

Montant remboursé dans 1 an : <img width="293" height="55" alt="Capture d’écran 2025-12-03 à 14 26 35" src="https://github.com/user-attachments/assets/854f9083-ba4d-4985-b722-0211f69410c0" /> 

# Étape 2 — Acheter 100 000 EUR avec les USD empruntés 

Avec 110 000 USD, tu achètes : 110 000 / 1.10 = 100 000 EUR 
Tu possèdes maintenant : 100 000 EUR 
Dans 1 an, tu dois rembourser : 115 657 USD (emprunt domestique) 

# Étape 3 — Placer ces 100 000 EUR au taux EUR = 2 % 

Dans 1 an, ton placement vaut : <img width="293" height="55" alt="Capture d’écran 2025-12-03 à 14 28 12" src="https://github.com/user-attachments/assets/85dbab85-e1fe-4044-b111-bb7aaa4ff4bd" /> 

# Étape 4 — Vendre ces 102 020 EUR à terme via un forward 

Tu signes un forward (prix = F) : 

➡ Tu vendras 102 020 EUR dans 1 an 
➡ Tu recevras 102 020 × F USD 

Donc, le montant que tu recevras dans un an en USD est : USD reçus = 102 020⋅𝐹 

Payoff final de la stratégie A (dans 1 an) Tu reçois : 102 020 ⋅F USD 
Tu payes : 115 657 USD (remboursement de l’emprunt USD) 
Donc : Payoff A = 102 020.F − 115 657 

Tout est en USD, car USD = devise domestique. 

# Stratégie B — Achat direct de 100 000 EUR forward 

Stratégie “pure” : Aucun cash aujourd’hui 

Dans 1 an, tu paies F USD pour 1 EUR Donc pour 100 000 EUR → tu paieras 100 000 × F USD 

Payoff net = 0 (juste un engagement). 

# Condition d’absence d’arbitrage 

Les deux stratégies doivent donner le même payoff dans un an, donc : 102 020.F −115 657 = 0 

On isole F : 𝐹 = 115 657 / 102 020 = 1.134 

# Vérification avec la formule théorique 
<img width="341" height="88" alt="Capture d’écran 2025-12-03 à 14 34 42" src="https://github.com/user-attachments/assets/c09d371a-dc21-474e-8281-cb22f9ec7c46" /> 

# Le forward EUR/USD dépend du différentiel de taux USD–EUR 

# Si les taux USD montent (rd ↑) 

Le terme (rd − rf) augmente, donc : 𝐹 ↑ 

Le forward EUR/USD devient plus élevé, tu paies plus de USD pour acheter 1 EUR dans le futur. 

Intuition : Emprunter en USD devient plus cher → la stratégie synthétique devient plus coûteuse → le forward doit monter pour éviter l’arbitrage. 

# Si les taux USD baissent (rd ↓) 

(rd − rf) diminue, donc : 𝐹 ↓ 

Le forward EUR/USD baisse, acheter des EUR dans le futur devient moins coûteux. 

# Si les taux EUR montent (rf ↑) 

(rd − rf) diminue, donc : 𝐹 ↓ diminue, donc : Le forward EUR/USD baisse. 

Intuition : Détenir des euros rapporte plus (rf ↑), donc il devient moins cher d’acheter des euros aujourd’hui et de les placer : le forward doit baisser pour neutraliser cet avantage. 

# Si les taux EUR baissent (rf ↓) 
(rd − rf) augmente, donc : 𝐹 ↑ Le forward EUR/USD monte.

# CONVERSION DELTA -> STRIKE


delta = 0.25
a = -1 * st.norm.ppf(delta * (1 / rf_discFact))  # d1 associé au delta FX

def d_1(F, X, vol, t):
    return (math.log(F / X) + 0.5 * vol**2 * t) / (vol * math.sqrt(t))

def d_2(F, X, vol, t):
    return d_1(F, X, vol, t) - vol * math.sqrt(t)

X_3 = np.array([])  # CALL 25D
X_1 = np.array([])  # PUT 25D
X_2 = np.array([])  # ATM

for x in range(len(T)):

    # PUT 25D
    X_25D_PUT = F[x] * math.exp(
        -(a[x] * Vol_25D_PUT[x] * math.sqrt(T[x])) +
        0.5 * Vol_25D_PUT[x]**2 * T[x]
    )
    X_1 = np.append(X_1, X_25D_PUT)

    # ATM
    X_ATM = F[x] * math.exp(0.5 * Vol_ATM[x]**2 * T[x])
    X_2 = np.append(X_2, X_ATM)

    # CALL 25D
    X_25D_CALL = F[x] * math.exp(
        +(a[x] * Vol_25D_CALL[x] * math.sqrt(T[x])) +
        0.5 * Vol_25D_CALL[x]**2 * T[x]
    )
    X_3 = np.append(X_3, X_25D_CALL)

# Contexte : 

En FX, un 25Δ Put signifie :

Le marché te dit par exemple :

“Put 25 Delta = 12.5% de volatilité”

Mais il NE te donne PAS le strike du put 25Δ.

Donc on doit retrouver d1, puis retrouver K.

En FX, la formule du delta d’un CALL européen est :

<img width="467" height="135" alt="Capture d’écran 2025-12-03 à 17 36 59" src="https://github.com/user-attachments/assets/31d66e87-b78f-473b-9544-57f6a6ea89b7" />

--<img width="585" height="492" alt="Capture d’écran 2025-12-03 à 17 37 52" src="https://github.com/user-attachments/assets/73d49275-d035-40a6-976c-2390234b3ed9" />

def d_1(F, X, vol, t):
    return (math.log(F / X) + 0.5 * vol**2 * t) / (vol * math.sqrt(t))

def d_2(F, X, vol, t):
    return d_1(F, X, vol, t) - vol * math.sqrt(t)
    
<img width="585" height="440" alt="Capture d’écran 2025-12-03 à 17 43 11" src="https://github.com/user-attachments/assets/a9ad85db-ed66-43b5-8c2c-5e75c5f05ce8" />


À chaque itération x, tu travailles avec une maturité T[x] et :

- un forward F[x]
- une vol 25D put Vol_25D_PUT[x]
- une vol ATM Vol_ATM[x]
- une vol 25D call Vol_25D_CALL[x]
- le a[x] associé à 25Δ via la formule delta → d1

Et tu reconstruis les trois strikes correspondants.
- X_3 = np.array([])  # CALL 25D
- X_1 = np.array([])  # PUT 25D
- X_2 = np.array([])  # ATM

<img width="585" height="158" alt="Capture d’écran 2025-12-03 à 17 44 02" src="https://github.com/user-attachments/assets/fdc43f5a-6200-4eaf-8d93-0a63c8982a61" />

for x in range(len(T)):

    PUT 25D
    X_25D_PUT = F[x] * math.exp(
        -(a[x] * Vol_25D_PUT[x] * math.sqrt(T[x])) +
        0.5 * Vol_25D_PUT[x]**2 * T[x]
    )
    X_1 = np.append(X_1, X_25D_PUT)

    # ATM
    X_ATM = F[x] * math.exp(0.5 * Vol_ATM[x]**2 * T[x])
    X_2 = np.append(X_2, X_ATM)

    # CALL 25D
    X_25D_CALL = F[x] * math.exp(
        +(a[x] * Vol_25D_CALL[x] * math.sqrt(T[x])) +
        0.5 * Vol_25D_CALL[x]**2 * T[x]
    )
    X_3 = np.append(X_3, X_25D_CALL)

Ces trois points (K_put25,σ_put25),(K_atm,σ_atm),(K_call25 ,σ_call25) sont ensuite utilisés par Vanna-Volga pour :

- reconstruire la volatilité à n’importe quel strike entre les deux ailes
- capturer le skew (déséquilibre put/call)
- capturer la convexité (butterfly)

C’est la base de la reconstitution de ton smile FX.

# METHODE VANNA-VOLGA

def VolSurface(F, X, t, X_1, X_2, X_3, sig_PUT, sig_ATM, sig_CALL):

    # Poids log-métriques (structure du smile)
    z1 = (math.log(X_2 / X) * math.log(X_3 / X)) / \
         (math.log(X_2 / X_1) * math.log(X_3 / X_1))

    z2 = (math.log(X / X_1) * math.log(X_3 / X)) / \
         (math.log(X_2 / X_1) * math.log(X_3 / X_2))

    z3 = (math.log(X / X_1) * math.log(X / X_2)) / \
         (math.log(X_3 / X_1) * math.log(X_3 / X_2))

    First_Ord_Approx = (
        z1 * sig_PUT + z2 * sig_ATM + z3 * sig_CALL
    ) - sig_ATM

    Second_Ord_Approx = (
        z1 * d_1(F, X_1, sig_PUT, t) * d_2(F, X_1, sig_PUT, t) * (sig_PUT - sig_ATM)**2 +
        z3 * d_1(F, X_3, sig_CALL, t) * d_2(F, X_3, sig_CALL, t) * (sig_CALL - sig_ATM)**2
    )

    d1_d2 = d_1(F, X, sig_ATM, t) * d_2(F, X, sig_ATM, t)

    vol = sig_ATM + (
        -sig_ATM + math.sqrt(
            sig_ATM**2 + d1_d2 * (2 * sig_ATM * First_Ord_Approx +
                                 Second_Ord_Approx)
        )
    ) / d1_d2

    return vol


L’interpolation “Vanna-Volga” utilisée en construction de smile FX repose sur deux blocs complémentaires :

un terme de premier ordre, qui reproduit la pente (skew) du smile

un terme de second ordre, qui injecte la courbure (convexité) réelle que l’on observe dans les ailes FX.

Les deux blocs utilisent comme base les trois points liquides du marché FX :

- Put 25Δ → (K1,σ1)
- ATM → (K2,σ2)
- Call 25Δ → (K3,σ3)

et permettent d’estimer une volatilité implicite pour n’importe quel strike 𝐾.

# 1) LES POIDS LOG-MÉTRIQUES

<img width="277" height="200" alt="Capture d’écran 2025-12-03 à 18 02 46" src="https://github.com/user-attachments/assets/8294d0f5-9ad4-4d2d-b614-dab6060951ad" />

Les poids log-métriques disent simplement :

“À quel point ton strike K ressemble plus à Put25, à l’ATM ou au Call25.”
C’est juste une manière de mesurer la position de K dans le smile.

# Le premier ordre reproduit la pente du skew du marché autour de l'ATM
<img width="469" height="107" alt="Capture d’écran 2025-12-03 à 18 05 18" src="https://github.com/user-attachments/assets/6c7e5d83-3074-4f9f-8b92-153234314561" />

Tu combines les trois vols du marché pour reproduire la variation du smile,
puis tu retires la vol ATM pour recentrer l’interpolation sur l’ATM et garantir que l’ATM reste l’ancre du smile et que le premier ordre représente uniquement la pente.

# Le second ordre = LA COURBURE DU SMILE

Le second ordre sert à reproduire la convexité du smile FX (le BF).

En FX, le smile n’est jamais linéaire :

- Le Put 25Δ est souvent très au-dessus de l’ATM → skew
- Le Call 25Δ est parfois moins cher → skew

Mais même quand le skew est faible, la convexité est toujours présente.

Si tu n’ajoutes pas ce second-terme → ton smile est petit et plat.

<img width="646" height="84" alt="Capture d’écran 2025-12-03 à 18 09 42" src="https://github.com/user-attachments/assets/6f090646-f6cc-410e-8f19-56d69b851fbb" />

1) Le carré (𝜎𝑖 − 𝜎2)^2 :

mesure la force du skew entre l’aile (Put25 ou Call25) et l’ATM

- si Put25 ou Call25 sont très éloignés de l’ATM → skew fort → courbure forte
- si les vols sont proches → skew faible → smile plat

Le carré amplifie cet effet :
plus le skew est important, plus le smile doit “bomber”.

2) Le terme d1(Ki).d2(Ki) :

C’est un amplificateur de la courbure et la profondeur d’aile :

- 👉 d1 = où ton strike se situe par rapport au forward, mesuré en “écarts de vol”
- 👉 d2 = la même chose mais ajusté par la vol

En pratique :

- près de l’ATM → d1 et d2 sont petits
- loin de l’ATM (profond OTM) → d1 et d2 deviennent très grands en valeur absolue

Donc : d1 et d2 mesurent la profondeur d’aile.

- près de l’ATM → d1·d2 est petit → courbure faible
- dans les ailes profondes → d1·d2 devient très grand → courbure forte

3) Pourquoi seulement 𝑧1 et 𝑧3 ?

Parce que la courbure (butterfly) vient des ailes, pas de l’ATM :

- l’ATM fixe le niveau
- les ailes (K1 et K3) fixent la convexité du smile

Donc le second ordre ne fait intervenir que les points 25Δ.

➤ Vision marché

Le second ordre sert à reproduire le bombage réel du smile FX :

- correction plus forte dans les ailes
- courbure amplifiée lorsque Put25/Call25 sont loin de l’ATM
- smile non linéaire, forme “U” ou “smirkée” réaliste

# La formule finale

<img width="830" height="84" alt="Capture d’écran 2025-12-03 à 18 23 50" src="https://github.com/user-attachments/assets/f5ec5f3b-a20b-4887-be58-688efa5bae89" />

La formule complète dit :

On part du niveau ATM, et on ajoute une correction contrôlée par :

- la pente (first order),
- la convexité (second order),
- et amplifie ça en fonction de la profondeur d’aile (d1·d2).
Le tout sous racine pour rester positif.

Ce qui donne un smile :

- incliné si RR ≠ 0
- bombé si BF ≠ 0
- plus extrême dans les ailes
- stable et sans vol négative
- cohérent avec Put25, ATM, Call25
