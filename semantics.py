import itertools

class AbstractArgumentationFramework:
    def __init__(self):
        self.arguments = set()
        self.attacks = set()

    def add_argument(self, argument):
        self.arguments.add(argument)

    def add_attack(self, attacker, target):
        self.arguments.add(attacker)
        self.arguments.add(target)
        self.attacks.add((attacker, target))

    def get_grounded_extension(self):
        in_args = set()
        out_args = set()
        attackers = {arg: set() for arg in self.arguments}
        for attacker, target in self.attacks:
            attackers[target].add(attacker)

        while True:
            added_to_in = False
            for arg in self.arguments:
                if arg not in in_args and arg not in out_args:
                    if all(attacker in out_args for attacker in attackers[arg]):
                        in_args.add(arg)
                        added_to_in = True
            for arg in self.arguments:
                if arg not in in_args and arg not in out_args:
                    if any(attacker in in_args for attacker in attackers[arg]):
                        out_args.add(arg)
            if not added_to_in:
                break
        return in_args

    def get_preferred_extensions(self):
        def is_conflict_free(arg_set):
            for attacker, target in self.attacks:
                if attacker in arg_set and target in arg_set:
                    return False
            return True

        def defends_itself(arg_set):
            for arg in arg_set:
                attackers = [a for a, t in self.attacks if t == arg]
                for attacker in attackers:
                    defended = any((defender, attacker) in self.attacks for defender in arg_set)
                    if not defended:
                        return False
            return True

        admissible_sets = []
        arg_list = list(self.arguments)

        for i in range(len(arg_list), -1, -1):
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

class Argument:
    def __init__(self, conclusion, rules=None, sub_args=None):
        self.name = conclusion
        self.conclusion = conclusion
        self.rules = rules or []
        self.sub_args = sub_args or []

def is_contradiction(c1, c2):
    return c1 == "~" + c2 or c2 == "~" + c1

def generate_attacks(arguments):
    direct_attacks = set()

    for arg1 in arguments:
        for arg2 in arguments:
            if arg1 == arg2: continue

            if is_contradiction(arg1.conclusion, arg2.conclusion):
                direct_attacks.add((arg1.name, arg2.name))

            if arg1.conclusion.startswith("~") and arg1.conclusion[1:] in arg2.rules:
                direct_attacks.add((arg1.name, arg2.name))

    all_attacks = set(direct_attacks)
    for attacker, target in direct_attacks:
        for arg in arguments:
            if target in arg.sub_args:
                all_attacks.add((attacker, arg.name))

    return list(all_attacks)


# --- NOWE DANE WEJŚCIOWE ---

# Kn = a
arg_a = Argument("a")

# Kp = b, c, d, e, f, g, h
arg_b = Argument("b")
arg_c = Argument("c")
arg_d = Argument("d")
arg_e = Argument("e")
arg_f = Argument("f")
arg_g = Argument("g")
arg_h = Argument("h")

# Rs = {r1: a -> i}
arg_i = Argument("i", rules=["r1"], sub_args=["a"])

# Rd = {r2: b => j, r3: c => ~j, r4: i, d => ~r3, r5: e => ~d, r6: f => ~e, r7: g => k, r8: h => ~k}
arg_j = Argument("j", rules=["r2"], sub_args=["b"])
arg_not_j = Argument("~j", rules=["r3"], sub_args=["c"])
arg_not_r3 = Argument("~r3", rules=["r4"], sub_args=["i", "d"])
arg_not_d = Argument("~d", rules=["r5"], sub_args=["e"])
arg_not_e = Argument("~e", rules=["r6"], sub_args=["f"])
arg_k = Argument("k", rules=["r7"], sub_args=["g"])
arg_not_k = Argument("~k", rules=["r8"], sub_args=["h"])

# Pełna lista argumentów
arguments_list = [
    arg_a, arg_b, arg_c, arg_d, arg_e, arg_f, arg_g, arg_h,
    arg_i, arg_j, arg_not_j, arg_not_r3, arg_not_d, arg_not_e, arg_k, arg_not_k
]

# --- KONIEC NOWYCH DANYCH ---

attacks = generate_attacks(arguments_list)
dung_framework = AbstractArgumentationFramework()

for arg in arguments_list:
    dung_framework.add_argument(arg.name)

for attacker, target in attacks:
    dung_framework.add_attack(attacker, target)

grounded = dung_framework.get_grounded_extension()
preferred = dung_framework.get_preferred_extensions()

print("--- Wygenerowane ataki (ASPIC+) ---")
for a, t in sorted(attacks):
    print(f"{a} atakuje {t}")

print("\n--- Wyniki Semantyk ---")
print(f"Semantyka Ugruntowana (Grounded): \n  {sorted(list(grounded))}")

print("\nSemantyka Preferowana (Preferred):")
for i, ext in enumerate(preferred, 1):
    print(f"  Opcja {i}: {sorted(list(ext))}")

odrzucone = sorted(list(dung_framework.arguments - grounded))
print(f"\nOdrzucone lub nierozstrzygnięte: \n  {odrzucone}")