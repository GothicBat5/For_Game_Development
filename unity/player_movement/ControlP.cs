using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[RequireComponent(typeof(CharacterController))]
public class ControlP : MonoBehaviour
{
    /*
if it's still floaty
gravity = -20f;
jumpForce = 2.5f;
fallMultiplier = 2.5f or 3f;

*/
    public float moveSpeed = 6f;
    public float jumpForce = 1.8f;
    public float gravity = -9.81f;
    public float fallMultiplier = 2.5f; 

    private CharacterController controller;
    private Vector3 velocity;
    private bool isGrounded;

    [HideInInspector] public Vector3 moveDirection;

    void Start()
    {
        controller = GetComponent<CharacterController>();
    }

    void Update()
    {
        GroundCheck();
        Move();
        ApplyGravity();
        Jump();
    }

    void GroundCheck()
    {
        isGrounded = controller.isGrounded;
    }

    void Move()
    {
        Vector3 move = moveDirection * moveSpeed;
        controller.Move(move * Time.deltaTime);
    }

    void ApplyGravity()
    {
        if (isGrounded && velocity.y < 0)
        {
            velocity.y = -2f;  // small downward force to keep grounded
        }

        if (velocity.y < 0)
        {
            velocity.y += gravity * fallMultiplier * Time.deltaTime;
        }
        else
        {
            velocity.y += gravity * Time.deltaTime;
        }

        controller.Move(velocity * Time.deltaTime);
    }


    void Jump()
    {
        if (Input.GetKeyDown(KeyCode.Space) && isGrounded)
        {
            velocity.y = Mathf.Sqrt(jumpForce * -2f * gravity);
        }
    }
}
