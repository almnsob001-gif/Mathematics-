import os
import sys
import time
import threading

from app import app as flask_app

FLASK_PORT = 5000


def start_flask():
    flask_app.run(host='127.0.0.1', port=FLASK_PORT,
                  debug=False, use_reloader=False, threaded=True)


def is_pydroid():
    """كشف Pydroid بناءً على التشخيص الفعلي"""
    try:
        if 'pydroid' in sys.executable.lower():
            return True
    except Exception:
        pass
    try:
        from jnius import autoclass
        activity = autoclass('org.kivy.android.PythonActivity').mActivity
        return activity is None
    except Exception:
        return True
    return False


# ---------- تشغيل Flask ----------
threading.Thread(target=start_flask, daemon=True).start()
time.sleep(2)

in_pydroid = ('ANDROID_ARGUMENT' not in os.environ) or is_pydroid()

print("=" * 50)
print(f"✅ Flask: http://127.0.0.1:{FLASK_PORT}")
print(f"   البيئة: {'Pydroid (اختبار)' if in_pydroid else 'APK (تطبيق حقيقي)'}")
print("=" * 50)


# ---------- Pydroid: متصفح للاختبار فقط ----------
if in_pydroid:
    import webbrowser
    webbrowser.open(f'http://127.0.0.1:{FLASK_PORT}')
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass


# ---------- APK: WebView داخلي (تطبيق حقيقي) ----------
else:
    from kivy.app import App
    from kivy.uix.floatlayout import FloatLayout
    from kivy.uix.label import Label
    from kivy.clock import Clock
    from android.runnable import run_on_ui_thread
    from jnius import autoclass

    class MathSolverApp(App):
        def build(self):
            self.root_box = FloatLayout()
            self.status = Label(
                text="Loading...",
                font_size='22sp',
                size_hint=(1, 1),
                pos_hint={'x': 0, 'y': 0}
            )
            self.root_box.add_widget(self.status)
            return self.root_box

        def on_start(self):
            Clock.schedule_once(self.load_webview, 1)

        def load_webview(self, dt):
            @run_on_ui_thread
            def _setup():
                try:
                    WebView = autoclass('android.webkit.WebView')
                    WebViewClient = autoclass('android.webkit.WebViewClient')
                    activity = autoclass('org.kivy.android.PythonActivity').mActivity
                    webview = WebView(activity)
                    s = webview.getSettings()
                    s.setJavaScriptEnabled(True)
                    s.setDomStorageEnabled(True)
                    s.setAllowFileAccess(True)
                    webview.setWebViewClient(WebViewClient())
                    webview.loadUrl(f'http://127.0.0.1:{FLASK_PORT}')
                    activity.setContentView(webview)
                except Exception as e:
                    print("WebView error:", e)
                    self.status.text = f"Error:\n{e}"
            _setup()

    MathSolverApp().run()
