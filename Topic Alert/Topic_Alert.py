from urllib import request
from urllib import parse
from bs4 import BeautifulSoup
import chardet
import json
import re
import multiprocessing
from email.mime.text import MIMEText
import smtplib
from email.header import Header



def checkWebsites(keyWords, webSites, head):
    articleDict={}
    for url in webSites:
        req= request.Request(url, headers=head);
        response= request.urlopen(req);
        htmldata= response.read();

        charset=chardet.detect(htmldata);
        htmldata= htmldata.decode(charset["encoding"]);

        soup= BeautifulSoup(htmldata, 'lxml');

        urlParts=list( parse.urlsplit(url));

        rootUrlFlag=0;
        rootUrlEndPos=0;

        while rootUrlFlag<2 and rootUrlEndPos<5:
            if urlParts[rootUrlEndPos]:
                rootUrlFlag+=1;

            rootUrlEndPos+=1;

        for k in range(rootUrlEndPos,5):
            urlParts[k]='';
      
        rootUrl=parse.urlunsplit(urlParts);

        # LOCAL FILES FOR DEBUGGING
        #htmlFile= open('OE.html','r',encoding='utf-8');
        #soup= BeautifulSoup(htmlFile, 'html5lib');

        tagList= soup.find_all(name='a');

        for item in tagList:
            if item==None or item.string==None:
                continue;
            for keyWord in keyWords:
                if re.search (keyWord, item.string, re.IGNORECASE):
                    articleName= item.string.lstrip().rstrip();
                    articleUrl= item.get('href');
                    #print (articleName+'\n'+ rootUrl+articleUrl+'\n\n');
                    articleDict[articleName]= rootUrl+articleUrl;

        
    return articleDict

class send_email():
    add1 = 'lithiumHack2018'#@gmail.com
    psw = 'hack6666'
    host ='smtp.gmail.com'
    add2=str()
    dictData=dict()
    msg=MIMEText('')
    server=smtplib.SMTP_SSL()
    def __init__(self, dictData, add_to):
        self.add2 =add_to
        self.dictData=dictData
        text= ""
        index=1;
        for k,v in self.dictData.items():
            text+= str(index)+'. '+ k +'\n' + v +'\n\n'
            index+=1;

        self.msg =MIMEText(text,'plain','utf-8')
        subject ='Paper update'
        self.msg['Subject'] =Header(subject,'utf-8')
        #self.msg['From']= Header("host",'utf-8')
        #self.msg['To']= Header("user",'utf-8')
        #self.login()
        #self.send()
        self.server = smtplib.SMTP_SSL(self.host, 465)
        self.server.login(self.add1,self.psw)
        self.server.sendmail(self.add1, self.add2, self.msg.as_string())
        self.server.quit()



#comparing dictionaries
def new_items(old_dict, new_dict):
    res=dict()
    for k,v in new_dict.items():
        if not k in old_dict:
            res[k]=v
    return res

def is_email(email_addr):
    return len(email_addr)>=6

def checkAlert(keyWords, urlList, email_option, popup_option, email_addr):
    

    #keyWords= {'laser','enhanced'};

    #urlList= {"http://www.osapublishing.org/oe/upcomingissue.cfm", "http://journals.aps.org/prl/recent", "http://www.nature.com/nphoton/research"};

    head={ "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"};

    articleDict = checkWebsites(keyWords,urlList, head);
    
    oldArticleDict=json.load(open('TextFile1.txt'))
    
    updated_topic= new_items(oldArticleDict, articleDict)

    if len(updated_topic)>0:
        if email_option and is_email(email_addr):
            send_email(updated_topic,email_addr)
        
        if popup_option:
            index=1
            for k,v in updated_topic.items():
                print(str(index)+'. '+k+'\n'+v+'\n\n')
                index+=1
        file= open('TextFile1.txt','w',encoding='utf-8');
        file.write(json.dumps(articleDict))
        file.close()