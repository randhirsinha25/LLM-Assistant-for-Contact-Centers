import pandas as pd
from data_processing import prepare_data,prepare_data_text, prepare_data_audio

if __name__ == "__main__":
    input_type = 'audio'
    if input_type =='csv':
        path = 'data/call_recordings.csv'
        df=prepare_data(path)
    elif  input_type == 'text':
        user_text= """I'm calling to express my satisfaction with the PR-9876 printer I bought from your company. My name is Christopher Green, and my order number is 876543. It was easy to set up, and the print quality is excellent. I especially appreciate the fast printing speed. It has significantly improved my productivity. Thank you!"""
        type = 'Compliment'
        df = prepare_data_text(user_text,type)
    elif  input_type == 'audio':
         user_path = "D:/New folder/office 2013/OneDrive - Algoworks Technologies Pvt. Ltd/Desktop/Audio/call_recording_01.wav"
         type = 'Complaint'
         df = prepare_data_audio(user_path,type)