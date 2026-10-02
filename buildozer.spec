[app]
title = Cyras
package.name = cyras
package.domain = org.cyras
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3,kivy==2.2.1,plyer,urllib3,charset-normalizer,idna,requests
orientation = portrait
fullscreen = 1

android.permissions = INTERNET,RECORD_AUDIO,MODIFY_AUDIO_SETTINGS
android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a

[buildozer]
log_level = 2
warn_on_root = 1
