from pythonforandroid.recipe import PipRecipe

class SympyRecipe(PipRecipe):
    name = 'sympy'
    version = '1.12' # استخدمنا 1.12 لأنه أكثر استقرارًا مع p4a
    depends = ['python3', 'setuptools', 'mpmath']
