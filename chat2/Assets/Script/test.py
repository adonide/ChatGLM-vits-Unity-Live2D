# -*- coding: UTF-8 -*-
import UnityEngine as ue
import io
import sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')
inputField = ue.Object.FindObjectOfType(ue.UI.InputField)
a = inputField.text 
b = "啊啊啊啊11aa"
inputField.text = b
ue.Debug.Log(b)
print(b)