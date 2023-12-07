# upload.py
import os

from joringels.src.joringels import Joringel
import joringels.src.settings as sts
import joringels.src.helpers as helpers

# run like: joringels chkey -n safe_one [-k "C:\Users\Lars\OneDrive\Dokumente\50 sonstiges\aktuell_2021.kdbx"]


def run(action: str, *args, **kwargs) -> None:
    """
    imports secrets from source and saves it into .ssp folder
    NOTE: NON-DIGESTIVE, encrypted secretsFile remains in .ssp
    NOTE: this is only allowed on a local host computer

    run like: joringels load -n safe_one -src kdbx
    """
    # change key
    Joringel(*args, **kwargs).chkey(*args, **kwargs)
    return True


def main(*args, **kwargs) -> None:
    """
    imports source and connector from src and con argument
    then runs load process using imported source an connector
    """
    return run(*args, **kwargs)
