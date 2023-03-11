import torch

from torchvision import datasets
from torch.utils.data import DataLoader
from facenet_pytorch import MTCNN,InceptionResnetV1



class JoloRecognition:
    
    def __init__(self):

        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        
        # face detection
        self.mtcnn  = MTCNN(image_size=160, margin=0, min_face_size=40,select_largest=False, device=self.device)
        
        # facial recognition
        self.facenet = InceptionResnetV1(pretrained='vggface2').eval().to(self.device)
        
        # load known faces data
        self.Saved_Data = torch.load('FaceDetection/Model/data.pt', map_location='cpu')
        self.Embeding_List = self.Saved_Data[0]
        self.Name_List = self.Saved_Data[1]
        
    # for face recognition
    def Face_Compare(self, face, threshold=0.6):
    
        with torch.no_grad():
            
            # check if there is detected faces
            face,prob = self.mtcnn(face, return_prob=True)
            
            # check if there is face and probability of 90%
            if face  is not None and prob > 0.90:
                
                # calculcate the face distance
                emb  = self.facenet(face.unsqueeze(0)).detach()
                
                match_list = []
                
                # self.Embeding_List is the load data.pt 
                
                for idx, emb_db in enumerate(self.Embeding_List):
                    try:
                        # torch.dist = is use to compare the face detected into batch of faceas in self embediing
                        dist = torch.dist(emb, emb_db).item()
                        
                        # append the comparing result
                        match_list.append(dist)
                    except:
                        break
                
                # check if there is recognize faces               
                if len(match_list) > 0:
                    
                    # match_list is the result of comparing faces
                    min_dist = min(match_list)

                    # since it has result we need to setup the accuracy level 
                    # threshold is the bias point number for accuracy
                    # in this if statment we set a threshold value of 0.6
                    # meaning all the result of comparing faces should atleast 0.6 value in order to recognize people
                    
                    if min_dist < threshold:
                        
                        idx_min = match_list.index(min_dist)
                        
                        print(self.Name_List[idx_min])
                        return (self.Name_List[idx_min], min_dist)
                    else:
                        return ('No match detected', None)
                
                else:
                    return ('No match detected', None)
                
            else:
                ('No match detected', None)
    
    # training from dataset
    def Face_Train(self, Dataset_Folder, location):
        
        def collate_fn(x):
            return x[0]
        
        # locate the dataset of known faces
        Datasets = datasets.ImageFolder(Dataset_Folder)
        
        # load the folder name in dataset
        label_names = {i:c for c,i in Datasets.class_to_idx.items()}
        
        # load the dataset
        loader = DataLoader(Datasets, collate_fn=collate_fn,pin_memory=True)
        
        Name_list = []
        embedding_list = []
        
        for images, label in loader:
            
            print("Training...")    
            with torch.no_grad():
                
                # for facial detection level 2 --- Using MTCNN model
                face, prob = self.mtcnn(images,return_prob=True)
                
                # check if there  is detected face and has probability of 90%
                if face is not None and prob > 0.90:
                    
                    # calculate face distance
                    emb =  self.facenet(face.unsqueeze(0))
                    
                    embedding_list.append(emb.detach())
                    Name_list.append(label_names[label])
                    
        data = [embedding_list, Name_list]
        
        # save the calculated face distance into data.pt
        torch.save(data,location + '/data.pt')
        return "done"


