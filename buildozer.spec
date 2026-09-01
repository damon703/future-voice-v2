[app]
title = FutureVoiceV2
package.name = futurevoicev2
package.domain = org.futurevoicev2
source.dir = .
source.include_exts = py,png,jpg,kv
version = 0.2

requirements = python3,kivy,requests,android

services = Service:service.py:foreground:sticky

android.permissions = INTERNET,FOREGROUND_SERVICE,ACCESS_NETWORK_STATE,WRITE_EXTERNAL_STORAGE
android.api = 33
android.minapi = 24
android.archs = arm64‑v8a

orientation = portrait
fullscreen = 0
log_level = 2

[buildozer]
log_level = 2
warn_on_root = 1