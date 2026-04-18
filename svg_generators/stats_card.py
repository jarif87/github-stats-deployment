from config import Config

def generate_stats_card(username: str, stats: dict, theme: dict, hidden: list = None) -> str:
    if hidden is None:
        hidden = []

    total_contributions = stats['total_commits'] + stats['total_prs'] * 10 + stats['total_issues'] * 5

    if total_contributions >= 10000:
        rank = "S+"
        rank_color = "#FFD700"
        rank_label = "LEGENDARY"
    elif total_contributions >= 5000:
        rank = "S"
        rank_color = "#FFD700"
        rank_label = "ELITE"
    elif total_contributions >= 2000:
        rank = "A+"
        rank_color = "#10B981"
        rank_label = "EXPERT"
    elif total_contributions >= 1000:
        rank = "A"
        rank_color = "#10B981"
        rank_label = "ADVANCED"
    elif total_contributions >= 500:
        rank = "B+"
        rank_color = "#3B82F6"
        rank_label = "SKILLED"
    else:
        rank = "B"
        rank_color = "#3B82F6"
        rank_label = "RISING"

    stats_config = {
        "stars": {"icon": "⭐", "label": "Stars", "value": f"{stats['total_stars']:,}"},
        "commits": {"icon": "💻", "label": "Commits", "value": f"{stats['total_commits']:,}"},
        "prs": {"icon": "🔄", "label": "Pull Requests", "value": f"{stats['total_prs']:,}"},
        "issues": {"icon": "🐛", "label": "Issues", "value": f"{stats['total_issues']:,}"},
        "repos": {"icon": "📦", "label": "Repositories", "value": f"{stats['public_repos']:,}"},
        "followers": {"icon": "👥", "label": "Followers", "value": f"{stats['followers']:,}"}
    }

    stats_items = [v for k, v in stats_config.items() if k not in hidden]

    items_per_row = 3
    rows = (len(stats_items) + items_per_row - 1) // items_per_row
    card_width = 520
    card_height = 150 + rows * 58

    item_width = (card_width - 72) // items_per_row

    current_streak = stats.get('current_streak', 0)
    longest_streak = stats.get('longest_streak', 0)

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{card_width}" height="{card_height}" viewBox="0 0 {card_width} {card_height}">
    <defs>
        <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" style="stop-color:{theme['bg']}"/>
            <stop offset="100%" style="stop-color:{theme['bg_card']}"/>
        </linearGradient>
        <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">
            <feGaussianBlur in="SourceAlpha" stdDeviation="8"/>
            <feOffset dx="0" dy="8" result="offsetblur"/>
            <feComponentTransfer>
                <feFuncA type="linear" slope="0.5"/>
            </feComponentTransfer>
            <feMerge>
                <feMergeNode/>
                <feMergeNode in="SourceGraphic"/>
            </feMerge>
        </filter>
        <filter id="glow" height="200%" width="200%" x="-50%" y="-50%">
            <feGaussianBlur stdDeviation="2.5" result="coloredBlur"/>
            <feMerge>
                <feMergeNode in="coloredBlur"/>
                <feMergeNode in="SourceGraphic"/>
            </feMerge>
        </filter>
    </defs>
    
    <rect width="{card_width}" height="{card_height}" rx="16" fill="url(#bgGrad)" filter="url(#shadow)"/>
    <rect x="1" y="1" width="{card_width-2}" height="{card_height-2}" rx="16" fill="none" stroke="{theme['border']}" stroke-width="1.5"/>
    
    <g transform="translate(28, 24)">
        <text x="0" y="0" fill="{theme['text']}" font-family="'Inter', 'Segoe UI', system-ui, sans-serif" font-size="18.5" font-weight="700" letter-spacing="-0.3px">{username}'s GitHub Stats</text>
        <text x="0" y="19" fill="{theme['text_secondary']}" font-family="'Inter', 'Segoe UI', system-ui, sans-serif" font-size="10.5" font-weight="500" letter-spacing="0.4px">CONTRIBUTION OVERVIEW</text>
    </g>
