#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  1 14:01:04 2025

@author: yassinelaabi
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as st
from mpl_toolkits import mplot3d
import math
import matplotlib as mpt

# -----------------------------------------------------------
# 1) TENORS DE MARCHÉ (EXPRIMÉS EN ANNÉES)
# -----------------------------------------------------------

T = np.array([0.0194,0.04166,0.0833,0.1666,0.25,0.3333,0.4166,0.5,
              0.75,1,1.25,1.5,2,3,4,5])

# -----------------------------------------------------------
# 2) VOLATILITÉS DE MARCHÉ (POINTS LIQUIDES)
# -----------------------------------------------------------

Vol_25D_PUT = np.array([0.121,0.1215,0.1105,0.113,0.1224,0.1236,0.125,0.116,
                        0.1175,0.1322,0.136,0.14,0.1411,0.1433,0.1445,0.145])

Vol_25D_CALL = np.array([0.1205,0.12,0.115,0.109,0.1125,0.121,0.119,0.108,
                         0.116,0.1275,0.131,0.133,0.1388,0.14,0.1405,0.139])

Vol_ATM = np.array([0.118,0.1182,0.1015,0.1029,0.115,0.116,0.118,0.105,
                    0.108,0.121,0.124,0.132,0.135,0.1375,0.14,0.141])

# -----------------------------------------------------------
# 3) TAUX D’INTÉRÊT DOMESTIQUE (rd) ET FOREIGN (rf)
# -----------------------------------------------------------

rd_input = np.array([0.005,0.0052,0.0059,0.006,0.0063,0.0069,0.007,0.0072,
                     0.0075,0.0077,0.008,0.0085,0.009,0.00925,0.0095,0.0098])

rf_input = np.array([0.0043,0.004,0.005,0.0055,0.0068,0.0071,0.0066,0.0078,
                     0.0085,0.0083,0.0088,0.0079,0.0082,0.0087,0.0093,0.0095])

# Discount factors
rd_discFact = np.exp(-1 * rd_input * T)
rf_discFact = np.exp(-1 * rf_input * T)

# q = rd - rf (drift FX)
q = rd_discFact - rf_discFact

# -----------------------------------------------------------
# 4) CALCUL DU FORWARD FX
# -----------------------------------------------------------

S = 1.5
F = S * np.exp(q * T)

# -----------------------------------------------------------
# 5) CONVERSION DELTA -> STRIKE
# -----------------------------------------------------------

delta = 0.25
a = -1 * st.norm.ppf(delta * (1 / rf_discFact))  # d1 associé au delta FX

# -----------------------------------------------------------
# 6) d1 ET d2 BLACK-SCHOLES (FX)
# -----------------------------------------------------------

def d_1(F, X, vol, t):
    return (math.log(F / X) + 0.5 * vol**2 * t) / (vol * math.sqrt(t))

def d_2(F, X, vol, t):
    return d_1(F, X, vol, t) - vol * math.sqrt(t)

# -----------------------------------------------------------
# 7) CALCUL DES STRIKES 25D PUT / ATM / 25D CALL
# -----------------------------------------------------------

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

# -----------------------------------------------------------
# 8) METHODE VANNA-VOLGA
# -----------------------------------------------------------

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

# -----------------------------------------------------------
# 9) CONSTRUCTION DE LA SURFACE : STRIKE × TENOR
# -----------------------------------------------------------

opt_strike = (1 + np.arange(-0.15, 0.16, 0.01)) * S
vanna_volga_implied = np.zeros((31, 16), dtype=float)

for i in range(31):
    for j in range(16):
        vanna_volga_implied[i, j] = VolSurface(
            F[j],
            opt_strike[i],
            T[j],
            X_1[j],
            X_2[j],
            X_3[j],
            Vol_25D_PUT[j],
            Vol_ATM[j],
            Vol_25D_CALL[j]
        )

# Sauvegarde CSV
df = pd.DataFrame(vanna_volga_implied)
df.to_csv("ameya.csv", index=False)

# -----------------------------------------------------------
# 10) VISUALISATION AMÉLIORÉE (COULEURS + ANNOTATIONS)
# -----------------------------------------------------------

x_axis = T
y_axis = opt_strike
x_axis, y_axis = np.meshgrid(x_axis, y_axis)
z_axis = df.values

fig = plt.figure(figsize=(14, 9))
ax = fig.add_subplot(projection="3d")

vol_surface = ax.plot_surface(
    x_axis, y_axis, z_axis,
    cmap="viridis",
    linewidth=0,
    antialiased=True,
    alpha=0.95
)

fig.colorbar(vol_surface, shrink=0.5, aspect=10, label="Volatilité (%)")

ax.set_title("Surface de Volatilité FX – Méthode Vanna-Volga", fontsize=16, pad=20)
ax.set_xlabel("Maturité (années)", fontsize=12)
ax.set_ylabel("Strike", fontsize=12)
ax.set_zlabel("Volatilité implicite", fontsize=12)

ax.view_init(elev=25, azim=235)

ax.text(
    T[5], opt_strike[15], z_axis[15, 5],
    "Exemple\n(T, K)",
    color="white"
)

plt.show()
