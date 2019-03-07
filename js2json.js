// ディレクトリ構造生成およびJSからのAST生成

let fs = require("fs");
let path = require("path");
let acorn = require("acorn");

const outputTo = path.join(__dirname, "partspy");
if (!fs.existsSync(outputTo)) {
    fs.mkdirSync(outputTo);
}
const partsClassesPath = path.join(__dirname, "parts");
const partsClasses = fs.readdirSync(partsClassesPath);
for (let partsClass of partsClasses) {
    if (partsClass.indexOf(".") == 0) {
        continue;
    }
    let parts = fs.readdirSync(path.join(partsClassesPath, partsClass));
    if (!fs.existsSync(path.join(outputTo, partsClass))) {
        fs.mkdirSync(path.join(outputTo, partsClass));
    }

    for (let part of parts) {
        if (part.indexOf(".") == 0) {
            continue;
        } else if (part.indexOf(".ejs") >= 0) {
            continue;
        }
        let partspyPath = path.join(outputTo, partsClass, part);
        if (!fs.existsSync(partspyPath)) {
            fs.mkdirSync(partspyPath);
        }
        let filePath = path.join(partsClassesPath, partsClass, part);
        let files = fs.readdirSync(filePath);
        for (let file of files) {
            if (file.indexOf(".js") >= 0) {
                // AST(json)生成
                let buf = fs.readFileSync(path.join(filePath, file), "utf-8");
                let json = acorn.parse(buf);
                fs.writeFileSync(
                    path.join(partspyPath, "index.json"),
                    JSON.stringify(json, null, "\t")
                );
                continue;
            } else if (file.indexOf(".") == 0) {
                continue;
            }
            fs.copyFileSync(
                path.join(filePath, file),
                path.join(partspyPath, file)
            );
        }
    }
}
// let text = fs.readFileSync("./index.js", "utf-8");
// let json = acorn.parse(text);
// fs.writeFileSync("test.json", JSON.stringify(json, null, '\t'));