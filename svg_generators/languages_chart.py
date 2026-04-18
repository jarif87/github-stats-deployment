import math
from config import Config

def generate_languages_chart(username: str, languages: dict, theme: dict, layout: str = "horizontal", top: int = 10, animated: bool = True) -> str:
    if not languages:
        return generate_empty_chart(theme)

    top_langs = dict(sorted(languages.items(), key=lambda x: x[1], reverse=True)[:top])
    colors = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", "#FFEAA7", "#F3A683", "#98D8C8", "#F7D794", "#778BEB", "#A8E6CF"]

    if layout == "vertical":
        return generate_vertical_chart(username, top_langs, languages, theme, colors, animated)
    else:
        return generate_horizontal_chart(username, top_langs, languages, theme, colors, animated)

def generate_empty_chart(theme: dict) -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="600" height="140" viewBox="0 0 600 140">
    <defs>
        <linearGradient id="emptyBg" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" style="stop-color:{theme['bg']}"/>
            <stop offset="100%" style="stop-color:{theme['bg_card']}"/>
        </linearGradient>
    </defs>
    <rect width="600" height="140" fill="url(#emptyBg)" rx="14"/>
    <rect width="600" height="2.5" rx="1.25" fill="{theme['primary']}" opacity="0.5"/>
    <text x="300" y="75" fill="{theme['text_secondary']}" text-anchor="middle" font-family="'Inter', sans-serif" font-size="12">NO LANGUAGE DATA AVAILABLE</text>
