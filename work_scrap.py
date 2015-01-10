import smtplib
import requests
import bs4
import xlwt


def scrap_data_page(arg_pageItems=None):
    print "\n\n starting the work for part1 facebook apps \n\n"
    # to get the top apps from page
    if arg_pageItems:
        response = requests.get(
            'http://metricsmonk.com/rankings/custom?type=APP&dimension=MAU&category=all&gender=&age=&country=&date=&paging=' + arg_pageItems)
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
                launch_date_estimate = line.next.string  # .decode('unicode_escape').encode('ascii','ignore')
                print 'Launch Date Estimate: ', launch_date_estimate
            if line == 'User Rating':
                user_rating = line.next
                print "User Rating:", user_rating

        main_data_set.append([link, app_name, app_developer, mau, dau, app_type, category,
                              sub_category, launch_date_estimate, user_rating])

    print "\n\n\n main_data: ", main_data_set
    return main_data_set


# ========================================================================================================


def scrap_data_page_part2(url, arg_pageItems=None):
    print "\n\n starting the work for part2 iOS Apps\n\n"

    if arg_pageItems:
        part2_url = url + arg_pageItems
    else:
        part2_url = url

    part2_response = requests.get(part2_url)
    part2_soup = bs4.BeautifulSoup(part2_response.text)

    # import ipdb
    # ipdb.set_trace()
    part2_table = part2_soup.findChildren('table')[0]
    part2_links = []
    main_data_set = []

    for row in part2_table.findChildren('tr'):
        if row.findChildren('a'):
            link = row.find('a')['href']
            part2_links.append(link)

    for link in part2_links:
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
        Category = app_details_list[1].text
        Sub_category = app_details_list[-1].text

        print "Category: ", Category, "Sub_category: ", Sub_category
        print "\n\n"
        main_data_set.append([app_name, link, Category, Sub_category])

    return main_data_set

# ========================
# writing in xls file
#========================

filepath = '/home/stonex/game_data2.xls'


#  Call following fucntion with pageItems you want to scrap on main page.

