const fs = require("fs")
const https = require("https")
const cheerio = require("cheerio")

// 起点的是随便写的, 有小概率不好使

const html = fs.readFileSync("./list.html", "utf-8")
fs.unlinkSync("./list.html")

const $ = cheerio.load(html)

const title = $("title")
    .text()
    .replace(/^.*《/, "")
    .replace(/》.*$/, "")

/** 存放路径 */
const file_src = `./result/${title}.txt`
fs.writeFileSync(file_src, "")

const finds = $(".volume")
    .find("ul")
    .first()
    .find("a")
    .toArray()
    .map(v => {
        return {
            title: v.childNodes[0].data,
            src: "https:" + v.attribs.href
        }
    })
get_and_read()
async function get_and_read() {
    for await (const fi of finds) {
        fs.appendFileSync(file_src, `\n${fi.title}\n`)
        console.log(fi.title)

        await get_one(fi.src)
    }
}
async function get_one(src) {
    return new Promise(suc => {
        https.get(src, e => {
            const buffer = []
            let size = 0
            e.on("data", ck => {
                buffer.push(ck)
                size += ck.length
            })
            e.on("end", () => {
                const data = Buffer.concat(buffer, size)
                const html = data.toString()
                const $ = cheerio.load(html)
                const txt = $(".j_readContent")
                    .text()
                    .replace(/\s+/g, "\n")
                fs.appendFileSync(file_src, txt + "\n")
                setTimeout(() => {
                    suc()
                }, 1500)
            })
        })
    })
}