'''

    y_offset = 71
    for row in range(rows):
        for col in range(items_per_row):
            idx = row * items_per_row + col
            if idx >= len(stats_items):
                break
            item = stats_items[idx]
            x_offset = 26 + col * (item_width + 14)
            
            svg += f'''
    <g transform="translate({x_offset}, {y_offset + row * 58})">
        <text x="0" y="15" fill="{rank_color}" font-family="'Segoe UI', Arial, sans-serif" font-size="19" font-weight="400">{item['icon']}</text>
        <text x="29" y="15.5" fill="{theme['text_secondary']}" font-family="'Inter', 'Segoe UI', system-ui, sans-serif" font-size="10.2" font-weight="600" letter-spacing="0.6px" text-transform="uppercase">{item['label']}</text>
        <text x="0" y="38" fill="{theme['text']}" font-family="'Inter', 'Segoe UI', system-ui, sans-serif" font-size="18.5" font-weight="700" letter-spacing="-0.4px">{item['value']}</text>
    </g>
'''

    line_y = card_height - 52

    svg += f'''
    <g transform="translate(28, {line_y})">
        <text x="0" y="0" fill="{theme['text_secondary']}" font-family="'Inter', 'Segoe UI', system-ui, sans-serif" font-size="10.5" font-weight="500">🔥 Current Streak</text>
        <text x="0" y="17" fill="{theme['text']}" font-family="'Inter', 'Segoe UI', system-ui, sans-serif" font-size="15.5" font-weight="700">{current_streak} days</text>
        
        <text x="158" y="0" fill="{theme['text_secondary']}" font-family="'Inter', 'Segoe UI', system-ui, sans-serif" font-size="10.5" font-weight="500">📅 Longest Streak</text>
        <text x="158" y="17" fill="{theme['text']}" font-family="'Inter', 'Segoe UI', system-ui, sans-serif" font-size="15.5" font-weight="700">{longest_streak} days</text>
    </g>
    
    <g transform="translate({card_width - 58}, {line_y + 1})">
        <circle cx="0" cy="0" r="23" fill="none" stroke="{rank_color}" stroke-width="2.5" opacity="0.25"/>
        <circle cx="0" cy="0" r="18.5" fill="{rank_color}" opacity="0.08"/>
        <text x="0" y="7" fill="#FFFFFF" text-anchor="middle" font-family="'Inter', 'Segoe UI', system-ui, sans-serif" font-size="15" font-weight="900" letter-spacing="-0.5px" filter="url(#glow)">{rank}</text>
    </g>
    
    <text x="27" y="{card_height - 13}" fill="{theme['text_secondary']}" font-family="'Inter', 'Segoe UI', system-ui, sans-serif" font-size="8.2" opacity="0.65" letter-spacing="0.3px">Powered by GitHub API • Real-time • Updated now</text>
</svg>'''
    return svg

def generate_error_svg(error_message: str) -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="520" height="138" viewBox="0 0 520 138">
    <defs>
        <linearGradient id="errBg" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" style="stop-color:#0D1117"/>
            <stop offset="100%" style="stop-color:#161B22"/>
        </linearGradient>
    </defs>
    <rect width="520" height="138" rx="16" fill="url(#errBg)"/>
    <rect x="1" y="1" width="518" height="136" rx="16" fill="none" stroke="#30363D" stroke-width="1.5"/>
    
    <text x="260" y="48" fill="#F85149" text-anchor="middle" font-family="'Inter', 'Segoe UI', system-ui, sans-serif" font-size="14.5" font-weight="700" letter-spacing="-0.2px">⚠️ Failed to Load GitHub Stats</text>
    <text x="260" y="72" fill="#8B949E" text-anchor="middle" font-family="'Inter', 'Segoe UI', system-ui, sans-serif" font-size="11" font-weight="500">{error_message[:68]}</text>
    <text x="260" y="92" fill="#6E7681" text-anchor="middle" font-family="'Inter', 'Segoe UI', system-ui, sans-serif" font-size="9.5" opacity="0.85">Check the username spelling or try again in a moment</text>
    <text x="260" y="118" fill="#6E7681" text-anchor="middle" font-family="'Inter', 'Segoe UI', system-ui, sans-serif" font-size="8" opacity="0.6">GitHub API may be rate-limited • Please refresh later</text>
</svg>'''