def main_function(facebook_apps = None, Top_Free_iOS_Games_US = None, Top_Paid_iOS_Games_US = None,
                  Top_Grossing_iOS_Games_US = None, Top_Free_iPad_Games_US = None, Top_Paid_iPad_Games_US = None,
                  Top_Grossing_iPad_Games_US = None):

    filepath = '/home/stonex/game_data2.xls'


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
        for i, l in enumerate(main_data_part1):
            for j, col in enumerate(l):
                sheet1.write(i, j, col)

    if Top_Free_iOS_Games_US:
        main_data_part2_1 = scrap_data_page_part2(url=url_list[0])
        # writing data in sheet 2_1
        sheet2 = book.add_sheet("Top Free iOS Games (US)")
        for i, l in enumerate(main_data_part2_1):
            for j, col in enumerate(l):
                sheet2.write(i, j, col)

    if Top_Paid_iOS_Games_US:
        main_data_part2_2 = scrap_data_page_part2(url=url_list[1])
        # writing data in sheet 2_2
        sheet3 = book.add_sheet("Top Paid iOS Games (US)")
        for i, l in enumerate(main_data_part2_2):
            for j, col in enumerate(l):
                sheet3.write(i, j, col)

    if Top_Grossing_iOS_Games_US:
        main_data_part2_3 = scrap_data_page_part2(url=url_list[2])
        # writing data in sheet 2_3
        sheet4 = book.add_sheet("Top Grossing iOS Games (US)")
        for i, l in enumerate(main_data_part2_3):
            for j, col in enumerate(l):
                sheet4.write(i, j, col)

    if Top_Free_iPad_Games_US:
        main_data_part2_4 = scrap_data_page_part2(url=url_list[3])
        # writing data in sheet 2_4
        sheet5 = book.add_sheet("Top Free iPad Games (US)")
        for i, l in enumerate(main_data_part2_4):
            for j, col in enumerate(l):
                sheet5.write(i, j, col)

    if Top_Paid_iPad_Games_US:
        main_data_part2_5 = scrap_data_page_part2(url=url_list[4])
        # writing data in sheet 2_5
        sheet6 = book.add_sheet("Top Paid iPad Games (US)")
        for i, l in enumerate(main_data_part2_5):
            for j, col in enumerate(l):
                sheet6.write(i, j, col)

    if Top_Grossing_iPad_Games_US:
        main_data_part2_6 = scrap_data_page_part2(url=url_list[5])
        # writing data in sheet 2_6
        sheet7 = book.add_sheet("Top Grossing iPad Games (US)")
        for i, l in enumerate(main_data_part2_6):
            for j, col in enumerate(l):
                sheet7.write(i, j, col)

    # xls file is ready to sent in mail as attachment

    mail_user = "snehal.java@gmail.com"
    mail_pwd = ""
    FROM = 'mail_from'
    TO = ['mail_to'] #must be a list
    SUBJECT = "Testing sending using gmail"
    TEXT = """From: From Person <from@fromdomain.com>
              To: To Person <to@todomain.com>
              MIME-Version: 1.0
              Content-type: text/html
              Subject: SMTP HTML e-mail test

              This is an e-mail message to be sent in HTML format

              <b>This is HTML message.</b>
              <h1>This is headline.</h1>
              """

    # Prepare actual message
    message = """\From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        #server = smtplib.SMTP(SERVER)
        server = smtplib.SMTP("smtp.gmail.com", 587) #or port 465 doesn't seem to work!
        server.ehlo()
        server.starttls()
        server.login(mail_user, mail_pwd)
        server.sendmail(FROM, TO, message)
        #server.quit()
        server.close()
        print 'successfully sent the mail'
        return 0
    except:
        print "failed to send mail"
        return 1




# ====================================================================================================

main_data_part1 = scrap_data_page()

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

# no_pages = raw_input("Please enter the number of pages to srcap data: ")

# import ipdb
# ipdb.set_trace()
main_data_part2_1 = scrap_data_page_part2(url=url_list[0])
main_data_part2_2 = scrap_data_page_part2(url=url_list[1])
main_data_part2_3 = scrap_data_page_part2(url=url_list[2])
main_data_part2_4 = scrap_data_page_part2(url=url_list[3])
main_data_part2_5 = scrap_data_page_part2(url=url_list[4])
main_data_part2_6 = scrap_data_page_part2(url=url_list[5])

# filepath = raw_input("Please provide the file path with file name for xls file (i.e: /home/game.xls ): ")

print "\nwriting data to xls file path: ", filepath


# writing data in sheet 1
book = xlwt.Workbook(encoding="utf-8")
sheet1 = book.add_sheet("Part 1 game data")

for i, l in enumerate(main_data_part1):
    for j, col in enumerate(l):
        sheet1.write(i, j, col)

# writing data in sheet 2_1
sheet2 = book.add_sheet("Top Free iOS Games (US)")
for i, l in enumerate(main_data_part2_1):
    for j, col in enumerate(l):
        sheet2.write(i, j, col)

sheet3 = book.add_sheet("Top Paid iOS Games (US)")
for i, l in enumerate(main_data_part2_2):
    for j, col in enumerate(l):
        sheet3.write(i, j, col)

sheet4 = book.add_sheet("Top Grossing iOS Games (US)")
for i, l in enumerate(main_data_part2_3):
    for j, col in enumerate(l):
        sheet4.write(i, j, col)

sheet5 = book.add_sheet("Top Free iPad Games (US)")
for i, l in enumerate(main_data_part2_4):
    for j, col in enumerate(l):
        sheet5.write(i, j, col)

sheet6 = book.add_sheet("Top Paid iPad Games (US)")
for i, l in enumerate(main_data_part2_5):
    for j, col in enumerate(l):
        sheet6.write(i, j, col)

sheet7 = book.add_sheet("Top Grossing iPad Games (US)")
for i, l in enumerate(main_data_part2_6):
    for j, col in enumerate(l):
        sheet7.write(i, j, col)

print "\nwriting done"

book.save(filepath)

