"""小红书爆文分析 Agent 测试。"""
import os
import subprocess
import sys
from pathlib import Path

# 使用相对路径定位 src 目录（从 tests/ 上一级到项目根，再进入 src）
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
_SRC_DIR = _PROJECT_ROOT / "src"


def test_mock_mode_runs():
    """验证 Mock 模式可正常运行（不需要 API key）。"""
    env = {**os.environ, "DASHSCOPE_API_KEY": ""}
    result = subprocess.run(
        [sys.executable, "-m", "agent.main", "美妆"],
        capture_output=True,
        text=True,
        cwd=str(_SRC_DIR),
        env=env,
    )
    assert result.returncode == 0
    assert "美妆" in result.stdout
    assert "标题模式" in result.stdout
    assert "封面规律" in result.stdout


def test_no_keyword_enters_chat_mode():
    """验证无参数时进入对话模式，输入 exit 可正常退出。"""
    env = {**os.environ, "DASHSCOPE_API_KEY": ""}
    result = subprocess.run(
        [sys.executable, "-m", "agent.main"],
        capture_output=True,
        text=True,
        cwd=str(_SRC_DIR),
        env=env,
        input="exit\n",
        timeout=20,
    )
    assert result.returncode == 0
    assert "对话模式" in result.stdout
    assert "再见" in result.stdout


def test_chat_mode_analyzes_category():
    """验证对话模式下，输入品类关键词可触发分析。"""
    env = {**os.environ, "DASHSCOPE_API_KEY": ""}
    result = subprocess.run(
        [sys.executable, "-m", "agent.main"],
        capture_output=True,
        text=True,
        cwd=str(_SRC_DIR),
        env=env,
        input="美妆\n退出\n",
        timeout=30,
    )
    assert result.returncode == 0
    assert "标题模式" in result.stdout or "封面规律" in result.stdout
    assert "美妆" in result.stdout


def test_chat_mode_followup_uses_context():
    """验证追问能复用上一轮品类上下文。"""
    env = {**os.environ, "DASHSCOPE_API_KEY": ""}
    result = subprocess.run(
        [sys.executable, "-m", "agent.main"],
        capture_output=True,
        text=True,
        cwd=str(_SRC_DIR),
        env=env,
        input="母婴\n标题一般怎么写\nexit\n",
        timeout=30,
    )
    assert result.returncode == 0
    # 追问阶段应该出现「母婴」上下文下的标题追问响应
    assert "标题模式追问" in result.stdout
    assert "母婴" in result.stdout


def test_trend_fetcher_returns_mock_data():
    """验证数据检索工具返回数据（从 JSON 文件或兆底 Mock）。"""
    sys.path.insert(0, str(_SRC_DIR))
    from agent.tools.trend_fetcher import fetch_trending_notes

    notes = fetch_trending_notes("母婴", top_n=2)
    assert len(notes) == 2
    assert "title" in notes[0]
    assert "likes" in notes[0]
