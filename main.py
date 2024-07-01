import asyncio
import nodriver as uc
import json

login_email = ""
login_pwd = ""
async def main():
    option = read_option('option.json')
    
    section = option['seats']['section']
    row = option['seats']['row']
    

    browser = await uc.start()
    page = await browser.get('https://auth.ticketmaster.com/as/authorization.oauth2?client_id=8bf7204a7e97.web.ticketmaster.us&response_type=code&scope=openid%20profile%20phone%20email%20tm&redirect_uri=https://identity.ticketmaster.com/exchange&visualPresets=tm&lang=en-us&placementId=mytmlogin&hideLeftPanel=false&integratorId=prd1741.iccp&intSiteToken=tm-us&deviceId=tQSfkNxoUcHHwbnHwMfDxsDGwcej32q9bpwWCQ&doNotTrack=false')
    await page.wait(10)
    await page.get_content()
    
    elems = await page.select_all('*[src]')
    for elem in elems:
            await elem.flash()

    print('Finding registration form input and enter...')

    await page.wait_for("input[type=email]", timeout=100)
    await page.wait_for("input[type=password]", timeout=100)

    email_input = await page.select("input[type=email]")
    await email_input.send_keys(login_email)

    pwd_input = await page.select("input[type=password]")
    await pwd_input.send_keys(login_pwd)

    sign_btn = await page.select("button[name=sign-in]")
    await sign_btn.click()

    print('Finished login...')
    await page.wait(10)
    print('Go to ticket list page.')

    await page.get(option['url'])
    await page.reload()
    await page.get_content()

    await page.wait_for(".quick-picks-container", timeout=100)
    print ("Now, purchase was prepared.")

    await page.wait_for('.sc-stoanl-6', timeout=100)
    await page.wait(5)

    btn_pre_checkout = await page.find(text=make_item_name(section, row), best_match=True, timeout=100)
    await btn_pre_checkout.click()

    await page.wait(5)

    btn_next = await page.select("button[data-analytics=quick-pick-buy-now]", timeout=100)
    await btn_next.click()

    await page.wait(3000000)

def read_option(file_path):
    data = dict()
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def make_item_name(section, row):
     txt = "Sec " + str(section) + " • " + "Row " + str(row)
     return txt

if __name__ == '__main__':
    uc.loop().run_until_complete(main())