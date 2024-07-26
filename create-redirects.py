

def transform(rule: str) -> str:
    print(rule)
    if rule.startswith(" ${base}"):
        rule = rule.split(" ${base}")[1]
    if rule.startswith("/${version}"):
        print("START")
        rule = rule.split("/${version}")[1]
    ##add leading slash to rules
    print(rule)
    return rule

def main() -> None:
    source_file =  "docs-k8s-operator.txt"
    destination_file = "netlify-docs-k8s-operator.txt"
    from_base = "docs/kubernetes-operator"

    with open(source_file, "r") as f:
        rules = [
            (rule[0].split(None, 1)[1], rule[1])
            for rule in (line.split("->", 1) for line in f.read().split("\n"))
            if len(rule) >1
        ]
    output_rules = []

    for rule_from, rule_to in rules[2:]:
        rule_from = rule_from.split(from_base)[1]
        rule_from = transform(rule_from)
        rule_to = transform(rule_to)

        
        ##replace version, delete base and or/stable in rule to
        output_rules.append("from = "+ rule_from + "\rto = "+ rule_to + "\r")
        # print(f"raw: {rule_from} -> {rule_to}")

    with open(destination_file, "w") as f:
        f.write("[[redirects]] \r" + (" \r [[redirects]] \r").join(output_rules))



if __name__ == "__main__":
    main()