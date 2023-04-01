using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Diagnostics;
using System.Text;
using System.Net.Http;
using System.Threading.Tasks;
public class test : MonoBehaviour
{
    // Start is called before the first frame update
    static UnityEngine.UI.InputField inputField;
    static UnityEngine.UI.Text chatText;
    static AudioSource audioSource;
    static AudioClip ss;
    static bool feeling;
    static Animator animator;
    
    void Start()
    {
        inputField = FindAnyObjectByType<UnityEngine.UI.InputField>();
        chatText = GameObject.Find("chatText").GetComponent<UnityEngine.UI.Text>();
        audioSource = GameObject.Find("Audio Source").GetComponent<AudioSource>();
        animator = GameObject.Find("mao_pro_t02").GetComponent<Animator>();
        inputField.Select();
        inputField.ActivateInputField();
        inputField.onEndEdit.AddListener(async delegate { await OnEndEdit(inputField); });
    }

    async Task OnEndEdit(UnityEngine.UI.InputField inputField)
    { 
        if (Input.GetKeyDown(KeyCode.Return))
        {
            await MyMethod();
            inputField.Select();
            inputField.ActivateInputField();
        }
    }

    async Task MyMethod()
    {
        using var client = new HttpClient();
        string url = "http://127.0.0.1:5000/?Text="+ inputField.text;
        chatText.text = "loading...";
        var response = await client.GetAsync(url);
        var content = await response.Content.ReadAsStringAsync();

        if (content == "clear") {
            chatText.text = content;
            return;
        }
        else if(content.Length>7)
        {
            if (content.Substring(0, 6) == "change") {
                chatText.text = content;
                return;
            }    
        }
        if (content[0] == '0')
        {
            feeling = false;
        }
        else {
            feeling = true;
        };

        chatText.text = content.Substring(1);
        UnityEngine.Debug.Log("start load");
        StartCoroutine(LoadAudio());
        /*ss = Resources.Load("res") as AudioClip;
        audioSource.clip = ss;
        audioSource.Play();*/
        UnityEngine.Debug.Log(content);
    }

    IEnumerator LoadAudio()
    {
        WWW www = new("file://" + Application.dataPath + "/ChatGLM-6B-main/res.wav");
        yield return www;
        AudioClip audioClip = www.GetAudioClip();
        audioSource.clip = audioClip;
        audioSource.Play();
        animator.SetBool("feeling", feeling);
    }
}