</svg>'''

def generate_vertical_chart(username: str, top_langs: dict, all_languages: dict, theme: dict, colors: list, animated: bool) -> str:
    lang_count = len(top_langs)
    
    if lang_count <= 5:
        width = 700
        bar_gap = 18
    elif lang_count <= 8:
        width = 800
        bar_gap = 16
    else:
        width = 900
        bar_gap = 14
    
    height = 500

    chart_top = 110
    chart_bottom = 430
    chart_left = 70
    chart_right = width - 70

    chart_height = chart_bottom - chart_top
    chart_width = chart_right - chart_left

    bar_width = (chart_width - (lang_count - 1) * bar_gap) / lang_count
    max_bar_h = chart_height - 30

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
    <defs>
        <style>@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&amp;display=swap');</style>
        <linearGradient id="bgMain" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" style="stop-color:{theme['bg']}"/>
            <stop offset="100%" style="stop-color:{theme['bg_card']}"/>
        </linearGradient>
        <linearGradient id="accentLine" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" style="stop-color:{theme['primary']};stop-opacity:0"/>
            <stop offset="35%" style="stop-color:{theme['primary']};stop-opacity:0.8"/>
            <stop offset="65%" style="stop-color:{theme['secondary']};stop-opacity:0.8"/>
            <stop offset="100%" style="stop-color:{theme['secondary']};stop-opacity:0"/>
        </linearGradient>
        <filter id="outerShadow" x="-8%" y="-8%" width="116%" height="116%">
            <feDropShadow dx="0" dy="6" stdDeviation="12" flood-color="#000" flood-opacity="0.4"/>
        </filter>
        <filter id="barGlow" x="-30%" y="-30%" width="160%" height="160%">
            <feGaussianBlur stdDeviation="2.5" result="blur"/>
            <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
        </filter>
    </defs>

    <rect width="{width}" height="{height}" fill="url(#bgMain)" rx="18" filter="url(#outerShadow)"/>
    <rect x="0" y="0" width="{width}" height="2.5" fill="url(#accentLine)" rx="1.25"/>
    <rect x="1" y="1" width="{width-2}" height="{height-2}" fill="none" stroke="{theme['primary']}" stroke-width="0.5" rx="18" opacity="0.08"/>

    <g transform="translate({width/2}, 35)">
        <text font-family="'Inter', sans-serif" font-size="20" fill="{theme['text']}" text-anchor="middle" font-weight="800" letter-spacing="2">LANGUAGE DISTRIBUTION</text>
        <text y="16" font-family="'Inter', sans-serif" font-size="8" fill="{theme['primary']}" text-anchor="middle" font-weight="600" letter-spacing="3" opacity="0.8">{username.upper()} · REPOSITORY ANALYSIS</text>
    </g>

    <rect x="25" y="68" width="{width-50}" height="1" fill="url(#accentLine)" opacity="0.4"/>

    <line x1="{chart_left}" y1="{chart_top}" x2="{chart_left}" y2="{chart_bottom}" stroke="{theme['border']}" stroke-width="1" opacity="0.5"/>
    <line x1="{chart_left}" y1="{chart_bottom}" x2="{chart_right}" y2="{chart_bottom}" stroke="{theme['border']}" stroke-width="1" opacity="0.5"/>
'''

    for i in range(0, 101, 25):
        y_pos = chart_bottom - (i / 100) * max_bar_h
        if chart_top - 5 <= y_pos <= chart_bottom + 5:
            svg += f'''
    <line x1="{chart_left}" y1="{y_pos}" x2="{chart_right}" y2="{y_pos}" stroke="{theme['border']}" stroke-width="0.5" stroke-dasharray="4,4" opacity="0.25"/>
    <text x="{chart_left-6}" y="{y_pos+3}" fill="{theme['text_secondary']}" text-anchor="end" font-family="'Inter', sans-serif" font-size="7.5" font-weight="500">{i}%</text>
'''

    x_pos = chart_left
    for i, (lang, percent) in enumerate(top_langs.items()):
        bar_h = (percent / 100) * max_bar_h
        color = colors[i % len(colors)]
        bar_y = chart_bottom - bar_h

        svg += f'''
    <defs><linearGradient id="vbar{i}" x1="0%" y1="100%" x2="0%" y2="0%">
        <stop offset="0%" style="stop-color:{color};stop-opacity:0.4"/>
        <stop offset="100%" style="stop-color:{color};stop-opacity:1"/>
    </linearGradient></defs>
'''

        if animated:
            svg += f'''
    <rect x="{x_pos}" y="{chart_bottom}" width="{bar_width}" height="0" rx="5" fill="url(#vbar{i})" filter="url(#barGlow)">
        <animate attributeName="y" from="{chart_bottom}" to="{bar_y}" dur="0.6s" begin="{i*0.08}s" fill="freeze"/>
        <animate attributeName="height" from="0" to="{bar_h}" dur="0.6s" begin="{i*0.08}s" fill="freeze"/>
    </rect>
'''
        else:
            svg += f'''
    <rect x="{x_pos}" y="{bar_y}" width="{bar_width}" height="{bar_h}" rx="5" fill="url(#vbar{i})" filter="url(#barGlow)"/>
'''

        display_lang = lang if len(lang) <= 10 else lang[:8] + "..."
        svg += f'''
    <text x="{x_pos + bar_width/2}" y="{chart_bottom + 22}" fill="{theme['text']}" text-anchor="middle" font-family="'Inter', sans-serif" font-size="8" font-weight="500">{display_lang}</text>
    <text x="{x_pos + bar_width - 5}" y="{bar_y + 4}" fill="{color}" text-anchor="end" font-family="'Inter', sans-serif" font-size="9" font-weight="700">{percent}%</text>
'''
        x_pos += bar_width + bar_gap

    svg += f'''
</svg>'''
    return svg

