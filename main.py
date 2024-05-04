
import asyncio
import datetime
from fileinput import FileInput
import logging,os,random,sys
from pathlib import Path
from pathlib import Path
from string import Template
import time
import os
from tinydb import TinyDB, Query
from dotenv import load_dotenv


load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
db = TinyDB('db.json')

from telebot.async_telebot import AsyncTeleBot
today = datetime.date.today()




dirf = os.getcwd()
# print output to the console
print(dirf)

folder = dirf+'/logs'

#Path(folder).mkdir(parents=True, exist_ok=False) # Create folder if not exists
filename =  datetime.datetime.now().strftime("%Y_%m_%d")



logging.basicConfig(filename=folder + '/log_' +filename + ".log" , format='%(filename)s: %(message)s',
                    level=logging.DEBUG , encoding='utf-8')



bot = AsyncTeleBot(TELEGRAM_TOKEN)

def read_file(dir, loai,group_id, user_id):
    list_dir = os.listdir(dir)
    filei = ''    
    while True:
        if not list_dir:
            filei = ''
            break
        filei = random.choice(list_dir) 
        im = Query()
        check = db.search((im.type == loai) & (im.user_id == user_id) & (im.file ==filei) & (im.group_id == group_id))          
        if not check:        
            break
        else:
            list_dir.remove(filei)        
    
    return filei
        
 
@bot.message_handler(commands=['gaixinh', 'gx'])
async def gaixinh(message):
     
    filei = read_file (dirf+"/data/images/", 'gaixinh',message.chat.id,message.from_user.id)           
    print(filei)
    if filei == '':
         
        await bot.reply_to(message, "Đã hết file mới")
    else:        
        photo = open(dirf+"/data/images/" + filei, 'rb')    
        await bot.send_photo(message.chat.id, photo, message_thread_id=message.message_thread_id )    
        db.insert({'type': 'gaixinh', 'user_id': message.from_user.id,'file':filei,'username':message.from_user.username , 'group_id': message.chat.id })

@bot.message_handler(commands=['18plus', '18+'])
async def sendphoto_18plus(message):
 
    filei = read_file (dirf+"/data/18plus/photos/", '18plus',message.chat.id,message.from_user.id)           
    print(filei)
    if filei == '':
         
        await bot.reply_to(message, "Đã hết file mới")
    else:        
        photo = open(dirf+"/data/18plus/photos/" + filei, 'rb')    
        await bot.send_photo(message.chat.id, photo, message_thread_id=message.message_thread_id )    
        db.insert({'type': '18plus', 'user_id': message.from_user.id,'file':filei, 'username':message.from_user.username, 'group_id': message.chat.id})
 
 

@bot.message_handler(commands=['videos', 'v18+'])
async def sendvideo_18plus(message):
 
    filei = read_file (dirf+"/data/18plus/video_files/", '18plus_video',message.chat.id,message.from_user.id)           
    print(filei)
    if filei == '':
         
        await bot.reply_to(message, "Đã hết file mới")
    else:        
        photo = open(dirf+"/data/18plus/video_files/" + filei, 'rb')    
        await bot.send_video(message.chat.id, photo, message_thread_id=message.message_thread_id )    
        db.insert({'type': '18plus_video', 'user_id': message.from_user.id,'file':filei,'username':message.from_user.username, 'group_id': message.chat.id})
 
@bot.message_handler(commands=['info', 'i'])
async def info(message):   
    path = Path(dirf+'/data/18plus/photos/')
    photo18plus = (sum(1 for x in path.glob('*') if x.is_file())) 
    
    path = Path(dirf+'/data/18plus/video_files/')
    video18plus = (sum(1 for x in path.glob('*') if x.is_file())) 

    template = """
    Tổng photo 18+ : $photo18plus file
    Tổng video 18+ : $video18plus file
    Cú Pháp: 
    /info : thông tin bot
    /videos : video 18+
    /18plus : photo 18+
    /gaixinh : gái binh thường 
    """
    prine = Template(template).substitute(photo18plus=photo18plus,video18plus=video18plus)
    
    await bot.reply_to(message, prine) 
 

while True:
    try:
        asyncio.run(bot.polling(non_stop=True, interval=1, timeout=0))
    except:
        time.sleep(5)