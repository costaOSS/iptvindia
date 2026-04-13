import os
import requests
import re
import concurrent.futures

INDIAN_KEYWORDS = [
    'Hindi', 'Bollywood', 'India', 'Indian',
    'Star Plus', 'Star Gold', 'Star Movies', 'Star Sports', 'Star Cricket', 'Star World',
    'Sony TV', 'Sony Max', 'Sony Max 2', 'Sony Ten', 'Sony Six', 'Sony Pal', 'Sony SAB',
    'Colors TV', 'Colors HD', 'Colors Bangla', 'Colors Marathi', 'Colors Tamil', 'Colors Kannada', 'Colors Infinity',
    'Zee TV', 'Zee HD', 'Zee Cinema', 'Zee Action', 'Zee Anmol', 'Zee Bangla', 'Zee Tamil', 'Zee Yuva', 'Zee Punjabi',
    'DD National', 'DD News', 'DD India', 'DD Sports', 'Doordarshan',
    'NDTV', 'Aaj Tak', 'Republic', 'Times Now', 'India Today', 'ABP', 'News18', 'TV9',
    'ETV', 'ETV HD', 'ETV Plus', 'ETV Cinema', 'ETV Life', 'ETV Abhiruchi',
    '9XM', '9X', 'B4U', 'MTV', 'MTV India',
    'Sun TV', 'Sun News', 'Jaya', 'Asianet', 'Asianet Plus', 'Surya', 'Mazhavil', 'Sun NXT',
    'Gemini TV', 'Polimer', 'Captain', 'Kumari', 'Vijay', 'Kalaignar',
    'Goldmines', 'Manoranjan', 'Zee Classic', 'And Pictures', 'Andpictures',
    'Ten 1', 'Ten 2', 'Ten 3', 'Ten Sports',
    'Hotstar', 'Jio', 'Tata Play', 'Airtel',
    'Sahara One', 'Maha TV', 'Maha',
    'Star Pravah', 'Star Jalsha', 'Star Bharat',
    'DD Malayalam', 'DD Tamil', 'DD Telugu', 'DD Kannada', 'DD Marathi', 'DD Gujarati', 'DD Punjabi', 'DD Chandana',
    'KBS', 'Sahara', 'Shakti', 'Act',
    'Aakaash', 'Aathavan', 'Adhyatm', 'AKD', 'Alankar', 'Amar', 'Amrita', 'Anand', 'Ananda', 'Angel',
    'Bharat', 'Bhoomi', 'Bloomberg', 'Bollywood', 'Box', 'Britannia',
    'Camera', 'Chardikla', 'Dabangg', 'Dahaad', 'Dhayi', 'Dilli', 'Divya',
    'ETV Balaji', 'Fastway', 'Food', 'G',
    'GNN', 'Gulistan', 'Gurukripa',
    'HD', 'Himalaya',
    ' IBC', 'Ichchapuran', 'Indl',
    'Jan', 'Jhanjar', 'Jonack',
    'Kall',
    'Labistro', 'Lokmat',
    'Madhav', 'Madhya', 'Magadan', 'Mahua', 'Malai', 'Manoranjan', 'Mathrubhumi', 'MBC',
    'Mega', 'Mirror', 'MJ',
    'Naada', 'Nadira', 'News', 'Nireeksha',
    'Om', 'Orchid',
    'Paras', 'Pehla', 'Platinum', 'Prakash', 'Prime', 'Punjab',
    'Rangiya', 'Rising', 'RSTV',
    'Sagarika', 'Sakshi', 'Samay', 'Sandesh', 'Sanskar', 'Shubhang', 'Sikkim', 'Sillunu', 'Sirippoli', 'Sonia', 'Sri',
    'Tarang', 'Tazaa', 'Tehzeeb', 'Tippan', 'Travel', 'TV', 'TV5', 'TV9',
    'Udaya', 'Ugc',
    'V4', 'Vanity', 'Vasanth', 'Vijay', 'Vismay', 'Vividh',
    'Wion',
    'Zee', 'Zee24', 'ZeeMPC'
]

EXCLUDED_GROUPS = [
    'Bangladeshi', 'Bangladesh', 'Pakistan', 'Pakistani',
    'UK', 'USA', 'United Kingdom', 'United States', 'Canada', 'Australia',
    'Arabic', 'Islamic', 'Islamic Channel', 'Muslim',
    'Football', 'Documentary',
    'Kids', 'Cartoon', 'Anime',
    'Music', 'Radio',
    'Roku', 'XUMO', 'LG Channels', 'Vizio', 'Fire TV', 'Redbox', 'Tablo', 'Samsung TV', 'Xiaomi'
]

