using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[RequireComponent(typeof(ControlP))]
public class CameraGo : MonoBehaviour
{
    public Transform cameraTransform;

    private ControlP control;

    void Start()
    {
        control = GetComponent<ControlP>();
    }

    void Update()
    {
        float h = Input.GetAxis("Horizontal");
        float v = Input.GetAxis("Vertical");

        Vector3 forward = cameraTransform.forward;
        Vector3 right = cameraTransform.right;

        forward.y = 0f;
        right.y = 0f;

        forward.Normalize();
        right.Normalize();

        Vector3 move = forward * v + right * h;

        control.moveDirection = move;
    }
}
