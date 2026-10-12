#!/usr/bin/env python3
"""
간이 iCalendar HTTP 서버
구글 캘린더 테스트용 로컬 서버
실행: python3 server.py [포트번호, 기본값: 8080]
"""

import http.server
import socketserver
import sys
import os

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def end_headers(self):
        # iCalendar MIME 타입 지정 및 캐시 제어
        if self.path.endswith('.ics'):
            self.send_header('Content-Type', 'text/calendar; charset=utf-8')
            self.send_header('Cache-Control', 'no-cache, must-revalidate')
        super().end_headers()

if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"🚀 물때 iCalendar 서버가 시작되었습니다: http://localhost:{PORT}/tides_west_2027.ics")
        print("Ctrl+C 로 종료할 수 있습니다.")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n서버를 종료합니다.")