ADDITIONAL_SOURCES = [
    'https://raw.githubusercontent.com/iptv-org/iptv/master/streams/in.m3u',
    'https://raw.githubusercontent.com/iptv-org/iptv/master/streams/in_distro.m3u',
    'https://raw.githubusercontent.com/iptv-org/iptv/master/streams/in_doordarshan.m3u',
    'https://raw.githubusercontent.com/iptv-org/iptv/master/streams/in_pishow.m3u',
    'https://raw.githubusercontent.com/iptv-org/iptv/master/streams/in_tango.m3u',
]

WORKING_DOMAINS = [
    'amagi', 'samsungin', 'akamaized', 'cloudfront', 'cdn', 'wiseplayout',
    'jsrdn', 'yuppcdn', 'yupp', 'intoday', 'akamaized.net', 'cloudfront.net'
]

def is_indian_channel(channel_name, group, url, tvg_id=''):
    channel_name = channel_name or ''
    group = group or ''
    url = url or ''
    tvg_id = tvg_id or ''
    
    channel_lower = channel_name.lower()
    group_lower = group.lower()
    url_lower = url.lower()
    tvg_id_lower = tvg_id.lower()
    
    for excluded in EXCLUDED_GROUPS:
        if excluded.lower() in group_lower:
            return False
    
    if 'bangladesh' in group_lower or ' bd ' in channel_lower or '.bd' in channel_lower:
        return False
    
    if '.in@' in tvg_id_lower:
        return True
    
    if any(kw.lower() in channel_lower for kw in INDIAN_KEYWORDS):
        return True
    
    if any(kw.lower() in group_lower for kw in ['hindi', 'punjabi', 'tamil', 'telugu', 'malayalam', 'kannada', 'marathi', 'gujarati', 'bengali', 'indian', 'regional']):
        return True
    
    if 'samsungin' in url_lower or 'amagi' in url_lower or 'india' in url_lower:
        return True
    
    return False

def is_likely_working(url):
    url_lower = url.lower()
    for domain in WORKING_DOMAINS:
        if domain in url_lower:
            return True
    return False

def check_stream(channel):
    url = channel['url']
    try:
        response = requests.head(url, timeout=8, allow_redirects=True)
        if response.status_code < 400:
            return channel
    except:
        pass
    return None

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
        print(f"Error: {e}")
        return []

    lines = content.split('\n')
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith('#EXTINF:'):
            extinf = line
            url = lines[i+1].strip() if i+1 < len(lines) else ''
            
            tvg_id_match = re.search(r'tvg-id="([^"]*)"', extinf)
            tvg_id = tvg_id_match.group(1) if tvg_id_match else ''
            
            group_match = re.search(r'group-title="([^"]*)"', extinf)
            group = group_match.group(1) if group_match else ''
            
            name_match = re.search(r',([^,\n]+)$', extinf)
            channel_name = name_match.group(1).strip() if name_match else ''
            
            logo_match = re.search(r'tvg-logo="([^"]*)"', extinf)
            logo = logo_match.group(1) if logo_match else ''
            
            if url and is_indian_channel(channel_name, group, url, tvg_id):
                if '.m3u8' in url or '.m3u' in url:
                    playlist.append({'logo': logo, 'group': group, 'channel_name': channel_name, 'url': url, 'tvg_id': tvg_id})
        i += 1
    
    print(f"Found {len(playlist)} Indian channels from {source[:40]}...")
    return playlist

def combine_playlists(all_sources):
    combined_playlist = []
    seen_urls = set()
    seen_names_lower = set()
    
    for source in all_sources:
        source_playlist = read_m3u_playlist(source)
        for channel in source_playlist:
            url_clean = channel['url'].strip().lower()
            name_clean = channel['channel_name'].strip().lower()
            
            if url_clean in seen_urls:
                continue
            
            if name_clean in seen_names_lower:
                continue
            
            if not is_likely_working(channel['url']):
                continue
            
            seen_urls.add(url_clean)
            seen_names_lower.add(name_clean)
            combined_playlist.append(channel)
    
    return combined_playlist

def validate_streams(playlist, max_workers=30):
    print(f"Validating {len(playlist)} streams...")
    working_channels = []
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(check_stream, playlist))
        for channel in results:
            if channel:
                working_channels.append(channel)
    
    print(f"Working streams: {len(working_channels)}/{len(playlist)}")
    return working_channels

def write_to_file(playlist, output_file, include_credits=False):
    credit_text = "# India-only IPTV - iptv-org\n"
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
    default_sources = ADDITIONAL_SOURCES
    
    output_file = 'combined_playlist.m3u'
    include_credits = True  

    combined_playlist = combine_playlists(default_sources)
    
    working_playlist = validate_streams(combined_playlist)

    write_to_file(working_playlist, output_file, include_credits)

    print(f"\n=== Final Result ===")
    print(f"Working India-only playlist written to {output_file}")
    print(f"Total working Indian channels: {len(working_playlist)}")