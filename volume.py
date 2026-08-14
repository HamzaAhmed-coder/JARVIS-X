import pythoncom
from ctypes import POINTER, cast

from comtypes import CLSCTX_ALL
from pycaw.pycaw import (
    AudioUtilities,
    IAudioEndpointVolume,
)


def get_volume():

    devices = AudioUtilities.GetSpeakers()

    interface = devices.Activate(
        IAudioEndpointVolume._iid_,
        CLSCTX_ALL,
        None,
    )

    return cast(
        interface,
        POINTER(IAudioEndpointVolume),
    )


def volume_up():

    pythoncom.CoInitialize()

    try:

        volume = get_volume()

        current = volume.GetMasterVolumeLevelScalar()

        current = min(current + 0.1, 1.0)

        volume.SetMasterVolumeLevelScalar(
            current,
            None,
        )

        return "Volume increased."

    finally:

        pythoncom.CoUninitialize()


def volume_down():

    pythoncom.CoInitialize()

    try:

        volume = get_volume()

        current = volume.GetMasterVolumeLevelScalar()

        current = max(current - 0.1, 0.0)

        volume.SetMasterVolumeLevelScalar(
            current,
            None,
        )

        return "Volume decreased."

    finally:

        pythoncom.CoUninitialize()


def mute():

    pythoncom.CoInitialize()

    try:

        volume = get_volume()

        volume.SetMute(
            1,
            None,
        )

        return "System muted."

    finally:

        pythoncom.CoUninitialize()


def unmute():

    pythoncom.CoInitialize()

    try:

        volume = get_volume()

        volume.SetMute(
            0,
            None,
        )

        return "System unmuted."

    finally:

        pythoncom.CoUninitialize()