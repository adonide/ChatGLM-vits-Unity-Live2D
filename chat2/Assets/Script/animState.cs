using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class animState : MonoBehaviour
{
    // Start is called before the first frame update
    static Animator animator;
    static AnimatorStateInfo animatorInfo;
    void Start()
    {
        animator = GameObject.Find("mao_pro_t02").GetComponent<Animator>();

    }

    // Update is called once per frame
    void Update()
    {
        animatorInfo = animator.GetCurrentAnimatorStateInfo(0);
        if ((animatorInfo.normalizedTime > 1.0f) && (animatorInfo.IsName("mtn_02")))
        {
            animator.SetBool("feeling", false);
        }
    }
}
