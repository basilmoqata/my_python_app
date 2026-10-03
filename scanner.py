from datetime import datetime
import requests


def scan_target(target_url):
  print("\n" + "=" * 50)
  print(f"[*] Starting Security Scan for: {target_url}")
  print(f"[*] Scan Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
  print("=" * 50)

  report_data = []

  # التأكد من بداية الرابط
  if not target_url.startswith("http"):
    target_url = "https://" + target_url

  # فحص الـ Security Headers (HTTP Headers Analysis)
  try:
    response = requests.get(target_url, timeout=5)
    headers = response.headers

    print("\n[+] Checking Security Headers...")
    security_headers = [
        "X-Frame-Options",
        "Content-Security-Policy",
        "Strict-Transport-Security",
        "X-Content-Type-Options",
    ]

    for header in security_headers:
      if header in headers:
        msg = (
            f"  [SECURE] Header '{header}' is present. (Value:"
            f" {headers[header]})"
        )
        print(msg)
        report_data.append(msg)
      else:
        msg = f"  [VULNERABLE] Missing Security Header: '{header}'"
        print(msg)
        report_data.append(msg)

  except requests.exceptions.RequestException as e:
    err_msg = f"[-] Error connecting to the target: {e}"
    print(err_msg)
    report_data.append(err_msg)

  # حفظ التقرير بملف نصي تلقائياً (Report Generator)
  report_filename = "security_scan_report.txt"
  with open(report_filename, "w", encoding="utf-8") as f:
    f.write(f"Security Scan Report for: {target_url}\n")
    f.write(
        f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        + "-" * 40
        + "\n"
    )
    for line in report_data:
      f.write(line + "\n")

  print(
      "\n[+] Scan Completed Successfully! Report saved as"
      f" '{report_filename}'."
  )


# تشغيل الأداة
if __name__ == "__main__":
  target = input("Enter target URL or domain (e.g., example.com): ").strip()
  scan_target(target)