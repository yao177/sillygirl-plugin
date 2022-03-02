// [rule: 外卖]
// [rule: 外卖红包]
// [rule: 美团]
// [rule: 美团外卖]
// [rule: 美团红包]
// [rule: 美团外卖红包]
// [rule: 饿了么]
// [rule: 饿了么外卖]
// [rule: 饿了么红包]
// [rule: 饿了么外卖红包]
// [cron: 20 11,17 * * *]

/**
 * @author 红叶
 * @modify 2022-03-02
 */


/**
 * 自定义部分
 * mt：美团红包，可以放置多组随机取
 * elm：饿了么红包，可以放置多组随机取
 * groups：开启定时任务推送的群，自行配置
 */
var mt = [
    ["https://s2.loli.net/2022/02/21/kzfjpIFYZ9LeDn6.jpg", "https://s2.loli.net/2022/02/21/v4KVDUlp1d9SGzs.jpg", "https://s2.loli.net/2022/02/21/aukBLKISW6eHFoi.jpg"],
    ["https://s2.loli.net/2022/02/22/SaxeUO4sFnANvG7.jpg", "https://s2.loli.net/2022/02/22/QbC3N2pguMLP8GR.jpg", "https://s2.loli.net/2022/02/22/KGFJC5oYiVSIUjc.jpg"],
    ["https://s2.loli.net/2022/02/22/zi1EZGdr8kwSJnY.jpg", "https://s2.loli.net/2022/02/22/jOHkPRZvWQfBlob.jpg", "https://s2.loli.net/2022/02/22/4tHVwK1eCpQclP8.jpg"]
]
var elm = [
    ["https://s2.loli.net/2022/02/21/j8GUtlaS3csXCQ5.jpg", "https://s2.loli.net/2022/02/21/OrIiHKs7pjS9vP2.jpg"],
    ["https://s2.loli.net/2022/02/22/2ZLGEAxs5FNgOtH.jpg", "https://s2.loli.net/2022/02/22/PQ1lNAr9kBd6mDg.jpg", "https://s2.loli.net/2022/02/22/wOeHmp9ls7joLIK.jpg"]
]
var groups = [{
    imType: "wx",
    groupCode: 18843026371,
}, {
    imType: "wx",
    groupCode: 6565357519,
}, {
    imType: "tg",
    groupCode: 12345678910
}]


require('Math')

function pic2txt(x) {
    var a = ""
    for (var i = 0; i < x.length; ++i) {
        a += image(x[i]);
    }
    return a
}

function getRandomMT() {
    return pic2txt(mt[Math.floor(Math.random() * mt.length)])
}

function getRandomELM() {
    return pic2txt(elm[Math.floor(Math.random() * elm.length)])
}

function main() {
    var imType = ImType();
    if (imType == 'fake') {
        for (var i = 0; i < groups.length; i++) {
            groups[i]["content"] = "快到饭点了，干饭机器人提醒大家要记得点外卖喔～" + getRandomELM() + getRandomMT()
            push(groups[i])
        }
        return
    }

    var inTxt = GetContent()
    if (inTxt.indexOf("饿了么") >= 0) {
        if (imType == 'wxmp') {
            var elms = elm[Math.floor(Math.random() * elm.length)]
            sendImage(elms[Math.floor(Math.random() * elms.length)])
            return
        }
        sendText("" + getRandomELM())
        return
    }
    if (inTxt.indexOf("美团") >= 0) {
        if (imType == 'wxmp') {
            var mts = mt[Math.floor(Math.random() * mt.length)]
            sendImage(mts[Math.floor(Math.random() * mts.length)])
            return
        }
        sendText("" + getRandomMT())
        return
    }

    var sec = param(1);
    var i = 0;
    while (sec == "" || sec == "0" || isNaN(sec)) {
        if (sec == "q") {
            sendText("客户输入" + sec + "已退出")
            return
        }
        sendText("输入\"1\"选择「饿了么」输入\"2\"选择「美团」")
        i++
        if (i > 3) {
            sendText("客户输入" + typeof sec + sec + "，输入错误次数过多，立即退出。")
            return
        }
        sec = input()
        if (typeof sec != 'number') {
            sec = parseInt(sec)
        }
    }
    if (sec > 1) {
        sendText("" + getRandomMT() + "\n已成功获取美团外卖红包，请稍后领取使用。")
        return
    }
    sendText("" + getRandomELM() + "\n已成功获取饿了么外卖红包，请稍后领取使用。")
}

main()
