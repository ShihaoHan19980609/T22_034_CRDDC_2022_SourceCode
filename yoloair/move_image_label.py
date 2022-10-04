import os
import shutil
from tqdm import tqdm

# "Japan", "India", "Czech", "Norway", "United_States", "China_MotorBike", "China_Drone"
path = os.path.join('RDD2022', 'VOCdevkit')
if os.path.exists(path):
    print('VOCdevkit已存在')
    pass
else:
    os.makedirs(path)
image_path = os.path.join(path, 'images')  # 训练集路径
if os.path.exists(image_path):
    print('images已存在')
    pass
else:
    os.makedirs(image_path)
label_path = os.path.join(path, 'annotations')  # 训练集标签路径
if os.path.exists(label_path):
    print('annotations已存在')
    pass
else:
    os.makedirs(label_path)
countries = os.listdir('RDD2022')
train_image_txt = open('all_country.txt', "w")
for country in countries:
    if country not in {"Japan", "India", "Czech", "Norway", "United_States", "China_MotorBike"}:
        continue
    each_country_list = open(country + '.txt', "w")
    train_images_path = os.path.join('RDD2022', country, 'train/images')
    train_labels_path = os.path.join('RDD2022', country, 'train/annotations/xmls')
    train_image_list = os.listdir(train_images_path)
    train_label_list = os.listdir(train_labels_path)
    # print(country, '训练集:', len(train_image_list))
    for img in tqdm(train_image_list):
        full_image_path = os.path.join(train_images_path, img)
        full_label_path = os.path.join(train_labels_path, img).replace('jpg', 'xml')
        if not os.path.exists(full_label_path):
            print(full_image_path, '不存在对应标注!')
            pass
        shutil.copy(full_image_path, image_path)  # 移动训练集图片
        shutil.copy(full_label_path, label_path)
        new_image_path = os.path.join(image_path, img)
        new_label_path = os.path.join(label_path, img.replace('jpg', 'xml'))
        each_country_list.write(new_image_path + "\n")
        train_image_txt.write(new_image_path + "\n")  # 新路径
    each_country_list.close()
train_image_txt.close()
