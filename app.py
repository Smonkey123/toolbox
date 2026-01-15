from fasthtml.common import *
from utils.qr_generator import generate_qr_code
from utils.serial_lookup import lookup_serial
from utils.acronym_lookup import lookup_acronym

# 创建FastHTML应用
app, rt = fast_app(
    hdrs=(
        Link(rel="stylesheet", href="/static/css/style.css"),
        Script(src="https://unpkg.com/htmx.org@1.9.10"),
    )
)


# 导航栏组件
def Navbar():
    return Nav(
        Div(
            A("🧰 软件工具箱", href="/", cls="logo"),
            Div(
                A("二维码生成", href="/qr-generator", cls="nav-link"),
                A("序列号查询", href="/serial-lookup", cls="nav-link"),
                A("缩写查询", href="/acronym-lookup", cls="nav-link"),
                cls="nav-links"
            ),
            cls="navbar"
        )
    )


# 主页
@rt('/')
def get():
    return Html(
        Head(
            Title("软件工具箱"),
            Meta(charset="utf-8"),
            Meta(name="viewport", content="width=device-width, initial-scale=1"),
        ),
        Body(
            Navbar(),
            Main(
                Div(
                    H1("欢迎使用软件工具箱", cls="hero-title"),
                    P("一个简洁高效的在线工具集合", cls="hero-subtitle"),
                    Div(
                        A("开始探索", href="/qr-generator", cls="cta-button"),
                        cls="cta-container"
                    ),
                    cls="hero-section"
                ),
                Div(
                    Div(
                        Div(
                            H3("📱 二维码生成器"),
                            P("快速生成各种类型的二维码"),
                            A("使用工具", href="/qr-generator", cls="tool-link"),
                            cls="tool-card"
                        ),
                        Div(
                            H3("🔍 产品序列号查询"),
                            P("查询产品序列号信息"),
                            A("使用工具", href="/serial-lookup", cls="tool-link"),
                            cls="tool-card"
                        ),
                        Div(
                            H3("📚 英文缩写查询"),
                            P("查询英文术语和缩写含义"),
                            A("使用工具", href="/acronym-lookup", cls="tool-link"),
                            cls="tool-card"
                        ),
                        cls="tools-grid"
                    ),
                    cls="container"
                ),
                cls="main-content"
            )
        )
    )


# 二维码生成器页面
@rt('/qr-generator')
def get():
    return Html(
        Head(Title("二维码生成器")),
        Body(
            Navbar(),
            Main(
                Div(
                    H2("二维码生成器", cls="page-title"),
                    Form(
                        Div(
                            Label("输入内容:", for_="qr-content"),
                            Textarea(
                                id="qr-content",
                                name="content",
                                placeholder="请输入要生成二维码的内容...",
                                rows=4,
                                cls="form-input"
                            ),
                            cls="form-group"
                        ),
                        Div(
                            Label("二维码尺寸:", for_="qr-size"),
                            Select(
                                Option("小 (200x200)", value="200"),
                                Option("中 (400x400)", value="400", selected=True),
                                Option("大 (600x600)", value="600"),
                                id="qr-size",
                                name="size",
                                cls="form-select"
                            ),
                            cls="form-group"
                        ),
                        Button(
                            "生成二维码",
                            type="submit",
                            hx_post="/generate-qr",
                            hx_target="#qr-result",
                            hx_indicator="#loading",
                            cls="submit-button"
                        ),
                        cls="tool-form"
                    ),
                    Div(
                        Div(id="loading", style="display:none;",
                            content="正在生成二维码..."),
                        Div(id="qr-result"),
                        cls="result-container"
                    ),
                    cls="container"
                )
            )
        )
    )


# 生成二维码API
@rt('/generate-qr')
def post(content: str, size: int = 400):
    if not content:
        return Div(P("请输入内容！", cls="error-message"), cls="result")

    try:
        qr_image = generate_qr_code(content, size)
        return Div(
            H4("生成的二维码:"),
            Img(src=f"data:image/png;base64,{qr_image}", cls="qr-image"),
            Div(
                A(
                    "下载二维码",
                    href=f"data:image/png;base64,{qr_image}",
                    download="qrcode.png",
                    cls="download-link"
                ),
                cls="download-container"
            ),
            cls="qr-result"
        )
    except Exception as e:
        return Div(P(f"生成失败: {str(e)}", cls="error-message"), cls="result")


# 序列号查询页面
@rt('/serial-lookup')
def get():
    return Html(
        Head(Title("序列号查询")),
        Body(
            Navbar(),
            Main(
                Div(
                    H2("产品序列号查询", cls="page-title"),
                    Form(
                        Div(
                            Label("输入序列号:", for_="serial-number"),
                            Input(
                                type="text",
                                id="serial-number",
                                name="serial",
                                placeholder="请输入产品序列号...",
                                cls="form-input"
                            ),
                            cls="form-group"
                        ),
                        Button(
                            "查询",
                            type="submit",
                            hx_post="/lookup-serial",
                            hx_target="#lookup-result",
                            cls="submit-button"
                        ),
                        cls="tool-form"
                    ),
                    Div(id="lookup-result", cls="result-container"),
                    cls="container"
                )
            )
        )
    )


# 序列号查询API
@rt('/lookup-serial')
def post(serial: str):
    if not serial:
        return Div(P("请输入序列号！", cls="error-message"), cls="result")

    result = lookup_serial(serial)
    if result:
        return Div(
            H4("查询结果:"),
            Div(
                Div(P(f"产品名称: {result['name']}"), cls="result-item"),
                Div(P(f"型号: {result['model']}"), cls="result-item"),
                Div(P(f"生产日期: {result['manufacture_date']}"), cls="result-item"),
                Div(P(f"保修状态: {result['warranty_status']}"), cls="result-item"),
                cls="result-details"
            ),
            cls="result"
        )
    else:
        return Div(P("未找到该序列号的相关信息", cls="not-found"), cls="result")


# 缩写查询页面
@rt('/acronym-lookup')
def get():
    return Html(
        Head(Title("英文缩写查询")),
        Body(
            Navbar(),
            Main(
                Div(
                    H2("英文术语缩写查询", cls="page-title"),
                    Form(
                        Div(
                            Label("输入缩写或术语:", for_="acronym-term"),
                            Input(
                                type="text",
                                id="acronym-term",
                                name="term",
                                placeholder="请输入英文缩写或术语...",
                                cls="form-input"
                            ),
                            cls="form-group"
                        ),
                        Button(
                            "查询",
                            type="submit",
                            hx_post="/lookup-acronym",
                            hx_target="#acronym-result",
                            cls="submit-button"
                        ),
                        cls="tool-form"
                    ),
                    Div(id="acronym-result", cls="result-container"),
                    cls="container"
                )
            )
        )
    )


# 缩写查询API
@rt('/lookup-acronym')
def post(term: str):
    if not term:
        return Div(P("请输入缩写或术语！", cls="error-message"), cls="result")

    results = lookup_acronym(term)
    if results:
        return Div(
            H4("查询结果:"),
            *[Div(
                Div(P(f"缩写: {result['acronym']}", cls="acronym-title")),
                Div(P(f"含义: {result['meaning']}", cls="acronym-meaning")),
                Div(P(f"领域: {result['field']}", cls="acronym-field")),
                cls="acronym-item"
            ) for result in results],
            cls="result"
        )
    else:
        return Div(P("未找到相关缩写或术语", cls="not-found"), cls="result")


# 静态文件路由
@rt('/static/{filepath:path}')
def get(filepath: str):
    return FileResponse(f'static/{filepath}')


# 启动应用
if __name__ == "__main__":
    serve()