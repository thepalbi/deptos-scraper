import imp
from playwright.sync_api import sync_playwright, Request

target = "https://www.zonaprop.com.ar/departamentos-venta-belgrano-nunez-saavedra-con-balcon-mas-de-2-ambientes-mas-de-1-garage-mas-45-m2-cubiertos-hasta-20-anos-75000-145000-dolar-orden-publicado-descendente.html"

def handle_req_finished(req: Request):
    if req.url == target:
        print("Finished with status: ", req.response().status)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto(target)
    page.on("requestfinished", handle_req_finished)
    print(page.content())
    browser.close()