SOURCE_FILENAME = "spark-connector.txt"
SOURCE_FILE = './mut-redirects/'+SOURCE_FILENAME
DESTINATION_FILE = "./netlify-redirects/netlify-"+SOURCE_FILENAME
BASE = "docs/spark-connector"


def transform(rule: str) -> str:
    # remove base if in rule
    if rule.startswith(" ${base}"):
        rule = rule.split(" ${base}")[1]
    # remove version if in path
    if rule.startswith("/${version}"):
        rule = rule.split("/${version}")[1]
    ##add leading slash to rules
    return rule

def main() -> None:
    with open(SOURCE_FILE, "r") as f:
        rules = [
            (rule[0].split(None, 1)[1], rule[1])
            ##split each line into origin and destination path
            for rule in (line.split("->", 1) for line in f.read().split("\n"))
            ##check that the line parsed is a redirect rule and not a symlink rule 
            if len(rule) >1
            if not rule[0].startswith("symlink")
        ]
    output_rules = []

    for rule_from, rule_to in rules[2:]:
        if not rule_from.find(BASE) == -1:
            rule_from = rule_from.split(BASE)[1]
        elif not rule_from.find("${prefix}") == -1:
            rule_from = rule_from.split("${prefix}")[1]
        rule_from = transform(rule_from)
        rule_to = transform(rule_to)

        
        output_rules.append("from = "+ rule_from + "\rto = "+ rule_to + "\r")

    with open(DESTINATION_FILE, "w") as f:
        f.write("[[redirects]] \r" + (" \r[[redirects]] \r").join(output_rules))



if __name__ == "__main__":
    main()