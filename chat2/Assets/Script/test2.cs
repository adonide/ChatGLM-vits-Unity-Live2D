using System.Collections;
using System.Collections.Generic;
using UnityEngine;
//注意  一定要引用下面这个命名空间
using System.Diagnostics;
using System.Text;
public class test2 : MonoBehaviour
{
    //private static UnityEngine.UI.Text chatText;
    void Start(){
        UnityEngine.UI.InputField inputField = UnityEngine.Object.FindAnyObjectByType<UnityEngine.UI.InputField>();
        //chatText = GameObject.Find("chatText").GetComponent<UnityEngine.UI.Text>();
        inputField.onEndEdit.AddListener(delegate { OnEndEdit(inputField); });
    }

    void OnEndEdit(UnityEngine.UI.InputField inputField)
    {
        if (Input.GetKeyDown(KeyCode.Return))
        {
            string content = inputField.text;
            RunPythonScript(content);
            inputField.text = "";
            inputField.Select();
            inputField.ActivateInputField();
        }
    }
    private static void RunPythonScript(string argvs)
    {
        Process p = new Process();
        string path = @"E:\project\ChatGLM-6B-main\start.py";
        // foreach (string temp in argvs)
        // {
        //     path += " " + temp;
        // }
        p.StartInfo.FileName = @"C:\Users\A\AppData\Local\Programs\Python\Python310\python.exe";

        p.StartInfo.UseShellExecute = false;
        p.StartInfo.Arguments = path+ " " + argvs;
        p.StartInfo.RedirectStandardOutput = true;
        p.StartInfo.RedirectStandardError = true;
        p.StartInfo.RedirectStandardInput = true;
        p.StartInfo.CreateNoWindow = true;

        p.Start();
        p.BeginOutputReadLine();
        p.OutputDataReceived += new DataReceivedEventHandler(Get_data);
        p.WaitForExit();
    }
    private static void Get_data(object sender,DataReceivedEventArgs eventArgs)
    {
        if (!string.IsNullOrEmpty(eventArgs.Data))
        {
            UnityEngine.UI.Text chatText = GameObject.Find("chatText").GetComponent<UnityEngine.UI.Text>();
            string chat = eventArgs.Data;
            chatText.text = eventArgs.Data;
            print(eventArgs.Data);
        }
    }
}
