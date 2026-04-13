import os
import requests
import re

INDIAN_GROUPS = ['Hindi', 'Hindi Movies', 'Hindi Music', 'Indian Bangla News', 
                'Kolkata Bangla', 'Kolkata Bangla Movies', 'Punjabi', 'Tamil',
                'Telugu', 'Malayalam', 'Kannada', 'Marathi', 'Gujarati', 'Bengali',
                'Sports', 'PSL 2026', 'LiveSports', 'DD Sports']

INDIAN_KEYWORDS = ['India', 'Hindi', 'Bollywood', 'DD Sports', 'Star Sports',
                  'Sony', 'Colors', 'Zee', 'Sun', 'Star Plus', 'Star Gold',
                  'Star Movies', 'And', 'B4U', 'Sahara', 'ETV', 'ABN',
                  'NDTV', 'Aaj Tak', 'Republic', 'Times Now', 'India Today',
                  'ABP', 'News18', 'TV9', 'Doordarshan', 'DD', 'Soni',
                  'TV', 'Star', 'Zee TV', 'MTV', '9XM', '9X', 'Etv', 'GEM',
                  'Goldmines', 'Manoranjan', 'Zee Action', 'Zee Classic',
                  'Zee Bollywood', 'Zee Cinema', 'Zee Anmol', 'Sony Pal',
                  'Sony SAB', 'Sony TV', 'Sony Max', 'Sony Max 2', 'Sony Ten',
                  'Colors HD', 'Colors TV', 'Colors Infinity', 'Colors Bangla',
                  'Colors Marathi', 'Colors Tamil', 'Colors Kannada', 'Colors HD',
                  'ETV HD', 'ETV', 'Star Plus', 'Star Pravah', 'Star Jalsha',
                  'Star Sports', 'Star Cricket', 'Star Movies', 'Star Gold',
                  'Star World', 'Hotstar', 'Jio', 'Tata Play', 'Airtel',
                  'Asianet', 'Surya', 'Kumari', 'Asianet Plus', 'Mazhavil',
                  'Zee Tamil', 'Sun TV', 'Sun News', 'Jaya', 'Jaya Plus',
                  'Polimer', 'Captain', 'Gemini', 'ETV Plus', 'ETV Life',
                  'ETV Abhiruchi', 'ETV Cinema', 'Zee Yuva', 'Zee Bangla',
                  'Star Sports 1', 'Star Sports 2', 'Star Sports 3',
                  'Ten 1', 'Ten 2', 'Ten 3', 'Ten Sports', 'Sony Six',
                  'Sony Ten', 'DD National', 'DD News', 'DD India', 'DD Urdu',
                  'DD Chandana', 'DD Malayalam', 'DD Tamil', 'DD Telugu',
                  'DD Kannada', 'DD Marathi', 'DD Gujarati', 'DD Punjabi']

EXCLUDED_GROUPS = ['Bangladeshi', 'Bangla', 'Bangladeshi 🇧🇩', 'Pakistan', 'PSL 🇵🇰',
                  'UK', 'USA', 'Arabic', 'Islamic', 'Cricket 🏏', 'Football',
                  'English Movies', 'English News', 'Documentary', 'KIDS', 'Kids',
                  'Promo', 'ISLAMIC CHANNELS', 'Bangla Movies', 'Bangla Music',
                  'Relagion Channel', 'Roku', 'XUMO', 'LG', 'Vizio', 'Fire TV',
                  'Redbox', 'DistroTV', 'Local Now', 'Tablo', 'Samsung', 'Xiaomi']

ADDITIONAL_SOURCES = [
    'https://raw.githubusercontent.com/iptv-org/iptv/master/streams/in_distro.m3u',
    'https://raw.githubusercontent.com/iptv-org/iptv/master/streams/in_doordarshan.m3u',
    'https://raw.githubusercontent.com/iptv-org/iptv/master/streams/in_pishow.m3u',
    'https://raw.githubusercontent.com/iptv-org/iptv/master/streams/in_tango.m3u',
    'https://raw.githubusercontent.com/Free-TV/IPTV/master/playlist.m3u8',
    'https://raw.githubusercontent.com/freecasthub/public-iptv/main/playlist.m3u',
    'https://raw.githubusercontent.com/BuddyChewChew/app-m3u-generator/refs/heads/main/playlists/roku_all.m3u',
    'https://iptv-org.github.io/iptv/index.m3u',
    'https://apsattv.com/ssungusa.m3u',
    'https://www.apsattv.com/xumo.m3u',
    'https://www.apsattv.com/lg.m3u',
    'https://www.apsattv.com/localnow.m3u',
    'https://www.apsattv.com/redbox.m3u',
    'https://www.apsattv.com/distro.m3u',
    'https://www.apsattv.com/xiaomi.m3u',
    'https://www.apsattv.com/vizio.m3u',
    'https://www.apsattv.com/firetv.m3u',
    'https://www.apsattv.com/cineverse.m3u',
    'https://www.apsattv.com/tablo.m3u',
    'https://www.apsattv.com/klowd.tv',
    'https://tvpass.org/playlist/m3u',
]

