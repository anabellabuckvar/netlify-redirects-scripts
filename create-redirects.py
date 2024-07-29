import sys

 ## name of the txt file to run script on, ex: "spark-connector.txt"
SOURCE_FILENAME = sys.argv[1] 
## base path for given propertydocs/spark-connector
BASE = sys.argv[2] 
SOURCE_FILE = './mut-redirects/'+SOURCE_FILENAME
DESTINATION_FILE = "./netlify-redirects/netlify-"+SOURCE_FILENAME




def transform(rule: str) -> str:
    ##remove either the explicit prefix or the prefix representation from source path
    if not rule.find(BASE) == -1:
        rule = rule.split(BASE)[1]
    elif not rule.find("${prefix}") == -1:
        rule = rule.split("${prefix}")[1]

    # remove base if in path
    if rule.startswith(" ${base}"):
        rule = rule.split(" ${base}")[1]

    # remove version if in path
    if rule.startswith("/${version}"):
        rule = rule.split("/${version}")[1]

    if not rule.startswith("/"):
        rule = "/"+rule
    return rule


def main() -> None:
    with open(SOURCE_FILE, "r") as f:
        rules = []
        comment = []
        for line in f.read().split("\n"):
            line.split("->", 1)
            rule = line.split("->", 1)
            if (len(rule) > 1) & (not rule[0].startswith("#")): 
                rules.append((rule[0].split(None, 1)[1], rule[1]))
                comment.append("##"+line)
                    

    output_rules = []

    for index, rule in enumerate(rules):
        ##transform source and destination paths
        rule_from = transform(rule[0]).strip()
        rule_to = transform(rule[1]).strip()

        ##add comment, from and to keyword, quotes, line separation
        output_rules.append(comment[index] +"\n[[redirects]] \rfrom = \""+ rule_from + "\"\rto = \""+ rule_to + "\"\r\r")



    with open(DESTINATION_FILE, "w") as f:
        f.write("".join(output_rules))



if __name__ == "__main__":
    main()