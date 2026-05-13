from __future__ import annotations

from fastmcp import FastMCP

from app.tools.check_outdated_packages import check_outdated_packages
from app.tools.detect_template_drift import detect_template_drift
from app.tools.get_file_structure import get_file_structure
from app.tools.get_package_changelog import get_package_changelog
from app.tools.get_package_version import get_package_version
from app.tools.get_project_info import get_project_info
from app.tools.get_python_version import get_python_version
from app.tools.list_packages import list_packages
from app.tools.suggest_drift_fixes import suggest_drift_fixes
from settings import settings

mcp = FastMCP(name=settings.app.mcp_name)

mcp.tool(get_package_version)
mcp.tool(list_packages)
mcp.tool(get_python_version)
mcp.tool(get_package_changelog)
mcp.tool(check_outdated_packages)
mcp.tool(detect_template_drift)
mcp.tool(suggest_drift_fixes)
mcp.tool(get_file_structure)
mcp.tool(get_project_info)

mcp_app = mcp.http_app(path="/")

if __name__ == "__main__":
    mcp.run()