def is_indian_channel(channel_name, group):
    group = group or ''
    channel_name = channel_name or ''
    channel_name_lower = channel_name.lower()
    group_lower = group.lower()
    
    for excluded in EXCLUDED_GROUPS:
        if excluded.lower() in group_lower:
            return False
    
    if 'bd' in group_lower or 'bangladesh' in group_lower:
        return False
    
    for keyword in INDIAN_KEYWORDS:
        if keyword.lower() in channel_name_lower:
            return True
    
    for indian_group in INDIAN_GROUPS:
        if indian_group.lower() in group_lower:
            return True
    
    return False

def read_m3u_playlist(source):
    playlist = []
    if not source or source == 'None':
        return []

    print(f"Fetching: {source[:60]}...")
    
    try:
        if source.startswith("http"):
            response = requests.get(source, timeout=30)
            content = response.text
        else:
            with open(source, 'r') as f:
                content = f.read()
    except Exception as e:
        print(f"Error fetching {source}: {e}")
        return []

    lines = content.split('\n')
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith('#EXTINF:'):
            extinf = line
            url = lines[i+1].strip() if i+1 < len(lines) else ''
            
            group_match = re.search(r'group-title="([^"]*)"', extinf)
            group = group_match.group(1) if group_match else ''
            
            name_match = re.search(r',([^,\n]+)$', extinf)
            channel_name = name_match.group(1).strip() if name_match else ''
            
            logo_match = re.search(r'tvg-logo="([^"]*)"', extinf)
            logo = logo_match.group(1) if logo_match else ''
            
            if url and is_indian_channel(channel_name, group):
                if '.m3u8' in url or '.m3u' in url:
                    playlist.append({'logo': logo, 'group': group, 'channel_name': channel_name, 'url': url})
        i += 1
    
    print(f"Found {len(playlist)} Indian channels from {source[:40]}...")
    return playlist

def combine_playlists(all_sources):
    combined_playlist = []
    seen_channels = set()
    seen_names = set()
    
    for source in all_sources:
        source_playlist = read_m3u_playlist(source)
        for channel in source_playlist:
            channel_name_clean = channel['channel_name'].strip().lower()
            url_clean = channel['url'].strip()
            
            channel_identity = (channel_name_clean, url_clean)
            
            if channel_identity not in seen_channels:
                if channel_name_clean not in seen_names:
                    seen_names.add(channel_name_clean)
                    seen_channels.add(channel_identity)
                    combined_playlist.append(channel)
                else:
                    seen_channels.add(channel_identity)
    
    return combined_playlist

def write_to_file(playlist, output_file, include_credits=False):
    credit_text = "# India-only IPTV - Filtered from PiratesTV\n"
    with open(output_file, 'w') as f:
        f.write("#EXTM3U\n")  
        if include_credits:
            f.write(credit_text)
        for item in playlist:
            logo = item['logo'] if item['logo'] else ''
            group = item['group'] if item['group'] else ''
            name = item['channel_name']
            url = item['url']
            f.write(f"#EXTINF:-1 tvg-logo=\"{logo}\" group-title=\"{group}\",{name}\n{url}\n")

if __name__ == "__main__":
    default_sources = [
        'https://raw.githubusercontent.com/FunctionError/PiratesTv/main/combined_playlist.m3u',
        'https://raw.githubusercontent.com/iptv-org/iptv/master/streams/in.m3u'
    ] + ADDITIONAL_SOURCES
    
    output_file = 'combined_playlist.m3u'
    include_credits = True  

    combined_playlist = combine_playlists(default_sources)

    write_to_file(combined_playlist, output_file, include_credits)

    print(f"\n=== Final Result ===")
    print(f"Combined India-only playlist written to {output_file}")
    print(f"Total Indian channels: {len(combined_playlist)}")