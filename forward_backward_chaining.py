# ( {pozytywne}, {negatywne} )
RULES = [
    ({"ograniczenie do 50", "szybkość ponizej 50"}, set(), "prawidłowa predkosc"),
    (set(), {"prawidłowa predkosc"}, "nalezy zwolnic"),  # ~prawidłowa predkosc -> nalezy zwolnic
    ({"prawidłowa predkosc", "trudne warunki"}, set(), "nalezy zwolnic"),
    ({"prawidłowa predkosc"}, {"trudne warunki"}, "jedz jak chcesz"),  # prawidłowa && ~trudne -> jedz
    ({"mgla"}, set(), "trudne warunki"),
    ({"snieg"}, set(), "trudne warunki"),
    ({"ograniczenie do 90", "szybkość ponizej 90"}, set(), "prawidłowa predkosc")
]


def forward_chaining(facts):
    known_facts = set(facts)
    new_discovery = True

    while new_discovery:
        new_discovery = False
        for pos_pre, neg_pre, conclusion in RULES:
            if pos_pre.issubset(known_facts) and \
                    all(n not in known_facts for n in neg_pre) and \
                    conclusion not in known_facts:
                known_facts.add(conclusion)
                new_discovery = True
    return known_facts


def backward_chaining(goal, facts):
    if goal in facts:
        return True

    for pos_pre, neg_pre, conclusion in RULES:
        if conclusion == goal:
            pos_ok = all(backward_chaining(p, facts) for p in pos_pre)

            neg_ok = all(not backward_chaining(n, facts) for n in neg_pre)

            if pos_ok and neg_ok:
                return True

    return False


print("Dostępne fakty: ograniczenie do 50, ograniczenie do 90, szybkość ponizej 50, szybkość ponizej 90, mgla, snieg")

user_input = input("\nWpisz fakty oddzielone przecinkiem: ").lower()
current_facts = {f.strip() for f in user_input.split(",") if f.strip()}

print(f"\nAktywne fakty: {current_facts}")
print("-" * 30)

result_forward = forward_chaining(current_facts)
print(f"Wnioskowanie w przód - Odkryte fakty: {sorted(result_forward)}")

goal = "nalezy zwolnic"
print(f"\nWnioskowanie w tył - Sprawdzam cel: '{goal}'...")
if backward_chaining(goal, current_facts):
    print(f"WYNIK: TAK, należy zwolnić.")
else:
    print(f"WYNIK: NIE, nie ma podstaw do zwolnienia.")