from ultralytics import YOLO
from digit_model_architecture import DigitNetwork
import torch
import torchvision.transforms as transforms


grid_model_path = 'client/grid_model.pt'
digit_model_path = 'client/digit_model.pt'

grid_model = YOLO(grid_model_path)
digit_model = DigitNetwork()
digit_model.load_state_dict(torch.load(digit_model_path))

def process_digit(image):

    # Load transforms
    image_transform = transforms.Compose([transforms.ToTensor(), transforms.Grayscale(num_output_channels=1),])
    
    # Transform image
    image_tensor = image_transform(image)

    # Unsqueeze tensor (to fit in model)
    image_tensor = image_tensor.unsqueeze(0)

    # Predict using softmax
    result = digit_model(image_tensor)

    # Get index of max value
    max_val = result.flatten()[0]
    max_ind = 0
    for ind, value in enumerate(result.flatten()):
        if value > max_val:
            max_val = value
            max_ind = ind
    

    return str(max_ind)


def process_grid(image):

    resized_image = image.resize((576, 576))
    grid = ''

    for i in range(81):
        y_top = i // 9
        x_left = i % 9
        cell = resized_image.crop((x_left * 64, y_top * 64, x_left * 64 + 64, y_top * 64 + 64))

        grid += process_digit(cell)

    return grid



def process_canvas(image, return_type = 'grid'):
    results = grid_model(image)
    for result in results:
        if len(result.boxes.xyxy) == 0: continue

        x1, y1, x2, y2 = result.boxes.xyxy[0].tolist()

        # Rounding the corners
        round_int = lambda x: int(round(x))
        x1 = round_int(x1)
        x2 = round_int(x2)
        y1 = round_int(y1)
        y2 = round_int(y2)

        if return_type == 'grid':

            cropped_grid = image.crop((x1, y1, x2, y2))

            return process_grid(cropped_grid)
        
        elif return_type == 'bounds':

            return (x1, y1, x2, y2)
        
        else:
            raise Exception('Invalid return type')

    return None



