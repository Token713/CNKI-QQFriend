# coding=gbk

import splinter
import time
import selenium
import os
import shutil

document_folder = os.path.abspath('.') + '\output'


def download_document(document_title):
    browser = splinter.Browser('chrome')
    browser.visit('http://www.cnki.net/')

    input_box = browser.find_by_id('txt_1_value1')
    input_box.fill(document_title.decode('gbk'))

    search_btn = browser.find_by_id('btnSearch')
    search_btn.click()

    # browser.find_by_css("body")

    browser.driver.switch_to_frame("iframeResult")
    first_link = browser.find_by_xpath('//*[@id="ctl00"]/table/tbody/tr[2]/td/table/tbody/tr[2]/td[2]/a')
    first_link.click()

    # browser = splinter.Browser('chrome')
    # browser.visit('http://www.cnki.net/KCMS/detail/detail.aspx?QueryID=0&CurRec=1&recid=&filename=JXCY201401007&dbname=CJFD2014&dbcode=CJFQ&pr=&urlid=&yx=&v=MTYyODdTN0RoMVQzcVRyV00xRnJDVVJMeWVaK1JxRnk3bFZiclBMelhJZDdHNEg5WE1ybzlGWTRSOGVYMUx1eFk=')

    detail_window = browser.driver.window_handles[1]
    browser.driver.close()
    browser.driver.switch_to.window(detail_window)

    pdf_link = browser.find_by_xpath('//*[@id="QK_nav"]/ul/li[2]/a')
    pdf_link.click()

    # browser.find_link_by_text(u"PDF下载")
    # browser.driver.quit()


def download_from_niuniu(document_title, entrance_no):
    options = selenium.webdriver.ChromeOptions()
    prefs = {'download.default_directory': document_folder}
    options.add_experimental_option("prefs", prefs)
    # options.add_argument('intl.charset_default=GBK')
    # options.add_argument('start-maximized')
    options.add_argument('lang=zh-CN')
    # options.add_argument('download.default_directory=' + os.path.abspath('.') + '\output')

    # dc = options.to_capabilities()
    # browser = splinter.Browser('chrome', desired_capabilities=dc)

    print 'go to the login page'
    browser = splinter.Browser('chrome', options=options)
    browser.visit('http://www.niuniulib.com/e/member/login/')

    print 'input username..'
    input_box_username = browser.find_by_id('username')
    input_box_username.fill('6007544018')

    print 'input password..'
    input_box_password = browser.find_by_id('password')
    input_box_password.fill('415344')

    # browser.choose('lifetime', '3600')

    print 'click "Submit"'
    search_btn = browser.find_by_name('Submit')
    search_btn.click()

    # browser.is_text_present('登录成功'.decode('gbk'), wait_time=10)
    print 'sleep 5 seconds..'
    time.sleep(5)

    print 'go to the main page'
    mainpage_link = browser.find_by_xpath('/html/body/div[2]/div[2]/div[4]/a[1]')
    mainpage_link.click()

    print 'go to the Chinese library page'
    chineselib_link = browser.find_by_xpath('//*[@id="content"]/div[1]/div[2]/dl[1]/dt/a')
    chineselib_link.click()

    # browser.visit('http://www.niuniulib.com/zhongwenku/')

    print 'go to one of the recommended entrances'
    recommended_link = browser.find_by_xpath('//*[@id="maincolumn"]/div[2]/div[2]/span[' + str(entrance_no) + ']/a')
    recommended_link.click()

    new_window = browser.driver.window_handles[1]
    browser.driver.close()
    browser.driver.switch_to.window(new_window)

    print 'sleep 5 seconds..'
    time.sleep(5)

    print 'input the title: ' + document_title.decode('gbk')
    input_box = browser.find_by_id('txt_1_value1')
    input_box.fill(document_title.decode('gbk'))

    print 'click "Search"'
    search_btn = browser.find_by_id('btnSearch')
    search_btn.click()

    browser.driver.switch_to_frame("iframeResult")

    try_time = 0
    while True:
        first_link = browser.find_by_xpath('//*[@id="ctl00"]/table/tbody/tr[2]/td/table/tbody/tr[2]/td[2]/a')
        try:
            print 'try to click the first article..'
            first_link.click()
            break
        except AttributeError, e:
            print AttributeError, ": ", e
            print "download_from_niuniu::first_link.click() failed, try_time = " + str(try_time)
            if try_time > 3:
                print "download_from_niuniu::first_link.click() failed, too many attempts, abort."
                browser.quit()
                return ''
            else:
                try_time += 1
                browser.reload()

    # browser = splinter.Browser('chrome')
    # browser.visit('http://www.cnki.net/KCMS/detail/detail.aspx?QueryID=0&CurRec=1&recid=&filename=JXCY201401007&dbname=CJFD2014&dbcode=CJFQ&pr=&urlid=&yx=&v=MTYyODdTN0RoMVQzcVRyV00xRnJDVVJMeWVaK1JxRnk3bFZiclBMelhJZDdHNEg5WE1ybzlGWTRSOGVYMUx1eFk=')

    detail_window = browser.driver.window_handles[1]
    browser.driver.close()
    browser.driver.switch_to.window(detail_window)

    pdf_link = browser.find_by_xpath('//*[@id="QK_nav"]/ul/li[2]/a')
    try:
        print 'try to download the article..'
        pdf_link.click()
    except AttributeError, e:
        print AttributeError, ": ", e
        print "download_from_niuniu::pdf_link.click() failed."
        browser.quit()
        return ''

    try:
        alert = browser.get_alert()
        print "alert text = " + alert.text
        if alert.text.contains("并发数"):
            print "download failed, too many people are downloading documents. Abort."
            alert.accept()
            browser.quit()
            return ''
    except selenium.common.exceptions.NoAlertPresentException, e:
        # print selenium.common.exceptions.NoAlertPresentException, ": ", e
        print "No alert window, good! go on.."

    document_file = is_document_downloaded()
    if document_file != '':
        print "download succeed, document_title = " + document_title.decode('gbk')
    else:
        print "download_from_niuniu failed, no file generated."
    browser.quit()
    return document_file

    # download_url = pdf_link['href']
    # print "download_url = " + download_url.decode('gbk')
    # import requests
    #
    # cookies = {browser.cookies.all()[0]["name"]: browser.cookies.all()[0]["value"]}
    # result = requests.get(download_url, cookies=cookies)
    # print "download succeed, document_title = " + document_title.decode('gbk')
    #
    # pdf = open("C:/111.pdf", 'w')
    # pdf.write(result.content)
    # pdf.close()
    # print "document generated, path = " + "C:/111.pdf"
    #
    # browser.quit()
    # return True


def do_delete():
    shutil.rmtree(document_folder)


def is_document_downloaded():
    try_time = 0
    while True:
        has_file = False
        for file in os.listdir(document_folder):
            has_file = True
            print "found file = " + file.decode('gbk')
            if file.endswith('.crdownload'):
                print "download not complete yet, try_time = " + str(try_time)
                if try_time < 5:
                    print "wait for 5 seconds to try again.."
                    try_time += 1
                    time.sleep(5)
                else:
                    print "already tried 5 times, abort."
                    return ""
            elif file.endswith('.pdf') or file.endswith('.caj'):
                print "download complete."
                return str(file)
            else:
                print "strange file found, filename = " + file.decode('gbk')
                return ""
        if not has_file:
            print "download is not started, abort."
            return ""

if __name__ == '__main__':
    # download_document('计算机')
    download_from_niuniu('中德两国高中生数学能力的分析及比较', 4)
    # do_delete()
    # is_document_downloaded()