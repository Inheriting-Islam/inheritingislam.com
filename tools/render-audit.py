#!/usr/bin/env python3
"""Drive Chrome over CDP: exact device metrics (macOS won't let a real window go
narrow), full-page capture, and an overflow/console audit per page."""
import json, subprocess, time, os, sys, base64, urllib.request, websocket, shutil

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
PORT = 9333
PROFILE = "/tmp/cdp-profile-ii"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "shots")
os.makedirs(OUT, exist_ok=True)


class Tab:
    def __init__(self, port=PORT):
        info = json.load(urllib.request.urlopen(f"http://127.0.0.1:{port}/json"))
        page = [t for t in info if t["type"] == "page"][0]
        self.ws = websocket.create_connection(page["webSocketDebuggerUrl"],
                                              timeout=40, max_size=200 * 1024 * 1024)
        self.i = 0

    def send(self, method, **params):
        self.i += 1
        self.ws.send(json.dumps({"id": self.i, "method": method, "params": params}))
        while True:
            msg = json.loads(self.ws.recv())
            if msg.get("id") == self.i:
                if "error" in msg:
                    raise RuntimeError(f"{method}: {msg['error']}")
                return msg.get("result", {})


def start():
    shutil.rmtree(PROFILE, ignore_errors=True)
    p = subprocess.Popen([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                          f"--remote-debugging-port={PORT}", f"--user-data-dir={PROFILE}",
                          "--no-first-run", "--remote-allow-origins=*",
                          "--window-size=1200,900", "about:blank"],
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for _ in range(60):
        try:
            urllib.request.urlopen(f"http://127.0.0.1:{PORT}/json", timeout=1)
            return p
        except Exception:
            time.sleep(0.25)
    raise RuntimeError("chrome did not start")


def shoot(tab, url, path, width, height, full=True, scale=2, mobile=False):
    tab.send("Emulation.setDeviceMetricsOverride", width=width, height=height,
             deviceScaleFactor=scale, mobile=mobile)
    tab.send("Page.enable")
    tab.send("Runtime.enable")
    tab.send("Page.navigate", url=url)
    time.sleep(1.5)
    # force any reveal-on-scroll content in
    tab.send("Runtime.evaluate", expression="document.querySelectorAll('.reveal').forEach(e=>e.classList.add('in'))")
    time.sleep(0.4)
    audit = tab.send("Runtime.evaluate", expression="""JSON.stringify({
        sw: document.documentElement.scrollWidth, iw: window.innerWidth,
        h: document.documentElement.scrollHeight,
        title: document.title,
        wide: [...document.querySelectorAll('body *')].filter(e=>e.getBoundingClientRect().right > window.innerWidth+1)
                .slice(0,6).map(e=>e.tagName+'.'+(e.className&&e.className.toString().slice(0,40)))
    })""", returnByValue=True)["result"]["value"]
    shot = tab.send("Page.captureScreenshot", format="png", captureBeyondViewport=full,
                    fromSurface=True)
    open(path, "wb").write(base64.b64decode(shot["data"]))
    return json.loads(audit)


if __name__ == "__main__":
    proc = start()
    try:
        tab = Tab()
        base = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8792"
        pages = sys.argv[2].split(",") if len(sys.argv) > 2 else ["/"]
        widths = [("d", 1440, 900, False), ("m", 390, 844, True)]
        themes = ["light", "dark"]
        bad = []
        for p in pages:
            for tag, w, h, mob in widths:
                for th in themes:
                    slug = (p.strip("/").replace("/", "-") or "home") + f"-{tag}-{th}"
                    url = f"{base}{p}?theme={th}"
                    a = shoot(tab, url, f"{OUT}/{slug}.png", w, h, mobile=mob)
                    over = a["sw"] > a["iw"] + 1
                    if over:
                        bad.append((slug, a["sw"], a["iw"], a["wide"]))
                    print(f"{slug:34} {a['sw']:>5}/{a['iw']:<5} h={a['h']:<6}"
                          f"{'  ** OVERFLOW ' + str(a['wide']) if over else ''}")
        print("\nOVERFLOWS:", len(bad))
    finally:
        proc.terminate()
