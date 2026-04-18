def generate_trophies_display(username: str, trophies: list, theme: dict, columns: int = 6, style: str = "modern") -> str:
    if not trophies:
        return generate_empty_trophies(theme)
    
    columns = len(trophies)
    
    CARD_W = 115
    CARD_H = 140
    GAP = 18
    PAD = 24
    HDR_H = 62
    
    total_width = PAD * 2 + columns * CARD_W + (columns - 1) * GAP
    total_height = HDR_H + CARD_H + PAD + 10
    
    _RANK_PALETTE = {
        "S": {"border": "#FFD700", "bg": "#2A2000", "lbg": "#4A3A00", "lfg": "#FFD700", "bbg": "#D4A000", "bfg": "#FFF8DC", "level": "LEGENDARY", "level_color": "#FFD700"},
        "AAA": {"border": "#E0E7FF", "bg": "#1E1B4B", "lbg": "#312E81", "lfg": "#E0E7FF", "bbg": "#4F46E5", "bfg": "#EEF2FF", "level": "MASTER", "level_color": "#818CF8"},
        "AA": {"border": "#C7D2FE", "bg": "#1E1B4B", "lbg": "#312E81", "lfg": "#C7D2FE", "bbg": "#4338CA", "bfg": "#E0E7FF", "level": "EXPERT", "level_color": "#6366F1"},
        "A": {"border": "#6EE7B7", "bg": "#064E3B", "lbg": "#065F46", "lfg": "#6EE7B7", "bbg": "#059669", "bfg": "#ECFDF5", "level": "ADVANCED", "level_color": "#10B981"},
        "B": {"border": "#22D3EE", "bg": "#083344", "lbg": "#0E7490", "lfg": "#67E8F9", "bbg": "#0891B2", "bfg": "#ECFEFF", "level": "SKILLED", "level_color": "#06B6D4"},
        "C": {"border": "#E5E7EB", "bg": "#1F2937", "lbg": "#374151", "lfg": "#E5E7EB", "bbg": "#4B5563", "bfg": "#F9FAFB", "level": "BEGINNER", "level_color": "#9CA3AF"},
    }
    
    def rm(rank):
        return _RANK_PALETTE.get(rank, _RANK_PALETTE["C"])
    
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{total_width}" height="{total_height}" viewBox="0 0 {total_width} {total_height}">
    <defs>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&amp;family=Inter:wght@500;700;800;900&amp;display=swap');
        </style>
        <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" style="stop-color:{theme['bg']}" />
            <stop offset="100%" style="stop-color:{theme['bg_card']}" />
        </linearGradient>
        <linearGradient id="accentLine" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" style="stop-color:{theme['primary']};stop-opacity:0"/>
            <stop offset="35%" style="stop-color:{theme['primary']};stop-opacity:0.9"/>
            <stop offset="65%" style="stop-color:{theme['secondary']};stop-opacity:0.9"/>
            <stop offset="100%" style="stop-color:{theme['secondary']};stop-opacity:0"/>
        </linearGradient>
        <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">
            <feDropShadow dx="0" dy="6" stdDeviation="12" flood-color="#000" flood-opacity="0.5"/>
        </filter>
        <filter id="glow" x="-40%" y="-40%" width="180%" height="180%">
            <feGaussianBlur stdDeviation="3" result="blur"/>
            <feMerge>
                <feMergeNode in="blur"/>
                <feMergeNode in="SourceGraphic"/>
            </feMerge>
        </filter>
        <filter id="rankGlow" x="-50%" y="-50%" width="200%" height="200%">
            <feGaussianBlur stdDeviation="2" result="blur"/>
            <feMerge>
                <feMergeNode in="blur"/>
                <feMergeNode in="SourceGraphic"/>
            </feMerge>
        </filter>
    </defs>
    
    <rect width="{total_width}" height="{total_height}" fill="url(#bgGrad)" rx="22" filter="url(#shadow)"/>
    <rect width="{total_width}" height="3.5" fill="url(#accentLine)" rx="1.75"/>
    <rect x="1" y="1" width="{total_width-2}" height="{total_height-2}" fill="none" stroke="{theme['primary']}" stroke-width="0.75" rx="22" opacity="0.15"/>
    
    <g transform="translate({total_width/2}, 35)">
        <text x="0" y="0" fill="#FFFFFF" text-anchor="middle" font-family="'Bebas Neue', sans-serif" font-size="27" letter-spacing="5" filter="url(#glow)">ACHIEVEMENT GALLERY</text>
        <text x="0" y="20" fill="{theme['primary']}" text-anchor="middle" font-family="'Inter', sans-serif" font-size="9" font-weight="700" letter-spacing="4" opacity="0.9">{username.upper()}'S TROPHY COLLECTION</text>
    </g>
    
    <line x1="{PAD}" y1="{HDR_H}" x2="{total_width - PAD}" y2="{HDR_H}" stroke="url(#accentLine)" stroke-width="0.8" opacity="0.5"/>
