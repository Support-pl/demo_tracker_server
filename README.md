# Requests

## `POST /signup`
Params:
```
username=..., // Any random username
```
Response:
```jsonc
{
    "response" : {
        "token" : "..." // char[32] random token
    }
}
```

## `POST /write`
Request:
```
token=...,  // Ur token
lat=0,      // Latitude:  float
lng=0       // Longitude: float
```
Response: `""` - 200

## `GET /read`
Request:
```
token="...",      // Ur token
stime=0,          // From which time to collect records as a timestamp
etime=1500000000  // Till which time to collect records as a timestamp
```
Response:
```jsonc
[
  {
    "lat": 52,
    "lng": 28,
    "ts": 1588943717
  },
  {
    "lat": 53,
    "lng": 28,
    "ts": 1588943720
  }
]
```