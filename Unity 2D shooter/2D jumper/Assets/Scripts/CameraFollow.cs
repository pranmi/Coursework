using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CameraFollow : MonoBehaviour
{
    // Start is called before the first frame update
    public GameObject target;

    private Transform _t;
    private Camera camera;

    void Awake()
    {
        camera = GetComponent<Camera>();
        camera.orthographicSize = ((Screen.height / 2.0f) / 100f);
    }

    void Start()
    {
        _t = target.transform;
    }

    // Update is called once per frame
    void Update()
    {
        if(_t)
        transform.position = new Vector3(_t.position.x, _t.position.y, _t.position.z - 10f);
    }
}
