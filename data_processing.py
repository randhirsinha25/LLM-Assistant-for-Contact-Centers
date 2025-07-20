import pandas as pd
from llm import get_prompt,get_openai_response, transcribe_audio
import os

def prepare_data(path):
    # df = pd.read_csv(path,delimiter=',')
    df = pd.read_csv(path)
    if os.path.exists('reply_recordings.xlsx'):
        reply_recordings = pd.read_excel('reply_recordings.xlsx')
    else :
        reply_recordings=pd.DataFrame()
    temp=reply_recordings[reply_recordings['id'] == df['id'][0]].reset_index()
    print(temp["reply"][0])
    print(df['Type'].unique())
    for i in range(len(df)):
        if (len(reply_recordings)>0) :
            temp=reply_recordings[reply_recordings['id'] == df['id'][i]].reset_index()
            print(temp)
            if len(temp) == 0 :
                type = df['Type'][i]
                transcript = df['Transcript'][i]
                prompt = get_prompt(type,transcript)
                prompt = prompt+'\n'+ "Customer Voice message : " + transcript
                
                reply = get_openai_response(prompt)
            
                new_row = pd.DataFrame({'id':[df['id'][i]],'reply':[reply]})
                reply_recordings = pd.concat([reply_recordings,new_row],ignore_index=True)
                print(reply)
            
        elif len(reply_recordings)==0:
            
            type = df['Type'][i]
            transcript = df['Transcript'][i]
            prompt = get_prompt(type,transcript)
            prompt = prompt+'\n'+ "Customer Voice message : " + transcript
            
            reply = get_openai_response(prompt)
        
            new_row = pd.DataFrame({'id':[df['id'][i]],'reply':[reply]})
            reply_recordings = pd.concat([reply_recordings,new_row],ignore_index=True)
            print(reply)
        
    reply_recordings.to_excel('reply_recordings.xlsx',index=False)
def prepare_data_text(transcript,type):

    prompt = get_prompt(type,transcript)
    prompt = prompt+'\n'+ "Customer Voice message : " + transcript
                
    reply = get_openai_response(prompt)
    #print(reply)
    return reply
def prepare_data_audio(user_path,type):
    transcript = transcribe_audio(user_path)
    prompt = get_prompt(type,transcript)
    prompt = prompt+'\n'+ "Customer Voice message : " + transcript
                
    reply = get_openai_response(prompt)
    #print(reply)
    return reply,transcript