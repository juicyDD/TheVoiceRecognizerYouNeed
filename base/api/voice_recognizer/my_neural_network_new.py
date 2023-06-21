import os
import torch
import torch.nn as nn 
from torch.nn import functional as F
#GeForce MX250 => Compute capability = 6.1 => CUDA ver 8.0 => downgrade python xuống 3.6 nhaa
#virtualenv --python="C:/Users/DELL/AppData/Local/Programs/Python/Python36/python.exe" "C:/Users/DELL/Desktop/DATN/currentcode/virtualenv/"
# pip install "C:\Users\DELL\Desktop\DATN\currentcode\torch-0.4.0-cp36-cp36m-win_amd64.whl"
from base.api.voice_recognizer import nhi_config

class PretrainedEncoder(nn.Module):
    def load_pretrained(self, saved_model):
        my_state_dict = torch.load(saved_model, map_location=nhi_config.DEVICE) 
        self.load_state_dict(my_state_dict["encoder_state_dict"])
      
'''LONG SHORT-TERM MEMORY MODEL'''
class JennieJisoo(PretrainedEncoder):
    def __init__(self, saved_model=""):
        super(JennieJisoo, self).__init__()
        self.lstm = nn.LSTM(
            input_size=nhi_config.N_MFCC,
            hidden_size=nhi_config.LSTM_HIDDEN_SIZE,
            num_layers=nhi_config.LSTM_NUM_LAYERS,
            batch_first=True,
            bidirectional=nhi_config.BI_LSTM)

        #--------- if there is a pretrained model, load it
        if saved_model:
            self.load_pretrained(saved_model)

    '''join output frames'''
    def join_frames(self, batch_output):
        if nhi_config.FRAME_AGGREGATION_MEAN:
            return torch.mean(
                batch_output, dim=1, keepdim=False)
        else:
            return batch_output[:, -1, :]
    def forward(self, x):
        D = 2 if nhi_config.BI_LSTM else 1
        #-----------h0: hidden state; c0: cell state
        h0 = torch.zeros(D * nhi_config.LSTM_NUM_LAYERS, x.shape[0], nhi_config.LSTM_HIDDEN_SIZE)
        c0 = torch.zeros(D * nhi_config.LSTM_NUM_LAYERS, x.shape[0], nhi_config.LSTM_HIDDEN_SIZE)
        y, (hn, cn) = self.lstm(x.to(nhi_config.DEVICE), (h0.to(nhi_config.DEVICE), c0.to(nhi_config.DEVICE)))
        return self.join_frames(y)

'''TRANSFORMER MODEL'''
class MomoTzuyu(PretrainedEncoder):
    def __init__(self, saved_model=""):
        super(MomoTzuyu, self).__init__()
        self.linear_layer = nn.Linear(nhi_config.N_MFCC, nhi_config.TRANSFORMER_DIM)

        self.encoder = nn.TransformerEncoder(
            nn.TransformerEncoderLayer(d_model=nhi_config.TRANSFORMER_DIM, nhead=nhi_config.TRANSFORMER_HEADS, batch_first=True),
            num_layers=nhi_config.TRANSFORMER_ENCODER_LAYERS)
        
        self.decoder = nn.TransformerDecoder(
            nn.TransformerDecoderLayer(d_model=nhi_config.TRANSFORMER_DIM, nhead=nhi_config.TRANSFORMER_HEADS, batch_first=True),
            num_layers=1)

        if saved_model:
            self.load_pretrained(saved_model)

    def forward(self, x):
        encoder_input = torch.sigmoid(self.linear_layer(x))
        encoder_output = self.encoder(encoder_input)
        tgt = torch.zeros(x.shape[0], 1, nhi_config.TRANSFORMER_DIM).to(nhi_config.DEVICE)
        output = self.decoder(tgt, encoder_output)
        return output[:, 0, :]

