from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import formatdate
import smtplib
import requests
import bs4
import xlwt
from email.mime.multipart import MIMEMultipart


def scrap_data_page(arg_page_items=None):
    print "\n\n starting the work for part1 facebook apps \n\n"
    # to get the top apps from page
    if arg_page_items:
        response = requests.get(
            'http://metricsmonk.com/rankings/custom?type=APP&dimension=MAU&category=all&gender=&age=&country=&date=&paging=' + arg_page_items)
    else:
        response = requests.get(
            'http://metricsmonk.com/rankings/custom?type=APP&dimension=MAU&category=all&gender=&age=&country=&date=&paging=')
    main_data_set = []
    links = []

    soup = bs4.BeautifulSoup(response.text)
    table = soup.findChildren('table')[0]

    for row in table.findChildren('tr'):
        if row.findChildren('a'):
            link = row.find('a')['href']
            links.append(link)

    print " \n\n Got links from main page \n\n "

    # sub link part to get the app data
    for link in links:
        app_developer = None
        app_type = None
        sub_category = None
        category = None
        launch_date_estimate = None
        user_rating = None

        print "\nURL link: ", link
        sub_response = requests.get(link)
        sub_soup = bs4.BeautifulSoup(sub_response.text)

        # for app name
        app_tag = sub_soup.findChildren('h1')[0]
        app_name = app_tag.text

        # for develop by
        if 'by' in app_name:
            app_developer = app_name.split('by')[1]
            app_name = app_name.split('by')[0]
            print "app_name: ", app_name
            print "app_developer: ", app_developer
        else:
            print "app_name: ", app_name

        # unicode remove:
        app_name = app_name.encode('utf8')

        # for MAU and DAU
        developerorplatform = sub_soup.select('div.developerorplatform')[0]
        mau_dau_data = developerorplatform.findChildren('th')
        mau = int(mau_dau_data[2].text.replace(',', ''))
        dau = int(mau_dau_data[3].text.replace(',', ''))

        # for category, sub_category, (type not yet final)
        left_menu = sub_soup.select('div#app_menubar_left')[0]

        for line in left_menu.strings:
            if line == 'Categories':
                cat_data = line.next
                cat_list = cat_data.split('>>')
                app_type = cat_list[0]

                if len(cat_list) == 2:
                    category = cat_list[1]
                elif len(cat_list) > 2:
                    sub_category = cat_list[2]
                else:
                    category = None
                    sub_category = None
                print "Type: ", app_type, "Category: ", category, " Sub_category: ", sub_category
            if line == 'Launch Date Estimate':
                launch_date_estimate = line.next.string
                print 'Launch Date Estimate: ', launch_date_estimate
            if line == 'User Rating':
                user_rating = line.next
                print "User Rating:", user_rating

        main_data_set.append([link, app_name, app_developer, mau, dau, app_type, category,
                              sub_category, launch_date_estimate, user_rating])

    return main_data_set

# ========================================================================================================


def scrap_data_page_part2(url, arg_page_items=None):
    print "\n\n starting the work for part2 iOS Apps\n\n"

    if arg_page_items:
        part2_url = url + arg_page_items
    else:
        part2_url = url

    part2_response = requests.get(part2_url)
    part2_soup = bs4.BeautifulSoup(part2_response.text)

    part2_table = part2_soup.findChildren('table')[0]
    part2_links = []
    main_data_set = []

    for row in part2_table.findChildren('tr'):
        if row.findChildren('a'):
            link = row.find('a')['href']
            part2_links.append(link)

    for link in part2_links:
        category = None
        sub_category = None
        app_developer = None
        sub_response = requests.get(link)
        sub_soup = bs4.BeautifulSoup(sub_response.text)

        # for app name
        app_tag = sub_soup.findChildren('h1')[0]
        app_name = app_tag.text

        # for develop by
        if 'by' in app_name:
            app_developer = app_name.split('by')[1]
            app_name = app_name.split('by')[0]
            print "app_name: ", app_name
            print "app_developer: ", app_developer
        else:
            print "app_name: ", app_name
        # unicode remove:
        app_name = app_name.encode('utf8')

        app_details_list = sub_soup.select('div#app_menubar_left a')
        if len(app_details_list) >= 1:
            category = app_details_list[1].text
            sub_category = app_details_list[-1].text

        print "Category: ", category, "Sub_category: ", sub_category
        print "\n\n"
        main_data_set.append([app_name, link, app_developer, category, sub_category])

    return main_data_set

