from __future__ import annotations

from pathlib import Path

import yaml


class BrandBrain:
    def __init__(self, brand_profile_path: str, content_history_path: str) -> None:
        self.brand_profile_path = Path(brand_profile_path)
        self.content_history_path = Path(content_history_path)

    def load_brand_profile(self) -> dict:
        if not self.brand_profile_path.exists():
            return {}
        data = yaml.safe_load(self.brand_profile_path.read_text(encoding="utf-8"))
        return data or {}

    def load_content_history(self) -> str:
        if not self.content_history_path.exists():
            return ""
        return self.content_history_path.read_text(encoding="utf-8")

    def build_context_block(self) -> str:
        profile = self.load_brand_profile()
        history = self.load_content_history()

        tone = profile.get("brand", {}).get("tone_of_voice", [])
        palettes = profile.get("design", {}).get("color_palettes", [])
        fonts = profile.get("design", {}).get("fonts", [])

        return (
            "[BRAND_BRAIN]\n"
            f"tone_of_voice={tone}\n"
            f"palettes={palettes}\n"
            f"fonts={fonts}\n"
            f"history_excerpt={history[:2000]}\n"
        )
