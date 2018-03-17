name = config['name']

rule rulename1:
     input:
        "hello.txt"

rule target1:
     output:
        "hello.txt"
     shell:
        "echo hello {name} > {output}"

rule target2:
     output:
        "goodbye.txt"
     shell:
        "echo goodbye {name} > {output}"
