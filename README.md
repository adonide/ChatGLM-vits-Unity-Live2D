# ChatGLM-vits-Unity-Live2D

## 来源
chatglm:https://huggingface.co/THUDM/chatglm-6b-int4

vits:https://github.com/CjangCjengh/vits

中英模型:https://github.com/Plachtaa/VITS-fast-fine-tuning


## 文件结构
UnityBuild

      |---chat2Data

              |------ChatGLM-6B-main

                            |------start.py

                            |------chatglm-6b

                            |------vmodel

                                      |----config.json

                                      |----model.pth

## 运行

      pip install -r requirements.txt

下载chatglm-6b-int4所有文件放到chatglm-6b文件夹

下载vits模型放到vmodel，命名为model.pth和config.json

运行start.py启动服务器

运行chat.exe
