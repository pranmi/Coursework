using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;

public class Explode : MonoBehaviour
{

    public BodyParts bodyPart;
    public int totalParts = 8;
    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    void OnTriggerEnter2D(Collider2D target)
    {
        if (target.gameObject.tag == "Deadlier")
            OnExplode();
    }

    void OnCollisionEnter2D(Collision2D target)
    {
        if (target.gameObject.tag == "Deadlier")
            OnExplode();
    }

    public void OnExplode()
    {
        Destroy(gameObject);

        var t = transform;
        for(int i = 0; i < totalParts; i++)
        {
            t.TransformPoint(0, -100, 0);
            BodyParts clone = Instantiate(bodyPart, t.position, Quaternion.identity) as BodyParts;
            clone.myRB2D.AddForce(Vector3.right * Random.Range(-50, 50));
            clone.myRB2D.AddForce(Vector3.up * Random.Range(100, 400));
        }
        GameObject go = new GameObject("CLicktoContinue");
        ClickToContinue script = go.AddComponent<ClickToContinue>();
        Scene scene = SceneManager.GetActiveScene();
        script.scene = scene.name;

        go.AddComponent<DisplayRestartText>();
    }
}
