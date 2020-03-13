from PIL import Image
import os
import tensorflow as tf
import json


def image_batch():
    for i in range(400, 410):   # 1265):
        num = str(i + 1).zfill(4)
        filename = 'tuberculosis-phone-' + str(num) + '.json'
        img_name = 'tuberculosis-phone-' + str(num) + '.jpg'

        filepath = './Labels/' + filename
        in_file = open(filepath, "r")
        loc = json.load(in_file)
        in_file.close()

        image_path = './Original_dataset/' + img_name

        img = Image.open(image_path)
        black_img = Image.open(image_path)
        crop_single_image(img, loc, num, black_img)

        print('Finish cropping image {}'.format(num))


def crop_single_image(img, loc, num, black_img):
    #csv_path = '../BME590_ML_Final_Project/crop_image.py'
    #csv_path = os.path.join(os.path.dirname(__file__), csv_path)
    xmin = loc['xmin']
    xmax = loc['xmax']
    ymin = loc['ymin']
    ymax = loc['ymax']
    for i in range(len(xmin)):
        count = str(i + 1).zfill(2)
        xc = round((xmax[i] + xmin[i])/2)
        yc = round((ymax[i] + ymin[i])/2)
        coords_crop = (xc - 50, yc - 50, xc + 50, yc + 50)
        coords_black = (xmin[i], ymin[i], xmax[i], ymax[i])

        saved_location = './TB_Image/TB_Image_' + num + '_' + count + '.jpg'

        crop(img, coords_crop, saved_location)
        black_out_tb(black_img, coords_black)

    black_img.save('./Black Box Image/Image_w_black_box' + num + '.jpg')
    crop_non_tb(black_img, num)


def crop_non_tb(img, num):
    # random crop, 10 for each image
    for i in range(10):

        img_arr = tf.image.random_crop(img, [100, 100, 3])
        with tf.Session() as session:
            non_tb_img = session.run(img_arr)
        non_tb_img = Image.fromarray(non_tb_img)
        save = check_TB_region(non_tb_img)

        img_name = ('./Non-TB_Image/nonTB_Image_{}_{}.jpg'.format(num, i))
        if save == bool(1):
            print('Non-TB cropped image saved')
            non_tb_img.save(img_name)
        else:
            print('Image contains TB region')


def crop(image_obj, coords, saved_location):
    """
    :param img: the image to edit
    :param image_obj: original image
    :param coords: A tuple of x/y coordinates (x1, y1, x2, y2)
    :param saved_location: Path to save the cropped image
    :param coords2:
    :return:
    """

    save_TB = check_image_size(coords, image_obj)
    if save_TB is True:
        cropped_image = image_obj.crop(coords)
        cropped_image.save(saved_location)
    else:
        print('Outside of image bound')


def black_out_tb(img, coords2):

    pixelMap = img.load()
    pixelsNew = img.load()

    for i in range(img.size[0]):
        if coords2[0] <= i <= coords2[2]:
            for j in range(img.size[1]):
                if coords2[1] <= j <= coords2[3]:
                    pixelMap[i, j] = (0, 0, 0, 255)
                else:
                    pixelsNew[i, j] = pixelMap[i, j]


def check_TB_region(img):
    pixelMap = img.load()
    save = bool(1)
    for i in range(img.size[0]):
            for j in range(img.size[1]):
                if pixelMap[i, j] == (0, 0, 0):
                    save = bool(0)
    return save


def check_image_size(coords, img):
    save_TB = bool(1)
    if coords[0] < 0 or coords[1] < 0:
        save_TB = bool(0)
    if coords[2] > img.size[0]:
        save_TB = bool(0)
    if coords[3] > img.size[1]:
        save_TB = bool(0)
    return save_TB


if __name__ == '__main__':
    image_batch()
