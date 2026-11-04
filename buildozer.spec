[app]
title = Mathematics
package.name = mathematics
package.domain = org.almnsob
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,txt,md
version = 1.0

# تثبيت الإصدارات المتوافقة
requirements = python3==3.10.12,hostpython3==3.10.12,kivy,flask,sympy==1.12,mpmath==1.3.0

# استخدام الفرع التطويري لـ p4a للحصول على آخر الإصلاحات
p4a.branch = develop

# *** الأهم: تحديد إصدار NDK متوافق ***
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
