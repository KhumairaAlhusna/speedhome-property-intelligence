import pandas as pd
from io import BytesIO


def dataframe_to_csv(df):
    """
    Convert DataFrame menjadi CSV bytes
    """

    return df.to_csv(
        index=False
    ).encode("utf-8")


def dataframe_to_excel(df):
    """
    Convert DataFrame menjadi Excel bytes
    """

    output = BytesIO()

    with pd.ExcelWriter(
        output,
        engine="openpyxl"
    ) as writer:

        df.to_excel(
            writer,
            index=False,
            sheet_name="Properties"
        )

    output.seek(0)

    return output.getvalue()


def create_summary_table(stats):

    summary = pd.DataFrame({

        "Metric": [

            "Total Properties",

            "Average Price",

            "Median Price",

            "Mode Price",

            "Minimum Price",

            "Maximum Price",

            "Standard Deviation",

            "Q1",

            "Q3",

            "IQR",

            "Fair Price"

        ],

        "Value": [

            stats["count"],

            round(stats["average"], 2),

            round(stats["median"], 2),

            stats["mode"],

            stats["minimum"],

            stats["maximum"],

            round(stats["std"], 2),

            round(stats["q1"], 2),

            round(stats["q3"], 2),

            round(stats["iqr"], 2),

            round(stats["fair_price"], 2)

        ]

    })

    return summary