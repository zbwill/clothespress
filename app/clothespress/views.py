# coding:utf-8
import os
import time

from flask import request, redirect, url_for, render_template, flash
from werkzeug.utils import secure_filename

from app.clothespress.resize_img import resize_img
from utils.Log import LOG
from . import clothespress
from config import Config
from ..models import Clothes, ClothesType, Tag
from .. import db


@clothespress.route('/')
def index():
    clothes_list = Clothes.query.all()
    clothes_list = [clothes_list[i:i+4] for i in range(0,len(clothes_list),4)]
    return render_template('clothespress/index.html', clothesList=clothes_list)


@clothespress.route('/clothesByType/<int:clothesTypeId>')
def clothes_by_type(clothesTypeId):
    clothesType = ClothesType.query.get_or_404(clothesTypeId)
    clothes_list = Clothes.query.filter_by(clothesTypeId=clothesTypeId).all()
    clothes_list = [clothes_list[i:i + 4] for i in range(0, len(clothes_list), 4)]
    return render_template('clothespress/clothesByType.html', clothesList=clothes_list, clothesType=clothesType)

@clothespress.route('/modifyClothes/<int:clothesId>', methods=['GET', 'POST'])
def modify_clothes(clothesId):
    clothes_type_list = ClothesType.query.all()
    clothes = Clothes.query.get_or_404(clothesId)
    if request.method == 'GET':
        return render_template('clothespress/modifyClothes.html', clothes=clothes, clothesTypeList=clothes_type_list)
    if request.method == 'POST':
        clothes.remark = request.form.get('desc')
        clothes.clothesTypeId = request.form.get('clothesType')
        try:
            db.session.commit()
            flash('衣服修改成功')
        except Exception as err:
            LOG.error(str(err))
            db.session.rollback()
            flash('衣服修改失败')
        return redirect(url_for('clothespress.clothes_info', clothesId=clothesId))


@clothespress.route('/addClothes/', methods=['GET', 'POST'])
def add_clothes():
    clothes_type_list = ClothesType.query.all()
    if request.method == 'GET':
        return render_template('clothespress/addClothes.html', clothesTypeList=clothes_type_list)
    if request.method == 'POST':
        # 获取上传的图片
        file = request.files['imgFile']
        # 生成图片和缩略图在服务器上保存的路径
        pic_name = secure_filename(file.filename)
        timestamp = str(time.time()).replace('.', '')
        tmp_list = pic_name.rsplit('.', 1)
        filename = '{0}_{1}.{2}'.format(tmp_list[0], timestamp, tmp_list[1])
        thumbnail_name = '{0}_{1}_thumbnail.{2}'.format(tmp_list[0], timestamp, tmp_list[1])
        file_path = os.path.join(Config.BASE_DIR, 'img', filename)
        thumbnail_path = os.path.join(Config.BASE_DIR, 'img', thumbnail_name)
        # 保存图片
        file.save(file_path)
        # 生成缩略图
        resize_img(ori_img=file_path, dst_img=thumbnail_path)

        clothes = Clothes(picPath=Config.PIC_DOMAIN_URL+filename,
                          thumbnailPath=Config.PIC_DOMAIN_URL+thumbnail_name,
                          remark=request.form.get('desc'),
                          clothesTypeId=request.form.get('clothesType'))
        db.session.add(clothes)
        try:
            db.session.commit()
            flash('衣服添加成功')
        except Exception as err:
            LOG.error(str(err))
            db.session.rollback()
            flash('衣服添加失败')
        return redirect(url_for('clothespress.index'))


@clothespress.route('/deleteClothes/<int:clothesId>')
def delete_clothes(clothesId):
    clothes = Clothes.query.get_or_404(clothesId)
    db.session.delete(clothes)
    try:
        db.session.commit()
        flash('衣服删除成功')
    except Exception as err:
        db.session.rollback()
        flash('衣服删除失败')
        LOG.err(str(err))
    return redirect(url_for('clothespress.index'))


@clothespress.route('/clothesInfo/<int:clothesId>')
def clothes_info(clothesId):
    clothes = Clothes.query.get_or_404(clothesId)
    return render_template('clothespress/clothes.html', clothes=clothes)


@clothespress.route('/addClothesType/', methods=['GET', 'POST'])
def add_clothes_type():
    if request.method == 'GET':
        return render_template('clothespress/addClothesType.html')
    if request.method == 'POST':
        type_name = request.form.get('typeName')
        desc = request.form.get('desc')
        if ClothesType.query.filter_by(typeName=type_name).first():
            flash('已存在该分类')
        else:
            clothes_type = ClothesType(typeName=type_name, remark=desc)
            db.session.add(clothes_type)
            try:
                db.session.commit()
                flash('分类添加成功')
            except Exception as err:
                LOG.error(str(err))
                db.session.rollback()
                flash('分类添加失败')
        return redirect(url_for('clothespress.clothes_type_manage'))


@clothespress.route('/modifyClothesType/<int:clothesTypeId>', methods=['GET', 'POST'])
def modify_clothes_type(clothesTypeId):
    clothes_type = ClothesType.query.get_or_404(clothesTypeId)
    if request.method == 'GET':
        return render_template('clothespress/modifyClothesType.html', clothesType=clothes_type)
    if request.method == 'POST':
        type_name = request.form.get('typeName')
        desc = request.form.get('desc')
        if (type_name != clothes_type.typeName) and ClothesType.query.filter_by(typeName=type_name).first():
            flash('已存在该分类')
        else:
            clothes_type.typeName = type_name
            clothes_type.remark = desc
            db.session.add(clothes_type)
            try:
                db.session.commit()
                flash('分类添加成功')
            except Exception as err:
                LOG.error(str(err))
                db.session.rollback()
                flash('分类修改失败')
        return redirect(url_for('clothespress.clothes_type_manage'))


@clothespress.route('/clothesTypeManage/')
def clothes_type_manage():
    clothes_type_list = ClothesType.query.all()
    return render_template('clothespress/clothesTypeManage.html', clothesTypeList=clothes_type_list)


@clothespress.route('/deleteClothesType/<int:clothesTypeId>')
def delete_clothes_type(clothesTypeId):
    clothes_type = ClothesType.query.get_or_404(clothesTypeId)
    db.session.delete(clothes_type)
    try:
        db.session.commit()
        flash('类型删除成功')
    except Exception as err:
        db.session.rollback()
        flash('类型删除失败')
        LOG.err(str(err))
    return redirect(url_for('clothespress.clothes_type_manage'))

