import itertools


def get_grounded_extension(arguments, attacks):
    """Zwraca rozszerzenie ugruntowane (zawsze jeden zbiór)."""
    in_args = set()
    out_args = set()

    attackers = {arg: set() for arg in arguments}
    for attacker, target in attacks:
        if attacker in arguments and target in arguments:
            attackers[target].add(attacker)

    while True:
        added_to_in = False
        for arg in arguments:
            if arg not in in_args and arg not in out_args:
                if all(attacker in out_args for attacker in attackers[arg]):
                    in_args.add(arg)
                    added_to_in = True

        for arg in arguments:
            if arg not in in_args and arg not in out_args:
                if any(attacker in in_args for attacker in attackers[arg]):
                    out_args.add(arg)

        if not added_to_in:
            break

    return in_args


def get_preferred_extensions(arguments, attacks):
    """Zwraca listę rozszerzeń preferowanych (maksymalnych zbiorów dopuszczalnych)."""

    def is_conflict_free(arg_set):
        for attacker, target in attacks:
            if attacker in arg_set and target in arg_set:
                return False
        return True

    def defends_itself(arg_set):
        for arg in arg_set:
            # Znajdź wszystkich, którzy atakują nasz argument
            attackers = [a for a, t in attacks if t == arg]
            for attacker in attackers:
                # Sprawdź, czy w naszym zbiorze jest ktoś, kto kontratakuje
                defended = any((defender, attacker) in attacks for defender in arg_set)
                if not defended:
                    return False
        return True

    admissible_sets = []
    arg_list = list(arguments)
    n = len(arg_list)

    for i in range(n, -1, -1):
        for combo in itertools.combinations(arg_list, i):
            subset = set(combo)
            if is_conflict_free(subset) and defends_itself(subset):
                admissible_sets.append(subset)

    preferred_extensions = []
    for adm_set in admissible_sets:
        is_maximal = True
        for pref_ext in preferred_extensions:
            if adm_set.issubset(pref_ext):
                is_maximal = False
                break
        if is_maximal:
            preferred_extensions.append(adm_set)

    return preferred_extensions



args = {'A', 'B', 'C', 'D', 'E'}
atts = [
    ('A', 'B'),
    ('B', 'C'),
    ('B', 'D'),
    ('D', 'B'),
    ('D', 'E'),
    ('E', 'D')
]

grounded = get_grounded_extension(args, atts)
preferred = get_preferred_extensions(args, atts)

print("--- Graf Argumentacji ---")
print(f"Argumenty: {sorted(args)}")
print(f"Ataki: {atts}\n")

print("--- Wyniki Semantyk ---")
print(f"Grounded (Ugruntowana): {sorted(list(grounded))}")

print("Preferred (Preferowana):")
for i, ext in enumerate(preferred, 1):
    print(f"  Opcja {i}: {sorted(list(ext))}")