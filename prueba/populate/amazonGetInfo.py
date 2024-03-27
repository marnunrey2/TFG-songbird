import requests

access_token = "Atza|IwEBIESSM8jZt3FKc5EzHVxGyh-4Sm1WbQTXvabJERNmr_Cp4uEQ-QdqHYfgFmFGHnaQy4BD-GD14iNxjgX3Cq51NkD82gmoP8lQZU1KPjvUBTv4AiPD4Gbie9KTtCIbSKr2OTcP3GtPoNSvlYQPOVN8djPCrZxx_532Sa7qnOz5vTG5mp8UQLbP48B84lwbJRUg00ya6Mfr5P5Pt2KORQTAhuynGd9aPtAB7SKXbT0E8at9pDQRLslmhEGks1_rU5YQdNwmQ9iipR9-k1HtGwo6BJ57B7ZhmnMD6X2t_HBNniODtYwQ6lhqniWkKeBzy2EVo5X7vyMmSk-9eA8p1bUVhM8iAN5589_RD9edEJ3zeLF3xzyghMji1e_Hks-QU8nGn65QkXa3TTNpwQdUN4T2rT9wuVv40YLnsXQd8eLDYs_D4w"
refresh_token = "Atzr|IwEBIGCosn2DFu1u3WYB83Uac6LA9zh4j8Cjo0RwGFMWnoaoP6z86ER6XTBOlOLK_yyI6OBKnTKKSsoP2Xk7AuihZNNqkkcOVdN4dDpYvu-OIHN_fA7zjzY0kTro-VtHI09H402TG9HDGIJ6yPhIijmM6yi2jtzdKAVev0_mEqAt1Q7pU9R_o7GzOLI4N7vE-w-X6cHkeXF-jdcSzWJB1x4btypdGegzawk8FFd4kUWc94aXGgJJOR5wl5r5iafES_r54jMsvpONl0zg2Ee1aD-x5blq07h-eASZGDMEaa4gdfYxvGT2YHjYeMed4pLH3x3aUfYQCh9FZYB5laUcCn-l-8bgzP4bPWcfba442w-3P4MJxC901np5wM8sQ4V3T1LwdkPoI8N6LZdXQFcMt02nq5Nw"
expires_in = 3600
client_id = "amzn1.application-oa2-client.7c0d83cb1c9d4f048bfa5e9b4f390806"
client_secret = (
    "amzn1.oa2-cs.v1.9287a294bb74d3afd078534e40484585d191601050eacaa08709598335ea5012"
)
profile_id = "amzn1.application.74322dfd69484a38a70aa2fad85c93da"

url = "https://api.music.amazon.dev/v1/artists/B00E5UGNYI"

headers = {
    "Authorization": f"Bearer {access_token}",
    "x-api-key": profile_id,
    "Content-Type": "application/json",
}

response = requests.get(url, headers=headers)
print(response.json())
