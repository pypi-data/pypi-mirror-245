# -*- coding: UTF-8 -*-
import pyuc
from pyuc.py_api_b import PyApiB
if PyApiB.tryImportModule("bs4",installName="bs4"):
    from bs4 import BeautifulSoup
if PyApiB.tryImportModule("imaplib", installName="imaplib"):
    import imaplib,email
    from email.message import Message


class EmailPartInfo:

    def __init__(self, part:Message):
        self.__contentType = part.get_content_type()
        self.__contentHtml = None
        self.__contentPlain = None
        self.__content:bytes = part.get_payload(decode=True)
        if self.__contentType == "text/html":
            self.__contentHtml:BeautifulSoup = None if self.__content==None else pyuc.htmlU().parseByStr(self.__content.decode('utf-8'))
        elif self.__contentType == "multipart/alternative":
            pass
        elif self.__contentType == "text/plain":
            self.__contentPlain:str = "" if self.__content==None else self.__content.decode('utf-8')


    @property
    def contentType(self)->str:
        return self.__contentType

    @property
    def contentHtml(self)->BeautifulSoup:
        return self.__contentHtml

    @property
    def contentPlain(self)->str:
        return self.__contentPlain

    @property
    def contentBytes(self)->bytes:
        return self.__content

    @property
    def contentStr(self)->str:
        return "" if self.__content==None else self.__content.decode('utf-8')

    def __findOriginParm(self, key):
        if self.contentType == "text/plain":
            plains = self.contentPlain.split("\n")
            for p in plains:
                if p.startswith(f"{key}: "):
                    return p[len(f"{key}: "):]
        elif self.contentType == "text/html":
            aas = self.contentHtml.find_all(attrs={"class": "xm_mail_oringinal_describe"})
            for aa in aas:
                p = aa.getText()
                if p.startswith(f"{key}: "):
                    return p[len(f"{key}: "):]
        else:
            return ""

    @property
    def From(self):
        return self.__findOriginParm("From")
    
    @property
    def To(self):
        return self.__findOriginParm("To")

    @property
    def Date(self):
        return self.__findOriginParm("Date")

    @property
    def Subject(self):
        return self.__findOriginParm("Subject")

    def __dict__(self):
        return {
            "From": self.From,
            "To": self.To,
            "Date": self.Date,
            "Subject": self.Subject,
            "ContentType": self.contentType,
            "content": self.contentStr
        }

    def __str__(self):
        return pyuc.jsonU().toString(self.__dict__())

class EmailU(PyApiB):
    """
    Email相关
    """
    @staticmethod
    def produce(key=None):
        return PyApiB._produce(key, __class__)

    def login(self, email, pswd):
        """ 登录 """
        if email.endswith("@qq.com"):
            self.imap_server = imaplib.IMAP4_SSL('imap.qq.com')
            self.imap_server.login(email, pswd)

    def getMailIds(self, mailbox="INBOX", query="(UNSEEN)"):
        """ 
        获取邮件id
        @mailbox 文件夹名
        @query   查找语句，例如：
                              "(FROM 'xxxx@qq.com') UNSEEN SINCE '11-28-2023'"   发件人，未读，日期
                              "SUBJECT 'xxxx'"      标题中有xxxx的邮件
        """
        self.imap_server.select(mailbox)
        status, data = self.imap_server.search(None,query.encode('utf-8'))
        return data[0].split()

        
    def getMail(self, mail_id):
        """ 获取邮件 """
        status, data = self.imap_server.fetch(mail_id, '(RFC822)')
        raw_email = data[0][1]
        # 解析邮件内容
        email_message = email.message_from_bytes(raw_email)
        mailPartInfos:list[EmailPartInfo] = []
        for part in email_message.walk():
            # 获取HTML格式的邮件内容
            mailPartInfos.append(EmailPartInfo(part))
        return mailPartInfos

    def markSeen(self, mail_id):
        self.imap_server.store(mail_id, "+FLAGS", "\SEEN") 

        