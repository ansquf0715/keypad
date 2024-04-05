using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using TMPro;
using Photon.Pun;

public class buttonScript : MonoBehaviour
{
    public string enteredNumbers = "010-";
    int maxEnter = 12;
    public Button[] buttons;
    TextMeshProUGUI display;
    AudioSource sound;
    AudioClip[] clips;
    AudioClip backClip;
    AudioClip clearClip;

    // Start is called before the first frame update
    void Start()
    {
        buttons = new Button[10];
        //audioSources = new AudioSource[10];
        clips = new AudioClip[10];

        sound = GameObject.Find("Audio").GetComponent<AudioSource>();

        for (int i = 0; i < 10; i++)
        {
            int buttonIndex = i;
            buttons[i] = GameObject.Find("Button" + buttonIndex).GetComponent<Button>();
            buttons[i].onClick.AddListener(() => ButtonClicked(buttonIndex));

            clips[i] = Resources.Load<AudioClip>("Audio/" + i.ToString());
            //Debug.Log(clips[i]);
        }

        backClip = Resources.Load<AudioClip>("Audio/back");
        clearClip = Resources.Load<AudioClip>("Audio/clear");

        display = GameObject.Find("display").GetComponent<TextMeshProUGUI>();
        display.text = enteredNumbers;
    }

    void ButtonClicked(int buttonIndex)
    {
        if (enteredNumbers.Length >= maxEnter)
            return;

        //Debug.Log(buttonIndex + "is pushed");
        enteredNumbers += buttonIndex.ToString();
        display.text = FormatEnteredNumbers();
        //Debug.Log(enteredNumbers.Length);
        sound.clip = clips[buttonIndex];
        sound.Play();
    }

    string FormatEnteredNumbers()
    {
        if (enteredNumbers.Length >= 9)
        {
            return enteredNumbers.Substring(0, 8) + "-" + enteredNumbers.Substring(8);
        }
        else
        {
            return enteredNumbers;
        }
    }


    public void back()
    {
        if (enteredNumbers.Length > 4)
        {
            enteredNumbers = enteredNumbers.Substring(0, enteredNumbers.Length - 1);
            display.text = FormatEnteredNumbers();
            sound.clip = backClip;
            sound.Play();
        }
    }

    public void clear()
    {
        //Debug.Log("clear button is pushed");

        if (enteredNumbers.Length == maxEnter)
        {
            Debug.Log("완성");
            GetComponent<PhotonView>().RPC("SendEnteredNumbersToServer", RpcTarget.All, enteredNumbers);
        }
        else
        {
            Debug.Log("실패");
        }

        sound.clip = clearClip;
        sound.Play();
    }
}
