using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class BodyParts : MonoBehaviour
{
    public Rigidbody2D myRB2D;

    private SpriteRenderer spriteRenderer;
    private Renderer myRenderer;
    private Color start;
    private Color end;
    private float t = 0.0f;
    // Start is called before the first frame update
    void Start()
    {
        spriteRenderer = GetComponent<SpriteRenderer>();
        myRenderer = GetComponent<Renderer>();
        myRB2D = GetComponent<Rigidbody2D>();
        start = spriteRenderer.color;
        end = new Color(start.r, start.g, start.b, 0.0f);
    }

    // Update is called once per frame
    void Update()
    {
        t += Time.deltaTime;

        myRenderer.material.color = Color.Lerp(start, end, t / 2);

        if (myRenderer.material.color.a <= 0.0)
            Destroy(gameObject);
    }
}
