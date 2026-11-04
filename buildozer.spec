[app]
title = Mathematics
package.name = mathematics
package.domain = org.almnsob
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,txt,md
version = 1.0

# تثبيت إصدارات متوافقة ومعروفة بالاستقرار
requirements = python3==3.10.12,hostpython3==3.10.12,kivy==2.3.0,flask,sympy==1.12,mpmath==1.3.0

# إجبار استخدام الفرع الرئيسي المستقر
p4a.branch = master

# رفع واجهة برمجة التطبيقات لتجنب مشاكل الأندرويد الحديثة
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
