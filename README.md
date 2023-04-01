# ChatGLM-vits-Unity-Live2D

## 介绍

缝合了chatglm、vits、live2d

使用百度paddlehub进行文本情感判断

支持中英双语

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
                                      
## 命令

可以在对话框中输入命令

切换语言,例如:

      language en
      
切换speaker,例如:

      speaker 111
      
清除历史：

      clear

## 运行

python3.10

      pip install -r requirements.txt

下载chatglm-6b-int4所有文件放到chatglm-6b文件夹

下载vits模型放到vmodel，命名为model.pth和config.json

运行start.py启动服务器

运行chat.exe
