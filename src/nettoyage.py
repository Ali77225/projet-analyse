import pandas as pd


def nettoyer(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """Nettoie Online Retail et renvoie (df propre, journal chiffré)."""
    df = df.copy()
    journal = {"lignes_initiales": len(df)}

    # 1. Doublons exacts
    n = len(df)
    df = df.drop_duplicates()
    journal["doublons_supprimes"] = n - len(df)

    # 2. Annulations (factures commençant par « C »)
    n = len(df)
    df = df[~df["InvoiceNo"].astype(str).str.startswith("C")]
    journal["annulations_supprimees"] = n - len(df)

    # 3. Quantités ou prix <= 0
    n = len(df)
    df = df[(df["Quantity"] > 0) & (df["UnitPrice"] > 0)]
    journal["quantite_prix_invalides"] = n - len(df)

    # 4. Dates : conversion, puis suppression des dates invalides
    n = len(df)
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], errors="coerce")
    df = df.dropna(subset=["InvoiceDate"])
    journal["dates_invalides"] = n - len(df)

    # 5. Texte et types
    df["Description"] = df["Description"].str.strip()
    df["InvoiceNo"] = df["InvoiceNo"].astype(str)
    df["StockCode"] = df["StockCode"].astype(str)

    # 6. Colonne calculée
    df["CA"] = df["Quantity"] * df["UnitPrice"]

    journal["lignes_finales"] = len(df)
    return df, journal


def charger(chemin: str) -> pd.DataFrame:
    """Charge le CSV avec les bons types, sans aucun nettoyage."""
    return pd.read_csv(chemin,
                       dtype={"InvoiceNo": str, "StockCode": str},
                       parse_dates=["InvoiceDate"])