class Lisa(PretrainedEncoder):
    def __init__(self, saved_model=""):
        super(Lisa, self).__init__()
        self.lstm1 = nn.LSTM( input_size=nhi_config.N_MFCC, hidden_size=nhi_config.LSTM_HIDDEN_SIZE, num_layers=nhi_config.LSTM_NUM_LAYERS, batch_first=True, bidirectional=nhi_config.BI_LSTM)
        self.lstm2= nn.LSTM( input_size=nhi_config.LSTM_HIDDEN_SIZE * 2, hidden_size=nhi_config.LSTM_HIDDEN_SIZE, num_layers=nhi_config.LSTM_NUM_LAYERS, batch_first=True, bidirectional=nhi_config.BI_LSTM)
        self.linear1 = nn.Linear(128, 128)
        self.linear2 = nn.Linear(128, 128) 
        self.linear_pe = nn.Linear(128, 1)
        if saved_model:
            self.load_pretrained(saved_model)

    '''join output frames'''
    def join_frames(self, batch_output):
        if nhi_config.FRAME_AGGREGATION_MEAN:
            return torch.mean(
                batch_output, dim=1, keepdim=False)
        else:
            return batch_output[:, -1, :]
    def forward(self, x):
        D = 2 if nhi_config.BI_LSTM else 1
        h0 = torch.zeros(D * nhi_config.LSTM_NUM_LAYERS, x.shape[0], nhi_config.LSTM_HIDDEN_SIZE)
        c0 = torch.zeros(D * nhi_config.LSTM_NUM_LAYERS, x.shape[0], nhi_config.LSTM_HIDDEN_SIZE)
        y1, (hn, cn) = self.lstm1(x.to(nhi_config.DEVICE), (h0.to(nhi_config.DEVICE), c0.to(nhi_config.DEVICE)))
        y2, _ = self.lstm2(y1)
        h_conc_linear1  = F.relu(self.linear1(y1))
        h_conc_linear2  = F.relu(self.linear2(y2))
        y =  y1 + y2 + h_conc_linear1 + h_conc_linear2
        return self.join_frames(y)
        
class Rose(PretrainedEncoder):
    def __init__(self, saved_model=""):
        super(Rose, self).__init__()
        self.lstm1 = nn.LSTM( input_size=nhi_config.N_MFCC, hidden_size=nhi_config.LSTM_HIDDEN_SIZE, num_layers=nhi_config.LSTM_NUM_LAYERS, batch_first=True, bidirectional=nhi_config.BI_LSTM)
        self.lstm2= nn.LSTM( input_size=nhi_config.LSTM_HIDDEN_SIZE * 2, hidden_size=nhi_config.LSTM_HIDDEN_SIZE, num_layers=nhi_config.LSTM_NUM_LAYERS, batch_first=True, bidirectional=nhi_config.BI_LSTM)

        if saved_model:
            self.load_pretrained(saved_model)

    '''join output frames'''
    def join_frames(self, batch_output):
        if nhi_config.FRAME_AGGREGATION_MEAN:
            return torch.mean(
                batch_output, dim=1, keepdim=False)
        else:
            return batch_output[:, -1, :]
    def forward(self, x):
        D = 2 if nhi_config.BI_LSTM else 1
        h0 = torch.zeros(D * nhi_config.LSTM_NUM_LAYERS, x.shape[0], nhi_config.LSTM_HIDDEN_SIZE)
        c0 = torch.zeros(D * nhi_config.LSTM_NUM_LAYERS, x.shape[0], nhi_config.LSTM_HIDDEN_SIZE)
        y1, (hn, cn) = self.lstm1(x.to(nhi_config.DEVICE), (h0.to(nhi_config.DEVICE), c0.to(nhi_config.DEVICE)))
        y2, _ = self.lstm2(y1)
        y = y1 + y2
        return self.join_frames(y)
        

def get_speaker_encoder(name="jennie"): #function to get encoder(model)
    if name=="jennie":
        return JennieJisoo(nhi_config.MODEL_DICT["jennie"]["path"]).to(nhi_config.DEVICE)
    elif name=="jisoo":
        return JennieJisoo(nhi_config.MODEL_DICT["jisoo"]["path"]).to(nhi_config.DEVICE)
    elif name=="lisa":
        return Lisa(nhi_config.MODEL_DICT["lisa"]["path"]).to(nhi_config.DEVICE)
    elif name=="rose":
        return Rose(nhi_config.MODEL_DICT["rose"]["path"]).to(nhi_config.DEVICE)
    
    


    
    