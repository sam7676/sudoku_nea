from imports import *
from training import *

class convert:
    def __init__(x,inp,debug=False):
        
        #Given input image, attempts to find grid inside
        x.digit_array = []
        start_time = perf_counter()
        imgs = x.search(inp)

        #Loading models and processing potential grid images
        grid_model = tf.keras.models.load_model(grid_model_location)
        digit_model = tf.keras.models.load_model(digit_model_location)
        img_preds=[]
        temp_image_store=[]
        global_max=False

        # Enumerates through
        # If prediction > pval, there is at least one somewhat valid grid found within image
        # Keep a stack of the past 5 image predictions. If they have a low mean, it is likely
        # that a grid is not present (else the results would be more consistent).
        # If there is a low mean and a somewhat valid grid has been found, terminate and find
        # the highest-scoring grid

        for i, img in enumerate(imgs):
            img2 = tf.keras.preprocessing.image.img_to_array(img)/255.0
            image = tf.convert_to_tensor([img2])
            predict = grid_model.predict(image,verbose=0)[0][0]
            img_preds.append(predict)

            if predict>pval:
                global_max=True
            if len(temp_image_store)>=img_set:
                temp_image_store.pop(0)
            temp_image_store.append(predict)

            if debug==True:
                print(i,predict)

            if (statistics.mean(temp_image_store)<meanpval and max(temp_image_store)<pval) and global_max==True:
                break

        if debug==True:
            plt.plot([i for i in range(len(img_preds))],img_preds)
            plt.show()

        x.max_predict = max(img_preds)
        
        #Allow saving of the grid if the minimum prediction confidence has been achieved
        x.saving=True
        if x.max_predict<pval:
            x.saving=False
        
        print(f'Grid prediction confidence: {round(x.max_predict/0.01,1)}%')
        max_img = imgs[img_preds.index(x.max_predict)]
        x.img = max_img
        if x.saving==True:
            max_img.save(f'{grid_location}\\1\\{x.max_predict}{get_name()}.png')
        results = ''

        #Split the grid into 81 squares of equal area. These are expected to be the cells.
        #Use second model to predict digit for each of the cells, return result

        indent = img_size/9
        for j in range(9):
            for i in range(9):

                #Crop max image, resize it, process it
                img = max_img.copy()
                img = img.crop(((i*indent)//1,(j*indent)//1,((i+1)*indent)//1,((j+1)*indent)//1))
                img = img.resize((digit_size,digit_size))
                img = img.convert('RGB')
                
                image = tf.keras.preprocessing.image.img_to_array(img)
                image = image / 255.0
                image = tf.convert_to_tensor([image])

                predict = digit_model.predict(image,verbose=0).tolist()[0]

                #Get the maximum probability digit
                maxProb,maxI = 0,0
                for h in range(len(predict)):
                    if predict[h]>maxProb:
                        maxProb = predict[h]
                        maxI = h
                predict = maxI
                if maxProb==0:
                    predict='0'

                #Append image to digit array (for potential saving of grid)
                x.digit_array.append([img,i,j,str(predict)])

                results+=str(predict)
        x.ans = results
        print(f"Conversion: {round(perf_counter()-start_time,3)}s")
    def search(x,input_image):
        
        #Resize image so the tensor is the same size
        t = resize_images(input_image,img_size)

        #Convert image from PIL to openCV and run selective search
        im = cv2.cvtColor(np.array(t[0]), cv2.COLOR_RGB2BGR)
        ss = cv2.ximgproc.segmentation.createSelectiveSearchSegmentation()
        ss.setBaseImage(im)
        ss.switchToSelectiveSearchFast()
        rects = ss.process()

        #For each co-ordinate given from selective search, get corner positions and area
        rects2 = []
        for i in range(len(rects)):
            rects2.append(np.array([rects[i][0],rects[i][1],rects[i][2],rects[i][3],rects[i][2]*rects[i][3]]))
        rects = rects2

        #Sort images by area
        rects.sort(key=lambda x: x[4],reverse=True)
        objs = []

        for i in range(len(rects)):

            #Get co-ordinates
            x1,y1,x2,y2 = rects[i][0],rects[i][1],rects[i][2],rects[i][3]

            #If width = 0 or height = 0, break
            #If width is not similar to height, cannot be square, break
            #If area is not large enough, break

            if (x2==0 or y2==0) or (x2//(img_size//50) != y2//(img_size//50)) or (x2*y2 < ((img_size)**2//100)):
                continue

            x2 += x1
            y2 += y1

            #Get image object, return list of all potential images sorted by size
            img = t[0]
            img = img.crop((x1,y1,x2,y2))
            img = resize_images(img,img_size)[0]
            objs.append(img)
        return objs
    def train(x,solution):
        
        # Given solution input, if saving has been allowed, save all digits
        # to their corresponding folders and print accuracy of prediction
        accuracy=0
        solution = flatten(solution)
        for img_arr in x.digit_array:
            if x.saving==True:
                img_arr[0].save(f'{digit_location}\\{solution[9*img_arr[2]+img_arr[1]]}\\{get_name()}.png')
            if solution[9*img_arr[2]+img_arr[1]] == img_arr[3]:
               accuracy+=1
        print(f'Conversion accuracy: {round(accuracy/0.81,1)}%')

            