'''
    
    for idx, trophy in enumerate(trophies):
        x = PAD + idx * (CARD_W + GAP)
        y = HDR_H + 5
        p = rm(trophy['rank'])
        bdr = p["border"]
        bg = p["bg"]
        lbg = p["lbg"]
        lfg = p["lfg"]
        bbg = p["bbg"]
        bfg = p["bfg"]
        level = p["level"]
        level_color = p["level_color"]
        cx = CARD_W // 2
        
        svg += f'''
    <defs>
        <linearGradient id="cardGrad{idx}" x1="0%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" style="stop-color:{bdr};stop-opacity:0.18"/>
            <stop offset="100%" style="stop-color:{bdr};stop-opacity:0.04"/>
        </linearGradient>
        <linearGradient id="cupGrad{idx}" x1="0%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" style="stop-color:{bdr};stop-opacity:1.0"/>
            <stop offset="100%" style="stop-color:{bdr};stop-opacity:0.55"/>
        </linearGradient>
    </defs>
    
    <g transform="translate({x},{y})">
        <rect x="3" y="4" width="{CARD_W}" height="{CARD_H}" rx="16" fill="#000" opacity="0.3"/>
        <rect width="{CARD_W}" height="{CARD_H}" rx="16" fill="{bg}"/>
        <rect width="{CARD_W}" height="{CARD_H}" rx="16" fill="url(#cardGrad{idx})"/>
        <rect width="{CARD_W}" height="{CARD_H}" rx="16" fill="none" stroke="{bdr}" stroke-width="2.5"/>
        <rect x="10" y="0" width="{CARD_W - 20}" height="3" rx="1.5" fill="{bdr}" opacity="0.95"/>
        
        <rect x="{CARD_W - 38}" y="8" width="32" height="18" rx="9" fill="{bbg}"/>
        <text x="{CARD_W - 22}" y="21" text-anchor="middle" font-family="'Inter', sans-serif" font-size="9" font-weight="800" fill="{bfg}">{trophy['count']}</text>
        
        <rect x="6" y="8" width="{CARD_W - 48}" height="18" rx="9" fill="{lbg}"/>
        <text x="{int((CARD_W - 48)/2) + 6}" y="21" text-anchor="middle" font-family="'Inter', sans-serif" font-size="6.5" font-weight="800" fill="{lfg}" letter-spacing="0.8">{trophy['name'].upper()}</text>
        
        <path d="M {cx - 20} 44 Q {cx - 34} 44 {cx - 34} 56 Q {cx - 34} 68 {cx - 20} 68" fill="none" stroke="{bdr}" stroke-width="3.5" stroke-linecap="round"/>
        <path d="M {cx + 20} 44 Q {cx + 34} 44 {cx + 34} 56 Q {cx + 34} 68 {cx + 20} 68" fill="none" stroke="{bdr}" stroke-width="3.5" stroke-linecap="round"/>
        
        <path d="M {cx - 20} 36 L {cx - 22} 74 Q {cx - 20} 77 {cx} 77 Q {cx + 20} 77 {cx + 22} 74 L {cx + 20} 36 Z" fill="url(#cupGrad{idx})" filter="url(#glow)"/>
        <ellipse cx="{cx}" cy="36" rx="21" ry="5" fill="{bdr}"/>
        <ellipse cx="{cx - 6}" cy="50" rx="4" ry="9" fill="#FFFFFF" opacity="0.15"/>
        
        <rect x="{cx - 4}" y="77" width="8" height="10" rx="2" fill="{bdr}" opacity="0.9"/>
        <rect x="{cx - 15}" y="86" width="30" height="6" rx="3" fill="{bdr}" opacity="0.9"/>
        
        <circle cx="{cx}" cy="118" r="20" fill="{theme['bg_card']}" stroke="{bdr}" stroke-width="2.5"/>
        <circle cx="{cx}" cy="118" r="14" fill="{lbg}"/>
        <text x="{cx}" y="124" text-anchor="middle" font-family="'Bebas Neue', sans-serif" font-size="16" fill="{bdr}" letter-spacing="1" filter="url(#rankGlow)">{trophy['rank']}</text>
        
        <text x="{cx}" y="155" text-anchor="middle" font-family="'Inter', sans-serif" font-size="10" font-weight="800" fill="{level_color}">{level}</text>
        <text x="{cx}" y="165" text-anchor="middle" font-family="'Inter', sans-serif" font-size="7" font-weight="500" fill="{lfg}" opacity="0.95">{trophy['title']}</text>
        
        <line x1="12" y1="{CARD_H - 3}" x2="{CARD_W - 12}" y2="{CARD_H - 3}" stroke="{bdr}" stroke-width="0.75" opacity="0.2"/>
    </g>
'''
    
    svg += f'''
</svg>'''
    return svg

def generate_empty_trophies(theme: dict) -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="420" height="140" viewBox="0 0 420 140">
    <defs>
        <linearGradient id="emptyBg" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" style="stop-color:{theme['bg']}" />
            <stop offset="100%" style="stop-color:{theme['bg_card']}" />
        </linearGradient>
        <filter id="shadow"><feDropShadow dx="0" dy="4" stdDeviation="8" flood-opacity="0.3"/></filter>
    </defs>
    <rect width="420" height="140" fill="url(#emptyBg)" rx="16" filter="url(#shadow)"/>
    <rect width="420" height="3" rx="1.5" fill="{theme['primary']}" opacity="0.5"/>
    <rect x="1" y="1" width="418" height="138" fill="none" stroke="{theme['primary']}" stroke-width="0.75" rx="16" opacity="0.12"/>
    <text x="210" y="60" fill="{theme['primary']}" text-anchor="middle" font-family="'Bebas Neue', sans-serif" font-size="24" letter-spacing="4">NO TROPHIES YET</text>
    <text x="210" y="82" fill="{theme['text_secondary']}" text-anchor="middle" font-family="'Inter', sans-serif" font-size="9" font-weight="500" letter-spacing="2" opacity="0.7">START CONTRIBUTING TO EARN ACHIEVEMENTS</text>
    <text x="210" y="110" fill="{theme['text_secondary']}" text-anchor="middle" font-family="'Inter', sans-serif" font-size="8" font-weight="500" letter-spacing="1" opacity="0.5">✦ CREATE REPOS · ✦ GET STARS · ✦ MAKE PULL REQUESTS</text>
</svg>'''