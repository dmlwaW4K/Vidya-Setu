[app]
title = Vidyasetu
package.name = vidyasetu
package.domain = org.drishti

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json,wav

version = 1.0

requirements = python3,kivy==2.2.1,requests,pytesseract,pillow,android

orientation = portrait
fullscreen = 0

# Android specific
android.permissions = INTERNET,CAMERA,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,ACCESS_NETWORK_STATE
android.api = 31
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True
android.arch = arm64-v8a

# iOS specific
ios.kivy_ios_url = https://github.com/kivy/kivy-ios
ios.kivy_ios_branch = master

[buildozer]
log_level = 2
warn_on_root = 1

# Meghalaya theme icon (replace with actual icon)
# icon.filename = %(source.dir)s/icon.png
# presplash.filename = %(source.dir)s/presplash.png
