[app]

# (str) عنوان التطبيق
title = Mathematics

# (str) اسم الحزمة (يجب أن يكون بحروف صغيرة)
package.name = mathematics

# (str) معرف الحزمة (يفضل أن يكون مقلوباً لدومين تملكه)
package.domain = org.almnsob

# (str) مجلد الكود المصدري
source.dir = .

# (list) الامتدادات التي سيتم تضمينها من مجلد المصدر
source.include_exts = py,png,jpg,kv,atlas,txt,md

# (str) إصدار التطبيق
version = 1.0

# (list) المتطلبات (هذا السطر هو الأهم، لا تغيره)
requirements = python3,kivy,flask,sympy==1.13.0,mpmath==1.3.0

# (str) اتجاه الشاشة (portrait للطول، landscape للعرض)
orientation = portrait

# (bool) هل تريد ملء الشاشة؟ (0 يعني إظهار شريط الحالة العلوي)
fullscreen = 0

# (list) صلاحيات التطبيق (مهم جداً ليعمل Flask داخل التطبيق)
android.permissions = INTERNET

# (int) نسخة أندرويد المستهدفة
# استخدام API 27 يمنع مشكلة حظر الاتصال المحلي (HTTP) في أندرويد 9+
android.api = 27

# (int) أقل نسخة أندرويد مدعومة
android.minapi = 21

# (list) معماريات المعالج (يدعم هواتف 64-bit و 32-bit)
android.archs = arm64-v8a, armeabi-v7a

[buildozer]

# (int) مستوى السجلات (2 يعني إظهار الأخطاء والتحذيرات)
log_level = 2

# (int) إظهار تحذير إذا تم التشغيل كـ root
warn_on_root = 1
