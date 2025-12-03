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
a = -1 * st.norm.ppf(delta * (1 / rf_discFact))  

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
