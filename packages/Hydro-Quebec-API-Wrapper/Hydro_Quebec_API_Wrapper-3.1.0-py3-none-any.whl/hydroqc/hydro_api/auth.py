"""Generate PKCE-compliant code verifier and code challenge."""

# Implement an HTTP call with the following details and capture the session cookie.
#
# GET https://connexion.solutions.hydroquebec.com/32bf9b91-0a36-4385-b231-d9a8fa3b05ab/
# b2c_1a_prd_signup_signin/oauth2/v2.0/authorize
#
# with the following query parameters
# redirect_uri:          msauth.com.hydroquebec.infos-pannes://auth
# client_id:             09b0ae72-6db8-4ecc-a1be-041b67afc1cd
# response_type:         code
# state:                 %7B%22redirectUrl%22:%22CONSO%22%7D
# scope:                 openid offline_access https://connexionhq.onmicrosoft.com/
# hq-clientele-mobile/Espace.Client
# prompt:                login
# ui_locales:            fr
# code_challenge:        VQhipatCIaStOosra0_550ztGC76U1ezBURCV9uKK1M
# code_challenge_method: S256
#
# and the following request http headers
# accept:           text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8

import base64
import hashlib
import secrets


def generate_code_verifier(length: int = 128) -> str:
    """Return a random PKCE-compliant code verifier.

    Parameters
    ----------
    length : int
        Code verifier length. Must verify `43 <= length <= 128`.

    Returns
    -------
    code_verifier : str
        Code verifier.

    Raises
    ------
    ValueError
        When `43 <= length <= 128` is not verified.
    """
    if not 43 <= length <= 128:
        msg = "Parameter `length` must verify `43 <= length <= 128`."
        raise ValueError(msg)
    code_verifier = secrets.token_urlsafe(96)[:length]
    return code_verifier


def generate_pkce_pair(code_verifier_length: int = 128) -> tuple[str, str]:
    """Return random PKCE-compliant code verifier and code challenge.

    Parameters
    ----------
    code_verifier_length : int
        Code verifier length. Must verify
        `43 <= code_verifier_length <= 128`.

    Returns
    -------
    code_verifier : str
    code_challenge : str

    Raises
    ------
    ValueError
        When `43 <= code_verifier_length <= 128` is not verified.
    """
    if not 43 <= code_verifier_length <= 128:
        msg = "Parameter `code_verifier_length` must verify "
        msg += "`43 <= code_verifier_length <= 128`."
        raise ValueError(msg)
    code_verifier = generate_code_verifier(code_verifier_length)
    code_challenge = get_code_challenge(code_verifier)
    return code_verifier, code_challenge


def get_code_challenge(code_verifier: str) -> str:
    """Return the PKCE-compliant code challenge for a given verifier.

    Parameters
    ----------
    code_verifier : str
        Code verifier. Must verify `43 <= len(code_verifier) <= 128`.

    Returns
    -------
    code_challenge : str
        Code challenge that corresponds to the input code verifier.

    Raises
    ------
    ValueError
        When `43 <= len(code_verifier) <= 128` is not verified.
    """
    if not 43 <= len(code_verifier) <= 128:
        msg = "Parameter `code_verifier` must verify "
        msg += "`43 <= len(code_verifier) <= 128`."
        raise ValueError(msg)
    hashed = hashlib.sha256(code_verifier.encode("ascii")).digest()
    encoded = base64.urlsafe_b64encode(hashed)
    code_challenge = encoded.decode("ascii")[:-1]
    return code_challenge
