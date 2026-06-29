import pandas as pd
import re


def clean_price(price):
    """
    Mengubah 'RM 1,300 / month' menjadi 1300
    """

    if pd.isna(price):
        return None

    numbers = re.sub(r"[^\d]", "", str(price))

    if numbers == "":
        return None

    return int(numbers)


def clean_size(size):
    """
    Mengubah '850 sq.ft' menjadi 850
    """

    if pd.isna(size):
        return None

    numbers = re.sub(r"[^\d]", "", str(size))

    if numbers == "":
        return None

    return int(numbers)


def calculate_statistics(df):
    """
    Menghitung statistik harga properti
    """

    df = df.copy()

    # Price
    df["Price_Num"] = df["Price"].apply(clean_price)

    # Size
    df["Size_Num"] = df["Size"].apply(clean_size)

    # Hapus harga kosong
    df = df.dropna(subset=["Price_Num"])

    average = df["Price_Num"].mean()
    median = df["Price_Num"].median()

    mode_series = df["Price_Num"].mode()

    if len(mode_series) > 0:
        mode = mode_series.iloc[0]
    else:
        mode = None

    minimum = df["Price_Num"].min()

    maximum = df["Price_Num"].max()

    std = df["Price_Num"].std()

    q1 = df["Price_Num"].quantile(0.25)

    q3 = df["Price_Num"].quantile(0.75)

    iqr = q3 - q1

    fair_price = median

    return {

        "average": average,

        "median": median,

        "mode": mode,

        "minimum": minimum,

        "maximum": maximum,

        "std": std,

        "q1": q1,

        "q3": q3,

        "iqr": iqr,

        "fair_price": fair_price,

        "count": len(df),

        "data": df

    }