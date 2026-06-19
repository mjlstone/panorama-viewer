"""一键启动本地服务器，用于测试 PWA。

用法：
    py serve.py

然后浏览器打开它打印的地址（手机测试用同一 WiFi 下的局域网地址）。
Service Worker / PWA 安装功能仅在 http(s) 下生效，所以本地测试必须用这个，
而不能直接双击 index.html（file:// 协议下 PWA 会失效）。
"""
import http.server
import socketserver
import socket
import sys

PORT = 8000


def get_lan_ip():
    """获取本机局域网 IP，供手机访问。"""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip


def main():
    handler = lambda *args, **kw: http.server.SimpleHTTPRequestHandler(
        *args, directory=".", **kw
    )
    try:
        with socketserver.TCPServer(("0.0.0.0", PORT), handler) as httpd:
            lan = get_lan_ip()
            print("=" * 52)
            print("  360° 全景浏览器 —— 本地服务器已启动")
            print("=" * 52)
            print(f"\n  本机访问:   http://localhost:{PORT}/")
            print(f"  手机访问:   http://{lan}:{PORT}/")
            print(f"              (手机需与电脑连同一 WiFi)")
            print("\n  按 Ctrl+C 停止\n")
            print("-" * 52)
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n已停止。")
    except OSError as e:
        print(f"\n端口 {PORT} 被占用或出错：{e}")
        print("可以修改本文件顶部的 PORT 变量换一个端口。")
        sys.exit(1)


if __name__ == "__main__":
    main()
