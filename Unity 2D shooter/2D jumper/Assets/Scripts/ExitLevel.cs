using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;

public class ExitLevel : MonoBehaviour
{
    public string scene;
    public AudioSource audioSource;
    public AudioClip clip;
    public float volume = 0.5f;
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
        if(target.gameObject.tag == "Player")
        {
            audioSource.PlayOneShot(clip, volume);
            Destroy(target.gameObject);
            SceneManager.LoadScene(scene);
        }
    }
}
