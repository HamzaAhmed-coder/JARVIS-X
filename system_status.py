from fastapi import APIRouter
import psutil
import platform


router = APIRouter()


@router.get("/system-status")
def system_status():

    cpu = psutil.cpu_percent(interval=0.1)

    memory = psutil.virtual_memory().percent

    disk = psutil.disk_usage("/").percent

    return {
        "backend": "ONLINE",
        "ai_model": "ONLINE",
        "voice_system": "READY",

        "cpu": round(cpu),
        "memory": round(memory),
        "disk": round(disk),

        "network": "STABLE",

        "system": platform.system(),

        "power": (
            "AC POWER"
            if psutil.sensors_battery() is None
            else (
                "CHARGING"
                if psutil.sensors_battery().power_plugged
                else "BATTERY"
            )
        )
    }