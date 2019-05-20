import os
import re
import json
import glob
import pathlib
import argparse

from prestring.python import PythonModule

### パーツは全てクラス定義一つであることを仮定
# TODO: キーワード引数(デフォルト引数)はJS側を編集すべき？ -> はい
# TODO: 文字列連結はJS側を編集すべき？

parser = argparse.ArgumentParser()
parser.add_argument("--file", help="set specific file[directory] name", type=str)
args = parser.parse_args()

class JsonToPy:
    def __init__(self, ast_json, prestr):
        self.m = prestr
        self.func_flag = False
        self.funcs = []
        self.func_names = []
        self.func_args = []
        self.func_count = 0
        self.promise_flag = False
        for stmt in ast_json["body"]:
            if stmt["type"] == "IfStatement":
                break
            else:
                self.get_statement(stmt)

    def snake(self, text):
        if text.isupper():
            return text
        return re.sub("([A-Z])+",lambda x:"_" + x.group().lower(), text)

    def get_statement(self, stt, replace_from="_DummyString_", replace_to=""):
        if stt["type"] == "ExpressionStatement":
            exp = stt["expression"]
            # 特殊処理(Object.defineProperty)
            if "callee" in exp and self.get_expression(exp["callee"]) == self.snake("Object.defineProperty"):
                for attr in exp["arguments"][2]["properties"]:
                    with self.m.def_(self.get_expression(attr["key"])):
                        for line in attr["value"]["body"]["body"]:
                            self.get_statement(line)
                    statements = ("setattr(" + self.get_expression(exp["arguments"][0]) +
                                ", " + self.get_expression(exp["arguments"][1]) +
                                ", " + self.get_expression(attr["key"]) + ")")
                    self.m.stmt(statements)
                return
            self.funcs = []
            self.func_flag = False
            self.get_expression(exp)
            if self.func_flag:
                self.create_funcs()
            self.m.stmt(self.get_expression(exp).replace(replace_from, replace_to))
            return
        
        if stt["type"] == "MethodDefinition":
            name = self.snake(stt["key"]["name"])
            method_name = "__init__" if name == "constructor" else name
            args = []
            if stt["static"]:
                self.m.stmt("@staticmethod")
            else:
                args.append("self")
            for arg in stt["value"]["params"]:
                args.append(self.snake(arg["name"]))
            if stt["value"]["async"]:
                with self.m.async_def_(method_name, *args):
                    content = stt["value"]
                    for line in content["body"]["body"]:
                        self.get_statement(line)
            else:
                with m.def_(method_name, *args):
                    content = stt["value"]
                    for line in content["body"]["body"]:
                        self.get_statement(line)
            return

        if stt["type"] == "ClassDeclaration":
            base = "" if stt["superClass"] is None else stt["superClass"]
            with self.m.class_(stt["id"]["name"], bases=base):
                bodies = stt["body"]["body"]
                for body in bodies:
                    self.get_statement(body)
            return
        
        if stt["type"] == "FunctionDeclaration":
            name = self.snake(self.get_expression(stt["id"]))
            args = []
            for arg in stt["params"]:
                args.append(self.snake(self.get_expression(arg)))
            with self.m.def_(name, *args):
                for line in stt["body"]["body"]:
                    self.get_statement(line)
            return

        if stt["type"] == "ReturnStatement":
            exp = stt["argument"]
            if exp:
                self.promise_flag = False
                self.funcs = []
                self.func_flag = False
                self.get_expression(exp)
                if self.promise_flag:
                    self.m.stmt("future = asyncio.get_event_loop().create_future()")
                if self.func_flag:
                    self.create_funcs()
                self.m.stmt("return " + self.get_expression(exp))
            else:
                self.m.stmt("return")
            return

        if stt["type"] == "IfStatement":
            with self.m.if_(self.get_expression(stt["test"])):
                if "body" in stt["consequent"]:
                    for line in stt["consequent"]["body"]:
                        self.get_statement(line)
                else:
                    self.get_statement(stt["consequent"])
            if not stt["alternate"]:
                return
            consequent = stt["alternate"]
            while consequent and consequent["type"] == "IfStatement":
                with self.m.elif_(self.get_expression(consequent["test"])):
                    if "body" in consequent["consequent"]:
                        for line in consequent["consequent"]["body"]:
                            self.get_statement(line)
                    else:
                        self.get_statement(consequent["consequent"])
                consequent = consequent["alternate"]
            if consequent:
                with self.m.else_():
                    if "body" in consequent:
                        for line in consequent["body"]:
                            self.get_statement(line)
                        return
                    else:
                        self.get_statement(consequent)
                        return
            return
        
        if stt["type"] == "SwitchStatement":
            cases = stt["cases"]
            fst = cases.pop(0)
            with self.m.if_(self.get_expression(stt["discriminant"]) +
                "==" +
                self.get_expression(fst["test"])):
                for line in fst["consequent"]:
                    if line["type"] != "BreakStatement":
                        self.get_statement(line)
            for case in cases:
                if not case["test"]:
                    with self.m.else_():
                        for line in case["consequent"]:
                            self.get_statement(line)
                else:
                    with self.m.elif_(self.get_expression(stt["discriminant"]) +
                                    "==" + self.get_expression(case["test"])):
                        for line in case["consequent"]:
                            if line["type"] != "BreakStatement":
                                self.get_statement(line)
            return

        if stt["type"] == "VariableDeclaration":
            for dec in stt["declarations"]:
                if dec["init"]:
                    self.funcs = []
                    self.func_flag = False
                    self.get_expression(dec["init"])
                    if self.func_flag:
                        self.create_funcs()
                    self.m.stmt(self.get_expression(dec["id"]) +
                                " = " + self.get_expression(dec["init"]))
                else:
                    self.m.stmt(self.get_expression(dec["id"]) + " = None")
            return

        if stt["type"] == "WhileStatement":
            with self.m.while_(self.get_expression(stt["test"])):
                if "body" in stt["body"]:
                    for line in stt["body"]["body"]:
                        self.get_statement(line)
                else:
                    self.get_statement(stt["body"])
            return

        if stt["type"] == "ForStatement":
            try:
                iterator = self.get_expression(stt["init"]["declarations"][0]["id"])
                init = self.get_expression(stt["init"]["declarations"][0]["init"])
                if self.get_expression(stt["test"]["left"]) == iterator:
                    limit = self.get_expression(stt["test"]["right"])
                    if "<=" in stt["test"]["operator"]:
                        limit += " + 1"
                    elif ">=" in stt["test"]["operator"]:
                        limit += " - 1"
                elif self.get_expression(stt["test"]["right"]) == iterator:
                    limit = self.get_expression(stt["test"]["left"])
                    if "<=" in stt["test"]["operator"]:
                        limit += " + 1"
                    elif ">=" in stt["test"]["operator"]:
                        limit += " - 1"
                else:
                    self.m.stmt("# TODO: failed to generate FOR statement(test doesnt include iterator)")
                    return
                if stt["update"]["type"] == "AssignmentExpression":
                    step = self.get_expression(stt["update"]["right"])
                elif stt["update"]["type"] == "UpdateExpression":
                    step = 1
                else:
                    self.m.stmt("# TODO: failed to generate FOR statement(unexpected update)")
                    return

                if "-" in stt["update"]["operator"]:
                    step *= -1
                with self.m.for_(iterator,
                                iterator="range({0}, {1}, {2})".format(init, limit, step)):
                    for line in stt["body"]["body"]:
                        self.get_statement(line)
                    return

            except:
                self.m.stmt("# TODO: failed to generate FOR statement")
                return
        
        if stt["type"] == "ForOfStatement":
            with self.m.for_(self.get_expression(stt["left"]["declarations"][0]["id"]),
                            iterator=self.get_expression(stt["right"])):
                for line in stt["body"]["body"]:
                    self.get_statement(line)
                return

        if stt["type"] == "ForInStatement":
            with self.m.for_(
                    self.get_expression(stt["left"]["declarations"][0]["id"]) + ", _",
                    iterator="enumerate(" + self.get_expression(stt["right"]) + ")"):
                for line in stt["body"]["body"]:
                    self.get_statement(line)
                return

        if stt["type"] == "BreakStatement":
            self.m.stmt("break")
            return

        if stt["type"] == "TryStatement":
            # with self.m.try_():
            #     for line in stt["block"]["body"]:
            #         self.get_statement(line)
            # with self.m.except_():
            #     for line in stt["handler"]["body"]["body"]:
            #         self.get_statement(line)
            self.m.stmt("# TODO: failed to TRY statement")
            return

        if stt["type"] == "ThrowStatement":
            # TODO:とりあえずエラーの引数は1つのみを仮定
            self.m.raise_(
                self.get_error(stt["argument"]["callee"]["name"]) +
                    "(" +
                    self.get_expression(stt["argument"]["arguments"][0]) +
                    ")"
                )
            return
        
        if stt["type"] == "EmptyStatement":
            return "pass"
        
        print("stt:", stt)

    def get_error(self, err):
        if err == "Error":
            return "Exception"
        # return err

    def get_expression(self, exp):
        if exp["type"] == "VariableDeclaration":
            # TODO:初期化が1つだけであることを仮定
            return (exp["declarations"][0]["id"]["name"] +
                " = " +
                self.get_expression(exp["declarations"][0]["init"])
            )
        
        if exp["type"] == "Identifier":
            if exp["name"] == "parseInt":
                return "int"
            elif exp["name"] == "undefined":
                return "None"
            return self.snake(exp["name"])

        if exp["type"] == "FunctionExpression":
            if self.func_names:
                return self.func_names.pop(0)
            else:
                self.func_flag = True
                self.funcs.append(exp)
                return ""
            # anonymous function
            # 現時点で単純な処理をするものにしか対応できていない
            # TODO:無名関数で文を使う必要がある場合，別に名前付き関数を定義する必要がある！
            # try: 
            #     params = ""
            #     for param in exp["params"]:
            #         params += param["name"] + ", "
            #     params = params[:-2]
            #     return ("lambda " + params + ": " +
            #             self.get_expression(exp["body"]["body"][0]["expression"]))
            # except:
            #     return "# TODO: failed to generate Function Expression"


        if exp["type"] == "ArrowFunctionExpression":
            if self.func_names:
                return self.func_names.pop(0)
            else:
                self.func_flag = True
                self.funcs.append(exp)
                return ""
            # try:
            #     params = ""
            #     for param in exp["params"]:
            #         params += param["name"] + ", "
            #     params = params[:-2]
            #     return ("lambda " + params + ": " +
            #             self.get_expression(exp["body"]["body"][0]["argument"]))
            # except KeyError:
            #     return "# TODO: ArrowFunctionExpression was here"

        if exp["type"] == "AssignmentExpression":
            return (self.get_expression(exp["left"]) +
                    " " + self.get_operator(exp["operator"]) +
                    " " + self.get_expression(exp["right"]))
        
        if exp["type"] == "LogicalExpression":
            return (self.get_expression(exp["left"]) +
                    " " + self.get_operator(exp["operator"]) +
                    " " + self.get_expression(exp["right"]))

        if exp["type"] == "BinaryExpression":
            # for string concatnation
            if ("+" in exp["operator"] and
                ("Literal" in exp["left"]["type"] and type(exp["left"]["value"]) is str)
                ):
                return (self.get_expression(exp["left"]) +
                        " " + self.get_operator(exp["operator"]) +
                        " str(" + self.get_expression(exp["right"]) + ")")
            elif ("+" in exp["operator"] and
                ("Literal" in exp["right"]["type"] and type(exp["right"]["value"]) is str)
                ):
                return ("str(" +self.get_expression(exp["left"]) +
                        ") " + self.get_operator(exp["operator"]) +
                        " " + self.get_expression(exp["right"]))

            if self.get_operator(exp["operator"]) in ["+", "-", ">>", "<<"]:
                return ("(" + self.get_expression(exp["left"]) +
                        " " + self.get_operator(exp["operator"]) +
                        " " + self.get_expression(exp["right"]) + ")")

            return (self.get_expression(exp["left"]) +
                    " " + self.get_operator(exp["operator"]) +
                    " " + self.get_expression(exp["right"]))

        if exp["type"] == "UnaryExpression":
            if exp["operator"] == "typeof":
                return "type(" + self.get_expression(exp["argument"]) + ")"
            if exp["operator"] == "!":
                return "not " + self.get_expression(exp["argument"])
            return exp["operator"] + self.get_expression(exp["argument"])

        if exp["type"] == "MemberExpression":
            if exp["computed"]:
                if "name" in exp["property"]:
                    name = self.snake(exp["property"]["name"])
                    return (self.get_expression(exp["object"]) +
                            "[" + name +
                            "]")
                return (self.get_expression(exp["object"]) +
                        "[" + self.get_expression(exp["property"]) +
                        "]")
            name = self.snake(exp["property"]["name"])
            if name == "bind":
                return self.get_expression(exp["object"])
            elif name == "length":
                return "len(" + self.get_expression(exp["object"]) + ")"
            if "object" in exp:
                return self.get_expression(exp["object"]) + "." + name
            return name

        if exp["type"] == "ThisExpression":
            return "self"
        
        if exp["type"] == "ArrayExpression" or exp["type"] == "ArrayPattern":
            if not exp["elements"]:
                listr = "[]"
            else:
                listr = "["
                for elm in exp["elements"]:
                    listr += self.get_expression(elm) + ", "
                listr = listr[:-2] + "]"
            return listr

        if exp["type"] == "Identifier":
            return self.snake(exp["name"])

        if exp["type"] == "Literal":
            if exp["raw"] == "null":
                return "None"
            return exp["raw"]
        
        if exp["type"] == "CallExpression":
            if not exp["arguments"]:
                listr = "[]"
            else:
                listr = "["
                for arg in exp["arguments"]:
                    listr += self.get_expression(arg) + ", "
                listr = listr[:-2] + "]"
            # bindに対する特例処理
            if (exp["callee"]["type"] == "MemberExpression" and
                "name" in exp["callee"]["property"] and
                exp["callee"]["property"]["name"] == "bind"):
                return self.get_expression(exp["callee"])
            # resolveに対する特例処理
            elif self.get_expression(exp["callee"]) == "resolve":
                if exp["arguments"]:
                    return "future.set_result(*" + listr + ")"
                else:
                    return "future.set_result()"
            return (self.get_expression(exp["callee"]) + 
                    "(*" + listr + ")")
        
        if exp["type"] == "ObjectExpression":
            obj = "AttrDefault(bool, {"
            if "properties" in exp:
                if len(exp["properties"]) == 0:
                    return "AttrDefault(bool, {})"
                for prop in exp["properties"]:
                    if "'" in self.get_expression(prop["key"]) or '"' in self.get_expression(prop["key"]):
                        obj += (
                            self.get_expression(prop["key"]) + ": " +
                            self.get_expression(prop["value"]) + ","
                        )
                    else:
                        obj += (
                            "'" + self.get_expression(prop["key"]) + "': " +
                            self.get_expression(prop["value"]) + ", "
                        )
                obj = obj[:-2] + "})"
                return obj

        if exp["type"] == "ConditionalExpression":
            # test ? T : F -> T if test else F
            return (self.get_expression(exp["consequent"]) +
                    " if " + self.get_expression(exp["test"]) +
                    " else " + self.get_expression(exp["alternate"]))
        
        if exp["type"] == "NewExpression":
            # TODO:
            if exp["callee"]["name"] == "Array":
                if exp["arguments"]:
                    return "[0] * " + self.get_expression(exp["arguments"][0])
                return "[]"
            elif exp["callee"]["name"] == "Set":
                if exp["arguments"]:
                    return self.get_expression(exp["arguments"][0])
                return "[]"
            elif exp["callee"]["name"] == "Promise":
                self.promise_flag = True
                    
                # return "await" + self.get_expression(exp["arguments"][0])
                return self.get_expression(exp["arguments"][0]) + "()"
            elif exp["callee"]["name"] == "Date":
                return "datetime.datetime.now()"
            else:
                if not exp["arguments"]:
                    return (self.get_expression(exp["callee"]) + "()")
                listr = "["
                for arg in exp["arguments"]:
                    listr += self.get_expression(arg) + ", "
                listr = listr[:-2] + "]"
                return (self.get_expression(exp["callee"]) + 
                        "(*" + listr + ")")
        
        if exp["type"] == "SpreadElement":
            # スプレッド演算子はPythonには存在しない
            # 呼ばれる関数の方から参照して処理を変えるべき(append or extend)
            return self.get_expression(exp["argument"])

        if exp["type"] == "AwaitExpression":
            return "await " + self.get_expression(exp["argument"])
        
        if exp["type"] == "TemplateLiteral":
            # https://developer.mozilla.org/ja/docs/Web/JavaScript/Reference/template_strings
            exps = [self.get_expression(e) for e in exp["expressions"]]
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
    
    def get_operator(self, ope):
        if ope == "===":
            return "=="
        if ope == "!==":
            return "!="
        if ope == "||":
            return "or"
        if ope == "&&":
            return "and"
        return ope

    def create_funcs(self):
        for func in self.funcs:
            args = []
            for arg in func["params"]:
                if arg["name"] == "resolve":
                    pass
                elif arg["name"] == "reject":
                    pass
                else:
                    args.append(self.snake(arg["name"]))

            with self.m.def_("anonymous" + str(self.func_count), *args):
                funcname = str(self.func_count)
                self.func_count += 1
                if not func["body"]["body"]:
                    self.m.stmt("pass")
                else:
                    for line in func["body"]["body"]:
                        self.get_statement(line)
                if func["params"] and func["params"][0]["name"] == "resolve":
                    # TODO: returnダブりないか？                    
                    self.m.stmt("return future")
            self.func_names.append("anonymous" + funcname)
            
            # self.func_args.append(func["params"])
        self.funcs = []
        self.func_flag = False


