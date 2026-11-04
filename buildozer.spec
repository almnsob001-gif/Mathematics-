[app]

# (str) عنوان التطبيق
title = Mathematics

# (str) اسم الحزمة (يجب أن يكون بحروف صغيرة)
package.name = mathematics

# (str) معرف الحزمة
package.domain = org.almnsob

# (str) مجلد الكود المصدري
source.dir = .

# (list) الامتدادات التي سيتم تضمينها
source.include_exts = py,png,jpg,kv,atlas,txt,md

# (str) إصدار التطبيق
version = 1.0

# (list) المتطلبات (أهم سطر: تثبيت بايثون 3.10 وإصدارات محددة للمكتبات)
requirements = python3==3.10.12,kivy,flask,sympy==1.13.0,mpmath==1.3.0

# (str) استخدام فرع التطوير من python-for-android لضمان التوافق
p4a.branch = develop

# (str) اتجاه الشاشة
orientation = portrait

# (bool) ملء الشاشة (0 يعني إظهار شريط الحالة)
fullscreen = 0

# (list) صلاحيات التطبيق (ضرورية ليعمل Flask)
android.permissions = INTERNET

# (int) نسخة أندرويد المستهدفة (27 ضروري لتجاوز حظر HTTP المحلي)
android.api = 27

# (int) أقل نسخة أندرويد مدعومة
android.minapi = 21

# (list) معماريات المعالج
android.archs = arm64-v8a, armeabi-v7a

[buildozer]

# (int) مستوى السجلات
log_level = 2

# (int) إظهار تحذير إذا تم التشغيل كـ root
warn_on_root = 1
