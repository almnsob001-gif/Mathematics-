from flask import Flask, request, render_template_string
import re
from fractions import Fraction

app = Flask(__name__)

def parse_equation(eq_str):
    eq_str = eq_str.replace(' ', '').replace('-', '+-')
    if '=' in eq_str:
        lhs, rhs = eq_str.split('=')
        if rhs.startswith('+-'): rhs = '-' + rhs[2:]
        elif not rhs.startswith('-'): rhs = '-' + rhs
        eq_str = lhs + rhs
    
    a, b, c = 0, 0, 0
    
    # استخراج معامل x^2
    match_a = re.search(r'([+-]?\d*)x\^2', eq_str)
    if match_a:
        coeff = match_a.group(1)
        a = 1 if coeff in ['', '+'] else (-1 if coeff == '-' else Fraction(coeff))
        eq_str = eq_str.replace(match_a.group(0), '')
        
    # استخراج معامل x
    match_b = re.search(r'([+-]?\d*)x', eq_str)
    if match_b:
        coeff = match_b.group(1)
        b = 1 if coeff in ['', '+'] else (-1 if coeff == '-' else Fraction(coeff))
        eq_str = eq_str.replace(match_b.group(0), '')
        
    # استخراج الحد الثابت
    if eq_str and eq_str not in ['+', '-']:
        c = Fraction(eq_str) if eq_str else 0
    elif eq_str == '+': c = 1
    elif eq_str == '-': c = -1
        
    return a, b, c

def frac_to_str(f):
    if f.denominator == 1: return str(f.numerator)
    return f"\\frac{{{f.numerator}}}{{{f.denominator}}}"

def solve_with_steps(eq_str):
    steps = []
    a, b, c = parse_equation(eq_str)
    
    steps.append({"title": "المعادلة الأصلية", "math": eq_str.replace('^', '^'), "text": ""})
    
    if a == 0 and b == 0:
        return steps, ["لا يوجد حل أو عدد لا نهائي من الحلول"]
        
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
        import math
        x1 = (-b + math.sqrt(delta)) / (2*a)
        x2 = (-b - math.sqrt(delta)) / (2*a)
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
                steps = [{"title": "خطأ", "text": str(e), "math": ""}]
    return render_template_string(HTML, steps=steps, solution=solution, equation=equation)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)
