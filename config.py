# config.py
"""Configuration settings for the application"""

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration"""
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    CACHE_DURATION_HOURS = int(os.getenv("CACHE_DURATION_HOURS", 1))
    API_TIMEOUT = int(os.getenv("API_TIMEOUT", 30))
    MAX_REPOS = int(os.getenv("MAX_REPOS", 100))
    
    # API Settings
    API_TITLE = "GitHub Stats Dashboard"
    API_DESCRIPTION = "Professional GitHub Statistics Generator"
    API_VERSION = "3.0.0"
    
    # Color palettes for charts
    CHART_COLORS = [
        "#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", "#FFEAA7",
        "#DDA0DD", "#98D8C8", "#F7D794", "#E77F67", "#786FA6",
        "#F3A683", "#778BEB", "#CFA5A5", "#A8E6CF", "#FFB8B8"
    ]
    
    # Chart dimensions
    VERTICAL_CHART_WIDTH = 800
    VERTICAL_CHART_HEIGHT = 520
    PIE_CHART_WIDTH = 550
    PIE_CHART_HEIGHT = 420
    HORIZONTAL_CHART_WIDTH = 650
    
    # Stats card dimensions
    STATS_CARD_WIDTH = 540
    
    @classmethod
    def validate(cls):
        """Validate configuration"""
        if not cls.GITHUB_TOKEN:
            print("⚠️ WARNING: GITHUB_TOKEN not set. API rate limits will be restricted.")
        else:
            print(f"✓ GitHub token configured (length: {len(cls.GITHUB_TOKEN)})")