import requests

access_token = "Atza|IwEBIEPOimrZncim8O1U8hSkD6cIQd0BQcRdPYXxNGX1xIB-ydDYSb1wyBHF_BECCWiWZA8mF_nSamb1udT0d4Y9PPOL7qzOpWx_LhfxxYIDgOxBowI7f8ZfZv_8616bMC6lVGqMedkzFB7adPnIWAaVRbUC-MgXAwZ1gvBbjQAHVK0fJIJHnXe_NZz4OaG41mMGtxkRl9oDOwwNwFlA8vCXwHCIr2ujDUXZkK2ko5RRSwHObD6ti07G9NLtDtxgIEc6SmcPtqdRun5Y9hajoOPsrbMhCmwaAz99clXqqOaLJ9SlFBhhuW94AFKBhZzPwbxMIXfdIP8tm4f3onVSOvgK14VLjOoOHGAWb-rhfsdkS0cTrcwm8-4-tocuk7reQQrcEc4-6vgGfi6qvD-n1r2TDcM_zEfSPWO6On8KhActXZdaiw"
refresh_token = "Atzr|IwEBIMOnjo6QYd0xWK8EFyXvH8TWQ10Y5RuRNBPYXPTJmwsbUoV4Wn6Pi8MsB_4BB9o5avIwOR21E7TbWFyFvfQylK6msxw_kwrMRKX6oqd86hvm2FuHc6Uncggpv8aJe0IGWYfizm_tBOQUMVzkboRu1iKRUCB83NlOCt7RY4OKZwWJ71tqDd_Ndz9uAqPRe5OFUDLLhmysWdkXMY7H99NaTVwngImGmyGSkxuV9YfSf0WvJIGkTI2Ju5zaEPf7W8WEIzFhKl7RiSjLcfgRLRgZj1gmZDtc0tKMKKb0W1Xt4NRW_xG4DEsliBkVeICYBNszX3cm3rg8iWAntP-Kc3G3lqijqq0jDIPA_PcmNAskHWQhd2udnCAk8o5z4-Es8jWnvY4DTWg7Wqmy94yHC19WL4ex"
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
