using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Meter : MonoBehaviour
{
    public float air = 10f;
    public float maxAir = 10f;
    public float airburnRate = 1f;

    public Texture2D bgTexture;
    public Texture2D airBarTexture;
    public int iconWidth = 32;
    public Vector2 airOffset = new Vector2(10, 10);

    private PlayerMovement Player;
    // Start is called before the first frame update
    void Start()
    {
        Player = GameObject.FindObjectOfType<PlayerMovement>();
    }

    void OnGUI()
    {
        var percent = Mathf.Clamp01(air / maxAir);

        if (!Player)
            percent = 0;

        DrawMeter(airOffset.x, airOffset.y, airBarTexture, bgTexture, percent);
    }

    void DrawMeter(float x, float y, Texture2D texture, Texture2D background, float percent)
    {
        var bgW = background.width;
        var bgH = background.height;

        GUI.DrawTexture(new Rect(x, y, bgW, bgH), background);

        var nW = ((bgW - iconWidth) * percent) + iconWidth;

        GUI.BeginGroup(new Rect(x, y, nW, bgH));
        GUI.DrawTexture(new Rect(0, 0, bgW, bgH), texture);
        GUI.EndGroup();
    }

    // Update is called once per frame
    void Update()
    {
        if (!Player)
            return;
        if(air > 0)
        {
            air -= Time.deltaTime * airburnRate;
        }
        else
        {
            Explode script = Player.GetComponent<Explode>();
            script.OnExplode();
        }
    }

    
}
