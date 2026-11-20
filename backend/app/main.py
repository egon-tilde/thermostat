"""Stub cloud backend for the Smart Thermostat (test fixture).

It reads its settings with PyYAML's yaml.load, which is the vulnerable function in CVE-2020-14343,
so CRA Sentinel's reachability check reports it as "called". Django, requests and Pillow are declared
in requirements.txt but never imported here, so they are reported as "not used".
"""
import yaml


def load_settings(text: str) -> dict:
    return yaml.load(text, Loader=yaml.FullLoader)


def temperature() -> dict:
    return {"celsius": 21.5}
