using UnityEngine;
using TMPro;

public class PlayerHealthV : MonoBehaviour
{
    public int maxHealth = 100;
    public int health;

    public int maxSanity = 100;
    public int sanity;

    public TMP_Text healthText;
    public TMP_Text sanityText;

    void Start()
    {
        health = maxHealth;
        sanity = maxSanity;

        UpdateUI();
    }

    public void TakeDamage(int amount)
    {
        health -= amount;
        health = Mathf.Clamp(health, 0, maxHealth);
        UpdateUI();
    }

    void UpdateUI()
    {
        healthText.text = "Health: " + health;
        sanityText.text = "Sanity: " + sanity;
    }
}