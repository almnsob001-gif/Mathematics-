from flask import Flask, request, render_template_string
import sympy as sp
from sympy.parsing.sympy_parser import (
    parse_expr, standard_transformations,
    implicit_multiplication_application, convert_xor
)

app = Flask(__name__)

TRANSFORMATIONS = standard_transformations + (
    implicit_multiplication_application,
    convert_xor
)

def solve_math_input(input_str):
    x = sp.Symbol('x')
    local_dict = {'x': x}
    input_str = input_str.replace(' ', '')
    is_equation = '=' in input_str
    steps = []
    
    try:
        if is_equation:
            # حل المعادلات
            lhs_str, rhs_str = input_str.split('=', 1)
            lhs = parse_expr(lhs_str, transformations=TRANSFORMATIONS, local_dict=local_dict)
            rhs = parse_expr(rhs_str, transformations=TRANSFORMATIONS, local_dict=local_dict)
            eq = sp.Eq(lhs, rhs)
            
            steps.append({"title": "المعادلة الأصلية", "math": sp.latex(eq), "text": ""})
            
            expr = sp.expand(eq.lhs - eq.rhs)
            steps.append({"title": "تجميع الحدود في طرف واحد", "math": f"{sp.latex(expr)} = 0", "text": ""})
            
            # محاولة التحليل إلى عوامل
            try:
                factored = sp.factor(expr)
                if factored != expr:
                    steps.append({"title": "تحليل المعادلة إلى عوامل", "math": f"{sp.latex(factored)} = 0", "text": ""})
            except:
                pass
            
            sols = sp.solve(eq, x)
            if not sols:
                steps.append({"title": "النتيجة", "math": "\\text{لا يوجد حل}", "text": "لم يتم العثور على حلول."})
                return steps, []
                
            for i, sol in enumerate(sols, 1):
                steps.append({"title": f"الحل {i}", "math": f"x = {sp.latex(sol)}", "text": ""})
                
            return steps, [sp.latex(s) for s in sols]
            
        else:
            # تبسيط التعبيرات الرياضية
            expr = parse_expr(input_str, transformations=TRANSFORMATIONS, local_dict=local_dict)
            steps.append({"title": "التعبير الأصلي", "math": sp.latex(expr), "text": ""})
            
            expanded = sp.expand(expr)
            if expanded != expr:
                steps.append({"title": "فك الأقواس", "math": sp.latex(expanded), "text": ""})
                
            factored = sp.factor(expr)
            if factored != expr and factored != expanded:
                steps.append({"title": "التحليل إلى عوامل", "math": sp.latex(factored), "text": ""})
                
            simplified = sp.simplify(expr)
            steps.append({"title": "التبسيط النهائي", "math": sp.latex(simplified), "text": ""})
            
            return steps, [sp.latex(simplified)]
            
    except Exception as e:
        steps.append({"title": "خطأ في القراءة", "text": "تأكد من كتابة المعادلة أو التعبير بشكل صحيح (مثال: x^2 - 4 أو 2x+3=7).", "math": ""})
        return steps, []

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
  .box { max-width: 700px; margin: auto; background: white; padding: 20px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,.1); }
  input[type=text] { width: 100%; padding: 12px; font-size: 1.1em; margin-bottom: 10px; box-sizing: border-box; border: 1px solid #ccc; border-radius: 8px; }
  button { width: 100%; padding: 12px; font-size: 1.1em; background: #3498db; color: white; border: none; border-radius: 8px; cursor: pointer;}
  button:hover { background: #2980b9; }
  .step { background: #eaf4fc; padding: 12px; border-radius: 8px; margin-bottom: 10px; border-right: 4px solid #3498db; }
  .step-title { font-weight: bold; color: #2c3e50; }
  .step-text { color: #444; margin: 5px 0; }
  .step-math { text-align: center; font-size: 1.2em; direction: ltr; padding: 10px 0; overflow-x: auto; }
  .solution { background: #d4edda; padding: 15px; border-radius: 8px; text-align: center; color: #155724; font-weight: bold; margin-top: 15px; }
</style>
</head>
<body>
<div class="box">
  <h2 style="text-align:center;">🧮 حل المسائل الذكي</h2>
  <form method="POST">
    <input type="text" name="equation" value="{{ equation }}" placeholder="مثال: (x+1)^2 أو 2x+3=7 أو x^3-8=0" required>
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
    {% if solution %}
    <div class="solution">
      النتيجة النهائية: 
      {% for sol in solution %}<span style="direction:ltr; display:inline-block;">$${{ sol }}$$</span>{% if not loop.last %} أو {% endif %}{% endfor %}
    </div>
    {% endif %}
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
            steps, solution = solve_math_input(equation)
    return render_template_string(HTML, steps=steps, solution=solution, equation=equation)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)
