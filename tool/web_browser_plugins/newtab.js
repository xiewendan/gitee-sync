
function PrintLink() {
    var dictData = {
        "daily":
        {
            "https://trello.com/geek05/home": "Trello",
            "https://note.youdao.com/web/": "有道笔记",
            "https://leetcode-cn.com/u/xiao-bao-8/": "leetcode",
            "https://xiewendan.github.io/": "个人github",
            "http://www.keybr.com/practice": "typing",
        },

        "资讯":
        {
            "http://www.woshipm.com/": "人人都是产品经理",
            "https://github.com/trending": "github trending",
            "https://www.infoq.cn/weekly/landing": "InfoQ",
            "https://km.netease.com/recent": "km七日最热",
			"https://v.netease.com/evideo/video_course/list":"易播",
        },
        "搜索":
        {
            "https://www.google.com.hk/": "goolge",
            "https://www.baidu.com/": "百度",
			"https://www.bilibili.com/": "B站",
            "https://www.zhihu.com/follow":"知乎",
			"https://stackoverflow.com/": "stackoverflow",
			"https://github.com/": "github搜索",
			"https://www.youtube.com/": "youtube",
			"https://translate.google.com/": "google翻译",
        },
        "网易":
        {
            "http://10.225.93.110:5001/": "remote open",
        },
        "架构师":
        {
            "https://github.com/kamranahmedse/developer-roadmap": "web developer roadmap",
            "https://github.com/xingshaocheng/architect-awesome": "后端架构师技术图谱",
			"https://www.brendangregg.com/linuxperf.html": "linux Performance"
        }
    };

    for (var szTitle in dictData) {
        document.write("<h1>" + szTitle);
        {
            document.write("<br />");
            dictUrl2Name = dictData[szTitle];

            for (var szUrl in dictUrl2Name) {
                szName = dictUrl2Name[szUrl];
                document.write('<a href="' + szUrl + '">' + szName + '</a>');
            }

        }
        document.write("</h1>");
    }
}

PrintLink();
