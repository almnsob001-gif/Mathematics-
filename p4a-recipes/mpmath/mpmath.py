from pythonforandroid.recipe import PipRecipe

class MpmathRecipe(PipRecipe):
    name = 'mpmath'
    version = '1.3.0'
    depends = ['python3', 'setuptools']
    # استخدمنا PipRecipe لأن mpmath هي مكتبة بايثون خالصة
    # يمكن تثبيتها مباشرة دون تجميع C
