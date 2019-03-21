import os
import re
import json
import pathlib
import argparse

from prestring.python import PythonModule

### パーツは全てクラス定義一つであることを仮定
# TODO: キーワード引数(デフォルト引数)はJS側を編集すべき？ -> はい
# TODO: 文字列連結はJS側を編集すべき？

parser = argparse.ArgumentParser()
parser.add_argument("--file", help="set specific file[directory] name", type=str)
args = parser.parse_args()

def snake(text):
    if text.isupper():
        return text
    return re.sub("([A-Z])+",lambda x:"_" + x.group().lower(), text)

def get_statement(stt, module, replace_from="_DummyString_", replace_to=""):
    if stt["type"] == "ExpressionStatement":
        exp = stt["expression"]
        # 特殊処理(Object.defineProperty)
        if "callee" in exp and get_expression(exp["callee"]) == snake("Object.defineProperty"):
            for attr in exp["arguments"][2]["properties"]:
                with module.def_(get_expression(attr["key"])):
                    for line in attr["value"]["body"]["body"]:
                        get_statement(line, module)
                statements = ("setattr(" +
                    get_expression(exp["arguments"][0]) +
                    ", " +
                    get_expression(exp["arguments"][1]) +
                    ", " +
                    get_expression(attr["key"]) +
                    ")")
                module.stmt(statements)
            return
        module.stmt(get_expression(exp).replace(replace_from, replace_to))
        return
    
    if stt["type"] == "MethodDefinition":
        name = snake(stt["key"]["name"])
        method_name = "__init__" if name == "constructor" else name
        args = []
        if stt["static"]:
            module.stmt("@staticmethod")
        else:
            args.append("self")
        for arg in stt["value"]["params"]:
            args.append(snake(arg["name"]))
        if stt["value"]["async"]:
            with module.async_def_(method_name, *args):
                content = stt["value"]
                for line in content["body"]["body"]:
                    get_statement(line, module)
        else:
            with m.def_(method_name, *args):
                content = stt["value"]
                for line in content["body"]["body"]:
                    get_statement(line, module)
        return

    if stt["type"] == "ClassDeclaration":
        base = "" if stt["superClass"] is None else stt["superClass"]
        with module.class_(get_expression(stt["id"]), bases=base):
            bodies = stt["body"]["body"]
            for body in bodies:
                get_statement(body, module)
        return
    
    if stt["type"] == "FunctionDeclaration":
        name = snake(get_expression(stt["id"]))
        args = []
        for arg in stt["params"]:
            args.append(snake(get_expression(arg)))
        with module.def_(name, *args):
            for line in stt["body"]["body"]:
                get_statement(line, module)
        return

    if stt["type"] == "ReturnStatement":
        exp = stt["argument"]
        if exp:
            module.stmt("return " + get_expression(exp))
        else:
            module.stmt("return")
        return

    if stt["type"] == "IfStatement":
        with module.if_(get_expression(stt["test"])):
            if "body" in stt["consequent"]:
                for line in stt["consequent"]["body"]:
                    get_statement(line, module)
            else:
                get_statement(stt["consequent"], module)
        if not stt["alternate"]:
            return
        consequent = stt["alternate"]
        while consequent and consequent["type"] == "IfStatement":
            with module.elif_(get_expression(consequent["test"])):
                if "body" in consequent["consequent"]:
                    for line in consequent["consequent"]["body"]:
                        get_statement(line, module)
                else:
                    get_statement(consequent["consequent"], module)
            consequent = consequent["alternate"]
        if consequent:
            with module.else_():
                if "body" in consequent:
                    for line in consequent["body"]:
                        get_statement(line, module)
                    return
                else:
                    get_statement(consequent, module)
                    return
        return
    
    if stt["type"] == "SwitchStatement":
        cases = stt["cases"]
        fst = cases.pop(0)
        with module.if_(get_expression(stt["discriminant"]) +
            "==" +
            get_expression(fst["test"])):
            for line in fst["consequent"]:
                if line["type"] != "BreakStatement":
                    get_statement(line, module)
        for case in cases:
            if not case["test"]:
                with module.else_():
                    for line in case["consequent"]:
                        get_statement(line, module)
            else:
                with module.elif_(get_expression(stt["discriminant"]) +
                    "==" +
                    get_expression(case["test"])):
                    for line in case["consequent"]:
                        if line["type"] != "BreakStatement":
                            get_statement(line, module)
        return

    if stt["type"] == "VariableDeclaration":
        for dec in stt["declarations"]:
            if dec["init"]:
                module.stmt(
                    dec["id"]["name"] +
                    " = " +
                    get_expression(dec["init"]))
            else:
                module.stmt(
                    dec["id"]["name"] +
                    " = None"
                )
        return

    if stt["type"] == "WhileStatement":
        with module.while_(get_expression(stt["test"])):
            if "body" in stt["body"]:
                for line in stt["body"]["body"]:
                    get_statement(line, module)
            else:
                get_statement(stt["body"], module)
        return

    if stt["type"] == "ForStatement":
        # TODO:
        try:
            # i = stt["init"]["declarations"][0]["id"]["name"]
            # if (get_expression(stt["init"]["declarations"][0]["init"]) == "0" and
            #     ("length" in stt["test"]["left"] or "length" in stt["test"]["right"]) and
            #     stt["update"]["operator"] == "++"):
            #     with module.for_("_i", iterator=iterator):
            #         for line in stt["body"]["body"]:
            #             get_statement(line,
            #                 module,
            #                 replace_from=iterator + "[" + i + "]",
            #                 replace_to="_i")
            #     return
            # else:
            #     module.stmt("# TODO: failed to generate FOR statement")
            #     return
            iterator = get_expression(stt["init"]["declarations"][0]["id"])
            init = get_expression(stt["init"]["declarations"][0]["init"])
            if get_expression(stt["test"]["left"]) == iterator:
                limit = get_expression(stt["test"]["right"])
                if "<=" in stt["test"]["operator"]:
                    limit += " + 1"
                elif ">=" in stt["test"]["operator"]:
                    limit += " - 1"
            elif get_expression(stt["test"]["right"]) == iterator:
                limit = get_expression(stt["test"]["left"])
                if "<=" in stt["test"]["operator"]:
                    limit += " + 1"
                elif ">=" in stt["test"]["operator"]:
                    limit += " - 1"
            else:
                module.stmt("# TODO: failed to generate FOR statement(test doesnt include iterator)")
                return
            if stt["update"]["type"] == "AssignmentExpression":
                # if get_expression(stt["update"]["left"]) == iterator:
                step = get_expression(stt["update"]["right"])
            elif stt["update"]["type"] == "UpdateExpression":
                step = 1
            else:
                module.stmt("# TODO: failed to generate FOR statement(unexpected update)")
                return

            if "-" in stt["update"]["operator"]:
                step *= -1
            with module.for_(iterator, iterator="range({0}, {1}, {2})".format(init, limit, step)):
                for line in stt["body"]["body"]:
                    get_statement(line, module)
                return

        except:
            module.stmt("# TODO: failed to generate FOR statement")
            return
    
    if stt["type"] == "ForOfStatement":
        with module.for_(
            get_expression(stt["left"]["declarations"][0]["id"]),
            iterator=get_expression(stt["right"])):
            for line in stt["body"]["body"]:
                get_statement(line, module)
            return

    if stt["type"] == "ForInStatement":
        with module.for_(
            get_expression(stt["left"]["declarations"][0]["id"]) + ", _",
            iterator="enumerate(" + get_expression(stt["right"]) + ")"):
            for line in stt["body"]["body"]:
                get_statement(line, module)
            return

    if stt["type"] == "BreakStatement":
        module.stmt("break")
        return

    if stt["type"] == "TryStatement":
        # with module.try_():
        #     for line in stt["block"]["body"]:
        #         get_statement(line, module)
        # with module.except_():
        #     for line in stt["handler"]["body"]["body"]:
        #         get_statement(line, module)
        module.stmt("# TODO: failed to TRY statement")
        return

    if stt["type"] == "ThrowStatement":
        # TODO:とりあえずエラーの引数は1つのみを仮定
        module.raise_(
            get_error(stt["argument"]["callee"]["name"]) +
                "(" +
                get_expression(stt["argument"]["arguments"][0]) +
                ")"
            )
        return
    
    if stt["type"] == "EmptyStatement":
        return "pass"
    
    print("stt:", stt)

