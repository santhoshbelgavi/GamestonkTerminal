"""Yahoo Finance Mutual Fund Model"""
__docformat__ = "numpy"

import logging
from typing import Dict

import yfinance as yf

from gamestonk_terminal.decorators import log_start_end

logger = logging.getLogger(__name__)


@log_start_end(log=logger)
def get_information(fund: str) -> Dict:
    """Get fund information for fund symbol

    Parameters
    ----------
    fund : str
        Symbol of fund

    Returns
    -------
    dict
        Dictionary containing fund information
    """
    return yf.Ticker(fund).info
