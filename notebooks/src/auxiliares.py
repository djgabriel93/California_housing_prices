import pandas as pd


def dataframe_coeficientes(coefs, colunas):
    coefs=coefs.ravel()
    return pd.DataFrame(data=coefs, index=colunas, columns=["coeficiente"]).sort_values(
        by="coeficiente"
    )
