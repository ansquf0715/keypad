using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Photon.Pun;
using Photon.Realtime;

public class transmission : MonoBehaviour
{
    void Start()
    {
        Screen.SetResolution(960, 600, false);
        PhotonNetwork.ConnectUsingSettings();
    }

    public void OnConnectedToMaster()
    {
        RoomOptions options = new RoomOptions();
        options.MaxPlayers = 5;
        PhotonNetwork.JoinOrCreateRoom("Room1", options, null);
    }
}
