import requests
from django.shortcuts import render, redirect
from datetime import time, datetime, timedelta
import base64
from PIL import Image
from io import BytesIO
import io
import numpy as np
import cv2
import json

def index(request):
    if request.method == 'POST':
        user_name = request.POST['user_name']
        return redirect('maple:equipment',user_name)
    return render(request,'maple/index.html')

def equipment(request,user_name):
    header = {
        'x-nxopen-api-key' : '',
    }
    character_name = user_name
    urlstring = 'https://open.api.nexon.com/maplestory/v1/id?character_name=' + character_name
    response = requests.get(urlstring,headers=header)
    ocid = response.json()['ocid']
    current_date = datetime.now()
    new_date = current_date - timedelta(days=1)
    formatted_date = new_date.strftime('%Y-%m-%d')
    urlstring = 'https://open.api.nexon.com/maplestory/v1/character/basic?ocid=' + ocid + '&date=' + formatted_date
    response = requests.get(urlstring,headers=header)
    response = response.json()
    world = {
        '스카니아':'https://i.namu.wiki/i/dfxogys6kCa4WF4pPjyiq2Y0r5WUfUsXFLaR3BnmaONqclU1ZuwLuVwENfjKe4uMhDlrjff0PhuyB1piTHKwGg.webp',
        '베라':'https://i.namu.wiki/i/TZ5WGxreOzdQbB5Ld7B59tLuAYRfi-sM0BT6j0cdwxjKxqP6w1AdUfChs0D0nCG6FPl_RQ7NVFz1iMvr28A9Qg.webp',
        '루나':'https://i.namu.wiki/i/0yrS0svA7fb9bR8CG6rNFErKjLuq48PkSH286Fzp69Vzh5nJisQruqSaxdK_hTyRqc7_RZqs1BBY9XuxhXDnMw.png',
        '제니스':'https://i.namu.wiki/i/I3PBXfziI9xDV16eHKAsx-9FOGlma1TQF1ta046JXaaBFXux0fHvSghcOUZdzYdW8ayktidjgAuMYIxHZb_0uQ.png',
        '크로아':'https://i.namu.wiki/i/XMsKojSy8J4di-1wNbq5LkbOiwU9e3EHNZJa-l9mCfBlujWtHywuNR4IIZTdr05pLhIxzJv4ozDzcaP9eiR27g.png',
        '유니온':'https://i.namu.wiki/i/_bZtNRvg-dalCP-ukOfk7IWlLvEURSnnbNHKx2Fd1VRmpyvVcd6qd_Pt_7JcDeluQss8XN_tVtXwl_RT5P6iDA.png',
        '엘리시움':'https://i.namu.wiki/i/9oiKn3TIIqGZc4d17IYd5EHt3cgGH1bY5bsrUUZy1NOM7cjCri8XuU7xXKm2qgWT_366mi40nDmi_C-PsQ4kNw.png',
        '이노시스':'https://i.namu.wiki/i/eGO_Bq9zvqWrE75KffQS8F5mhG0B3FmFWu3Y4QAgaI-zW6P1wjyUGzooG0bPbrj-H5nGPQdPHrVskpq_ddM0_Q.png',
        '레드':'https://i.namu.wiki/i/z_ee7Bhn6mQMUS8P3FvONPIcvYgpqd-OaePyY0biNVCFE8ljEou8dlkOmetdXt_icqz74l_zWo48goxotVSBfQ.png',
        '오로라':'https://i.namu.wiki/i/7LShf409xR4RoIhxpEywnzGGiM0WiVxeRQQXZQ7ZtUxYqppDzeaX0UtxWZUImOBsRqPISPPDaT7zfT6X20Yl9Q.webp',
        '아케인':'https://i.namu.wiki/i/Hr2OK1KvF9uNtClwxj9yboKV-2zX5ji67W-tn-dy_t0lfIEHyw5tXzNoOK_nZiaOW_9RcOhxm3XNPZ2kFugCBA.png',
        '노바':'https://i.namu.wiki/i/Ep4V5jW2QMaFiZDYjaR9_CLl1dJ1euA296TM8P-oJo0CMRKZlvifVqghhmxmPVBfpbyjo2auPWuDRybGUxhURw.png',
        '리부트':'https://i.namu.wiki/i/IJyccUBzDa6WOoEONVWn3pTct07AgIW8ZdKjJ3P9kep-HBqEN1pYsq70CjY_qx03eqtOiR_99urLgGIaUewRiw.webp',
        '리부트2':'https://i.namu.wiki/i/IJyccUBzDa6WOoEONVWn3pTct07AgIW8ZdKjJ3P9kep-HBqEN1pYsq70CjY_qx03eqtOiR_99urLgGIaUewRiw.webp',
    }
    guild = response['character_guild_name']
    world = world.get(response['world_name'], '')
    urlstring = 'https://open.api.nexon.com/maplestory/v1/character/item-equipment?ocid=' + ocid + '&date=' + formatted_date
    response2 = requests.get(urlstring,headers=header)
    equipment_data = response2.json()
    equipment_data = equipment_data['item_equipment']
    context = {
        '닉네임' : response['character_name'],
        '레벨': response['character_level'],
        '경험치': response['character_exp_rate'],
        '길드':response['character_guild_name'],
        '이미지':response['character_image'],
        '월드': world,
        '성별':response['character_gender'],
        'equipment_data':equipment_data,
    }
    return render(request,'maple/equipment.html',context)
