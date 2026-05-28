"""小红书爆文分析 Agent 测试。"""
import subprocess
import sys


def test_mock_mode_runs():
    """验证 Mock 模式可正常运行（不需要 API key）。"""
    result = subprocess.run(
        [sys.executable, "-m", "agent.main", "美妆"],
        capture_output=True,
        text=True,
        cwd="/Users/weichang/qoder_demo/AGENT_CLI_Alicloud/xiaohongshu-trend-agent/src",
        env={**__import__("os").environ, "DASHSCOPE_API_KEY": ""},
    )
    assert result.returncode == 0
    assert "美妆" in result.stdout
    assert "标题模式" in result.stdout
    assert "封面规律" in result.stdout


def test_no_keyword_shows_usage():
    """验证无参数时显示用法提示。"""
    result = subprocess.run(
        [sys.executable, "-m", "agent.main"],
        capture_output=True,
        text=True,
        cwd="/Users/weichang/qoder_demo/AGENT_CLI_Alicloud/xiaohongshu-trend-agent/src",
    )
    assert result.returncode == 1
    assert "用法" in result.stdout


def test_trend_fetcher_returns_mock_data():
    """验证数据检索工具返回 Mock 数据。"""
    sys.path.insert(0, "/Users/weichang/qoder_demo/AGENT_CLI_Alicloud/xiaohongshu-trend-agent/src")
    from agent.tools.trend_fetcher import fetch_trending_notes

    notes = fetch_trending_notes("母婴", top_n=2)
    assert len(notes) == 2
    assert "母婴" in notes[0]["title"]
    assert "likes" in notes[0]
