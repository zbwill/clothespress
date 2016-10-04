# coding:utf-8
import os
import time
from flask import request, redirect, url_for, render_template
from werkzeug.utils import secure_filename

from utils.Log import LOG
from . import clothespress
from config import Config


@clothespress.route('/')
def index():
    return render_template('clothespress/index.html')


@clothespress.route('/addClothes/', methods=['GET', 'POST'])
def add_clothes():
    if request.method == 'GET':
        return render_template('clothespress/addClothes.html')
    if request.method == 'POST':
        file = request.files['imgFile']
        filename = secure_filename(file.filename)
        timestamp = str(time.time()).replace('.', '')
        tmpList = filename.rsplit('.', 1)
        filename = '{0}_{1}.{2}'.format(tmpList[0], '_'+timestamp, tmpList[1])
        file.save(os.path.join(Config.BASE_DIR, 'img', filename))
        LOG.info('name: {name}'.format(name=request.form.get('name')))
        LOG.info('desc: {desc}'.format(desc=request.form.get('desc')))
        return redirect(url_for('clothespress.index'))