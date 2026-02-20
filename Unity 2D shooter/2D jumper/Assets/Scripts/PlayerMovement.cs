using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PlayerMovement : MonoBehaviour
{
    public float speed = 10f;
    public Vector2 maxVelocity = new Vector2(3, 5);
    public bool standing;
    public float jetSpeed = 5f;
    public float airSpeedMultiplier = .3f;

    public AudioClip leftFootSound;
    public AudioClip rightFootSound;
    public AudioClip thudSound;
    public AudioClip rocketSound;

    private Rigidbody2D rb;
    private PlayerController controller;
    private Animator animator;

    public TestProjectileVertical testprojectilevertical;

    // Start is called before the first frame update
    void Start()
    {
        rb = GetComponent<Rigidbody2D>();
        controller = GetComponent<PlayerController>();
        animator = GetComponent<Animator>();
    }


    void PlayLeftFootSound()
    {
        if (leftFootSound)
            AudioSource.PlayClipAtPoint(leftFootSound, transform.position);
    }

    void PlayRightFootSound()
    {
        if (rightFootSound)
            AudioSource.PlayClipAtPoint(rightFootSound, transform.position);
    }

    void OnCollisionEnter2D(Collision2D target)
    {
        if (!standing)
        {
            var absVelX = Mathf.Abs(rb.velocity.x);
            var absVelY = Mathf.Abs(rb.velocity.y);

            if(absVelX <= .1f || absVelY <= .1f)
            {
                if (thudSound)
                    AudioSource.PlayClipAtPoint(thudSound, transform.position);
            }
        }
    }

    void PLayRocketSound()
    {
        if (!rocketSound || GameObject.Find("RocketSound"))
            return;

        GameObject go = new GameObject("RocketSound");
        AudioSource aSrc = go.AddComponent<AudioSource>();
        aSrc.clip = rocketSound;
        aSrc.volume = 0.25f;
        aSrc.Play();

        Destroy(go, rocketSound.length);
    }
    // Update is called once per frame
    void Update()
    {
        var forceX = 0f;
        var forceY = 0f;

        var absVelX = Mathf.Abs(rb.velocity.x);
        var absVelY = Mathf.Abs(rb.velocity.y);

        if (absVelY < .2f)
        {
            standing = true;
        }
        else
        {
            standing = false;
        }

        if(controller.playerMoving.x != 0)
        {
            if(absVelX < maxVelocity.x)
            {
                forceX = standing ? speed * controller.playerMoving.x : (speed * controller.playerMoving.x * airSpeedMultiplier);
                transform.localScale = new Vector3(forceX > 0 ? -2 : 2, 2, 1);
            }

            animator.SetInteger("AnimState", 1);
        }
        else
        {
            animator.SetInteger("AnimState", 0);
        }


       if(controller.playerMoving.y > 0)
        {
            PLayRocketSound();
            if (absVelY < maxVelocity.y)
                forceY = jetSpeed * controller.playerMoving.y;

            animator.SetInteger("AnimState", 2);
        }else if(absVelY > 0)
        {
            animator.SetInteger("AnimState", 3);
        }

        rb.AddForce(new Vector2(forceX, forceY));

        if (Input.GetKey("space")){
            shootMagic();
        }
    }

    void shootMagic()
    {
        animator.SetInteger("AnimState", 5);

    }

    void OnShoot()
    {
        if (testprojectilevertical)
        {
            TestProjectileVertical clone = Instantiate(testprojectilevertical, transform.position, transform.rotation) as TestProjectileVertical;
        }
    }
}
