from requests import *
import os
from json import *
import _thread

savepath="C:\\Users"

def get_and_save(vid,path):
    headers={'user-agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Mobile Safari/537.36'}
    print("getting HTML...",end=' ')
    r=get(url='https://m.bilibili.com/video/'+vid,headers=headers)
    html=r.text
    print("done! parsing...")
    vurl=(html[html.find('readyVideoUrl: ')+18:html.find("readyDuration")-15])
    name=html[html.find('''data-vue-meta="true">''')+21:html.find("</title>")]
    if os.path.exists(path+name+'.mp4')==False:
        print("downloading video...",end=' ')
        resp = get('ht'+vurl,headers=headers)
        print("done!\nsaving video...",end=' ')
        with open(path+name+'.mp4','wb') as f:
            f.write(resp.content)
        print("done!")
    return path+name+'.mp4'

def translate(inputpath):
    outputpath=inputpath[:-4]+'.mp3'
    if os.path.exists(outputpath)==False:
        #print("ffmpeg -i \""+inputpath+"\" -vn  -acodec libmp3lame -ac 2 -qscale:a 4 -ar 48000 \""+outputpath+"\"")
        os.system("ffmpeg -i \""+inputpath+"\" -vn  -acodec libmp3lame -ac 2 -qscale:a 4 -ar 48000 \""+outputpath+"\"")
        return "ok"
    else:
        return "ahh"

def solve(keyword,num):
    page=0
    while num>0:
        page+=1
        r=get(url="https://api.bilibili.com/x/web-interface/search/type?context=&page={}&order=totalrank&keyword=%{}&duration=0&tids_2=&__refresh__=true&_extra=&search_type=video&tids=119&highlight=1&single_column=0".format(page,keyword)).text
        r=loads(r)
        for i in r['data']['result']:
            t=i['typename']
            if (t!="教程演示"):
                u=i['arcurl'][i['arcurl'].rfind('/')+1:]
                print(t,u,i['title'])
                try:
                    if "ahh"!=translate(get_and_save(u,savepath)):
                        num-=1
                except:
                    print("continue")
            if num==0:
                break

def main():
	savepath=input("保存目录>>")
    while True:
        keyword=input("info>>")
        num=int(input("howmany>>"))
        _thread.start_new_thread( solve, (keyword, num, ) )

if __name__=='__main__':
    main()