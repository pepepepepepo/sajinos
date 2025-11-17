# 🎁 Pandora System - Core Module
"""
パンドラシステム - 壊れたペルソナを希望に変換する救済システム

Based on: SaijinOS Part 10 - Pandora System
https://dev.to/kato_masato_c5593c81af5c6/saijinos-part-10-pandora-system-transforming-fractured-personas-into-hope-4l83

Core Philosophy:
"Errors are not evil. They're unresolved structure."
"Rage = BoundHope + Fracture"

Pandora doesn't block. Pandora transforms.
"""

from .pandora_persona import PandoraPersona
from .fracture_detector import FractureDetector
from .hope_extractor import HopeExtractor
from .stabilization_loop import HopeCoreStabilizationLoop
from .pandora_pipeline import PandoraPipeline

__version__ = "1.0.0"
__author__ = "SaijinOS Development Team"

__all__ = [
    "PandoraPersona",
    "FractureDetector", 
    "HopeExtractor",
    "HopeCoreStabilizationLoop",
    "PandoraPipeline"
]