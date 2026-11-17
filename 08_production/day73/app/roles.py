from dataclasses import dataclass


@dataclass(frozen=True)
class RoleSpec:
    name: str
    responsibility: tuple[str, ...]
    allowed_tools: frozenset[str]
    stop_condition: str


ROLES = {
    "researcher": RoleSpec(
        name="Researcher",
        responsibility=(
            "搜索相关技术资料",
            "提取关键事实",
            "记录资料来源",
        ),
        allowed_tools=frozenset({
            "search_docs",
        }),
        stop_condition="资料收集完成或达到搜索上限",
    ),

    "analyst": RoleSpec(
        name="Analyst",
        responsibility=(
            "比较技术方案",
            "总结优缺点",
            "给出分析结论",
        ),
        allowed_tools=frozenset({
            "analyze_data",
        }),
        stop_condition="形成完整分析结论",
    ),

    "reviewer": RoleSpec(
        name="Reviewer",
        responsibility=(
            "检查分析完整性",
            "评估结论质量",
            "决定是否通过",
        ),
        allowed_tools=frozenset({
            "validate_report",
        }),
        stop_condition="通过评审或达到最大评审次数",
    ),
}
