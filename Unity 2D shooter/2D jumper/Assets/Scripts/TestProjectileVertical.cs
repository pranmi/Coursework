using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class TestProjectileVertical : MonoBehaviour
{
    Rigidbody2D rb;
    public float thrust = 10f;
    // Start is called before the first frame update
    void Start()
    {
        rb = GetComponent<Rigidbody2D>();
        Fire();
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    void OnCollisionEnter2D(Collision2D target)
    {
        Destroy(gameObject);
    }

    void Fire()
    {
        rb.AddForce(transform.up * thrust, ForceMode2D.Impulse);
    }
}
