using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class AlienX1Vertical : MonoBehaviour
{
    public AudioClip attackSound;
    public float attackDelay = 3f;
    public TestProjectileVertical testprojectilevertical;

    private Animator animator;
    // Start is called before the first frame update
    void Start()
    {
        animator = GetComponent<Animator>();

        if (attackDelay > 0)
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
        if (attackSound)
            AudioSource.PlayClipAtPoint(attackSound, transform.position);
    }

    void OnShoot()
    {
        if (testprojectilevertical)
        {
            TestProjectileVertical clone = Instantiate(testprojectilevertical, transform.position, transform.rotation) as TestProjectileVertical;
        }
    }
}
