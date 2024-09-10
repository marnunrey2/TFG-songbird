import requests

access_token = "Atza|IwEBIJCwa7wG0u-DHljtM983PeWnE1XWzkk0b8V_7frwyP4KRcy84XZ_UxcXfk92JwBd_N0ny3Cw7cW_Qj-Enq-PyUodWhLCQQB0xfiwP40waClpdEXVKPGvtb1m2v0MfUK8f8TuehNivfG-47bKYoUqp5_Gq_2GMXOjpMP7cmdA2LPGaPs3ovkYrso7YGrausSuwsH5_EcMmnCwMkn4siW108buA2g17jHara_uLo5zkqDuKDMf7gHwRrODTfJ7JcpPZarGY9plfV289gKMV2WWgQniwnGT6Fv2MF2jX8IUIDB5M9flnXAEQdBIHZsBOWotfhPRbUHgJRQ8iLbdNSUX_7Eur1eLxZH9LrfoMtgCkAPnM8y7XLsbWsAqJcSr7xrvL5sydZqct0-Zpa7IdgE0KNFQ"
refresh_token = "Atzr|IwEBILsDzMHZh6r486SEHkwne5lGTTA_mbk2V0qNSmN7-0JqAW5291jDnRpyyQpVop41dDeCg1ssaoJTSPmQzGJXLcHGocDiTYaIKdsNWB4C8SFh-CU8UTn4eiFTKttUsBAT8LbFZ5J0Cj6cM6gr1TPrA4ljjZXgyQ8DKjDDLkNL5qYoXlGyPH2RClRjEx5i1h0HhVteg90LVMRBgAojvOcEPd4uGJ_PLqQoeG84h_s3WPCdtbn0OxqmGL6IWMtqiHkVllFMSZBT3tXYaJHqSGDZy6YoMyukOoh3kSHbFu0W0mGAJDWayOeprtzAbd1_9UVHzbAVDVXdngOQ2xJGwx3wY6LrOrUqT3xc-oJsINc_bBo5YOUVj-OfgkswdnC4gmXatcDLEkRBwzBw2MxCjosthvZx"
expires_in = 3600
client_id = "Amazon client id"
client_secret = (
    "Amazon client secret"
)
profile_id = "Amazon profile id"

url = "https://api.music.amazon.dev/v1/artists/B00E5UGNYI"

headers = {
    "Authorization": f"Bearer {access_token}",
    "x-api-key": profile_id,
    "Content-Type": "application/json",
}

response = requests.get(url, headers=headers)
print(response.json())
