using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PlayerController : MonoBehaviour
{
    public Vector2 playerMoving = new Vector2();
    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        playerMoving.x = playerMoving.y = 0;

        if (Input.GetKey("right"))
        {
            playerMoving.x = 1;
        }else if (Input.GetKey("left"))
        {
            playerMoving.x = -1;
        }

        if (Input.GetKey("up"))
        {
            playerMoving.y = 1;
        }
        else if (Input.GetKey("down"))
        {
            playerMoving.y = -1;
        }
    }

}
