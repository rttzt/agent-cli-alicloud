"""manifest 读写测试。"""

from pathlib import Path

import pytest
import yaml

from agent_cli_alicloud.core.manifest import (
    MANIFEST_FILENAME,
    SCHEMA_VERSION,
    read_manifest,
    write_manifest,
)


class TestWriteManifest:
    """write_manifest 测试集。"""

    def test_write_creates_file(self, tmp_path):
        """write_manifest 应创建 manifest 文件。"""
        result_path = write_manifest(
            path=tmp_path,
            name="my-project",
            template_name="agentscope",
            template_version="0.1.0",
            agent_directory="src/agent",
            cli_version="0.2.0",
        )
        assert result_path.exists()
        assert result_path.name == MANIFEST_FILENAME

    def test_write_content_structure(self, tmp_path):
        """写入的 manifest 应包含正确结构。"""
        write_manifest(
            path=tmp_path,
            name="my-project",
            template_name="agentscope",
            template_version="0.1.0",
            agent_directory="src/agent",
            cli_version="0.2.0",
        )

        data = yaml.safe_load((tmp_path / MANIFEST_FILENAME).read_text())
        assert data["schema_version"] == SCHEMA_VERSION
        assert data["name"] == "my-project"
        assert data["template"]["name"] == "agentscope"
        assert data["template"]["version"] == "0.1.0"
        assert data["agent_directory"] == "src/agent"
        assert data["cli_version"] == "0.2.0"
        assert "created_at" in data

    def test_write_invalid_path(self):
        """路径不存在时应抛出 ValueError。"""
        with pytest.raises(ValueError, match="不存在"):
            write_manifest(
                path=Path("/nonexistent/path/xyz"),
                name="my-project",
                template_name="agentscope",
                template_version="0.1.0",
                agent_directory="src/agent",
                cli_version="0.2.0",
            )


class TestReadManifest:
    """read_manifest 测试集。"""

    def test_read_from_directory(self, tmp_path):
        """从目录路径读取 manifest。"""
        write_manifest(
            path=tmp_path,
            name="test-read",
            template_name="agentscope",
            template_version="0.1.0",
            agent_directory="src/agent",
            cli_version="0.2.0",
        )

        data = read_manifest(tmp_path)
        assert data["name"] == "test-read"

    def test_read_from_file_path(self, tmp_path):
        """从文件路径读取 manifest。"""
        write_manifest(
            path=tmp_path,
            name="test-read-file",
            template_name="agentscope",
            template_version="0.1.0",
            agent_directory="src/agent",
            cli_version="0.2.0",
        )

        file_path = tmp_path / MANIFEST_FILENAME
        data = read_manifest(file_path)
        assert data["name"] == "test-read-file"

    def test_read_not_found(self, tmp_path):
        """manifest 文件不存在时应抛出 FileNotFoundError。"""
        with pytest.raises(FileNotFoundError, match="未找到"):
            read_manifest(tmp_path)

    def test_read_invalid_yaml(self, tmp_path):
        """无效 YAML 内容（非 dict）应抛出 ValueError。"""
        manifest_path = tmp_path / MANIFEST_FILENAME
        manifest_path.write_text("- item1\n- item2\n", encoding="utf-8")

        with pytest.raises(ValueError, match="格式错误"):
            read_manifest(tmp_path)

    def test_roundtrip(self, tmp_path):
        """写入后读取应得到相同数据（不含 created_at 精确时间）。"""
        write_manifest(
            path=tmp_path,
            name="roundtrip-test",
            template_name="agentscope",
            template_version="0.1.0",
            agent_directory="src/agent",
            cli_version="0.2.0",
        )

        data = read_manifest(tmp_path)
        assert data["schema_version"] == SCHEMA_VERSION
        assert data["name"] == "roundtrip-test"
        assert data["template"] == {"name": "agentscope", "version": "0.1.0"}
        assert data["agent_directory"] == "src/agent"
        assert data["cli_version"] == "0.2.0"