def get_error(err):
    if err == "Error":
        return "Exception"
    # return err

def get_expression(exp):
    if exp["type"] == "VariableDeclaration":
        # TODO:初期化が1つだけであることを仮定
        return (exp["declarations"][0]["id"]["name"] +
            " = " +
            get_expression(exp["declarations"][0]["init"])
        )
    
    if exp["type"] == "Identifier":
        return snake(exp["name"])

    if exp["type"] == "FunctionExpression":
        # anonymous function
        # 現時点で単純な処理をするものにしか対応できていない
        # TODO:無名関数で文を使う必要がある場合，別に名前付き関数を定義する必要がある！
        try: 
            params = ""
            for param in exp["params"]:
                params += param["name"] + ", "
            params = params[:-2]
            return ("lambda " +
                params +
                ": " +
                get_expression(exp["body"]["body"][0]["expression"]))
        except:
            return "# TODO: failed to generate Function Expression"

    if exp["type"] == "ArrowFunctionExpression":
        try:
            params = ""
            for param in exp["params"]:
                params += param["name"] + ", "
            params = params[:-2]
            return ("lambda " +
                params +
                ": " +
                get_expression(exp["body"]["body"][0]["argument"]))
        except KeyError:
            return "# TODO: ArrowFunctionExpression was here"

    if exp["type"] == "AssignmentExpression":
        return (get_expression(exp["left"]) +
            " " +
            get_operator(exp["operator"]) +
            " " +
            get_expression(exp["right"]))
    
    if exp["type"] == "LogicalExpression":
        return (get_expression(exp["left"]) +
            " " +
            get_operator(exp["operator"]) +
            " " +
            get_expression(exp["right"]))

    if exp["type"] == "BinaryExpression":
        if ("+" in exp["operator"] and
            ("Literal" in exp["left"]["type"] and type(exp["left"]["value"]) is str)
            ):
            return (get_expression(exp["left"]) +
            " " +
            get_operator(exp["operator"]) +
            " str(" +
            get_expression(exp["right"]) + ")")
        elif ("+" in exp["operator"] and
            ("Literal" in exp["right"]["type"] and type(exp["right"]["value"]) is str)
            ):
            return ("str(" +get_expression(exp["left"]) +
            ") " +
            get_operator(exp["operator"]) +
            " " +
            get_expression(exp["right"]))
        return (get_expression(exp["left"]) +
            " " +
            get_operator(exp["operator"]) +
            " " +
            get_expression(exp["right"]))

    if exp["type"] == "UnaryExpression":
        if exp["operator"] == "typeof":
            return "type(" + get_expression(exp["argument"]) + ")"
        if exp["operator"] == "!":
            return "not " + get_expression(exp["argument"])
        return exp["operator"] + get_expression(exp["argument"])

    if exp["type"] == "MemberExpression":
        if exp["computed"]:
            if "name" in exp["property"]:
                name = snake(exp["property"]["name"])
                return (get_expression(exp["object"]) +
                    "[" +
                    exp["property"]["name"] +
                    "]")
            return (get_expression(exp["object"]) +
                "[" +
                get_expression(exp["property"]) +
                "]")
        name = snake(exp["property"]["name"])
        if name == "bind":
            return get_expression(exp["object"])
        if "object" in exp:
            return get_expression(exp["object"]) + "." + name
        return name

    if exp["type"] == "ThisExpression":
        return "self"
    
    if exp["type"] == "ArrayExpression" or exp["type"] == "ArrayPattern":
        # return str([get_expression(elm) for elm in exp["elements"]])
        if not exp["elements"]:
            listr = "[]"
        else:
            listr = "["
            for elm in exp["elements"]:
                listr += get_expression(elm) + ", "
            listr = listr[:-2] + "]"
        return listr

    if exp["type"] == "Identifier":
        return snake(exp["name"])

    if exp["type"] == "Literal":
        return exp["raw"]
    
    if exp["type"] == "CallExpression":
        if not exp["arguments"]:
            return (get_expression(exp["callee"]) + "()")
        listr = "["
        for arg in exp["arguments"]:
            listr += get_expression(arg) + ", "
        listr = listr[:-2] + "]"
        # bindに対する特例処理
        if (exp["callee"]["type"] == "MemberExpression" and
            "name" in exp["callee"]["property"] and
            exp["callee"]["property"]["name"] == "bind"):
            return get_expression(exp["callee"])

        return (get_expression(exp["callee"]) + 
            "(*" +
            listr +
            ")")
    
    if exp["type"] == "ObjectExpression":
        obj = "{"
        if "properties" in exp:
            for prop in exp["properties"]:
                if "'" in get_expression(prop["key"]) or '"' in get_expression(prop["key"]):
                    obj += (
                        get_expression(prop["key"]) + ": " +
                        get_expression(prop["value"]) + ","
                    )
                else:
                    obj += (
                        "'" + get_expression(prop["key"]) + "': " +
                        get_expression(prop["value"]) + ", "
                    )
            obj = obj[:-2] + "}"
            return obj

    if exp["type"] == "ConditionalExpression":
        # test ? T : F
        # T if test else F
        return (get_expression(exp["consequent"]) +
            " if " +
            get_expression(exp["test"]) +
            " else " +
            get_expression(exp["alternate"]))
    
    if exp["type"] == "NewExpression":
        # TODO:
        if exp["callee"]["name"] == "Array":
            if exp["arguments"]:
                return "[0] * " + get_expression(exp["arguments"][0])
            return "[]"
        elif exp["callee"]["name"] == "Set":
            if exp["arguments"]:
                return get_expression(exp["arguments"][0])
            return "[]"
        elif exp["callee"]["name"] == "Promise":
            return "await" + get_expression(exp["arguments"][0])
        elif exp["callee"]["name"] == "Date":
            return "datetime.datetime.now()"
        else:
            if not exp["arguments"]:
                return (get_expression(exp["callee"]) + "()")
            listr = "["
            for arg in exp["arguments"]:
                listr += get_expression(arg) + ", "
            listr = listr[:-2] + "]"
            return (get_expression(exp["callee"]) + 
                    "(*" +
                    listr +
                    ")")

    
    if exp["type"] == "SpreadElement":
        # スプレッド演算子はPythonには存在しない
        # 呼ばれる関数の方から参照して処理を変えるべき(append or extend)
        return get_expression(exp["argument"])

    if exp["type"] == "AwaitExpression":
        return "await " + get_expression(exp["argument"])
    
    if exp["type"] == "TemplateLiteral":
        # https://developer.mozilla.org/ja/docs/Web/JavaScript/Reference/template_strings
        exps = [get_expression(e) for e in exp["expressions"]]
        quasis = exp["quasis"]
        template = ""
        for i, quas in enumerate(quasis):
            if quas["tail"]:
                template += quas["value"]["raw"]
                return '"' + template + '"'
            template += quas["value"]["raw"]
            template += '" + ' + exps[i] + ' + "'

    if exp["type"] == "UpdateExpression":
        # forの更新式はPythonでは必要ない
        return ""
    
    if exp["type"] == "SequenceExpression":
        # 使わない
        return ""
    print("exp", exp)

