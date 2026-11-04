[app]
title = Mathematics
package.name = mathematics
package.domain = org.almnsob
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,txt,md
version = 1.0

# تم حذف SymPy تماماً! لم يتبق سوى Flask و Kivy
requirements = python3==3.10.12,hostpython3==3.10.12,kivy,flask

android.accept_sdk_license = True
android.ndk = 27b
android.api = 30
android.minapi = 21
android.archs = arm64-v8a, armeabi-v7a
android.permissions = INTERNET
android.allow_backup = True

orientation = portrait
fullscreen = 0

[buildozer]
log_level = 2
warn_on_root = 1
