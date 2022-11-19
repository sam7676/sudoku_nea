from imports import *

def add_model_location():
    if not os.path.isdir('models'):
        os.mkdir('models')

def train_grid():

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
    a1size = len(arr)

    #Splitting all data into training and test
    x_train = imagepaths[int(round(a1size*split_rate)):]
    x_test = imagepaths[:int(round(a1size*(1-split_rate)))]

    y_train = labels[int(round(a1size*split_rate)):]
    y_test = labels[:int(round(a1size*(1-split_rate)))]

    #Convert to tensors
    x_train = tf.convert_to_tensor(x_train)
    x_test = tf.convert_to_tensor(x_test)

    y_train = tf.convert_to_tensor(y_train, dtype=tf.int32)
    y_test = tf.convert_to_tensor(y_test, dtype=tf.int32)


    #Standard convolutional model
    model = tf.keras.models.Sequential([

        #Computes dot products along every 3x3 grid inside the image which learns and generalises the colours
        tf.keras.layers.Conv2D(32, (3, 3), activation='relu',input_shape=dims),
        
        #Reduces size and number of parameters by using a max of the surrounding area
        tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),

        tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
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

    model.fit(x_train, y_train, epochs=epoch_rate)

    # Evaluate neural network performance and save
    model.evaluate(x_test,  y_test, verbose=2)
    add_model_location()
    model.save(grid_model_location)

    print(f"Grid training: {round(perf_counter()-start_time,1)}s")

def train_digits():

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
    a1size = len(arr)


    #Splitting all data into training and test
    x_train = imagepaths[int(round(a1size*split_rate)):]
    x_test = imagepaths[:int(round(a1size*(1-split_rate)))]

    y_train = labels[int(round(a1size*split_rate)):]
    y_test = labels[:int(round(a1size*(1-split_rate)))]


    #Convert to tensors
    x_train = tf.convert_to_tensor(x_train)
    x_test = tf.convert_to_tensor(x_test)

    y_train = tf.convert_to_tensor(y_train, dtype=tf.int32)
    y_test = tf.convert_to_tensor(y_test, dtype=tf.int32)


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

    model.fit(x_train, y_train, epochs=epoch_rate)

    #Evaluating and saving model
    model.evaluate(x_test,  y_test, verbose=2)
    add_model_location()
    model.save(digit_model_location)

    print(f"Digit training: {round(perf_counter()-start_time,1)}s")


