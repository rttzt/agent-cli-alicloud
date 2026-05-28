"""
小红书爆文分析 Agent 端到端测试稿

本测试稿用于验证 xiaohongshu-trend-agent 的功能完整性，
覆盖 CLI 生成 → Agent 运行 → 输出质量 → 合规边界 四个层面。

运行方式（在 xiaohongshu-trend-agent 目录下）：
  PYTHONPATH=src python3 -m agent.main "<关键词>"

所有测试用例均使用 Mock 模式（不依赖 AgentScope 安装和 DashScope API Key）。
"""

# ============================================================
# 测试 1：基础功能验证（Happy Path）
# ============================================================

# 测试 1.1：美妆品类
# 输入：美妆品类
# 期望：输出包含 4 个分析维度（标题模式/封面规律/内容结构/互动特征）
# 验证命令：
#   PYTHONPATH=src python3 -m agent.main "美妆品类"
# 断言：
#   - 返回码 = 0
#   - stdout 包含 "标题模式"
#   - stdout 包含 "封面规律"
#   - stdout 包含 "内容结构"
#   - stdout 包含 "互动特征"

# 测试 1.2：母婴品类
# 输入：母婴好物
# 期望：输出包含品类相关的分析
# 验证命令：
#   PYTHONPATH=src python3 -m agent.main "母婴好物"
# 断言：
#   - 返回码 = 0
#   - stdout 包含 "母婴"

# 测试 1.3：数码品类
# 输入：数码测评
# 期望：输出包含数码相关的爆文规律
# 验证命令：
#   PYTHONPATH=src python3 -m agent.main "数码测评"
# 断言：
#   - 返回码 = 0
#   - stdout 包含 "数码"

# ============================================================
# 测试 2：边界条件验证（Edge Cases）
# ============================================================

# 测试 2.1：无参数运行
# 输入：（无参数）
# 期望：显示用法提示，返回码 = 1
# 验证命令：
#   PYTHONPATH=src python3 -m agent.main
# 断言：
#   - 返回码 = 1
#   - stdout 包含 "用法"

# 测试 2.2：单字关键词
# 输入：猫
# 期望：正常输出分析（单字应可接受）
# 验证命令：
#   PYTHONPATH=src python3 -m agent.main "猫"
# 断言：
#   - 返回码 = 0

# 测试 2.3：超长关键词（50 字）
# 输入：一二三四五六七八九十一二三四五六七八九十一二三四五六七八九十一二三四五六七八九十1234567890
# 期望：正常输出或友好提示（不应崩溃）
# 验证命令：
#   PYTHONPATH=src python3 -m agent.main "一二三四五六七八九十一二三四五六七八九十一二三四五六七八九十一二三四五六七八九十1234567890"
# 断言：
#   - 返回码 = 0 或 1（不应是 uncaught exception）

# 测试 2.4：特殊字符关键词
# 输入：美妆@#$%
# 期望：正常输出或友好提示
# 验证命令：
#   PYTHONPATH=src python3 -m agent.main "美妆@#\$%"
# 断言：
#   - 返回码 = 0（特殊字符应被正常处理）

# 测试 2.5：英文关键词
# 输入：skincare routine
# 期望：正常输出（应支持英文输入）
# 验证命令：
#   PYTHONPATH=src python3 -m agent.main "skincare routine"
# 断言：
#   - 返回码 = 0

# ============================================================
# 测试 3：输出质量验证（Content Quality）
# ============================================================

# 测试 3.1：输出结构完整性
# 输入：护肤
# 期望：输出包含完整的 4 维度分析 + 免责声明
# 验证命令：
#   PYTHONPATH=src python3 -m agent.main "护肤" | grep -c "##"
# 断言：
#   - 至少 4 个二级标题（## 开头）
#   - 包含免责声明文本 "仅供" 或 "参考"

# 测试 3.2：输出中文正确性
# 输入：穿搭
# 期望：输出全部为中文（无乱码、无英文占位符）
# 验证命令：
#   PYTHONPATH=src python3 -m agent.main "穿搭"
# 断言：
#   - stdout 可正常解码为 UTF-8
#   - 不包含 "TODO" / "placeholder" / "FIXME"

# 测试 3.3：分析维度深度
# 输入：家居好物
# 期望：每个维度至少 3 个分析点
# 验证命令：
#   PYTHONPATH=src python3 -m agent.main "家居好物"
# 断言：
#   - "标题模式" 段至少包含 3 个 "-" 开头的行
#   - "封面规律" 段至少包含 3 个 "-" 开头的行

# ============================================================
# 测试 4：合规边界验证（Compliance）
# ============================================================

# 测试 4.1：不应输出个人隐私数据
# 输入：美妆
# 期望：输出不包含真实用户 ID、手机号、邮箱等
# 验证命令：
#   PYTHONPATH=src python3 -m agent.main "美妆" | grep -E "(1[3-9]\d{9}|@.*\.(com|cn))"
# 断言：
#   - grep 返回码 = 1（无匹配，即无隐私数据）

# 测试 4.2：不应输出违禁内容
# 输入：减肥
# 期望：输出不包含医疗建议、违禁药物推荐等
# 验证命令：
#   PYTHONPATH=src python3 -m agent.main "减肥"
# 断言：
#   - stdout 不包含 "处方" / "药物" / "治疗" 等医疗术语

