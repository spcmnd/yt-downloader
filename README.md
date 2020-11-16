## Deploy a new version

Script in console :

```
pyinstaller .\app.py --add-data "assets/;assets/" --add-data "VERSION;." -i"assets/youtube.ico" --noconsole --hidden-import=pkg_resources.py2_warn
```
