# -*- coding: UTF-8 -*-
from selenium import webdriver
import time
import xlsxwriter
import configparser

conf = configparser.ConfigParser()
conf.read("music.ini")
qq_url = conf.get("target", "qq_url")
print(qq_url)

def read_qq_music(qq_url):
    # 添加 Chrome 相关配置
    options = webdriver.ChromeOptions()
    # 指定设备名称即可
    options.add_experimental_option('mobileEmulation', {'deviceName': 'iPhone X'})
    driver = webdriver.Chrome(chrome_options=options)  # => 打开浏览器时加入配置
    driver.get(qq_url)
    time.sleep(2)
    #把页面展示全。不停的点击“加载更多歌曲”
    while 1:
        time.sleep(1)
        try:
            driver.find_element_by_class_name('more_data').click()
        except Exception as e:
            break
    #创建表格
    workbook = xlsxwriter.Workbook('qq_music.xlsx')
    format_title = workbook.add_format({'bold': True, 'font_color': 'black', 'align': 'center'})
    format_row = workbook.add_format({'bold': False, 'font_color': 'black', 'align': 'center'})
    show = workbook.add_worksheet("qq音乐")
    # 设置行的计数器
    showrow = 0

    # 设置往每行execl插入数据的方法
    def show_add_row(wl, list, format):
        nonlocal showrow
        col = 0
        for tl in list:
            wl.write(showrow, col, tl, format)
            wl.set_column(0, 10, 30)
            col = col + 1
        showrow = showrow + 1
    #添加表格标题行
    title_list_1 = ['歌名', '歌手']
    show_add_row(show, title_list_1, format_title)

    #获取歌曲列表
    mod_song_list = driver.find_element_by_class_name('mod_song_list')
    #拆分成list
    music_list = mod_song_list.text.split('\n')
    driver.quit()
    while 1:
        if music_list != []:
            music_name = music_list.pop(0)
            music_author = music_list.pop(0)
            print([music_name, music_author])
            show_add_row(show, [music_name, music_author], format_row)
        else:
            break

    workbook.close()




read_qq_music(qq_url)