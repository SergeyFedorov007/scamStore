from flask import Flask,session, render_template, request, flash, redirect, url_for
import datetime as dt
from flask import json
from typing import Dict, Any

app = Flask(__name__)
app.config['SECRET_KEY'] = '9918a0e4535fbb9771ac3d437f6f4570f84e51f2'
ADS_DATA:Dict[int, Any]={}




class Ads:
    def __init__(self, info: str,  time_to_del: dt.datetime):
        self.info = info
        self.time_to_del = time_to_del

    def checkTime(self) -> bool:
        # print(self.time_to_del, dt.datetime.now())
        return self.time_to_del > dt.datetime.now()

    def getContent(self) -> str:
        return self.info

    def getDate(self):
        return self.time_to_del.strftime("%Y-%m-%d")

    def getTime(self):
        return self.time_to_del.strftime("%H:%M")






def check_server_data():
    global ADS_DATA
    for id in list(ADS_DATA):
        if id in ADS_DATA.keys() and not ADS_DATA[id].checkTime():
            ADS_DATA.pop(id)

    if "ads_id_list" not in session:
        session["ads_id_list"] = []
    session["ads_id_list"] = list(filter(lambda x: x in ADS_DATA.keys(), session["ads_id_list"]))
    if not session.modified: #тк в сесии хранится не масив а ссылка на список лучше явно указать что мы именили данные
        session.modified = True

@app.route('/', methods=['GET', 'POST'])
def home():
    global ADS_DATA
    check_server_data()

    if request.method == 'POST':
        if request.form.get('add_redirect'):
            return redirect(url_for("add_page"))
        elif request.form.get('edit'):
            id = int(request.form.get('edit').replace('edit №', ''))
            return redirect(url_for("edit_page", id=id))






    return render_template('home.html', my_adds_id=session["ads_id_list"], all_ads=ADS_DATA)



@app.route('/add_ads', methods=['GET', 'POST'])
def add_page():
    global ADS_DATA
    if request.method == 'POST':
        if request.form.get('add_submit'):

            ads_content = request.form.get('ads_content')
            date_del = request.form.get('date_del')
            time_del = request.form.get('time_del')


            if ads_content == '':
                ads_content = 'dafaul_content'

            try:
                del_datetime = dt.datetime.strptime(date_del + ' ' + time_del , "%Y-%m-%d %H:%M")
            except ValueError: #удаляем через 30 секунд
                del_datetime = dt.datetime.now() + dt.timedelta(seconds=30)


            ad = Ads(ads_content, del_datetime)
            if not ad.checkTime():
                return render_template('add_ads.html')


            if ADS_DATA.keys():
                id = max(ADS_DATA.keys()) + 1
            else:
                id = 0


            ADS_DATA.update({id: ad})
            if "ads_id_list" not in session:
                session["ads_id_list"] = []

            session["ads_id_list"] += [id]
            if not session.modified: #тк в сесии хранится не масив а ссылка на список лучше явно указать что мы именили данные
                session.modified = True


            return redirect(url_for("home"))

    return render_template('add_ads.html')






@app.route('/edit', methods=['GET', 'POST'])
def edit_page():
    global ADS_DATA
    id = int(request.args['id'])
    if id not in ADS_DATA.keys():
        return redirect(url_for("home"))

    if request.method == 'POST':
        if request.form.get('change_submit'):
            ads_content = request.form.get('ads_content')
            date_del = request.form.get('date_del')
            time_del = request.form.get('time_del')


            if ads_content == '':
                ads_content = 'dafaul_content'

            try:
                del_datetime = dt.datetime.strptime(date_del + ' ' + time_del , "%Y-%m-%d %H:%M")
            except ValueError: #удаляем через 30 секунд
                del_datetime = dt.datetime.now() + dt.timedelta(seconds=30)

            ad = Ads(ads_content, del_datetime)
            if not ad.checkTime():
                return render_template('edit.html', id=id, info=ADS_DATA[id].getContent(), date=ADS_DATA[id].getDate(), time=ADS_DATA[id].getTime())

            ADS_DATA[id] = ad
            return redirect(url_for("home"))
        elif request.form.get('remove'):
            ADS_DATA.pop(id)
            return redirect(url_for("home"))



    return render_template('edit.html', id=id, info=ADS_DATA[id].getContent(), date=ADS_DATA[id].getDate(), time=ADS_DATA[id].getTime())








app.run(debug=True)
