## To fix cipher issue with pytube3

Replace line 301 of extract.py file by :

```
try:
	cipher_url = [ parse_qs(formats[i]["signatureCipher"]) for i, data in enumerate(formats) ]
except Exception: 
	cipher_url = [ parse_qs(formats[i]["cipher"]) for i, data in enumerate(formats) ]
```

## Deploy a new version

Script in console :

```
pyinstaller .\app.py --add-data "assets/;assets/" --add-data "VERSION;." -i"assets/youtube.ico" --noconsole
```
