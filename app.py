from flask import Flask, request, render_template_string
import sympy as sp
from sympy.parsing.sympy_parser import (
    parse_expr, standard_transformations,
    implicit_multiplication_application, convert_xor
)
from sympy import Symbol

TRANSFORMATIONS = standard_transformations + (
    implicit_multiplication_application,
    convert_xor
)

def parse_equation(eq_str, x):
    eq_str = eq_str.replace(' ', '')
    if '=' in eq_str:
        left, right = eq_str.split('=', 1)
        lhs = parse_expr(left, transformations=TRANSFORMATIONS, local_dict={'x': x})
        rhs = parse_expr(right, transformations=TRANSFORMATIONS, local_dict={'x': x})
    else:
        lhs = parse_expr(eq_str, transformations=TRANSFORMATIONS, local_dict={'x': x})
        rhs = 0
    return sp.Eq(lhs, rhs)

def substitute_display(expr, x, val):
    """يعرض التعبير مع التعويض بقيمة دون حساب الناتج"""
    tmp = Symbol('subval')
    return sp.latex(expr.subs(x, tmp), symbol_names={'subval': sp.latex(val)})

def solve_with_steps(eq_str):
    x = sp.symbols('x')
    eq = parse_equation(eq_str, x)
    steps = []

    steps.append({"title": "المعادلة الأصلية",
                  "math": f"{sp.latex(eq.lhs)} = {sp.latex(eq.rhs)}",
                  "text": ""})

    expr = sp.expand(eq.lhs - eq.rhs)
    steps.append({"title": "ننقل جميع الحدود إلى طرف واحد",
                  "math": f"{sp.latex(expr)} = 0",
                  "text": "نطرح الطرف الأيمن من الطرف الأيسر حتى يصبح الطرف الأيمن صفراً."})

    try:
        poly = sp.Poly(expr, x)
        degree = poly.degree()
    except sp.PolynomialError:
        solutions = sp.solve(eq, x)
        for i, s in enumerate(solutions, 1):
            steps.append({"title": f"الحل {i}", "math": f"x = {sp.latex(s)}", "text": ""})
        return steps, solutions

    steps.append({"title": "درجة المعادلة",
                  "math": f"{degree}",
                  "text": f"أعلى أس للـ x هو {degree}، إذن المعادلة من الدرجة {'الأولى' if degree == 1 else 'الثانية' if degree == 2 else degree}."})

    if degree == 2:
        a, b, c = poly.all_coeffs()
        steps.append({"title": "الصيغة القياسية للمعادلة التربيعية",
                      "math": f"{sp.latex(a)}x^2 + ({sp.latex(b)})x + ({sp.latex(c)}) = 0",
                      "text": "نكتب المعادلة على الصورة ax² + bx + c = 0."})
        steps.append({"title": "تحديد المعاملات",
                      "math": f"a = {sp.latex(a)}, \\quad b = {sp.latex(b)}, \\quad c = {sp.latex(c)}",
                      "text": "a هو معامل x²، b معامل x، و c الحد الثابت."})

        delta = sp.simplify(b**2 - 4*a*c)
        steps.append({"title": "حساب المميز (Δ)",
                      "math": f"\\Delta = b^2 - 4ac = ({sp.latex(b)})^2 - 4 \\cdot ({sp.latex(a)}) \\cdot ({sp.latex(c)})",
                      "text": "المميز يخبرنا بنوع الجذور قبل حسابها."})
        steps.append({"title": "قيمة المميز",
                      "math": f"\\Delta = {sp.latex(delta)}",
                      "text": ""})

        if delta > 0:
            steps.append({"title": "تفسير قيمة المميز",
                          "math": f"\\Delta = {sp.latex(delta)} > 0",
                          "text": "بما أن المميز موجب، فالمعادلة لها جذران حقيقيان مختلفان."})
        elif delta == 0:
            steps.append({"title": "تفسير قيمة المميز",
                          "math": f"\\Delta = {sp.latex(delta)} = 0",
                          "text": "بما أن المميز يساوي صفراً، فالمعادلة لها جذر حقيقي واحد مكرر."})
        else:
            steps.append({"title": "تفسير قيمة المميز",
                          "math": f"\\Delta = {sp.latex(delta)} < 0",
                          "text": "بما أن المميز سالب، فالمعادلة لها جذران مركبان (غير حقيقيان)."})

        steps.append({"title": "نطبّق القانون العام",
                      "math": "x = \\frac{-b \\pm \\sqrt{\\Delta}}{2a}",
                      "text": "هذا هو القانون العام لحل أي معادلة تربيعية."})
        steps.append({"title": "نعوّض القيم في القانون",
                      "math": f"x = \\frac{{-({sp.latex(b)}) \\pm \\sqrt{{{sp.latex(delta)}}}}}{{2 \\cdot ({sp.latex(a)})}}",
                      "text": ""})

        solutions = sp.solve(eq, x)

        if delta > 0:
            x1 = sp.simplify((-b + sp.sqrt(delta)) / (2*a))
            x2 = sp.simplify((-b - sp.sqrt(delta)) / (2*a))
            steps.append({"title": "الجذر الأول (بإشارة +)",
                          "math": f"x_1 = \\frac{{-({sp.latex(b)}) + \\sqrt{{{sp.latex(delta)}}}}}{{2 \\cdot ({sp.latex(a)})}} = {sp.latex(x1)}",
                          "text": "نأخذ الإشارة الموجبة قبل الجذر."})
            steps.append({"title": "الجذر الثاني (بإشارة −)",
                          "math": f"x_2 = \\frac{{-({sp.latex(b)}) - \\sqrt{{{sp.latex(delta)}}}}}{{2 \\cdot ({sp.latex(a)})}} = {sp.latex(x2)}",
                          "text": "نأخذ الإشارة السالبة قبل الجذر."})
            for xv in [x1, x2]:
                lhs_sub = substitute_display(eq.lhs, x, xv)
                lhs_val = sp.simplify(eq.lhs.subs(x, xv))
                rhs_val = sp.simplify(eq.rhs.subs(x, xv))
                steps.append({"title": f"التحقق بالتعويض عن x = {sp.latex(xv)}",
                              "math": f"{lhs_sub} = {sp.latex(lhs_val)} = {sp.latex(rhs_val)} \\; \\checkmark",
                              "text": "نعيد القيمة في المعادلة الأصلية، ونتحقق من أن الطرفين متساويان."})

        return steps, solutions

    elif degree == 1:
        a, b = poly.all_coeffs()
        steps.append({"title": "معادلة من الدرجة الأولى",
                      "math": f"{sp.latex(a)}x + ({sp.latex(b)}) = 0",
                      "text": ""})
        steps.append({"title": "نعزل الحد الذي يحتوي على x",
                      "math": f"{sp.latex(a)}x = {sp.latex(-b)}",
                      "text": "ننقل الحد الثابت إلى الطرف الآخر بإشارة معاكسة."})
        x_val = sp.simplify(-b/a)
        steps.append({"title": "نقسم الطرفين على معامل x",
                      "math": f"x = \\frac{{{sp.latex(-b)}}}{{{sp.latex(a)}}} = {sp.latex(x_val)}",
                      "text": ""})
        lhs_sub = substitute_display(eq.lhs, x, x_val)
        lhs_val = sp.simplify(eq.lhs.subs(x, x_val))
        rhs_val = sp.simplify(eq.rhs.subs(x, x_val))
        steps.append({"title": "التحقق بالتعويض",
                      "math": f"{lhs_sub} = {sp.latex(lhs_val)} = {sp.latex(rhs_val)} \\; \\checkmark",
                      "text": ""})
        return steps, [x_val]

    else:
        solutions = sp.solve(eq, x)
        for i, s in enumerate(solutions, 1):
            steps.append({"title": f"الحل {i}", "math": f"x = {sp.latex(s)}", "text": ""})
        return steps, solutions