#  Call following fucntion with pageItems you want to scrap on main page.

def main_function(facebook_apps=None, top_free_ios_games_us=None, top_paid_ios_games_us=None,
                  top_grossing_ios_games_us=None, top_free_ipad_games_us=None, top_paid_ipad_games_us=None,
                  top_grossing_ipad_games_us=None):

    book = xlwt.Workbook(encoding="utf-8")

    url_list = [
                'http://metricsmonk.com/rankings_ios?country=US&type=1&category=6014',
                # 'http://metricsmonk.com/rankings_ios?country=US&type=1&tCat=GAMES&category=6014&date=06%2F26%2F2014',

                'http://metricsmonk.com/rankings_ios?country=US&type=2&category=6014',
                # 'http://metricsmonk.com/rankings_ios?country=US&type=2&tCat=GAMES&category=6014&date=06%2F26%2F2014',

                'http://metricsmonk.com/rankings_ios?country=US&type=3&category=6014',
                # 'http://metricsmonk.com/rankings_ios?country=US&type=3&tCat=GAMES&category=6014&date=06%2F26%2F2014',

                'http://metricsmonk.com/rankings_ios?country=US&type=4&category=6014',
                # 'http://metricsmonk.com/rankings_ios?country=US&type=4&tCat=GAMES&category=6014&date=06%2F26%2F2014',

                'http://metricsmonk.com/rankings_ios?country=US&type=5&category=6014',
                # 'http://metricsmonk.com/rankings_ios?country=US&type=5&tCat=GAMES&category=6014&date=06%2F26%2F2014',

                'http://metricsmonk.com/rankings_ios?country=US&type=6&category=6014',
                # 'http://metricsmonk.com/rankings_ios?country=US&type=6&tCat=GAMES&category=6014&date=06%2F26%2F2014'
            ]

    if facebook_apps:
        main_data_part1 = scrap_data_page()
        # writing data in sheet 1
        sheet1 = book.add_sheet("Facebook Apps")
        headers = ['App Name', 'URL', 'Developer', 'MAU', 'DAU', 'Type', 'Category', 'Sub- category', 'Launch Date Estimate',
                                                                                              'User Rating']

        row, col = 0, 0
        for col in range(col, len(headers)):
            sheet1.write(row, col, headers[col])

        for i, l in enumerate(main_data_part1, start=1):
            for j, col in enumerate(l):
                sheet1.write(i, j, col)

    if top_free_ios_games_us:
        main_data_part2_1 = scrap_data_page_part2(url=url_list[0])
        # writing data in sheet 2_1
        sheet2 = book.add_sheet("Top Free iOS Games (US)")
        headers = ['App Name', 'URL', 'Developer', 'Category', 'Sub- category']

        row, col = 0, 0
        for col in range(col, len(headers)):
            sheet2.write(row, col, headers[col])

        for i, l in enumerate(main_data_part2_1, start=1):
            for j, col in enumerate(l):
                sheet2.write(i, j, col)

    if top_paid_ios_games_us:
        main_data_part2_2 = scrap_data_page_part2(url=url_list[1])
        # writing data in sheet 2_2
        sheet3 = book.add_sheet("Top Paid iOS Games (US)")
        headers = ['App Name', 'URL', 'Developer', 'Category', 'Sub- category']

        row, col = 0, 0
        for col in range(col, len(headers)):
            sheet3.write(row, col, headers[col])

        for i, l in enumerate(main_data_part2_2, start=1):
            for j, col in enumerate(l):
                sheet3.write(i, j, col)

    if top_grossing_ios_games_us:
        main_data_part2_3 = scrap_data_page_part2(url=url_list[2])
        # writing data in sheet 2_3
        sheet4 = book.add_sheet("Top Grossing iOS Games (US)")
        headers = ['App Name', 'URL', 'Developer', 'Category', 'Sub- category']

        row, col = 0, 0
        for col in range(col, len(headers)):
            sheet4.write(row, col, headers[col])

        for i, l in enumerate(main_data_part2_3, start=1):
            for j, col in enumerate(l):
                sheet4.write(i, j, col)

    if top_free_ipad_games_us:
        main_data_part2_4 = scrap_data_page_part2(url=url_list[3])
        # writing data in sheet 2_4
        sheet5 = book.add_sheet("Top Free iPad Games (US)")
        headers = ['App Name', 'URL', 'Developer', 'Category', 'Sub- category']

        row, col = 0, 0
        for col in range(col, len(headers)):
            sheet5.write(row, col, headers[col])

        for i, l in enumerate(main_data_part2_4, start=1):
            for j, col in enumerate(l):
                sheet5.write(i, j, col)

    if top_paid_ipad_games_us:
        main_data_part2_5 = scrap_data_page_part2(url=url_list[4])
        # writing data in sheet 2_5
        sheet6 = book.add_sheet("Top Paid iPad Games (US)")
        headers = ['App Name', 'URL', 'Developer', 'Category', 'Sub- category']

        row, col = 0, 0
        for col in range(col, len(headers)):
            sheet6.write(row, col, headers[col])

        for i, l in enumerate(main_data_part2_5, start=1):
            for j, col in enumerate(l):
                sheet6.write(i, j, col)

    if top_grossing_ipad_games_us:
        main_data_part2_6 = scrap_data_page_part2(url=url_list[5])
        # writing data in sheet 2_6
        sheet7 = book.add_sheet("Top Grossing iPad Games (US)")
        headers = ['App Name', 'URL', 'Developer', 'Category', 'Sub- category']

        row, col = 0, 0
        for col in range(col, len(headers)):
            sheet7.write(row, col, headers[col])

        for i, l in enumerate(main_data_part2_6, start=1):
            for j, col in enumerate(l):
                sheet7.write(i, j, col)

    # xls file is ready to sent in mail as attachment
    # ==================================================================================
    # following are mail settings, please config it, or use your own mail send function
    # and attach excel file created here

    filename = 'scrap_data.xls'
    book.save(filename)

    msg = MIMEMultipart()
    send_from = 'mail_from'
    send_to = 'mail_to'
    msg['From'] = 'mail_from'
    msg['To'] = 'mail_to'
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = "mail with excel attachment"
    msg.attach(MIMEText("text data"))

    part = MIMEBase('application', "octet-stream")
    part.set_payload(open(filename, "rb").read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename="scrap_data.xlsx"')
    msg.attach(part)

    #context = ssl.SSLContext(ssl.PROTOCOL_SSLv3)
    #SSL connection only working on Python 3+
    smtp = smtplib.SMTP("smtp.gmail.com", 587)
    smtp.starttls()
    try:
        smtp.login('mail_username', "mail_password")
        smtp.sendmail(send_from, send_to, msg.as_string())
        print "Successfully sent email"
    except Exception as e:
        print "Error: unable to send email, Exception: ", e

    smtp.quit()

if __name__ == '__main__':
    # calling main function here with all the options to pass here
    main_function(facebook_apps=1, top_free_ios_games_us=1, top_free_ipad_games_us=1, top_grossing_ios_games_us=1,
                  top_grossing_ipad_games_us=1, top_paid_ios_games_us=1, top_paid_ipad_games_us=1)

# ====================================================================================================
