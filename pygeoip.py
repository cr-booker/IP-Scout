#!/usr/bin/env python3
"""
A simple script that uses
'http://geoiplookup.net' api to get 
basic geo location information
for a given ip

Created: 07/04/2016
Python 3.x
Orginally written with qpython(3.2.2) for
Android.(Kit-kat)
"""
from bs4 import BeautifulSoup as bs
import ipaddress as ip #available Standard Lib in 3.3 or later
import os
import requests as req 
import socket
import tkinter as tk 
import tkinter.font as tkfont
from urllib.parse import urlparse

class Application():
    def __init__(self,master):
        """
        defines a gui window
        and its widgets.
        """
        #==========================Basic Window Config and Xml Tags======================================
        self.master = master #tk root window
        self.title = self.master.title('Py-Geo Ip Tool')   
        self.geo = self.master.geometry('550x300+200+200') 
        self.master.resizable(width= False, height= False)
        self.master.bind('<Return>',self.main)
        self.master.bind('<Escape>',lambda e: self.master.destroy())
        self.master.bind('<Delete>',self.clear_entry)
        self.tags = ['longitude', 'latitude', 'countryname', 
                     'countrycode', 'city', 'isp', 'host'] 
        self.headers = {'User-Agent':'Py-Geo Ip Tool'}
        #===========================Font, Image Files, and StringVar====================================
        self.about_image = tk.PhotoImage(file='images/bg.png')
        self.logo_image = tk.PhotoImage(file='images/globe.png')
        self.label_font = tkfont.Font(size=12, weight='bold', slant='italic')
        self.title_font = tkfont.Font(size=23, weight='bold', slant='italic', underline=1)   
        self.entry_var = tk.StringVar()  
        #====================================Labels=====================================================
        self.about_image_label = tk.Label(self.master,image=self.about_image)
        self.about_image_label.pack(fill= 'both')
        self.entry_label = tk.LabelFrame(self.master, text='Enter Ip or URL>>>', fg='white', bg='#4e4e4e')
        self.entry_label.place(x=0, y =220)
        self.geo_info_label = tk.LabelFrame(self.master, text='Geo Location Info', bg='#4e4e4e',
                                            fg='white', labelanchor='n', height=290, width=289, font=self.label_font)
        self.geo_info_label.place(x= 250, y=0)
        #==================================Entry Widget=================================================
        self.entry_bar = tk.Entry(self.entry_label, relief='sunken', textvariable=self.entry_var)
        self.entry_bar.pack()
        self.entry_bar.focus()
        #===================================Buttons=====================================================
        self.go_button = tk.Button(self.master, bg='#4e4e4e', fg='white', text='Go!', command=self.main)  
        self.go_button.place(x=180, y=230)
        self.clear_button = tk.Button(self.master, bg='#4e4e4e', fg='white', text='Clear!', command=self.clear_entry)
        self.clear_button.place(x=173, y=265)
        #==================================Text Box=====================================================
        self.hud = tk.Text(self.geo_info_label, bg='#c9c9c9', width=40)
        self.hud.place(x=0, y=0)
    
    def display(self,tags):   
        """
        Displays Geo location information to
        text widget(self.hud)

        Parameters:
        -----------
        tags(list):
            List of tuple pairs to interate over.
        
        Return:
        -------
        Output(None)
        """
        for k,v in tags:
            entry = "".join([k.title(),':',v,'\n','\n'])
            self.hud.insert('1.0',entry) 
        self.master.after(1000)
               
    def clear_entry(self,*args):
        """
        Clears entry widget

        Paramaters:
        -----------
        None        

        Return:
        -------
        Output(None)
        """
        current = len(self.entry_bar.get())
        self.entry_bar.delete(0,current)  
    
    def empty_textbox(self):
        """
        Clears text widget

        Paramaters:
        -----------
        None
        
        Return:
        -------
        Output(None)
        """    
        if self.hud.compare("end-1c", "==", "1.0"):
            return
        self.hud.delete("1.0", 'end')  
      
    def get_geo(self,ip):
        """
        Parses xml using bs4 to get
        geo information on given ip.
           
        uses requests module to access 
        geoiplookup.net. joins api url with ip argument,
        creates a tuple of  all tags in xml file,then uses a 
        list comprehension to iterate over the tags and 
        extract the text within.
           
        Parameters:
        ----------
        ip(string):
            The ip address to obtain the geolocation info for
        
        Return:
        -------
        Output(list):
            List of tuple pairs
        """
        try:
           
            api_link = 'http://api.geoiplookup.net/?query='
            ip_link = ''.join([api_link,ip])
            res = req.get(ip_link,headers= self.headers)
            xml_soup = bs(res.text,'lxml')
            info = [xml_soup.find(i).get_text() for i in self.tags]
            pairings = list(zip(self.tags,info))
            return pairings
        except req.exceptions.ConnectionError:  
            self.hud.insert('1.0','http://geoiplookup.net\nis currently unavailable.')
   
    def main(self,*args):
        """
        Main function that gets user input
        calls get_geo and displays results
           
        Waits for user input,expects a properly formatted url or 
        ip address, will raise a Value or socket.gai Error otherwise.
           
        Enters the try block where the function 
        adds 'http://' to front of user string
        if it was not already present.  
        calls urlparse to split the newly concactanated string 
        into a tuple, where we take the second entry, the 'netloc',
        and plug it into the socket.gethostbyname() function.
     
        Displays results from get_geo function on self.hud text
        widget

        Parameters:
        ----------
        Args*

        Return:
        -------
        Output(None)
  
        Exceptions:
        -----------
        Value Error:
            Raised if ip.ipaddress() is given a malformed ip.
           
        req.HTTPError: 
            Raised if something goes wrong wile trying
            to access geoiplookup.net.
           
        socket.gaierror: 
            Raised when given a malformed url/ip or a url that
            doesnt exist.
        """
        self.empty_textbox()
        user_entry = self.entry_bar.get() 
        if not user_entry:
            return
        scheme = ('http://','https://')   
        try:
            ip.ip_address(user_entry)
            ip_info = self.get_geo(user_entry)
            self.display(ip_info)
        except (ValueError,req.HTTPError):
            try:
                if not user_entry.startswith(scheme):
                    user_entry = ''.join((scheme[0],user_entry))
                parse_results = urlparse(user_entry)
                result = socket.gethostbyname(parse_results[1]) 
                ip_info = self.get_geo(result)   
                self.display(ip_info) 
            except (ValueError,req.HTTPError,socket.gaierror):
                self.hud.insert('1.0','Invalid!Please check your entry\nand try again.')
                 
if __name__ == '__main__':
     root = tk.Tk()
     app = Application(root)
     tk.mainloop()
     
    
