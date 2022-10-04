# CRDDC_2022_SourceCode
### 1.Clone repo and install requirements.txt in a Python>=3.7.0 environment, including PyTorch>=1.7.  
```python
git clone https://github.com/KentHan19980609/T22_034_han_shi_hao_CRDDC_2022_SourceCode.git
cd T22_034_han_shi_hao_CRDDC_2022_SourceCode/yoloair
pip install -r requirements.txt  # install
```
### 2.Process training images and labels,  
download from https://bigdatacup.s3.ap-northeast-1.amazonaws.com/2022/CRDDC2022/RDD2022/RDD2022.zip  
```python
python move_image_label.py 
python xml2yolo.py
```
### 3.download the model  

https://pan.baidu.com/s/1z3s9YEG8encVnSAF-7cshw  password: l5h1   
  
### 4.detect for each country
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
### 5.Mix all country results  
```python
python mix_all_country.py
```
### 6.train  
```python
python train_val.py # get val.txt

#yolov5x
python train.py --data data/road.yaml --cfg yolov5x_road.yaml --weight yolov5x.pt --batch-size 16 --img-size 640 

#yolov5x-transformer
python train.py --data data/road.yaml --cfg yolov5x-transformer.yaml --weights '' --hyp data/hyps/hyp.scratch-high.yaml --batch-size 16 --img-size 640 

#yolov7
python yolov7/train.py --data data/road.yaml --cfg yolov7x.yaml --weight yolov7x.pt --batch-size 16 --img-size 640 
```
