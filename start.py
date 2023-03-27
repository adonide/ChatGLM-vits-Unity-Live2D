import os
import platform
from transformers import AutoTokenizer, AutoModel
from scipy.io.wavfile import write
from mel_processing import spectrogram_torch
from text import text_to_sequence, _clean_text
from models import SynthesizerTrn
import utils
import commons
import sys
import re
from torch import no_grad, LongTensor
import logging
# import pyaudio
import numpy as np
# import io
import flask
import paddlehub as padd
import json
# utf-8解码
# sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')

senta = padd.Module(name="senta_lstm")

#--------------------------------------------------------------------------------
logging.getLogger('numba').setLevel(logging.WARNING)


def ex_print(text, escape=False):
    if escape:
        print(text.encode('unicode_escape').decode())
    else:
        print(text)


def get_text(text, hps, cleaned=False):
    if cleaned:
        text_norm = text_to_sequence(text, hps.symbols, [])
    else:
        text_norm = text_to_sequence(text, hps.symbols, hps.data.text_cleaners)
    if hps.data.add_blank:
        text_norm = commons.intersperse(text_norm, 0)
    text_norm = LongTensor(text_norm)
    return text_norm


def ask_if_continue():
    while True:
        answer = input('Continue? (y/n): ')
        if answer == 'y':
            break
        elif answer == 'n':
            sys.exit(0)


def print_speakers(speakers, escape=False):
    if len(speakers) > 100:
        return
    print('ID\tSpeaker')
    for id, name in enumerate(speakers):
        ex_print(str(id) + '\t' + name, escape)


def get_speaker_id(message):
    speaker_id = input(message)
    try:
        speaker_id = int(speaker_id)
    except:
        print(str(speaker_id) + ' is not a valid ID!')
        sys.exit(1)
    return speaker_id


def get_label_value(text, label, default, warning_name='value'):
    value = re.search(rf'\[{label}=(.+?)\]', text)
    if value:
        try:
            text = re.sub(rf'\[{label}=(.+?)\]', '', text, 1)
            value = float(value.group(1))
        except:
            print(f'Invalid {warning_name}!')
            sys.exit(1)
    else:
        value = default
    return value, text


def get_label(text, label):
    if f'[{label}]' in text:
        return True, text.replace(f'[{label}]', '')
    else:
        return False, text

import emoji

def remove_emoji(text):
    emoji_pattern = re.compile("["
    u"\U0001F600-\U0001F64F"  # emoticons
    u"\U0001F300-\U0001F5FF"  # symbols & pictographs
    u"\U0001F680-\U0001F6FF"  # transport & map symbols
    u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
    "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)


def voice(response):
    # if '--escape' in sys.argv:
    #     escape = True
    # else:
    #     escape = False
    print('loading......') 
    model = './vmodel/1/G_953000.pth'
    config = './vmodel/1/config.json'
    
    hps_ms = utils.get_hparams_from_file(config)
    n_speakers = hps_ms.data.n_speakers if 'n_speakers' in hps_ms.data.keys() else 0
    n_symbols = len(hps_ms.symbols) if 'symbols' in hps_ms.keys() else 0
    speakers = hps_ms.speakers if 'speakers' in hps_ms.keys() else ['0']
    use_f0 = hps_ms.data.use_f0 if 'use_f0' in hps_ms.data.keys() else False
    emotion_embedding = hps_ms.data.emotion_embedding if 'emotion_embedding' in hps_ms.data.keys() else False

    net_g_ms = SynthesizerTrn(
        n_symbols,
        hps_ms.data.filter_length // 2 + 1,
        hps_ms.train.segment_size // hps_ms.data.hop_length,
        n_speakers=n_speakers,
        emotion_embedding=emotion_embedding,
        **hps_ms.model)
    _ = net_g_ms.eval()
    utils.load_checkpoint(model, net_g_ms.to('cuda'))

   
    if n_symbols != 0:
        if not emotion_embedding:
            if(language == 'zh'):
                text = '[ZH]'+ remove_emoji(response) +'[ZH]'
            else:
                text = '[EN]'+ remove_emoji(response) +'[EN]'
            length_scale, text = get_label_value(
                text, 'LENGTH', 1.2, 'length scale')
            noise_scale, text = get_label_value(
                text, 'NOISE', 0.6, 'noise scale')
            noise_scale_w, text = get_label_value(
                text, 'NOISEW', 0.8, 'deviation of noise')
            cleaned, text = get_label(text, 'CLEANED')

            stn_tst = get_text(text, hps_ms, cleaned=cleaned)

            with no_grad():
                x_tst = stn_tst.unsqueeze(0).to('cuda')
                x_tst_lengths = LongTensor([stn_tst.size(0)]).to('cuda')
                sid = LongTensor([speaker_id]).to('cuda')
                audio = net_g_ms.infer(x_tst, x_tst_lengths, sid=sid, noise_scale=noise_scale,
                                        noise_scale_w=noise_scale_w, length_scale=length_scale)[0][0, 0].data.float().detach().cpu().numpy()

            write("E:/bc/UnityProject/chat2/Assets/Resources/res.wav",22050,audio)
            # p = pyaudio.PyAudio()
            # stream = p.open(format=pyaudio.paFloat32,channels=1,rate=22050,output=True)
            # print(f"ChatGLM-6B：{response}")
            # stream.write(audio.astype(np.float32).tobytes())
            # stream.stop_stream()
            # stream.close()
            # p.terminate()

#---------------------------------------------------------------------

tokenizer = AutoTokenizer.from_pretrained("./chatglm-6b", trust_remote_code=True)
model = AutoModel.from_pretrained("./chatglm-6b", trust_remote_code=True).half().quantize(4).cuda()
model = model.eval()

os_name = platform.system()

# history = []
# print("欢迎使用 ChatGLM-6B 模型，输入内容即可进行对话，clear 清空对话历史，stop 终止程序")
# speaker_id = get_speaker_id('输入speaker id:')#91,144
# language = input('zh or en:')
# while True:
#     query = input("\n用户：")
#     if query == "stop":
#         break
#     if query == "clear":
#         history = []
#         command = 'cls' if os_name == 'Windows' else 'clear'
#         os.system(command)
#         print("欢迎使用 ChatGLM-6B 模型，输入内容即可进行对话，clear 清空对话历史，stop 终止程序")
#         continue
#     if query == "speaker":
#         speaker_id = get_speaker_id('输入speaker id:')
#         continue
#     if query == "language":
#         language = input('zh or en:')
#         continue
#     response, history = model.chat(tokenizer, query, history=history)
#     voice(response)

#-----------------------------------------------------------
with open("./history.txt","r") as file:
    data = file.read()
    if data:
        history = json.loads(data)
    else:
        history = []
# history = []
speaker_id = 144
app = flask.Flask(__name__)

@app.route("/", methods=['GET'])
def chat():
    global language
    global speaker_id
    global history
    global file
    language = 'zh'
    
    query = flask.request.args.get("Text")
    if query == "clear":
        history = []
        command = 'cls' if os_name == 'Windows' else 'clear'
        os.system(command)
        return "clear"
    if query[:7] == "speaker":
        speaker_id = int(query[8:])
        return "change speaker %s" %speaker_id
    response, history = model.chat(tokenizer, query, history=history)
    with open('./history.txt',"w") as f:
        json.dump(history, f)
    print(response)
    feeling = senta.sentiment_classify(data={"text":[response]})
    voice(response)
    return str(feeling[0]["sentiment_label"])+response

if __name__ == "__main__":
    app.run()