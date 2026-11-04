from flask import Flask, request, render_template_string
import re
import math
from fractions import Fraction

app = Flask(__name__)

def parse_equation(eq_str):
    # تنظيف النص من المسافات وعلامات الضرب
    eq_str = eq_str.replace(' ', '').replace('*', '')
    
    # نقل كل الحدود إلى طرف واحد
    if '=' in eq_str:
        lhs, rhs = eq_str.split('=', 1)
        if rhs.startswith('-'):
            rhs = '+' + rhs[1:]
        elif rhs.startswith('+'):
            rhs = '-' + rhs[1:]
        else:
            rhs = '-' + rhs
        eq_str = lhs + rhs
        
    if not (eq_str.startswith('+') or eq_str.startswith('-')):
        eq_str = '+' + eq_str
        
    # تقسيم المعادلة إلى حدود منفصلة
    eq_str = eq_str.replace('-', '+-')
    terms = eq_str.split('+')
    
    a, b, c = Fraction(0), Fraction(0), Fraction(0)
    
    for term in terms:
        if not term: continue
        if 'x^2' in term:
            coeff_str = term.replace('x^2', '')
            if coeff_str in ['', '+']: a += 1
            elif coeff_str == '-': a -= 1
            else: a += Fraction(coeff_str)
        elif 'x' in term:
            coeff_str = term.replace('x', '')
            if coeff_str in ['', '+']: b += 1
            elif coeff_str == '-': b -= 1
            else: b += Fraction(coeff_str)
        else:
            if term == '-': c -= 1
            elif term == '+': c += 1
            else: c += Fraction(term)
            
    return a, b, c

def frac_to_str(f):
    if f.denominator == 1: return str(f.numerator)
    return f"\\frac{{{f.numerator}}}{{{f.denominator}}}"

def solve_with_steps(eq_str):
    steps = []
    steps.append({"title": "المعادلة الأصلية", "math": eq_str.replace('^', '^'), "text": ""})
    
    # التحقق من الدرجات الأعلى
    if 'x^3' in eq_str or 'x^4' in eq_str:
        steps.append({"title": "تنبيه", "text": "التطبيق يدعم حالياً المعادلات من الدرجة الأولى والثانية فقط.", "math": ""})
        return steps, ["غير مدعوم"]
        
    a, b, c = parse_equation(eq_str)
    
    if a == 0 and b == 0:
        return steps, ["لا يوجد حل أو عدد لا نهائي"]
        
    if a == 0:
        # معادلة خطية
        steps.append({"title": "معادلة من الدرجة الأولى", "math": f"{frac_to_str(b)}x + ({frac_to_str(c)}) = 0", "text": ""})
        steps.append({"title": "نعزل الحد الذي يحتوي على x", "math": f"{frac_to_str(b)}x = {frac_to_str(-c)}", "text": "ننقل الحد الثابت للطرف الآخر"})
        x = -c / b
        steps.append({"title": "نقسم الطرفين على معامل x", "math": f"x = {frac_to_str(x)}", "text": ""})
        return steps, [frac_to_str(x)]
        
    # معادلة تربيعية
    steps.append({"title": "درجة المعادلة", "math": "2", "text": "أعلى أس للـ x هو 2، إذن هي معادلة تربيعية."})
    steps.append({"title": "الصيغة القياسية", "math": f"{frac_to_str(a)}x^2 + ({frac_to_str(b)})x + ({frac_to_str(c)}) = 0", "text": ""})
    
    delta = b**2 - 4*a*c
    steps.append({"title": "حساب المميز (Δ)", "math": f"\\Delta = b^2 - 4ac = ({frac_to_str(b)})^2 - 4({frac_to_str(a)})({frac_to_str(c)}) = {frac_to_str(delta)}", "text": ""})
    
    if delta > 0:
        steps.append({"title": "تفسير المميز", "math": "\\Delta > 0", "text": "للمعادلة جذران حقيقيان مختلفان."})
        
        # التحقق من وجود جذر تربيعي دقيق
        num_sqrt = math.isqrt(delta.numerator)
        den_sqrt = math.isqrt(delta.denominator)
        
        if num_sqrt**2 == delta.numerator and den_sqrt**2 == delta.denominator:
            sqrt_delta = Fraction(num_sqrt, den_sqrt)
            x1 = (-b + sqrt_delta) / (2*a)
            x2 = (-b - sqrt_delta) / (2*a)
            steps.append({"title": "الجذر الأول", "math": f"x_1 = \\frac{{-({frac_to_str(b)}) + {frac_to_str(sqrt_delta)}}}{{2({frac_to_str(a)})}} = {frac_to_str(x1)}", "text": ""})
            steps.append({"title": "الجذر الثاني", "math": f"x_2 = \\frac{{-({frac_to_str(b)}) - {frac_to_str(sqrt_delta)}}}{{2({frac_to_str(a)})}} = {frac_to_str(x2)}", "text": ""})
            return steps, [frac_to_str(x1), frac_to_str(x2)]
        else:
            x1 = (-float(b) + math.sqrt(float(delta))) / (2*float(a))
            x2 = (-float(b) - math.sqrt(float(delta))) / (2*float(a))
            steps.append({"title": "الجذر الأول", "math": f"x_1 = \\frac{{-({frac_to_str(b)}) + \\sqrt{{{frac_to_str(delta)}}}}}{{2({frac_to_str(a)})}} \\approx {x1:.3f}", "text": ""})
            steps.append({"title": "الجذر الثاني", "math": f"x_2 = \\frac{{-({frac_to_str(b)}) - \\sqrt{{{frac_to_str(delta)}}}}}{{2({frac_to_str(a)})}} \\approx {x2:.3f}", "text": ""})
            return steps, [f"{x1:.3f}", f"{x2:.3f}"]
            
    elif delta == 0:
        steps.append({"title": "تفسير المميز", "math": "\\Delta = 0", "text": "للمعادلة جذر حقيقي واحد مكرر."})
        x = -b / (2*a)
        steps.append({"title": "الحل", "math": f"x = {frac_to_str(x)}", "text": ""})
        return steps, [frac_to_str(x)]
    else:
        steps.append({"title": "تفسير المميز", "math": "\\Delta < 0", "text": "للمعادلة جذور مركبة (غير حقيقية)."})
        return steps, ["جذور مركبة"]

