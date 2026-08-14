from app.tools.browser import (
    open_url,
    google_search,
    youtube_search,
    open_youtube,
    open_chatgpt,
    open_linkedin,
    open_github,
    open_google,
    open_instagram,
    open_gmail,
    #open_whatsapp,
    open_website
)
from app.tools.whatsapp import send_whatsapp
from app.tools.calendar import create_simple_event
from app.tools.calendar import create_event
from app.tools.volume import (
    volume_up,
    volume_down,
    mute,
    unmute,
)
from app.tools.gmail import send_email
from app.tools.gmail import read_latest_emails
from app.tools.search import (
    google_search,
    google_news,
)
from app.memory.memory import (
    remember,
    recall,
    recall_all,
)
from app.tools.memory import (
    remember,
    recall,
    get_all_memory,
    forget
)
from app.tools.file_search import (
    search_file,
    open_file
)
from app.tools.whatsapp import open_whatsapp
from app.tools.whatsapp import (
    open_whatsapp,
    send_whatsapp
)
from app.tools.desktop import (
    open_desktop,
    open_downloads,
    open_documents,
    open_pictures,
    open_file_explorer,
    open_cmd,
    open_paint,
    open_vscode
)
from app.tools.clipboard import (
    copy_text,
    read_clipboard
)
from app.tools.brightness import (
    brightness_up,
    brightness_down,
    brightness_max,
    brightness_min,
    set_brightness,
)
from app.tools.system import (
    open_calculator,
    open_notepad,
    open_application
)
from app.tools.files import (
    create_folder,
    create_text_file,
    delete_file,
    delete_folder
)
from app.tools.windows import (
    take_screenshot,
    lock_pc,
    shutdown_pc,
    restart_pc,
    sleep_pc
)

TOOLS = {}

def register_tool(name, function):
    TOOLS[name] = function

def get_tool(name):
    return TOOLS.get(name)

def tool_exists(name):
    return name in TOOLS

def list_tools():
    return list(TOOLS.keys())

register_tool("browser", open_url)
register_tool("google", google_search)
register_tool("youtube", youtube_search)
register_tool("youtube_home", open_youtube)
register_tool("calculator", open_calculator)
register_tool("notepad", open_notepad)
register_tool("chatgpt", open_chatgpt)
register_tool("linkedin", open_linkedin)
register_tool("github", open_github)
register_tool("google_home", open_google)
register_tool("instagram_home", open_instagram)
register_tool("gmail", open_gmail)
#register_tool("whatsapp", open_whatsapp)
register_tool("desktop", open_desktop)
register_tool("downloads", open_downloads)
register_tool("documents", open_documents)
register_tool("pictures", open_pictures)
register_tool("explorer", open_file_explorer)
register_tool("cmd", open_cmd)
register_tool("paint", open_paint)
register_tool("vscode", open_vscode)
register_tool("create_folder", create_folder)
register_tool("create_file", create_text_file)
register_tool("screenshot", take_screenshot)
register_tool("lock", lock_pc)
register_tool("shutdown", shutdown_pc)
register_tool("restart", restart_pc)
register_tool("sleep", sleep_pc)
register_tool("delete_file", delete_file)
register_tool("delete_folder", delete_folder)
register_tool("open_app", open_application)
register_tool("website", open_website)
register_tool("copy", copy_text)
register_tool("clipboard", read_clipboard)
register_tool("whatsapp_desktop", open_whatsapp)
register_tool("send_whatsapp", send_whatsapp)
register_tool("calendar_create", create_simple_event)
register_tool("read_emails", read_latest_emails)
register_tool("send_email", send_email)
register_tool("google_search", google_search)
register_tool("google_news", google_news)
register_tool("search_file", search_file)
register_tool("open_file", open_file)
register_tool("remember", remember)
register_tool("recall", recall)
register_tool("recall_all", recall_all)
register_tool("volume_up",volume_up,)
register_tool("volume_down",volume_down,)
register_tool("mute",mute,)
register_tool("unmute",unmute,)
register_tool("brightness_up", brightness_up)
register_tool("brightness_down", brightness_down)
register_tool("brightness_max", brightness_max)
register_tool("brightness_min", brightness_min)
register_tool("set_brightness", set_brightness)
register_tool("send_whatsapp", send_whatsapp)
register_tool("remember", remember)
register_tool("recall", recall)
register_tool("get_all_memory", get_all_memory)
register_tool("forget", forget)