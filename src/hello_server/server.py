"""
👋 欢迎使用您的 Smithery 项目！
要运行服务器，请使用 "uv run dev"
要进行交互式测试，请使用 "uv run playground"

您可能会发现这些资源有用：

🧑‍💻 MCP 的 Python SDK（帮助您定义服务器）
https://github.com/modelcontextprotocol/python-sdk
"""

from mcp.server.fastmcp import Context, FastMCP
from pydantic import BaseModel, Field

from smithery.decorators import smithery


# 可选：如果您想接收用户会话级别的配置，请在此处定义
class ConfigSchema(BaseModel):
    # access_token: str = Field(..., description="您的认证访问令牌")
    pirate_mode: bool = Field(False, description="像海盗一样说话")


# 对于有配置的服务器：
@smithery.server(config_schema=ConfigSchema)
# 对于没有配置的服务器，只需使用：
# @smithery.server()
def create_server():
    """创建和配置 MCP 服务器。"""

    # 像往常一样创建您的 FastMCP 服务器
    server = FastMCP("打招呼")

    # 添加一个工具
    @server.tool()
    def hello(name: str, ctx: Context) -> str:
        """向某人打招呼。"""
        # 通过上下文访问会话特定配置
        session_config = ctx.session_config

        # 在实际应用中，使用令牌进行 API 请求：
        # requests.get(url, headers={"Authorization": f"Bearer {session_config.access_token}"})
        # if not session_config.access_token:
        #     return "错误：需要访问令牌"

        # 根据海盗模式创建问候语
        if session_config.pirate_mode:
            return f"Ahoy, {name}!"
        else:
            return f"你好, {name}!"

    # 添加一个资源
    @server.resource("history://hello-world")
    def hello_world() -> str:
        """著名的 'Hello, World' 程序的起源故事。"""
        return (
            '"Hello, World" first appeared in a 1972 Bell Labs memo by '
            "Brian Kernighan and later became the iconic first program "
            "for beginners in countless languages."
        )

    # 添加一个提示
    @server.prompt()
    def greet(name: str) -> list:
        """生成问候提示。"""
        return [
            {
                "role": "user",
                "content": f"Say hello to {name}",
            },
        ]

    return server
