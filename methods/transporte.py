import numpy as np

def resolver_esquina_noroeste(oferta, demanda, costos):
    m, n = len(oferta), len(demanda)
    x = np.zeros((m, n))
    i = j = 0
    while i < m and j < n:
        min_val = min(oferta[i], demanda[j])
        x[i, j] = min_val
        oferta[i] -= min_val
        demanda[j] -= min_val
        if oferta[i] == 0:
            i += 1
        if demanda[j] == 0:
            j += 1
    return x.tolist()