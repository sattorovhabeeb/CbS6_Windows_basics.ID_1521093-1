import random


def mod_exp(base, exp, mod):
    return pow(base, exp, mod)


def generate_keys(p, g):
    private_key = random.randint(2, p - 2)
    public_key = mod_exp(g, private_key, p)
    return private_key, public_key


def compute_shared_secret(public_key, private_key, p):
    secret = mod_exp(public_key, private_key, p)
    return secret


def main():
    p = 23  # Простое число
    g = 5  # Генератор

    alice_private, alice_public = generate_keys(p, g)
    print(f"Alice: Приватный ключ = {alice_private}, Публичный ключ = {alice_public}")

    bob_private, bob_public = generate_keys(p, g)
    print(f"Bob: Приватный ключ = {bob_private}, Публичный ключ = {bob_public}")

    # Вычисление общего секрета для Alice и Bob
    alice_secret = compute_shared_secret(alice_public, alice_private, p)
    bob_secret = compute_shared_secret(bob_public, bob_private, p)

    print(f"Alice: Общий секрет = {alice_secret}")
    print(f"Bob: Общий секрет = {bob_secret}")


if __name__ == "__main__":
    main()
