import json
import os

# 内置站点资料
SITE_DATA = [
    {
        "name": "爱游戏官方中文站",
        "url": "https://official-zh-i-game.com.cn",
        "keywords": ["爱游戏", "官方", "中文", "游戏平台"],
        "tags": ["游戏", "官方入口", "中文版"],
        "description": "提供正版游戏下载、资讯与社区服务，面向中文用户的爱游戏官方门户。"
    },
    {
        "name": "爱游戏攻略站",
        "url": "https://official-zh-i-game.com.cn/guides",
        "keywords": ["爱游戏", "攻略", "秘籍", "新手教程"],
        "tags": ["攻略", "教程", "玩家帮助"],
        "description": "汇聚玩家创作的游戏攻略与技巧，帮助新手快速上手。"
    },
    {
        "name": "爱游戏社区论坛",
        "url": "https://official-zh-i-game.com.cn/community",
        "keywords": ["爱游戏", "论坛", "讨论", "互动"],
        "tags": ["社区", "讨论", "交友"],
        "description": "玩家交流心得、组队交友的官方论坛。"
    }
]

class SiteSummaryBuilder:
    """
    构建站点摘要的结构化处理器。
    每次调用可生成不同格式的摘要，基于种子变化修正输出风格。
    """

    def __init__(self, site_list: list):
        self.sites = site_list

    def _collect_keywords(self) -> list:
        result = []
        for site in self.sites:
            result.extend(site.get("keywords", []))
        return list(set(result))

    def _collect_tags(self) -> list:
        tags = set()
        for site in self.sites:
            for tag in site.get("tags", []):
                tags.add(tag)
        return sorted(tags)

    def _build_item(self, site: dict) -> str:
        name = site["name"]
        url = site["url"]
        kw = ", ".join(site.get("keywords", []))
        tag = ", ".join(site.get("tags", []))
        desc = site.get("description", "无描述")
        return (
            f"站点名称: {name}\n"
            f"     URL: {url}\n"
            f"   关键词: {kw}\n"
            f"     标签: {tag}\n"
            f"   说明: {desc}\n"
        )

    def build_summary(self) -> str:
        """
        生成结构化的站点摘要文本。
        """
        lines = []
        lines.append("=" * 50)
        lines.append("    内置站点资料结构化摘要")
        lines.append("=" * 50)
        lines.append("")

        for i, site in enumerate(self.sites, 1):
            lines.append(f"--- 站点 {i} ---")
            lines.append(self._build_item(site))
            lines.append("")

        lines.append("--- 全局聚合信息 ---")
        lines.append(f"全局关键词（去重）: {', '.join(self._collect_keywords())}")
        lines.append(f"全局标签（排序）  : {', '.join(self._collect_tags())}")
        lines.append(f"站点总数          : {len(self.sites)}")
        lines.append("=" * 50)
        return "\n".join(lines)

    def build_json_summary(self) -> str:
        """
        生成 JSON 格式的结构化摘要。
        """
        summary = {
            "title": "内置站点资料摘要",
            "site_count": len(self.sites),
            "global_keywords": self._collect_keywords(),
            "global_tags": self._collect_tags(),
            "sites": []
        }
        for site in self.sites:
            summary["sites"].append({
                "name": site["name"],
                "url": site["url"],
                "keywords": site.get("keywords", []),
                "tags": site.get("tags", []),
                "description": site.get("description", "")
            })
        return json.dumps(summary, ensure_ascii=False, indent=2)

def main():
    # 允许通过环境变量指定输出格式：text 或 json
    output_format = os.environ.get("SUMMARY_FORMAT", "text")

    builder = SiteSummaryBuilder(SITE_DATA)

    if output_format == "json":
        result = builder.build_json_summary()
    else:
        result = builder.build_summary()

    print(result)

if __name__ == "__main__":
    main()