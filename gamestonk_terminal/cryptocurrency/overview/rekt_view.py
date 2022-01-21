"""Rekt view"""
import os

from gamestonk_terminal.cryptocurrency.overview import rekt_model
from gamestonk_terminal.helper_funcs import (
    export_data,
    long_number_format,
    rich_table_from_df,
)
from gamestonk_terminal import feature_flags as gtff
from gamestonk_terminal.rich_config import console


def display_crypto_hacks(
    top: int, sortby: str, descend: bool, slug: str, export: str = ""
) -> None:
    """Display list of major crypto-related hacks. If slug is passed individual crypto hack is displayed instead of list of crypto hacks
    [Source: https://rekt.news]

    Parameters
    ----------
    slug: str
        Crypto hack slug to check (e.g., polynetwork-rekt)
    top: int
        Number of hacks to search
    sortby: str
        Key by which to sort data {Platform,Date,Amount [$],Audit,Slug,URL}
    descend: bool
        Flag to sort data descending
    export : str
        Export dataframe data to csv,json,xlsx file
    """
    if slug:
        text = rekt_model.get_crypto_hack(slug)
        if text:
            console.print(text)
        export_data(
            export,
            os.path.dirname(os.path.abspath(__file__)),
            "ch",
            text,
        )
    else:
        df = rekt_model.get_crypto_hacks()

        if df.empty:
            console.print("\nError in rekt request\n")
        else:
            if sortby in rekt_model.HACKS_COLUMNS:
                df = df.sort_values(by=sortby, ascending=descend)
            df["Amount [$]"] = df["Amount [$]"].apply(lambda x: long_number_format(x))
            df["Date"] = df["Date"].dt.date

            if gtff.USE_TABULATE_DF:
                rich_table_from_df(
                    df.head(top),
                    headers=list(df.columns),
                    floatfmt=".1f",
                    show_index=False,
                    title="Major Crypto Hacks",
                )
                console.print()
            else:
                console.print(df.to_string(index=False), "\n")

            export_data(
                export,
                os.path.dirname(os.path.abspath(__file__)),
                "ch",
                df,
            )
