import requests
from bs4 import BeautifulSoup
import os


# 获取除了图片以外的HTML页面
def getHTMLText(url, code='utf-8'):
    # 定义请求头
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"}
    # 发出get请求获取html页面资源
    html = requests.get(url, headers=headers)
    # 转成BeautifulSoup，可以供查询标签使用
    return BeautifulSoup(html.text, 'lxml')


# 按照分类创建输入目录
def mkdir(root_path, path):
    # 拼接存放图片的绝对路径
    path = os.path.join(root_path, str(path).strip())
    # 判断此路径是否已经存在
    if os.path.exists(path):
        # 进入到此文件夹中
        os.chdir(path)
        return path
    else:
        # 不存在，创建此路径
        os.makedirs(path)
        # 进入到此文件夹中
        os.chdir(path)
        return path


# 主程序入口
def main():
    # 获取图片存放的绝对路径
    root_path = os.path.abspath(os.path.dirname('search.py'))
    # 获取mzitu的Soup，用于后续查找使用
    main_page_soup = getHTMLText('https://www.mzitu.com/all/')
    # 查找每个需要打开的连接，打开这个连接后，里面的图片才是真正需要的爬的数据
    list_url = main_page_soup.find('div', class_='all').find('ul').find_all('a')
    # 获取到所有url，循环打开，获取里面图片
    for url in list_url:
        # 获取到连接的内容，座位输出文件夹的名称，可以做到分类输出
        title = url.get_text()
        # 按照标题创建文件夹，并进入到此文件夹，准备后续写入图片
        mkdir(root_path + '/www.mzitu.com', title)
        # 获取每类标题图片的链接
        href = url['href']
        # 防盗链
        ref_headers = {'referer': href,
                       'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"}
        # 获取最大页码数
        # html_soup = getHTMLText(href)
        # max_num = html_Soup.find('div', class_='pagenavi').find_all('span')[-2].get_text()

        # 图片页码太多，所以这里我使用了固定5页，有需要全部的，把5可以替换成max_num+1
        for page in range(1, 5):
            # 由于图片有分页，每个图片翻页连接刚好是页码数，所以拼接页码数地址
            page_url = href + '/' + str(page)
            # 获取图片HTML元素
            picture_soup = getHTMLText(page_url)
            # 获取图片地址
            img_url = picture_soup.find('div', class_='main-image').find('img')['src']
            # 图片的url截取作为图片名称
            name = img_url[-9:-4]
            # 请求图片资源
            img = requests.get(img_url, headers=ref_headers)
            # 获取图片流
            f = open(name + '.jpg', 'ab')
            # 图片写道本地磁盘
            f.write(img.content)
            # 关闭写出流
            f.close()
            print(img_url)


main()

