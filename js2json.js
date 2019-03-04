let fs = require("fs");
let acorn = require("acorn");

let text = fs.readFileSync("./index.js", "utf-8");
let json = acorn.parse(text);
fs.writeFileSync("test.json", JSON.stringify(json, null, '\t'));