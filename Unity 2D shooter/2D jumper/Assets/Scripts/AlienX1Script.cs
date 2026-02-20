using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class AlienX1Script : MonoBehaviour
{

    public float attackDelay = 3f;
    public XProjectile xprojectile;

    private Animator animator;
    // Start is called before the first frame update
    void Start()
    {
        animator = GetComponent<Animator>();

        if(attackDelay > 0)
        {
            StartCoroutine(OnAttack());
        }
    }

    // Update is called once per frame
    void Update()
    {
        animator.SetInteger("AnimState", 0);
    }

    IEnumerator OnAttack()
    {
        yield return new WaitForSeconds(attackDelay);
        Fire();
        StartCoroutine(OnAttack());
    }

    void Fire()
    {
        animator.SetInteger("AnimState", 1);
    }

    void OnShoot()
    {
        if (xprojectile)
        {
            XProjectile clone = Instantiate(xprojectile, transform.position, Quaternion.identity) as XProjectile;
        }
    }
}
