# CRDDC_2022_SourceCode
## 1.Clone repo and install requirements.txt in a Python>=3.7.0 environment, including PyTorch>=1.7.  
```python
git clone https://github.com/KentHan19980609/T22_034_han_shi_hao_CRDDC_2022_SourceCode.git
cd T22_034_han_shi_hao_CRDDC_2022_SourceCode/yoloair
pip install -r requirements.txt  # install
```

## 2.download the model  

model:https://pan.baidu.com/s/1z3s9YEG8encVnSAF-7cshw  password: l5h1  
data download from https://bigdatacup.s3.ap-northeast-1.amazonaws.com/2022/CRDDC2022/RDD2022/RDD2022.zip  
  
## 3.detect for each country
```python
#Japan
python detect.py --weight weight/all_640_5x_A.pt weight/Japan_448_5xTf.pt weight/Japan_640_5x_A.pt weight/Japan_640_5xTf.pt weight/Japan_640_yolov7.pt --country Japan --img 640 --source RDD2022/Japan/test/images/ --conf-thres 0.15 --iou-thres 0.999  --agnostic-nms --augment 
  
#India
python detect.py --weight weight/all_640_5x_A.pt weight/India_448_5x.pt weight/India_448_5xTf.pt weight/India_640_5x_A.pt weight/India_640_5xTf.pt weight/India_640_yolov7.pt --country India --img 640 --source RDD2022/India/test/images/ --conf-thres 0.15 --iou-thres 0.999  --agnostic-nms --augment 
  
#United_States
python detect.py --weight weight/all_640_5x_A.pt weight/US_640_5x_A.pt weight/US_640_5xTf.pt weight/US_640_yolov7.pt --country United_States --img 448 --source RDD2022/United_States/test/images/ --conf-thres 0.15 --iou-thres 0.999  --agnostic-nms --augment 
  
#Norway
python detect.py --weight weight/all_640_5x_A.pt weight/Norway_448_5xTf.pt weight/Norway_640_5x_A.pt weight/Norway_640_yolov7.pt --country Norway --img 640 --source RDD2022/Norway/test/images/ --conf-thres 0.15 --iou-thres 0.999  --agnostic-nms --augment 
  
#China_MotorBike
python detect.py --weight weight/all_640_5x_A.pt weight/Cz_Ch_640_5xTf.pt weight/China_640_5x_A.pt weight/Cz_Ch_640_yolov7.pt --country China_MotorBike --img 640 --source RDD2022/China_MotorBike/test/images/ --conf-thres 0.15 --iou-thres 0.999  --agnostic-nms --augment 
  
#Czech
python detect.py --weight weight/all_640_5x_A.pt weight/Cz_Ch_640_5xTf.pt weight/Czech_640_5x_A.pt weight/Cz_Ch_640_yolov7.pt --country Czech --img 640 --source RDD2022/Czech/test/images/ --conf-thres 0.15 --iou-thres 0.999  --agnostic-nms --augment 

```
## 4.Mix all country results  
```python
python mix_all_country.py
```
## 5.Process training images and labels  
Prepare for train
```python
python move_image_label.py 
python xml2yolo.py
```

## 6.Train  
```python
python train_val.py # get val.txt
```
For different countries, the corresponding data configuration file needs to be modified before training.  

Modify the data/road.yaml file training data to the file : all_ country.txt  
![image](https://user-images.githubusercontent.com/91840954/195822646-1dda3028-02dc-4498-b05a-a285b40de0b2.png)  
```
all_country.txt  
Japan.txt  
India.txt  
United_States.txt  
Norway.txt  
China_MotorBike.txt  
Czech.txt  
China_Czech.txt  
```
If the model does not use the Albumentations library, please modify the corresponding argument=False,as shown below:
![image](https://user-images.githubusercontent.com/91840954/195821951-4ec8156c-939a-41f8-a6cb-675fa845414c.png)  

The following table lists all model categories, A for  Albumentations  
![image](https://user-images.githubusercontent.com/91840954/195832044-548a646a-52e8-4e5d-b5cd-94fb355e7fe0.png)  

### 6.1 First train a general yolov5x model for all countries  
 
This model is used as the pre-training model for all the following yolov5x (including 640 and 448) models，not for yolov5x-transformer(640 and 448) and yolov7x-640  
```
#all-640-5x-Albumentations
python train.py --data data/road.yaml --cfg yolov5x_road.yaml --weight yolov5x.pt --batch-size 16 --img-size 640 --hyp data/hyps/hyp.scratch-low.yaml --epochs 300
```

### 6.2 We take the Japanese model as an example to train its five models  
First,replace with Japanese data  
```
#yolov5x-640
#Please replace the pre-training model parameters，  --weight {all-640-5x-Albumentations}
python train.py --data data/road.yaml --cfg yolov5x_road.yaml --weight yolov5x.pt --batch-size 16 --img-size 640 --hyp data/hyps/hyp.scratch-high.yaml --epochs 300
```

```
#yolov5x-448-Albumentations
#Please replace the pre-training model parameters，  --weight {all-640-5x-Albumentations}
python train.py --data data/road.yaml --cfg yolov5x_road.yaml --weight yolov5x.pt --batch-size 32 --img-size 448 --hyp data/hyps/hyp.scratch-low.yaml --epochs 100
```

```
#yolov5x-transformer-640
python train.py --data data/road.yaml --cfg yolov5x-transformer.yaml --weights '' --hyp data/hyps/hyp.scratch-high.yaml --batch-size 32 --img-size 640 --epochs 300
```

```
#yolov5x-transformer-448
python train.py --data data/road.yaml --cfg yolov5x-transformer.yaml --weights '' --hyp data/hyps/hyp.scratch-high.yaml --batch-size 16 --img-size 448 --epochs 300
```

```
#yolov7x-640
python yolov7/train.py --data data/road.yaml --cfg yolov7x.yaml --weight yolov7x.pt --hyp data/hyps/hyp.scratch-high.yaml --batch-size 16 --img-size 640 --epochs 300
```
### 6.3 For the rest of the countries, you can get it by referring to the training methods of Japan. Just change the data to the corresponding country.  
Please refer to the optimal results below to train the corresponding model  
![image](https://user-images.githubusercontent.com/91840954/195829399-8cea3d75-691a-4b6c-a3b2-514f6d469de4.png)  

Some models from China and the Czech were trained together,please refer to the table above, for China_Czech.txt  


