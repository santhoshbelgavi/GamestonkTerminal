import df2img
import pandas as pd

import bots.config_discordbot as cfg
from bots.config_discordbot import logger
from bots.helpers import save_image
from gamestonk_terminal.economy import finviz_model


def grains_command():
    """Displays grains futures data [Finviz]"""

    # Debug user input
    if cfg.DEBUG:
        logger.debug("econ-grains")

    # Retrieve data
    d_futures = finviz_model.get_futures()
    df = pd.DataFrame(d_futures["Grains"])

    # Check for argument
    if df.empty:
        raise Exception("No available data found")

    formats = {"last": "${:.2f}", "prevClose": "${:.2f}"}
    for col, value in formats.items():
        df[col] = df[col].map(lambda x: value.format(x))  # pylint: disable=W0640

    df = df.fillna("")
    df = df.set_index("label")
    df = df.sort_values(by="ticker", ascending=False)

    # Debug user output
    if cfg.DEBUG:
        logger.debug(df)

    df = df[
        [
            "prevClose",
            "last",
            "change",
        ]
    ]
    df.index.names = [""]
    df = df.rename(
        columns={"prevClose": "PrevClose", "last": "Last", "change": "Change"}
    )
    dindex = len(df.index)
    fig = df2img.plot_dataframe(
        df,
        fig_size=(800, (40 + (40 * dindex))),
        col_width=[6, 3, 3],
        tbl_cells=dict(
            align="left",
            height=35,
        ),
        template="plotly_dark",
        font=dict(
            family="Consolas",
            size=20,
        ),
        paper_bgcolor="rgba(0, 0, 0, 0)",
    )

    imagefile = save_image("econ-grains.png", fig)

    return {
        "title": "Economy: [Finviz] Grains Futures",
        "imagefile": imagefile,
    }
