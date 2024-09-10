import requests

access_token = "Atza|IwEBILf-9jZIjyV_smYGrwDxc1_GnpZlvMNy3FfxBgvOy70pLKP8W0qtcn4f07BDh5eUaSonbUSoOTEsWwItWgy13jeytNVaU7_0ZnTVL1Sd0LW3vPFAomyQtznD6y-51d-XFkq5LuqJsNCeuO1JDfl-awMX4bYQo_jLPpB_C5HmOmhZSNwLck-KwgS7fSYCzfF9Df2OclPa1z16IOXhW52gpsdyYHZ_90SK35qp_ZHDZm9DZJPKN66HGbbwYwasFMINA9JR66792VfpdfRZ9uNAa8-Kfy-FT8fNwE6Lo3vmYShTpfsiv9WRkhYUUibe70tU3DxgNzXOqiTr-ppNr4p9F7GamktUlsm9TtkbSYU5WbxeyhhxjIS_D2c7K2Vh35t892Un38a4OcfZwup7OKF46IM3"
refresh_token = "Atzr|IwEBIGCosn2DFu1u3WYB83Uac6LA9zh4j8Cjo0RwGFMWnoaoP6z86ER6XTBOlOLK_yyI6OBKnTKKSsoP2Xk7AuihZNNqkkcOVdN4dDpYvu-OIHN_fA7zjzY0kTro-VtHI09H402TG9HDGIJ6yPhIijmM6yi2jtzdKAVev0_mEqAt1Q7pU9R_o7GzOLI4N7vE-w-X6cHkeXF-jdcSzWJB1x4btypdGegzawk8FFd4kUWc94aXGgJJOR5wl5r5iafES_r54jMsvpONl0zg2Ee1aD-x5blq07h-eASZGDMEaa4gdfYxvGT2YHjYeMed4pLH3x3aUfYQCh9FZYB5laUcCn-l-8bgzP4bPWcfba442w-3P4MJxC901np5wM8sQ4V3T1LwdkPoI8N6LZdXQFcMt02nq5Nw"
expires_in = 3600

client_id = "Amazon client id"
client_secret = (
    "Amazon client secret"
)
url = "https://api.amazon.com/auth/o2/token"
grant_type = "refresh_token"
data = {
    "grant_type": grant_type,
    "refresh_token": refresh_token,
    "client_id": client_id,
    "client_secret": client_secret,
}
headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "charset": "UTF-8",
}
response = requests.post(url, data=data, headers=headers)

access_token = response.json().get("access_token")
refresh_token_1 = response.json().get("refresh_token")
expires_in = response.json().get("expires_in")

print(refresh_token == refresh_token_1)  # True

print(access_token)
print(refresh_token)
print(expires_in)
