# themes.py
"""Modern theme configurations for GitHub stats"""

THEMES = {
    "midnight": {
        "name": "Midnight Pro",
        "bg": "#0a0c10",
        "bg_card": "#0f1117",
        "bg_hover": "#1a1f2e",
        "primary": "#6366f1",
        "primary_gradient": "linear-gradient(135deg, #6366f1, #8b5cf6)",
        "secondary": "#10b981",
        "accent": "#f59e0b",
        "text": "#e5e7eb",
        "text_secondary": "#9ca3af",
        "border": "#1f2937",
        "success": "#10b981",
        "danger": "#ef4444",
        "warning": "#f59e0b",
        "info": "#3b82f6"
    },
    "aurora": {
        "name": "Aurora",
        "bg": "#0f172a",
        "bg_card": "#1e293b",
        "bg_hover": "#334155",
        "primary": "#06b6d4",
        "primary_gradient": "linear-gradient(135deg, #06b6d4, #3b82f6)",
        "secondary": "#8b5cf6",
        "accent": "#ec4899",
        "text": "#f8fafc",
        "text_secondary": "#94a3b8",
        "border": "#334155",
        "success": "#10b981",
        "danger": "#ef4444",
        "warning": "#f59e0b",
        "info": "#3b82f6"
    },
    "sunset": {
        "name": "Sunset",
        "bg": "#1a0b2e",
        "bg_card": "#2d1b4e",
        "bg_hover": "#3d2b5e",
        "primary": "#f43f5e",
        "primary_gradient": "linear-gradient(135deg, #f43f5e, #fb923c)",
        "secondary": "#a855f7",
        "accent": "#fbbf24",
        "text": "#fef3c7",
        "text_secondary": "#d4d4d8",
        "border": "#4c1d95",
        "success": "#22c55e",
        "danger": "#ef4444",
        "warning": "#f59e0b",
        "info": "#3b82f6"
    },
    "forest": {
        "name": "Forest",
        "bg": "#064e3b",
        "bg_card": "#065f46",
        "bg_hover": "#047857",
        "primary": "#34d399",
        "primary_gradient": "linear-gradient(135deg, #34d399, #10b981)",
        "secondary": "#fbbf24",
        "accent": "#f472b6",
        "text": "#ecfdf5",
        "text_secondary": "#a7f3d0",
        "border": "#059669",
        "success": "#10b981",
        "danger": "#ef4444",
        "warning": "#f59e0b",
        "info": "#3b82f6"
    },
    "ocean": {
        "name": "Deep Ocean",
        "bg": "#0c4a6e",
        "bg_card": "#075985",
        "bg_hover": "#0369a1",
        "primary": "#7dd3fc",
        "primary_gradient": "linear-gradient(135deg, #7dd3fc, #38bdf8)",
        "secondary": "#a78bfa",
        "accent": "#facc15",
        "text": "#f0f9ff",
        "text_secondary": "#bae6fd",
        "border": "#0284c7",
        "success": "#10b981",
        "danger": "#ef4444",
        "warning": "#f59e0b",
        "info": "#3b82f6"
    },
    "dark": {
        "name": "Dark Matter",
        "bg": "#000000",
        "bg_card": "#0a0a0a",
        "bg_hover": "#141414",
        "primary": "#ffffff",
        "primary_gradient": "linear-gradient(135deg, #ffffff, #a3a3a3)",
        "secondary": "#737373",
        "accent": "#525252",
        "text": "#ffffff",
        "text_secondary": "#a3a3a3",
        "border": "#262626",
        "success": "#22c55e",
        "danger": "#ef4444",
        "warning": "#f59e0b",
        "info": "#3b82f6"
    }
}

def get_theme(theme_name: str):
    """Get theme by name with fallback"""
    return THEMES.get(theme_name, THEMES["midnight"])