API密钥：
```
 0a87431e-5b19-48be-8084-855ef00f1816   //timestamp: 2024-07-10
```

参数说明：
airdrop
```
air_drop_request_info={
    "url" : "https://pro-api.coinmarketcap.com/v1/cryptocurrency/airdrops",
    "parameters" : 
    {
    "start": 1,
    "limit": 100,
    "status": "ongoing",
    "id":1,
    "slug":"bitcoin",
    "symbol": "BTC"
}
}
```

coin_id
```
coin_id_request_info={
    "url" : "https://pro-api.coinmarketcap.com/v1/cryptocurrency/map",
    "parameters" : 
    {
    "listing_status": "active",
    "start": 1,
    "limit": 100,
    "sort": "id",
    "symbol": "BTC",
    "aux": "platform,first_historical_data,last_historical_data,is_active"
}
}
```


