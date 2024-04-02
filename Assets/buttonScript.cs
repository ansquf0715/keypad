using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using TMPro;

public class buttonScript : MonoBehaviour
{
    private string enteredNumbers = "010";
    public Button[] buttons;
    TextMeshProUGUI display;

    void Start()
    {
        buttons = new Button[10];

        for(int i=0; i<10; i++)
        {
            int buttonIndex = i;
            buttons[i] = GameObject.Find("Button" + buttonIndex).GetComponent<Button>();
            buttons[i].onClick.AddListener(() => ButtonClicked(buttonIndex));
        }

        display = GameObject.Find("display").GetComponent<TextMeshProUGUI>();
        display.text = enteredNumbers;
    }

    void ButtonClicked(int buttonIndex)
    {
        //Debug.Log(buttonIndex + "is pushed");
        enteredNumbers += buttonIndex.ToString();
        //display.text = enteredNumbers;
        display.text = FormatEnteredNumbers();
    }

    //010- 형식 포맷 만들기부터 수정
    string FormatEnteredNumbers()
    {
        if(enteredNumbers.Length >= 4)
        {
            return enteredNumbers.Substring(0, 4) + " - " + enteredNumbers.Substring(4);
        }
        else
        {
            return enteredNumbers;
        }
    }


    public void back()
    {
        if(enteredNumbers.Length > 0)
        {
            enteredNumbers = enteredNumbers.Substring(0, enteredNumbers.Length - 1);
            display.text = enteredNumbers;
        }
    }

    public void clear()
    {
        Debug.Log("clear button is pushed");
    }
}
