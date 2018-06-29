from requests_html import HTMLSession
session = HTMLSession()
proxie = {
    'http': 'http://127.0.0.1:1080',
}
def get_page_list(url):
    print('开始获取漫画分页列表')
    r = session.get(url,proxies=proxie)
    container = r.html.find('#single-navi p',first=True)
    num = len(container.links)
    link_list = [url+'/'+str(x) for x in range(1,num+2)]
    # print(link_list)
    print('获取漫画分页列表完成')
    return link_list

def get_img_list(page_list):
    img_list = []
    for page in page_list:
        r = session.get(page,proxies=proxie)
        single_page_list = r.html.find('.entry-content img')
        for img in single_page_list:
            # print(img.attrs['src'])
            # print(img.attrs('src'))
            img_list.append(img.attrs['src'])
    # print(img_list)
    return img_list

page_list = get_page_list('http://www.177pic.info/html/2018/06/2138040.html')
get_img_list(page_list)