HTML = r"""
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>حل المسائل</title>
<script>window.MathJax = { tex: { inlineMath: [['$','$']] }, svg: { fontCache: 'global' } };</script>
<script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js"></script>
<style>
  body { font-family: Tahoma, sans-serif; background: #f0f4f8; padding: 1em; }
  .box { max-width: 700px; margin: auto; background: white; padding: 20px; border-radius: 12px; }
  input[type=text] { width: 100%; padding: 12px; font-size: 1.1em; margin-bottom: 10px; box-sizing: border-box; }
  button { width: 100%; padding: 12px; font-size: 1.1em; background: #3498db; color: white; border: none; border-radius: 8px; }
  .step { background: #eaf4fc; padding: 12px; border-radius: 8px; margin-bottom: 10px; border-right: 4px solid #3498db; }
  .step-title { font-weight: bold; color: #2c3e50; }
  .step-text { color: #444; margin: 5px 0; }
  .step-math { text-align: center; font-size: 1.2em; direction: ltr; padding: 10px 0; }
  .solution { background: #d4edda; padding: 15px; border-radius: 8px; text-align: center; color: #155724; font-weight: bold; margin-top: 15px; }
</style>
</head>
<body>
<div class="box">
  <h2 style="text-align:center;">🧮 حل المسائل</h2>
  <form method="POST">
    <input type="text" name="equation" value="{{ equation }}" placeholder="مثال: x^2 - 5x + 6 = 0" required>
    <button type="submit">حل</button>
  </form>
  {% if steps %}
  <div style="margin-top:20px;">
    {% for s in steps %}
      <div class="step">
        <div class="step-title">{{ loop.index }}. {{ s.title }}</div>
        {% if s.text %}<div class="step-text">{{ s.text }}</div>{% endif %}
        {% if s.math %}<div class="step-math">$${{ s.math|safe }}$$</div>{% endif %}
      </div>
    {% endfor %}
    <div class="solution">
      الحل النهائي: 
      {% for sol in solution %}<span style="direction:ltr; display:inline-block;">$$x = {{ sol }}$$</span>{% if not loop.last %} أو {% endif %}{% endfor %}
    </div>
  </div>
  {% endif %}
</div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def home():
    steps, solution = None, None
    equation = ""
    if request.method == 'POST':
        equation = request.form.get('equation', '').strip()
        if equation:
            try:
                steps, solution = solve_with_steps(equation)
            except Exception as e:
                steps = [{"title": "خطأ في القراءة", "text": "تأكد من كتابة المعادلة بشكل صحيح (مثال: x^2 - 5x + 6 = 0)", "math": ""}]
    return render_template_string(HTML, steps=steps, solution=solution, equation=equation)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)
