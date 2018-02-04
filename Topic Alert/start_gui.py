import tkinter as tk
from tkinter import messagebox
import Topic_Alert as TA
import time
from threading import Thread, Event


def delete_selection(listbox):
    sel= listbox.curselection()
    for index in sel[::-1]:
        listbox.delete(index)

class Controller(object):
    def __init__(self):
        self.thread1 =None
        self.stop_thread= Event()
        self.timer_sec=1800
        self.keywords=[]
        self.websites=[]
        self.email_option= False
        self.popup_option= False
    
    def notify_by_email(self):
        self.email_option= not self.email_option

    def notify_by_popup(self):
        self.popup_option= not self.popup_option

    def run_once(self):
        self.keywords= keyword_box.get(0,tk.END)
        self.websites= website_box.get(0,tk.END)
        email_addr= email_entry.get()
        TA.checkAlert(self.keywords, self.websites, self.email_option, self.popup_option, email_addr)

    def loop1(self):
        while not self.stop_thread.is_set():
            print("run once")
            self.run_once()
            time.sleep(self.timer_sec)

    def start_loop(self):
        try:
            timer_min= int(timer_entry.get())
            self.timer_sec= timer_min*1
            self.stop_thread.clear();
            self.thread1= Thread(target= self.loop1)
            self.thread1.start()
        except:
            tk.messagebox.showerror("Input Error", "Invalid timer setting")


    def stop_loop(self):
        self.stop_thread.set()
        self.thread1.join()
        self.thread1=None;
    


root=tk.Tk()
root.title("Topic Alert")
#root.geometry('800x640')

tk.Label(root,text="Article keywords").grid(row=0,column=0)
tk.Label(root,text="Websites").grid(row=0, column=2)


keyword_entry= tk.Entry(root);
keyword_entry.grid(row=1, column=0)

addkey_button=tk.Button(root, text="Add", command= lambda: keyword_box.insert(0,keyword_entry.get()))
addkey_button.grid(row=1, column=1)

website_entry= tk.Entry(root);
website_entry.grid(row=1, column=2)

addweb_button=tk.Button(root, text="Add", command= lambda: website_box.insert(0,website_entry.get()))
addweb_button.grid(row=1, column=3)

#keywords={'enhanced','transmission'}
#websites= {"http://www.osapublishing.org/oe/upcomingissue.cfm", "http://journals.aps.org/prl/recent", "http://www.nature.com/nphoton/research"}

keyword_box= tk.Listbox(root, selectmode=tk.EXTENDED);
website_box= tk.Listbox(root, selectmode=tk.EXTENDED);


keyword_box.grid(row=2,column=0)
website_box.grid(row=2,column=2)

delkey_button=tk.Button(root, text="Delete", command= lambda: delete_selection(keyword_box))
delkey_button.grid(row=2, column=1)

delweb_button=tk.Button(root, text="Delete", command= lambda: delete_selection(website_box))
delweb_button.grid(row=2, column=3)

control = Controller()

tk.Label(root, text="Notification by:").grid(row=3, column=0)

email_check=tk.Checkbutton(root, text="E-mail", command= control.notify_by_email)
email_check.grid(row=3, column=1)

popup_check= tk.Checkbutton(root, text="Pop-up", command= control.notify_by_popup)
popup_check.grid(row=3, column=2)

tk.Label(root, text="Timer:").grid(row=4, column=0)
tk.Label(root, text="/min").grid(row=4, column=2)
tk.Label(root, text="Email:").grid(row=4, column=3)

timer_entry= tk.Entry(root)
timer_entry.grid(row=4, column=1)
email_entry= tk.Entry(root)
email_entry.grid(row=4, column=4)



run_button = tk.Button(root, text="Run", command= control.start_loop)
run_button.grid(row=5,column=0)

stop_button = tk.Button(root, text="Stop", command= control.stop_loop)
stop_button.grid(row=5,column=1)

update_button = tk.Button(root, text="Check now", command=control.run_once)
update_button.grid(row=5,column=2)

file= open('TextFile1.txt', 'w',encoding='utf-8')
file.write('{}')
file.close()
root.mainloop()