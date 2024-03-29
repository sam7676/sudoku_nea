from imports import *

def add_model_location():
    if not os.path.isdir('models'):
        os.mkdir('models')
class train:
    def __init__(self, window=None):
        self.grid_accuracy = []
        self.grid_val_accuracy = []
        self.window = window

    def train_grid(self, epochs):

        start_time = perf_counter()

        #Fetch images
        image_list = []
        for root, directory, file in os.walk(grid_location):
            for files in file:
                image_list.append(f"{root}\\{files}")

        #Resize all images. Returns whether image has been modified or not and image object
        for image in image_list:
            new=False
            if image[len(root)-1]=='0':
                new = resize_images(image,img_size)
            elif image[len(root)-1]=='1':
                new = resize_stretch(image,img_size)
            else:
                print("Error")
            if new[1]==True:
                new[0].save(image)
                
        #Dimension size
        dims = (img_size,img_size,3)

        #Getting labels
        image_labels = []
        for image in image_list:
            label = int(image[len(grid_location)+1])
            image_labels.append(label)

        #Converting images to arrays
        for i,image in enumerate(image_list):
            image = tf.keras.preprocessing.image.img_to_array(Image.open(image))
            image_list[i] = image / 255.0

        #Shuffling all data
        arr = []
        for i in range(len(image_list)):
            arr.append([image_list[i],image_labels[i]])
        random.shuffle(arr)
        imagepaths = []
        labels = []
        for i in range(len(arr)):
            imagepaths.append(arr[i][0])
            labels.append(arr[i][1])


        #Data
        x = tf.convert_to_tensor(imagepaths)

        y = tf.convert_to_tensor(labels, dtype=tf.int32)


        #Standard convolutional model
        model = tf.keras.models.Sequential([

            #Computes dot products along every 3x3 grid inside the image which learns and generalises the colours
            tf.keras.layers.Conv2D(32, (3, 3), activation='relu',input_shape=dims),
            
            #Reduces size and number of parameters by using a max of the surrounding area
            tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),

            tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
            tf.keras.layers.MaxPooling2D(2, 2),
            tf.keras.layers.Conv2D(128, (3, 3), activation='relu'), 
            tf.keras.layers.MaxPooling2D(2, 2),
            
            #Removes unnecessary dimensions, alllowing for dense layers to be used
            tf.keras.layers.Flatten(),

            #Hidden neural network layer. Takes input, applies weights, outputs
            tf.keras.layers.Dense(32, activation='relu'),

            #Removes random nodes in the hidden layer, and this fixes overfitting
            tf.keras.layers.Dropout(0.5),

            #Returns final answer
            tf.keras.layers.Dense(1, activation='sigmoid')  
        ])


        # Train neural network
        model.compile(
            optimizer="adam",
            loss="binary_crossentropy",
            metrics=["accuracy"]
        )

        model.fit(x, y, epochs=epochs, validation_split=split_rate, callbacks=[GridCallback(self.window)])
        

        add_model_location()
        model.save(grid_model_location)

        print(f"Grid training: {round(perf_counter()-start_time,1)}s")

    def train_digits(self, epochs):
        start_time = perf_counter()

        #Fetch images
        image_list = []
        for root, directory, file in os.walk(digit_location):
            for files in file:
                image_list.append(f"{root}\\{files}")

        #Resize all images. Returns whether image has been modified or not and image object
        for image in image_list:
            new = resize_images(image,digit_size)
            if new[1]==True:
                new[0].save(image)
                
        #Dimension size
        dims = (digit_size,digit_size,3)

        #Getting labels
        image_labels = []
        for image in image_list:
            label = int(image[len(digit_location)+1])
            image_labels.append(label)

        #Converting images to arrays
        for i,image in enumerate(image_list):
            img = Image.open(image)
            img = img.convert('RGB')
            img = tf.keras.preprocessing.image.img_to_array(img)
            image_list[i] = img / 255.0

        #Shuffling all data
        arr = []
        for i in range(len(image_list)):
            arr.append([image_list[i],image_labels[i]])
        random.shuffle(arr)
        imagepaths = []
        labels = []
        for i in range(len(arr)):
            imagepaths.append(arr[i][0])
            labels.append(arr[i][1])


        x = tf.convert_to_tensor(imagepaths)
        y = tf.convert_to_tensor(labels,dtype=tf.int32)

        
        #creating model
        model = tf.keras.models.Sequential([
        tf.keras.layers.Conv2D(128, (3, 3), activation='relu',input_shape=dims),
        tf.keras.layers.Flatten(), #flattening shape
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dropout(0.5),
        tf.keras.layers.Dense(10)
        ])


        #compile
        model.compile(optimizer='adam',
                    loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                    metrics=['accuracy'])

        model.fit(x, y, epochs=epochs, validation_split=split_rate, callbacks=[DigitCallback(self.window)])

        add_model_location()
        model.save(digit_model_location)

        print(f"Digit training: {round(perf_counter()-start_time,1)}s")


class DigitCallback(keras.callbacks.Callback):
    def __init__(self, window):
        self.window = window
        self.digit_accuracy = []
        self.digit_val_accuracy = []
        self.canvas = None

    def on_epoch_end(self, epoch, logs=None):
        self.digit_accuracy.append(logs["accuracy"])
        self.digit_val_accuracy.append(logs["val_accuracy"])
        self.plot_digits()

    def plot_digits(self):
        if self.canvas: self.canvas.get_tk_widget().grid_remove()  # remove previous image
    
        # the figure that will contain the plot 
        fig = Figure(figsize = (6, 5), 
                    dpi = 100,) 
    
    
        # adding the subplot 
        plot1 = fig.add_subplot(111) 
    
        # plotting the graph 
        plot1.plot(self.digit_accuracy, label="Training data")
        plot1.plot(self.digit_val_accuracy, label="Validation data")

        plot1.legend() 

        plot1.set_xlabel("Epochs")
        plot1.set_ylabel("Accuracy")
        
        plot1.set_title("Digit training accuracy")
    
        # creating the Tkinter canvas 
        # containing the Matplotlib figure 
        canvas = FigureCanvasTkAgg(fig, 
                                master = self.window,)   
        canvas.draw() 
    
        # placing the canvas on the Tkinter window 
        canvas.get_tk_widget().grid(row=4)



class GridCallback(keras.callbacks.Callback):
    def __init__(self, window):
        self.window = window
        self.grid_accuracy = []
        self.grid_val_accuracy = []
        self.canvas = None

    def on_epoch_end(self, epoch, logs=None):
        self.grid_accuracy.append(logs["accuracy"])
        self.grid_val_accuracy.append(logs["val_accuracy"])
        self.plot_grid()

    def plot_grid(self):
        if self.canvas: self.canvas.get_tk_widget().grid_remove()  # remove previous image
    
        # the figure that will contain the plot 
        fig = Figure(figsize = (6, 5), 
                    dpi = 100,) 
    
    
        # adding the subplot 
        plot1 = fig.add_subplot(111) 
    
        # plotting the graph 
        plot1.plot(self.grid_accuracy, label="Training data")
        plot1.plot(self.grid_val_accuracy, label="Validation data")

        plot1.legend() 

        plot1.set_xlabel("Epochs")
        plot1.set_ylabel("Accuracy")
        
        plot1.set_title("Grid training accuracy")
    
        # creating the Tkinter canvas 
        # containing the Matplotlib figure 
        canvas = FigureCanvasTkAgg(fig, 
                                master = self.window,)   
        canvas.draw() 
    
        # placing the canvas on the Tkinter window 
        canvas.get_tk_widget().grid(row=4)

