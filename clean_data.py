"""Taller evaluable presencial"""

import pandas as pd
from pandas import DataFrame


def load_data(input_file) -> DataFrame:
    """Lea el archivo usando pandas y devuelva un DataFrame"""

    #
    # Esta parte es igual al taller anterior
    #
    df: DataFrame = pd.read_csv(input_file)
    return df


def create_key(df: DataFrame, n: int) -> DataFrame:
    """Cree una nueva columna en el DataFrame que contenga el key de la columna 'text'"""

    df = df.copy()
    df["key"] = df["text"]
    df["key"] = df["key"].str.strip()
    df["key"] = df["key"].str.lower()
    df["key"] = df["key"].str.replace(r"[^A-Za-z0-9\s]", "", regex=True)
    df["key"] = df["key"].str.split()

    # ------------------------------------------------------
    # Esta es la parte especifica del algoritmo de n-gram:
    #
    # - Una el texto sin espacios en blanco
    df["key"] = df["key"].str.join("")
    #
    # - Convierta el texto a una lista de n-gramas
    df["key"] = df["key"].apply(lambda x: [x[i : i + n - 1] for i in range(len(x))])
    #
    # - Ordene la lista de n-gramas y remueve duplicados
    df["key"] = df["key"].apply(lambda x: sorted(list(set(x))))
    #
    # - Convierta la lista de ngramas a una cadena
    df["key"] = df["key"].str.join("")
    ## ------------------------------------------------------

    return df


def generate_cleaned_column(df: DataFrame) -> DataFrame:
    """Crea la columna 'cleaned' en el DataFrame"""

    #
    # Este código es identico al anteior
    #
    df = df.copy()
    df = df.sort_values(by=["key", "text"], ascending=[True, True])
    keys: DataFrame = df.drop_duplicates(subset="key", keep="first")
    key_dict: dict[str, str] = dict(zip(keys["key"], keys["text"]))
    df["cleaned"] = df["key"].map(key_dict)

    return df


def save_data(df: DataFrame, output_file: str) -> None:
    """Guarda el DataFrame en un archivo"""
    #
    # Este código es identico al anteior
    #
    df = df.copy()
    df = df[["cleaned"]]
    df = df.rename(columns={"cleaned": "text"})
    df.to_csv(output_file, index=False)


def main(input_file: str, output_file: str, n: int = 2) -> None:
    """Ejecuta la limpieza de datos"""
    #
    # Este código es identico al anteior
    #
    df: DataFrame = load_data(input_file)
    df = create_key(df, n)
    df = generate_cleaned_column(df)
    df.to_csv("test.csv", index=False)
    save_data(df, output_file)


if __name__ == "__main__":
    main(
        input_file="input.txt",
        output_file="output.txt",
    )