def get_operator(ope):
    if ope == "===":
        return "=="
    if ope == "!==":
        return "!="
    if ope == "||" or ope == "|":
        return "or"
    if ope == "&&" or ope == "&":
        return "and"
    return ope

if __name__ == "__main__":

    file_path = pathlib.Path(__file__).parent
    part_jsons = list(file_path.glob("**/index.json"))
    if args.file:
        part_jsons = [part for part in part_jsons if args.file in str(part)]
    for num, part_json in enumerate(part_jsons):
        m = PythonModule()
        print("===start to generate " + str(part_json.parent) + "===")
        with open(part_json) as f:
            js = json.load(f)
        #### process ###
        parts_class = js["body"][0]
        if parts_class["type"] != "ClassDeclaration":
            raise Exception("Failed to generate python file.")

        get_statement(parts_class, m)
        
        tmp = str(m).replace("true", "True").replace("false", "False")  
        if "async" in tmp or "await" in tmp:
            tmp = "import asyncio\n\n" + tmp
        if "datetime" in tmp:
            tmp = "import datetime\n\n" + tmp
        with open(part_json.parent/"__init__.py", mode="w") as f:
            f.write(tmp)
        print("===" + part_json.parent.name + " (" + str(num+1) + "/" + str(len(part_jsons)) + ") completed===")
