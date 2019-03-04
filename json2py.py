import re
import json

from prestring.python import PythonModule

### パーツは全てクラス定義一つであることを仮定
### スネークケース変換 re.sub("([A-Z])+",lambda x:"_" + x.group().lower(), XXX)
# TODO: ドットアクセス対応 -> params だけクラスとして渡すか？
# https://qiita.com/icoxfog417/items/83a77a648b71a38a1bd5
# TODO: async拡張
# TODO: キーワード引数(デフォルト引数)はJS側を編集すべき？ -> はい
# TODO: 文字列連結はJS側を編集すべき？

def get_statement(stt, module):
    if stt["type"] == "ExpressionStatement":
        exp = stt["expression"]
        module.stmt(get_expression(exp))
    
    if stt["type"] == "ReturnStatement":
        exp = stt["argument"]
        module.stmt("return " + get_expression(exp))

    if stt["type"] == "IfStatement":
        with module.if_(get_expression(stt["test"])):
            for line in stt["consequent"]["body"]:
                get_statement(line, module)
        if stt["alternate"]:
            with module.else_():
                for line in stt["alternate"]["body"]:
                    get_statement(line, module)
    
    if stt["type"] == "VariableDeclaration":
        for dec in stt["declarations"]:
            module.stmt(
                dec["id"]["name"] +
                " = " +
                get_expression(dec["init"]))

def get_expression(exp):
    if exp["type"] == "Identifier":
        return re.sub("([A-Z])+",lambda x:"_" + x.group().lower(), exp["name"])

    if exp["type"] == "FunctionExpression":
        # anonymous function
        # 現時点で単純な処理をするものにしか対応できていない
        # 無名関数で文を使う必要がある場合，別に名前付き関数を定義する必要がある！
        params = ""
        for param in exp["params"]:
            params += param["name"] + ", "
        params = params[:-2]
        return ("lambda " +
            params +
            ": " +
            get_expression(exp["body"]["body"][0]["expression"]))

    if exp["type"] == "AssignmentExpression":
        return (get_expression(exp["left"]) +
            " " +
            exp["operator"] +
            " " +
            get_expression(exp["right"]))

    if exp["type"] == "BinaryExpression":
        return (get_expression(exp["left"]) +
            " " +
            exp["operator"] +
            " " +
            get_expression(exp["right"]))

    if exp["type"] == "UnaryExpression":
        if exp["operator"] == "typeof":
            return "type(" + get_expression(exp["argument"]) + ")"
        if exp["operator"] == "!":
            return "not " + get_expression(exp["argument"])
        return exp["operator"] + get_expression(exp["argument"])

    if exp["type"] == "MemberExpression":
        name = re.sub("([A-Z])+",lambda x:"_" + x.group().lower(), exp["property"]["name"])
        if name == "bind":
            return get_expression(exp["object"])
        if "object" in exp:
            return get_expression(exp["object"]) + "." + name
        return name

    if exp["type"] == "ThisExpression":
        return "self"
    
    if exp["type"] == "ArrayExpression":
        # return str([get_expression(elm) for elm in exp["elements"]])
        listr = "["
        for elm in exp["elements"]:
            listr += get_expression(elm) + ", "
        listr = listr[:-2] + "]"
        return listr

    if exp["type"] == "Identifier":
        return re.sub("([A-Z])+",lambda x:"_" + x.group().lower(), exp["name"])

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
                obj += (
                    "'" + prop["key"]["name"] + "': " +
                    get_expression(prop["value"]) + ", "
                )
            obj = obj[:-2] + "}"
            return obj


if __name__ == "__main__":
    m = PythonModule()

    with open("./test.json") as f:
        js = json.load(f)

    parts_class = js["body"][0]
    if parts_class["type"] != "ClassDeclaration":
        raise Exception("Failed to generate python file.")
    # クラス定義
    base = "" if parts_class["superClass"] is None else parts_class["superClass"]
    with m.class_(parts_class["id"]["name"], bases=base):
        bodies = parts_class["body"]["body"]
        for body in bodies:
            if body["type"] == "MethodDefinition":
                name = body["key"]["name"]
                name = re.sub("([A-Z])+",lambda x:"_" + x.group().lower(), name)
                method_name = "__init__" if name == "constructor" else name
                args = []
                # メソッド定義
                if body["static"]:
                    m.stmt("@staticmethod")
                else:
                    args.append("self")
                for arg in body["value"]["params"]:
                    args.append(arg["name"])
                with m.def_(method_name, *args):
                    # メソッドの内容
                    content = body["value"]
                    if content["type"] != "FunctionExpression":
                        m.stmt("# !!TODO here is not FuncExp!!")
                    else:
                        for line in content["body"]["body"]:
                            get_statement(line, m)

    # rawで取得した真偽値の変換
    m = str(m).replace("true", "True").replace("false", "False")    
    print(m)
    with open("./__init__.py", mode="w") as f:
        f.write(m)