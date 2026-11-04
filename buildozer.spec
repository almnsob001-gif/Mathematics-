[app]
title = Mathematics
package.name = mathematics
package.domain = org.almnsob
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,txt,md
version = 1.0

# إضافة setuptools وإصدارات مستقرة
requirements = python3==3.10.12,hostpython3==3.10.12,setuptools,kivy,flask,sympy==1.12,mpmath==1.3.0

# العودة إلى الفرع المستقر master لتجنب مشاكل develop
p4a.branch = master

# قبول تراخيص Android SDK تلقائياً (سبب شائع جداً للفشل)
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
