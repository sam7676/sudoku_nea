from ultralytics import YOLO
from torch.cuda import is_available
import shutil
import os

def main():
    # Check if GPU is enabled
    gpu_enabled = is_available()

    model = YOLO("yolov8n.yaml")

    if gpu_enabled:
        epochs = 100
        
        # Cuda support
        # https://pytorch.org/get-started/locally/ 
        model.to('cuda')
    else:
        epochs = 30


    model.train(data="server/dataset.yaml", epochs=epochs)  # train the model
    metrics = model.val()  # evaluate model performance on the validation set
    print(metrics)
    

    # Finding the most recent model in our runs folder
    i=2
    latest_model_path = None
    while os.path.exists(f'./runs/detect/train{i}'):
        if os.path.exists(f'./runs/detect/train{i}/weights/best.pt'):
            latest_model_path = f'./runs/detect/train{i}/weights/best.pt'

        i+=1

    if latest_model_path is not None:
        shutil.copy(latest_model_path, 'server/grid_model.pt')

if __name__ == '__main__':
    main()