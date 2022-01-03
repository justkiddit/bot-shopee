from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

import datetime
import time

link_produk=time_target=None
sekarang=datetime.datetime.now()

def InputData() :
    global link_produk,time_target,sekarang
    link_produk=(input(' (#) Link Produk Shopee : '))
    jam=int(input(' (#) Jam Beli : '))
    menit=int(input(' (#) Menit Beli : '))
    detik=int(input(' (#) Detik Beli : '))
    time_target=datetime.datetime(sekarang.year,sekarang.month,sekarang.day,jam,menit,detik)

def SetupSelenium():
    ### Inisialisasi Awal
    binary=FirefoxBinary('system/firefox/firefox.exe')
    selenium=r'system/firefox/geckodriver.exe'

    ### Setup Profil
    firefox_profile = webdriver.FirefoxProfile('system/profile')

    ### Buka Browser
    browser=webdriver.Firefox(executable_path=selenium,firefox_binary=binary,firefox_profile=firefox_profile)

    ### Clear Cache & Cookie
    browser.delete_all_cookies()
    
    return browser

def click(browser,element_css):
    WebDriverWait(browser, 60).until(
        ec.visibility_of_element_located((By.CSS_SELECTOR, element_css))
    )
    WebDriverWait(browser, 60).until(
        ec.element_to_be_clickable((By.CSS_SELECTOR, element_css))
    )
    browser.find_element_by_css_selector(element_css).click()

InputData()
browser=SetupSelenium()
# Buka halaman login
browser.get("https://shopee.co.id/buyer/login")
wait = WebDriverWait(browser, 60)
# Cek udah login
wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR, '.shopee-avatar')))
# Buka produk
browser.get(link_produk)

# Countdown timer
countdown=time_target-datetime.datetime.now()
time.sleep(countdown.seconds)
browser.refresh()

# Button Tipe
click(browser,'button.product-variation:nth-child(2)')

# Button Beli Sekarang
click(browser,'button.btn--l:nth-child(2)')
WebDriverWait(browser, 60).until(
    ec.invisibility_of_element((By.CSS_SELECTOR, '.action-toast'))
)
# Button Checkout
click(browser,'.shopee-button-solid')
WebDriverWait(browser, 60).until(
    ec.invisibility_of_element((By.CSS_SELECTOR, '.loading-spinner-popup'))
)
# Metode Pembayaran via Shopee Pay
click(browser,'.checkout-payment-setting__payment-methods-tab > span:nth-child(2) > button:nth-child(1)')
click(browser,'.checkout-bank-transfer-item__card')
WebDriverWait(browser, 60).until(
    ec.invisibility_of_element((By.CSS_SELECTOR, '.loading-spinner-popup'))
)
# Buat Pesanan
click(browser,'button.stardust-button:nth-child(2)')
WebDriverWait(browser, 60).until(
    ec.invisibility_of_element((By.CSS_SELECTOR, '.loading-spinner-popup__container'))
)
# Konfirmasi pembayaran via Shopee Pay
click(browser,'#pay-button')