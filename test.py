from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>منصة سند - المساعد الصوتي</title>
    <style>
        body { font-family: Tahoma, sans-serif; background-color: #f4f7f6; text-align: center; padding: 50px; }
        .container { background: white; padding: 40px; border-radius: 15px; box-shadow: 0px 4px 10px rgba(0,0,0,0.1); display: inline-block; width: 80%; max-width: 600px; }
        h1 { color: #0066cc; }
        .mic-btn { background-color: #28a745; color: white; border: none; padding: 20px 40px; font-size: 24px; border_radius: 50px; cursor: pointer; margin-top: 20px; box-shadow: 0px 4px 6px rgba(0,0,0,0.2); }
        .mic-btn:active { background-color: #218838; transform: scale(0.98); }
        #response-box { margin-top: 30px; font-size: 20px; color: #333; background: #e9ecef; padding: 15px; border_radius: 8px; }
    </style>
</head>
<body>

    <div class="container">
        <h1>منصة سند الذكية</h1>
        <p>اضغط على الزر وتحدث باللهجة الأردنية (مثلاً: بدي أجدد هوية ابني)</p>
        
        <button class="mic-btn" onclick="simulateVoiceInput()">🎤 احكي مع سند</button>
        
        <div id="response-box">النتيجة ستظهر هنا...</div>
    </div>

    <script>
        function simulateVoiceInput() {
            document.getElementById("response-box").innerHTML = "جاري الاستماع وتحليل اللهجة الأردنية...";
            
            setTimeout(() => {
                fetch('/process_request', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ speech: "بدي أجدد هوية ابني" })
                })
                .then(response => response.json())
                .then(data => {
                    document.getElementById("response-box").innerHTML = "<strong>النتيجة:</strong> " + data.message;
                });
            }, 1500);
        }
    </script>

</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/process_request', methods=['POST'])
def process_request():
    user_speech = request.json.get('speech', '')
    if "هوية" in user_speech or "أجدد" in user_speech:
        response_msg = "تم فهم طلبك: تجديد هوية شخصية. تم حجز موعد في أحوال الكرك غداً الساعة 10 صباحاً. الأوراق المطلوبة: الهوية القديمة وصورة شخصية."
    else:
        response_msg = "عذراً، لم أفهم طلبك بدقة، يرجى إعادة المحاولة."
    return jsonify({"message": response_msg})

if __name__ == '__main__':
    app.run(debug=True, port=5000)