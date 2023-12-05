from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException
from time import sleep
from auth import fb_login, fb_pass

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)

url = "https://tinder.com"
driver.get(url)

#Reject cookies
css_selector_reject_cookies = "div > div.Pos\(f\).Start\(0\).End\(0\).Z\(2\).Bxsh\(\$bxsh-4-way-spread\).B\(0\).Bgc\(\$c-ds-background-primary\).C\(\$c-ds-text-secondary\) > div > div > div.D\(f\)--ml > div:nth-child(2) > button > div.w1u9t036 > div.l17p5q9z"
reject_cookies_button = driver.find_element(By.CSS_SELECTOR,
                                            value=css_selector_reject_cookies)
reject_cookies_button.click()

#Click on log in
log_in = driver.find_element(By.LINK_TEXT, value="Inicia sesión")
log_in.click()

#Click on log in with fb
sleep(3)
log_in_fb_css = "main > div > div > div.Ta\(c\).H\(100\%\).D\(f\).Fxd\(c\).Pos\(r\) > div > div > div.H\(100\%\).D\(f\).Fxd\(c\) > div.Mt\(a\) > span > div:nth-child(2) > button > div.w1u9t036 > div.l17p5q9z > div > div"
log_in_fb_button = driver.find_element(By.CSS_SELECTOR,
                                             value=log_in_fb_css)
log_in_fb_button.click()

#Switch to fb login window
base_window = driver.window_handles[0]
fb_login_window = driver.window_handles[1]
driver.switch_to.window(fb_login_window)
#print(driver.title)

#Click on reject optional cookies
sleep(2)
reject_cookies_fb = driver.find_element(By.CSS_SELECTOR,
                                        value="[id^='u_0_g']")
reject_cookies_fb.click()

#Enter user/pass
user_input = driver.find_element(By.ID, value="email")
user_input.send_keys(fb_login)
pass_input = driver.find_element(By.ID, value="pass")
pass_input.send_keys(fb_pass)
pass_input.send_keys(Keys.ENTER)

#Switch back to main window:
driver.switch_to.window(base_window)
#print(driver.title)

#Probably need to confirm login in mobile, adding a long sleep
sleep(30)

#Allow location:
location_xpath = "/html/body/div[2]/main/div/div/div/div[3]/button[1]/div[2]/div[2]"
allow_location = driver.find_element(By.XPATH, value=location_xpath)
allow_location.click()
sleep(2)
#Disable notifications
disable_notifications_xpath = "/html/body/div[2]/main/div/div/div/div[3]/button[2]/div[2]/div[2]"
disable_notifications = driver.find_element(By.XPATH, value=disable_notifications_xpath)
disable_notifications.click()
sleep(2)

#There's a limit of 100 matches per day
for _ in range(100):
    sleep(1)
    try:
        body = driver.find_element(By.CSS_SELECTOR, "body")
        #Keyboard right key has the same effect as clicking "like" green heart
        body.send_keys(Keys.RIGHT)
    #In case it didn't have time to load the next choice
    except NoSuchElementException:
        sleep(2)
    #In case there's a match
    except ElementClickInterceptedException:
        print("There was a match!")
        match_popup = driver.find_element_by_css_selector(".itsAMatch a")
        match_popup.click()
driver.quit()
