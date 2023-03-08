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
        
        # known faces data
        self.Saved_Data = torch.load('FaceDetection/Model/data.pt', map_location='cpu')
        self.Embeding_List = self.Saved_Data[0]
        self.Name_List = self.Saved_Data[1]
        
    # for face recognition
    def Face_Compare(self, face, threshold=0.6):
    
        with torch.no_grad():
            
            face,prob = self.mtcnn(face, return_prob=True)
            
            if face  is not None and prob > 0.90:
                
                emb  = self.facenet(face.unsqueeze(0)).detach()
                
                match_list = []
                
                for idx, emb_db in enumerate(self.Embeding_List):
                    try:
                        dist = torch.dist(emb, emb_db).item()
                        match_list.append(dist)
                    except:
                        break
                
                # check if there is detected faces
                
                
                if len(match_list) > 0:
                    
                    min_dist = min(match_list)
        
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
        
        Datasets = datasets.ImageFolder(Dataset_Folder)
        label_names = {i:c for c,i in Datasets.class_to_idx.items()}
        loader = DataLoader(Datasets, collate_fn=collate_fn,pin_memory=True)
        
        Name_list = []
        embedding_list = []
        
        for images, label in loader:
            print("Training...")    
            with torch.no_grad():
                face, prob = self.mtcnn(images,return_prob=True)
                
                if face is not None and prob > 0.90:
                    
                    emb =  self.facenet(face.unsqueeze(0))
                    embedding_list.append(emb.detach())
                    Name_list.append(label_names[label])
                    
        data = [embedding_list, Name_list]
        torch.save(data,location + '/data.pt')
        return "done"


