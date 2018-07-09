from requests_html import HTMLSession
import time
session = HTMLSession()
proxie = {
    'http': 'http://127.0.0.1:1080',
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
    # 'Cookie': '__cfduid=d38a3b9c5846e5db96ef23a5eb78642e91530061695'
}

def duqu():
    with open('list.txt', 'r') as f:
        url_list = f.readlines()
    return url_list    
    

def mkdir(path):
    # 引入模块
    import os
    # 去除首位空格
    path=path.strip()
    # 去除尾部 \ 符号
    path=path.rstrip("\\")
 
    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists=os.path.exists(path)
 
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path) 
 
        print(path+' 创建成功')
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print(path+' 目录已存在')
        return False

def get_page_list(url):
    print('开始获取漫画分页列表')
    r = session.get(url,proxies=proxie)
    container = r.html.find('#single-navi p',first=True)
    title = r.html.find('h1',first=True).text
    num = len(container.links)
    link_list = [url+'/'+str(x) for x in range(1,num+2)]
    # print(link_list)
    # print(title)
    print('获取漫画分页列表完成')
    return title,link_list

def get_img_list(page_list):
    img_list = []
    for page in page_list:
        r = session.get(page,proxies=proxie)
        single_page_list = r.html.find('.entry-content img')
        img_list += [img.attrs['src'] for img in single_page_list]
    # print(img_list)
    print('获取图片列表完成')
    return img_list

def save(img_urls,title):
    n = 1
    mkpath = 'f:\\comic\\' + title
    mkdir(mkpath)
    for img_url in img_urls:
        res = session.get(img_url,proxies=proxie,headers=headers)
        # print(res.content)
        with open(mkpath + '\\%03d.jpg' % n,'wb') as f:
            f.write(res.content)
        total = len(img_urls)
        print('第%03d页下载完成/共%03d页' % (n,total))
        n += 1

if __name__ == '__main__':
    url_list = duqu()
    for url in url_list:
        url = url.strip()
        title,page_list = get_page_list(url)
        imgurls = get_img_list(page_list)
        save(imgurls,title)