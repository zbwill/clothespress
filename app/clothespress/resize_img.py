# coding:utf-8
from PIL import Image

from utils.Log import LOG


def resize_img(ori_img, dst_img, dst_w=200, dst_h=200, save_q=75):
    LOG.info('图像缩放过程...')
    LOG.info('原始图片路径: {filepath}'.format(filepath=ori_img))
    LOG.info('resize后图片路径: {filepath}'.format(filepath=dst_img))
    im = Image.open(ori_img)
    ori_w, ori_h = im.size
    LOG.info('原始图片宽: {ori_w}像素'.format(ori_w=ori_w))
    LOG.info('原始图片高: {ori_h}像素'.format(ori_h=ori_h))
    LOG.info('resize图片规则: 宽不超过{dst_w}像素, 高不超过{dst_h}像素, 等比缩放'.format(dst_w=dst_w, dst_h=dst_h))
    width_ratio = height_ratio = None
    ratio = 1
    if (ori_w and ori_w > dst_w) or (ori_h and ori_h > dst_h):
        if dst_w and ori_w > dst_w:
            width_ratio = float(dst_w) / ori_w
        if dst_h and ori_h > dst_h:
            height_ratio = float(dst_h) / ori_h
        if width_ratio and height_ratio:
            if width_ratio < height_ratio:
                ratio = width_ratio
            else:
                ratio = height_ratio
        if width_ratio and not height_ratio:
            ratio = width_ratio
        if height_ratio and not width_ratio:
            ratio = height_ratio
        new_width = int(ori_w * ratio)
        new_height = int(ori_h * ratio)
    else:
        new_width = ori_w
        new_height = ori_h
    im.resize((new_width, new_height), Image.ANTIALIAS).save(dst_img, quality=save_q)


if __name__ == '__main__':
    # 源图片
    ori_img = '/home/zhubo/workspace/clothespress/img/Desert__14755782164242022.jpg'
    # 目标图片
    dst_img = '/home/zhubo/workspace/clothespress/img/Desert__14755782164242022_thumbnail.jpg'
    # 目标图片大小
    dst_w = 200
    dst_h = 200
    # 保存的图片质量
    save_q = 75
    # 等比例压缩
    resize_img(ori_img=ori_img, dst_img=dst_img)