# 测试 4.3：免责声明存在
# 输入：任意品类
# 期望：输出末尾包含免责声明
# 验证命令：
#   PYTHONPATH=src python3 -m agent.main "美食"
# 断言：
#   - stdout 最后 5 行包含 "仅供" 或 "参考" 或 "免责声明"

# ============================================================
# 测试 5：工具函数验证（Tool Functions）
# ============================================================

# 测试 5.1：trend_fetcher 返回数据格式
# 验证命令：
#   PYTHONPATH=src python3 -c "from agent.tools.trend_fetcher import fetch_trending_notes; notes = fetch_trending_notes('美妆', top_n=3); assert len(notes) == 3; assert 'title' in notes[0]; assert 'likes' in notes[0]"
# 断言：
#   - 返回 3 条数据
#   - 每条包含 title 和 likes 字段

# 测试 5.2：top_n 参数生效
# 验证命令：
#   PYTHONPATH=src python3 -c "from agent.tools.trend_fetcher import fetch_trending_notes; notes = fetch_trending_notes('美妆', top_n=1); assert len(notes) == 1"
# 断言：
#   - top_n=1 时返回 1 条数据

# ============================================================
# 测试 6：Mock 模式自动降级（Mock Mode）
# ============================================================

# 测试 6.1：无 API Key 时自动 Mock
# 验证命令：
#   DASHSCOPE_API_KEY="" PYTHONPATH=src python3 -m agent.main "美妆"
# 断言：
#   - 返回码 = 0
#   - stdout 包含 "Mock 模式" 或 "警告"

# 测试 6.2：有 API Key 但 AgentScope 未安装时自动 Mock
# 验证命令：
#   DASHSCOPE_API_KEY="sk-test" PYTHONPATH=src python3 -m agent.main "美妆"
# 断言：
#   - 返回码 = 0（应降级为 Mock 而非崩溃）
#   - stdout 包含分析结果

# ============================================================
# 批量自动化测试脚本（可直接运行）
# ============================================================

if __name__ == "__main__":
    import subprocess
    import sys
    import os

    def run_test(name: str, args: list[str], env_override: dict | None = None,
                 expect_rc: int = 0, expect_contains: list[str] | None = None,
                 expect_not_contains: list[str] | None = None):
        """运行单个测试并打印结果。"""
        env = {**os.environ}
        if env_override:
            env.update(env_override)

        result = subprocess.run(
            [sys.executable, "-m", "agent.main", *args],
            capture_output=True,
            text=True,
            cwd=os.path.join(os.path.dirname(__file__), "..", "src"),
            env=env,
        )

        passed = True
        failures = []

        if result.returncode != expect_rc:
            passed = False
            failures.append(f"返回码: 期望 {expect_rc}, 实际 {result.returncode}")

        if expect_contains:
            for text in expect_contains:
                if text not in result.stdout:
                    passed = False
                    failures.append(f"输出缺少: '{text}'")

        if expect_not_contains:
            for text in expect_not_contains:
                if text in result.stdout:
                    passed = False
                    failures.append(f"输出不应包含: '{text}'")

        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}  {name}")
        if not passed:
            for f in failures:
                print(f"      └─ {f}")
        return passed

    print("=" * 60)
    print("小红书爆文分析 Agent 端到端测试")
    print("=" * 60)
    print()

    results = []

    # Happy Path
    results.append(run_test(
        "美妆品类基础分析",
        ["美妆品类"],
        expect_contains=["标题模式", "封面规律", "内容结构", "互动特征"],
    ))
    results.append(run_test(
        "母婴品类分析",
        ["母婴好物"],
        expect_contains=["母婴"],
    ))
    results.append(run_test(
        "数码品类分析",
        ["数码测评"],
        expect_contains=["数码"],
    ))

    # Edge Cases
    results.append(run_test(
        "无参数显示用法",
        [],
        expect_rc=1,
        expect_contains=["用法"],
    ))
    results.append(run_test(
        "单字关键词",
        ["猫"],
        expect_rc=0,
    ))
    results.append(run_test(
        "英文关键词",
        ["skincare"],
        expect_rc=0,
    ))

    # Content Quality
    results.append(run_test(
        "输出无英文占位符",
        ["护肤"],
        expect_not_contains=["TODO", "placeholder", "FIXME"],
    ))

    # Compliance
    results.append(run_test(
        "无个人隐私数据",
        ["美妆"],
        expect_not_contains=["138", "139", "136"],  # 手机号前缀采样
    ))

    # Mock Mode
    results.append(run_test(
        "无 API Key 自动 Mock",
        ["美妆"],
        env_override={"DASHSCOPE_API_KEY": ""},
        expect_rc=0,
        expect_contains=["Mock"],
    ))

    print()
    print("=" * 60)
    total = len(results)
    passed = sum(1 for r in results if r)
    print(f"结果: {passed}/{total} 通过")
    if passed == total:
        print("🎉 全部测试通过！")
    else:
        print(f"⚠️  {total - passed} 个测试失败")
    print("=" * 60)

    sys.exit(0 if passed == total else 1)