app = Flask(__name__)

HTML = r"""
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>حل المسائل الرياضية</title>
<script>
window.MathJax = {
  tex: { inlineMath: [['$','$']], displayMath: [['$$','$$']] },
  svg: { fontCache: 'global' }
};
</script>
<script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js"></script>
<style>
  body { font-family: Tahoma, sans-serif; background: #f0f4f8; margin: 0; padding: 1em; }
  .box { max-width: 700px; margin: auto; background: white; padding: 20px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,.1); }
  h1 { color: #2c3e50; text-align: center; margin-top: 0; }
  input[type=text] { width: 100%; padding: 12px; font-size: 1.1em; border: 1px solid #ccc; border-radius: 8px; box-sizing: border-box; margin-bottom: 10px; }
  button { width: 100%; padding: 12px; font-size: 1.1em; background: #3498db; color: white; border: none; border-radius: 8px; cursor: pointer; }
  button:hover { background: #2980b9; }
  .steps { margin-top: 20px; }
  .step { background: #eaf4fc; padding: 12px 15px; border-radius: 8px; border-right: 4px solid #3498db; margin-bottom: 10px; }
  .step-title { font-weight: bold; color: #2c3e50; margin-bottom: 6px; }
  .step-text { color: #444; margin-bottom: 8px; line-height: 1.6; }
  .step-math { text-align: center; font-size: 1.15em; padding: 6px 0; direction: ltr; }
  .solution { margin-top: 15px; padding: 15px; background: #d4edda; border-radius: 8px; text-align: center; color: #155724; }
  .solution-title { font-weight: bold; margin-bottom: 8px; }
  .solution .math { direction: ltr; font-size: 1.2em; }
  .or-word { font-weight: bold; margin: 4px 0; }
</style>
</head>
<body>
<div class="box">
  <h1>🧮 حل المسائل الرياضية</h1>
  <form method="POST">
    <input type="text" name="equation" value="{{ equation }}" placeholder="مثال: x^2 - 5x + 6 = 0" required>
    <button type="submit">🔍 حل</button>
  </form>

  {% if steps %}
  <div class="steps">
    {% for s in steps %}
      <div class="step">
        <div class="step-title">{{ loop.index }}. {{ s.title }}</div>
        {% if s.text %}<div class="step-text">{{ s.text }}</div>{% endif %}
        {% if s.math %}<div class="step-math">$${{ s.math|safe }}$$</div>{% endif %}
      </div>
    {% endfor %}
  </div>
  {% if solution_items %}
  <div class="solution">
    <div class="solution-title">✅ الحل النهائي</div>
    {% for item in solution_items %}
      {% if not loop.first %}<div class="or-word">أو</div>{% endif %}
      <div class="math">$${{ item|safe }}$$</div>
    {% endfor %}
  </div>
  {% endif %}
  {% endif %}
</div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def home():
    steps = None
    solution_items = None
    equation = ""
    if request.method == 'POST':
        equation = request.form.get('equation', '').strip()
        if equation:
            try:
                steps, solutions = solve_with_steps(equation)
                if solutions:
                    solution_items = [f"x_{{{i+1}}} = {sp.latex(s)}" for i, s in enumerate(solutions)]
                else:
                    solution_items = [r"\text{لا يوجد حل}"]
            except Exception as e:
                steps = [{"title": "حدث خطأ في فهم المعادلة", "text": str(e), "math": ""}]
    return render_template_string(HTML, steps=steps,
                                  solution_items=solution_items, equation=equation)

if __name__ == '__main__':
    print("🚀 التطبيق يعمل! افتح المتصفح على: http://127.0.0.1:8080")
    app.run(host='127.0.0.1', port=8080, debug=False, use_reloader=False)