def generate_horizontal_chart(username: str, top_langs: dict, all_languages: dict, theme: dict, colors: list, animated: bool) -> str:
    lang_count = len(top_langs)
    
    if lang_count <= 5:
        width = 650
        label_w = 140
    elif lang_count <= 8:
        width = 700
        label_w = 145
    else:
        width = 750
        label_w = 150
    
    row_height = 40
    padding_top = 90
    padding_btm = 30
    max_bar_width = width - label_w - 80

    total_height = padding_top + lang_count * row_height + padding_btm

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{total_height}" viewBox="0 0 {width} {total_height}">
    <defs>
        <style>@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&amp;display=swap');</style>
        <linearGradient id="bgMain" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" style="stop-color:{theme['bg']}"/>
            <stop offset="100%" style="stop-color:{theme['bg_card']}"/>
        </linearGradient>
        <linearGradient id="accentLine" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" style="stop-color:{theme['primary']};stop-opacity:0"/>
            <stop offset="40%" style="stop-color:{theme['primary']};stop-opacity:0.8"/>
            <stop offset="60%" style="stop-color:{theme['secondary']};stop-opacity:0.8"/>
            <stop offset="100%" style="stop-color:{theme['secondary']};stop-opacity:0"/>
        </linearGradient>
        <filter id="outerShadow" x="-8%" y="-8%" width="116%" height="116%">
            <feDropShadow dx="0" dy="6" stdDeviation="12" flood-color="#000" flood-opacity="0.4"/>
        </filter>
        <filter id="barGlow" x="-10%" y="-30%" width="120%" height="160%">
            <feGaussianBlur stdDeviation="2" result="blur"/>
            <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
        </filter>
    </defs>

    <rect width="{width}" height="{total_height}" fill="url(#bgMain)" rx="16" filter="url(#outerShadow)"/>
    <rect x="0" y="0" width="{width}" height="2.5" fill="url(#accentLine)" rx="1.25"/>
    <rect x="1" y="1" width="{width-2}" height="{total_height-2}" fill="none" stroke="{theme['primary']}" stroke-width="0.5" rx="16" opacity="0.08"/>

    <g transform="translate({width/2}, 32)">
        <text font-family="'Inter', sans-serif" font-size="20" fill="{theme['text']}" text-anchor="middle" font-weight="800" letter-spacing="2">LANGUAGE BREAKDOWN</text>
        <text y="16" font-family="'Inter', sans-serif" font-size="8" fill="{theme['secondary']}" text-anchor="middle" font-weight="600" letter-spacing="3" opacity="0.8">{username.upper()} · CODE COMPOSITION</text>
    </g>

    <rect x="20" y="65" width="{width-40}" height="1" fill="url(#accentLine)" opacity="0.4"/>

    <g transform="translate(20, 78)">
        <text font-family="'Inter', sans-serif" font-size="7" fill="{theme['text_secondary']}" letter-spacing="2" font-weight="600"># LANGUAGE</text>
        <text x="{label_w + max_bar_width/2}" y="0" font-family="'Inter', sans-serif" font-size="7" fill="{theme['text_secondary']}" text-anchor="middle" letter-spacing="2" font-weight="600">DISTRIBUTION</text>
        <text x="{width-45}" y="0" font-family="'Inter', sans-serif" font-size="7" fill="{theme['text_secondary']}" text-anchor="end" letter-spacing="2" font-weight="600">%</text>
    </g>
'''

    y = padding_top
    for i, (lang, percent) in enumerate(top_langs.items()):
        bar_val = (percent / 100) * max_bar_width
        color = colors[i % len(colors)]
        row_y = y + i * row_height
        cx = label_w + 25

        svg += f'''
    <defs><linearGradient id="hbar{i}" x1="0%" y1="0%" x2="100%" y2="0%">
        <stop offset="0%" style="stop-color:{color};stop-opacity:1"/>
        <stop offset="100%" style="stop-color:{color};stop-opacity:0.55"/>
    </linearGradient></defs>

    <rect x="20" y="{row_y}" width="{width-40}" height="34" rx="7" fill="{theme['bg']}" stroke="{theme['border']}" stroke-width="0.5" opacity="0.5"/>
    <rect x="20" y="{row_y}" width="3" height="34" rx="1.5" fill="{color}" opacity="0.9"/>

    <text x="38" y="{row_y+21}" font-family="'Inter', sans-serif" font-size="9" font-weight="700" fill="{color}" opacity="0.7">{str(i+1).zfill(2)}</text>
    <text x="55" y="{row_y+22}" font-family="'Inter', sans-serif" font-size="11" font-weight="600" fill="{theme['text']}">{lang}</text>

    <rect x="{cx}" y="{row_y+10}" width="{max_bar_width}" height="14" rx="7" fill="{theme['bg_card']}" stroke="{theme['border']}" stroke-width="0.5"/>
'''

        if animated:
            svg += f'''
    <rect x="{cx}" y="{row_y+10}" width="0" height="14" rx="7" fill="url(#hbar{i})" filter="url(#barGlow)">
        <animate attributeName="width" from="0" to="{bar_val}" dur="0.5s" begin="{i*0.07}s" fill="freeze"/>
    </rect>
'''
        else:
            svg += f'''
    <rect x="{cx}" y="{row_y+10}" width="{bar_val}" height="14" rx="7" fill="url(#hbar{i})" filter="url(#barGlow)"/>
'''

        svg += f'''
    <text x="{cx + bar_val + 8}" y="{row_y+21}" font-family="'Inter', sans-serif" font-size="10" font-weight="700" fill="{color}">{percent}%</text>
'''

    svg += f'''
</svg>'''
    return svg