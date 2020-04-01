"""Xonsh activate script for virtualenv"""
from xonsh.tools import get_sep as _get_sep

def _deactivate(args):
    if "pydoc" in aliases:
        del aliases["pydoc"]

    if ${...}.get("_OLD_VIRTUAL_PATH", ""):
        $PATH = $_OLD_VIRTUAL_PATH
        del $_OLD_VIRTUAL_PATH

    if ${...}.get("_OLD_VIRTUAL_PYTHONHOME", ""):
        $PYTHONHOME = $_OLD_VIRTUAL_PYTHONHOME
        del $_OLD_VIRTUAL_PYTHONHOME

    if "VIRTUAL_ENV" in ${...}:
        del $VIRTUAL_ENV

    if "VIRTUAL_ENV_PROMPT" in ${...}:
        del $VIRTUAL_ENV_PROMPT

    if "nondestructive" not in args:
        # Self destruct!
        del aliases["deactivate"]


# unset irrelevant variables
_deactivate(["nondestructive"])
aliases["deactivate"] = _deactivate

<<<<<<< HEAD
$VIRTUAL_ENV = r"/home/alexandre/GITHUB/Stay."
=======
$VIRTUAL_ENV = r"/home/cyriluri/Epitech/IONIS_FINISHER/Rester-Chez-Soi"
>>>>>>> 8f4415657912c1b7682b6ed62feed65b2a93dc4b

$_OLD_VIRTUAL_PATH = $PATH
$PATH = $PATH[:]
$PATH.add($VIRTUAL_ENV + _get_sep() + "bin", front=True, replace=True)

if ${...}.get("PYTHONHOME", ""):
    # unset PYTHONHOME if set
    $_OLD_VIRTUAL_PYTHONHOME = $PYTHONHOME
    del $PYTHONHOME

$VIRTUAL_ENV_PROMPT = ""
if not $VIRTUAL_ENV_PROMPT:
    del $VIRTUAL_ENV_PROMPT

aliases["pydoc"] = ["python", "-m", "pydoc"]