if __name__ == "__main__":

    file_path = pathlib.Path(__file__).parent
    # part_jsons = list(file_path.glob("**/index.json", recursive=True))
    part_jsons = glob.glob(str(file_path / "**/index.json"), recursive=True)
    if args.file:
        part_jsons = [part for part in part_jsons if args.file in str(part)]
    for num, part_json in enumerate(part_jsons):
        m = PythonModule()
        print("===start to generate " + str(pathlib.Path(part_json).parent) + "===")
        with open(part_json) as f:
            js = json.load(f)
        #### process ###
        # parts_class = js["body"][0]
        # if parts_class["type"] != "ClassDeclaration":
        #     raise Exception("Failed to generate python file.")
        JsonToPy(js, m)
        
        tmp = str(m).replace("true", "True").replace("false", "False")  
        if "async" in tmp or "await" in tmp:
            tmp = "import asyncio\n\n" + tmp
        if "datetime" in tmp:
            tmp = "import datetime\n\n" + tmp
        if "AttrDefault" in tmp:
            tmp = "from attrdict import AttrDefault\n\n" + tmp
        with open(pathlib.Path(part_json).parent/"__init__.py", mode="w") as f:
            f.write(tmp)
        print("===" + pathlib.Path(part_json).parent.name + " (" + str(num+1) + "/" + str(len(part_jsons)) + ") completed===")
