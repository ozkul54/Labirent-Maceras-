import json
import math
import random
import sys
import time
from array import array
from pathlib import Path

try:
    import pygame
except ImportError:
    print("Pygame kurulu degil. PowerShell'de 'python -m pip install pygame' komutunu calistirin.")
    raise

WIDTH, HEIGHT = 1000, 700
BOARD_SIZE = 600
PANEL_X = 650
FPS = 60

BG = (18, 24, 32)
PANEL = (28, 37, 49)
GRID = (48, 61, 76)
TILE = (24, 32, 43)
TILE_ALT = (27, 36, 48)
TEXT = (232, 238, 245)
MUTED = (155, 169, 184)
PLAYER = (72, 210, 140)
TARGET = (247, 197, 72)
ITEM = (205, 108, 235)
ENEMY = (235, 82, 91)
BOSS = (255, 120, 48)
GUARD = (255, 160, 48)
WALL = (76, 91, 108)
DEBRIS = (128, 96, 67)
SCORE_FILE = Path(__file__).with_name("highscore.json")
TUTORIAL_FILE = Path(__file__).with_name("tutorial.json")
SETTINGS_FILE = Path(__file__).with_name("settings.json")

DIFFICULTIES = {
    "Kolay": {"health": 5, "enemy_delay": 0.58, "chase_distance": 3, "guard_delay": 0.95},
    "Orta": {"health": 3, "enemy_delay": 0.38, "chase_distance": 5, "guard_delay": 0.65},
    "Zor": {"health": 2, "enemy_delay": 0.34, "chase_distance": 6, "guard_delay": 0.45},
}

CHARACTERS = [
    {"name": "Gezgin", "description": "Hizli hareket eder.", "color": (72, 210, 140), "speed_bonus": 0.08, "health_bonus": 0, "shield_bonus": 0},
    {"name": "Muhafiz", "description": "Ekstra can ve bir baslangic kalkani tasir.", "color": (82, 166, 235), "speed_bonus": 0, "health_bonus": 1, "shield_bonus": 1},
]

THEMES = {
    "forest": {"background": (18, 42, 32), "tile": (25, 58, 42), "tile_alt": (29, 66, 47), "wall": (45, 105, 62)},
    "cave": {"background": (25, 26, 42), "tile": (39, 39, 58), "tile_alt": (45, 45, 67), "wall": (103, 105, 126)},
    "desert": {"background": (62, 45, 27), "tile": (105, 76, 42), "tile_alt": (116, 84, 46), "wall": (181, 126, 59)},
    "ice": {"background": (20, 48, 65), "tile": (39, 91, 111), "tile_alt": (45, 102, 124), "wall": (133, 222, 235)},
    "lava": {"background": (63, 22, 20), "tile": (91, 35, 27), "tile_alt": (103, 40, 29), "wall": (126, 75, 61)},
    "city": {"background": (28, 31, 40), "tile": (53, 57, 68), "tile_alt": (59, 63, 75), "wall": (133, 139, 151)},
    "temple": {"background": (45, 33, 50), "tile": (72, 51, 67), "tile_alt": (80, 57, 74), "wall": (161, 117, 77)},
    "default": {"background": BG, "tile": TILE, "tile_alt": TILE_ALT, "wall": WALL},
}

TRANSLATIONS = {
    "tr": {
        "title": "LABIRENT MACERASI", "start": "Oyuna Basla", "exit": "Cikis", "settings": "Ayarlar",
        "settings_title": "AYARLAR", "language": "Dil", "turkish": "Turkce", "english": "English",
        "back": "Geri Don", "difficulty": "ZORLUK SEVIYESI", "character": "KARAKTERINI SEC",
        "easy": "Kolay", "medium": "Orta", "hard": "Zor", "shop": "DUKKAN", "continue": "Devam Et",
        "music": "Muzik", "effects": "Efekt sesi", "on": "ACIK", "off": "KAPALI",
        "music_toggle": "Muzigi Degistir", "music_help": "Muzigi ac/kapat", "music_volume": "Muzik sesi",
        "language_help": "Dil secimi", "controls": "Kontroller", "back_help": "M: muzik   L: dil   ESC: geri",
    },
    "en": {
        "title": "MAZE ADVENTURE", "start": "Start Game", "exit": "Exit", "settings": "Settings",
        "settings_title": "SETTINGS", "language": "Language", "turkish": "Turkish", "english": "English",
        "back": "Back", "difficulty": "DIFFICULTY", "character": "CHOOSE CHARACTER",
        "easy": "Easy", "medium": "Medium", "hard": "Hard", "shop": "SHOP", "continue": "Continue",
        "music": "Music", "effects": "Effects", "on": "ON", "off": "OFF",
        "music_toggle": "Toggle Music", "music_help": "Turn music on/off", "music_volume": "Music volume",
        "language_help": "Choose language", "controls": "Controls", "back_help": "M: music   L: language   ESC: back",
    },
}

SHOP_ITEMS = [
    {"name": "Can Iksiri", "price": 100, "description": "Bir can ekler.", "key": "health"},
    {"name": "Enerji Kalkani", "price": 150, "description": "Bir dusman carpmasini engeller.", "key": "shield"},
    {"name": "Hiz Kristali", "price": 200, "description": "Dusmanlari yavaslatir.", "key": "speed"},
    {"name": "Altin Tilsim", "price": 250, "description": "Kazanilan puanlari %25 artirir.", "key": "score"},
    {"name": "Duvar Kirici", "price": 180, "description": "Sonraki haritada bir duvari kaldirir.", "key": "wall"},
    {"name": "Sis Bombasi", "price": 220, "description": "Dusmanlarin takip mesafesini azaltir.", "key": "mist"},
]

LEVELS = [
    ("Giris", (2, 2), {(1, 1), (2, 1), (1, 2)}, 5),
    ("Orman", (3, 3), {(1, 0), (2, 1), (1, 2), (2, 3)}, 6),
    ("Magara", (4, 0), {(1, 1), (2, 2), (3, 2), (1, 3)}, 6),
    ("Dag", (0, 4), {(1, 1), (2, 1), (2, 3), (3, 3)}, 6),
    ("Vadi", (4, 4), {(0, 2), (2, 2), (3, 1), (3, 3)}, 6),
    ("Nehir", (3, 0), {(0, 1), (1, 1), (2, 2), (3, 3)}, 6),
    ("Kayalik", (4, 3), {(1, 2), (2, 2), (3, 1), (1, 4)}, 6),
    ("Col", (2, 4), {(1, 1), (2, 1), (3, 2), (1, 3)}, 6),
    ("Orman Kalesi", (4, 4), {(0, 1), (1, 1), (2, 2), (3, 2), (2, 3)}, 7),
    ("Son Sinav", (5, 5), {(1, 0), (2, 1), (3, 2), (2, 4), (4, 3)}, 7),
    ("Buz Vadisi", (6, 6), {(1, 1), (2, 1), (3, 2), (1, 4), (4, 4), (5, 2)}, 8, 2),
    ("Terk Edilmis Sehir", (7, 6), {(1, 0), (2, 1), (3, 1), (4, 2), (2, 4), (5, 4), (6, 3)}, 9, 2),
    ("Lav Tarlasi", (6, 7), {(1, 1), (1, 2), (3, 2), (4, 3), (2, 5), (5, 5), (6, 1)}, 9, 3),
    ("Golge Labirenti", (7, 7), {(1, 0), (2, 2), (4, 1), (3, 3), (5, 3), (1, 5), (6, 5), (4, 6)}, 9, 3),
    ("Kadim Tapinak", (7, 7), {(1, 1), (2, 1), (3, 2), (5, 1), (5, 3), (2, 4), (4, 5), (6, 5)}, 9, 3),
    ("Kristal Magarasi", (8, 8), {(1, 1), (3, 1), (5, 2), (2, 3), (4, 4), (6, 5), (1, 6), (5, 7)}, 10, 3),
    ("Firtina Limani", (9, 8), {(1, 0), (2, 2), (4, 1), (6, 2), (3, 4), (7, 4), (1, 6), (5, 7), (7, 8)}, 10, 3),
    ("Son Kapilar", (8, 9), {(1, 1), (3, 1), (5, 2), (2, 4), (4, 5), (7, 5), (1, 7), (5, 8)}, 10, 4),
]
BOSS_LEVEL = ("Karanlik Efendi", (4, 4), {(0, 2), (1, 2), (2, 1), (2, 3), (3, 2), (4, 1), (4, 3)}, 7, 3)


def text(surface, font, value, position, color=TEXT):
    surface.blit(font.render(value, True, color), position)


def free_cell(size, walls, forbidden):
    cells = [(x, y) for y in range(size) for x in range(size)]
    choices = [cell for cell in cells if cell not in walls and cell not in forbidden]
    return random.choice(choices)


def distant_free_cell(size, walls, forbidden, origin):
    cells = [(x, y) for y in range(size) for x in range(size)]
    available = [cell for cell in cells if cell not in walls and cell not in forbidden]
    minimum_distance = max(2, size - 1)
    distant_cells = [
        cell for cell in available
        if abs(cell[0] - origin[0]) + abs(cell[1] - origin[1]) >= minimum_distance
    ]
    if distant_cells:
        return random.choice(distant_cells)
    return max(
        available,
        key=lambda cell: abs(cell[0] - origin[0]) + abs(cell[1] - origin[1]),
    )


def find_path_cells(size, walls, start, target):
    queue = [start]
    parents = {start: None}
    while queue:
        current = queue.pop(0)
        if current == target:
            path = set()
            while current is not None:
                path.add(current)
                current = parents[current]
            return path
        x, y = current
        for neighbor in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if (0 <= neighbor[0] < size and 0 <= neighbor[1] < size
                    and neighbor not in walls and neighbor not in parents):
                parents[neighbor] = current
                queue.append(neighbor)
    return set()


def reachable_cell_count(size, walls, start):
    queue = [start]
    visited = {start}
    while queue:
        x, y = queue.pop(0)
        for neighbor in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if (0 <= neighbor[0] < size and 0 <= neighbor[1] < size
                    and neighbor not in walls and neighbor not in visited):
                visited.add(neighbor)
                queue.append(neighbor)
    return len(visited)


def expand_walls(size, base_walls):
    expanded = set(base_walls)
    original_reachable = reachable_cell_count(size, expanded, (0, 0))
    candidates = []
    for x in range(1, size - 1, 2):
        candidates.append((x, size - 2))
    for y in range(2, size - 1, 2):
        candidates.append((size - 2, y))
    for x in range(2, size - 1, 3):
        candidates.append((x, size - 3))
    random.shuffle(candidates)
    for candidate in candidates:
        if candidate in expanded or candidate == (0, 0):
            continue
        trial_walls = expanded | {candidate}
        if reachable_cell_count(size, trial_walls, (0, 0)) == original_reachable:
            expanded.add(candidate)
    return expanded


def choose_exit_cell(size, walls, start):
    cells = [(x, y) for y in range(size) for x in range(size)]
    minimum_distance = max(2, size - 1)
    reachable_cells = []
    distant_cells = []
    for cell in cells:
        if cell == start or cell in walls:
            continue
        if find_path_cells(size, walls, start, cell):
            reachable_cells.append(cell)
            distance = abs(cell[0] - start[0]) + abs(cell[1] - start[1])
            if distance >= minimum_distance:
                distant_cells.append(cell)
    if distant_cells:
        return random.choice(distant_cells)
    if reachable_cells:
        return random.choice(reachable_cells)
    return distant_free_cell(size, walls, {start}, start)


def target_guard_cell(size, walls, forbidden, target, protected_path):
    cells = [(x, y) for y in range(size) for x in range(size)]
    available = [
        cell for cell in cells
        if cell not in walls and cell not in forbidden and cell not in protected_path
    ]
    nearby = [
        cell for cell in available
        if abs(cell[0] - target[0]) + abs(cell[1] - target[1]) == 1
    ]
    if nearby:
        return random.choice(nearby)
    return None


class Game:
    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 1, 512)
        pygame.init()
        pygame.display.set_caption("Labirent Macerasi")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.title_font = pygame.font.Font(None, 46)
        self.heading_font = pygame.font.Font(None, 32)
        self.body_font = pygame.font.Font(None, 25)
        self.small_font = pygame.font.Font(None, 20)
        self.high_score = self.load_high_score()
        self.settings = self.load_settings()
        self.sound_item = self.make_tone(880, 0.12, 0.25)
        self.sound_damage = self.make_tone(180, 0.22, 0.3)
        self.sound_complete = self.make_tone(1046, 0.3, 0.25)
        self.music_cache = {}
        self.background_music = None
        self.tutorial_seen = self.load_tutorial_status()
        self.state = "menu" if self.tutorial_seen else "tutorial"
        self.difficulty_name = "Orta"
        self.character_index = 0
        self.character = CHARACTERS[0]
        self.reset()

    def load_settings(self):
        defaults = {"music_enabled": True, "music_volume": 0.35, "effects_volume": 0.5, "language": "tr"}
        try:
            with SETTINGS_FILE.open("r", encoding="utf-8") as settings_file:
                saved = json.load(settings_file)
                defaults.update(saved)
        except (OSError, ValueError, TypeError, json.JSONDecodeError):
            pass
        return defaults

    def tr(self, key):
        language = self.settings.get("language", "tr")
        return TRANSLATIONS.get(language, TRANSLATIONS["tr"]).get(key, key)

    def toggle_language(self):
        self.settings["language"] = "en" if self.settings.get("language", "tr") == "tr" else "tr"
        self.save_settings()

    def set_language(self, language):
        self.settings["language"] = language
        self.save_settings()

    def save_settings(self):
        try:
            with SETTINGS_FILE.open("w", encoding="utf-8") as settings_file:
                json.dump(self.settings, settings_file)
        except OSError:
            pass

    def apply_audio_settings(self):
        for sound in (self.sound_item, self.sound_damage, self.sound_complete):
            if sound is not None:
                sound.set_volume(self.settings["effects_volume"])
        if self.background_music is not None:
            self.background_music.set_volume(self.settings["music_volume"] if self.settings["music_enabled"] else 0)

    def toggle_music(self):
        self.settings["music_enabled"] = not self.settings["music_enabled"]
        self.apply_audio_settings()
        self.save_settings()

    def change_volume(self, setting_name, amount):
        self.settings[setting_name] = max(0, min(1, self.settings[setting_name] + amount))
        self.apply_audio_settings()
        self.save_settings()

    def make_tone(self, frequency, duration, volume):
        try:
            sample_rate = 44100
            samples = array("h")
            for index in range(int(sample_rate * duration)):
                fade = min(1.0, (sample_rate * duration - index) / (sample_rate * 0.04))
                value = int(32767 * volume * fade * math.sin(2 * math.pi * frequency * index / sample_rate))
                samples.append(value)
            return pygame.mixer.Sound(buffer=samples.tobytes())
        except pygame.error:
            return None

    def make_music(self, notes, tempo=0.28, volume=0.08):
        try:
            sample_rate = 22050
            samples = array("h")
            note_length = int(sample_rate * tempo)
            bass_notes = [max(55, note // 2) for note in notes]
            for note_index in range(24):
                frequency = notes[note_index % len(notes)]
                bass_frequency = bass_notes[note_index % len(bass_notes)]
                for sample_index in range(note_length):
                    position = sample_index / sample_rate
                    absolute_position = (note_index * note_length + sample_index) / sample_rate
                    vibrato = math.sin(2 * math.pi * 5.2 * position) * 2.5
                    flute_frequency = frequency + vibrato
                    flute = math.sin(2 * math.pi * flute_frequency * position)
                    flute += math.sin(2 * math.pi * flute_frequency * 2 * position) * 0.16
                    flute += math.sin(2 * math.pi * flute_frequency * 3 * position) * 0.05
                    bass = math.sin(2 * math.pi * bass_frequency * absolute_position) * 0.22
                    pad = math.sin(2 * math.pi * (frequency / 2) * absolute_position) * 0.08
                    pulse = math.sin(2 * math.pi * 2.0 * absolute_position) * 0.035
                    attack = min(1.0, sample_index / (sample_rate * 0.04))
                    release = min(1.0, (note_length - sample_index) / (sample_rate * 0.08))
                    envelope = attack * release
                    samples.append(int(32767 * volume * envelope * (flute + bass + pad + pulse)))
            return pygame.mixer.Sound(buffer=samples.tobytes())
        except pygame.error:
            return None

    def start_music(self, track_name="normal"):
        tracks = {
            "normal": ([220, 262, 330, 294, 247, 196, 247, 294], 0.28, 0.08),
            "forest": ([196, 247, 294, 330, 294, 247, 220, 247], 0.34, 0.07),
            "cave": ([147, 175, 196, 220, 175, 147, 131, 175], 0.42, 0.07),
            "desert": ([220, 247, 277, 330, 277, 247, 220, 196], 0.36, 0.07),
            "ice": ([330, 392, 440, 523, 440, 392, 330, 294], 0.24, 0.06),
            "lava": ([110, 131, 147, 175, 147, 131, 110, 98], 0.22, 0.09),
            "city": ([262, 330, 392, 330, 294, 330, 392, 440], 0.25, 0.07),
            "temple": ([175, 220, 262, 247, 220, 196, 175, 147], 0.38, 0.07),
            "boss": ([98, 123, 147, 110, 98, 82, 110, 123], 0.18, 0.1),
            "shop": ([330, 392, 440, 523, 440, 392, 330, 294], 0.45, 0.05),
        }
        notes, tempo, volume = tracks.get(track_name, tracks["normal"])
        if track_name not in self.music_cache:
            self.music_cache[track_name] = self.make_music(notes, tempo, volume)
        self.stop_music()
        self.background_music = self.music_cache[track_name]
        if self.background_music is not None:
            self.apply_audio_settings()
            self.background_music.play(loops=-1)

    def stop_music(self):
        if self.background_music is not None:
            self.background_music.stop()

    def play_sound(self, sound):
        if sound is not None:
            sound.play()

    def load_high_score(self):
        try:
            with SCORE_FILE.open("r", encoding="utf-8") as score_file:
                saved = json.load(score_file)
                self.best_time = float(saved.get("best_time", 0))
                self.best_items = int(saved.get("best_items", 0))
                return int(saved.get("high_score", 0))
        except (OSError, ValueError, TypeError, json.JSONDecodeError):
            self.best_time = 0
            self.best_items = 0
            return 0

    def load_tutorial_status(self):
        try:
            with TUTORIAL_FILE.open("r", encoding="utf-8") as tutorial_file:
                return bool(json.load(tutorial_file).get("seen", False))
        except (OSError, ValueError, TypeError, json.JSONDecodeError):
            return False

    def finish_tutorial(self):
        self.tutorial_seen = True
        try:
            with TUTORIAL_FILE.open("w", encoding="utf-8") as tutorial_file:
                json.dump({"seen": True}, tutorial_file)
        except OSError:
            pass
        self.state = "menu"

    def update_high_score(self):
        if self.score <= self.high_score:
            return
        self.high_score = self.score
        try:
            with SCORE_FILE.open("w", encoding="utf-8") as score_file:
                json.dump({
                    "high_score": self.high_score,
                    "best_time": self.best_time,
                    "best_items": self.best_items,
                }, score_file)
        except OSError:
            pass

    def save_run_records(self):
        total = self.total_elapsed()
        changed = False
        if self.state == "summary" and (self.best_time == 0 or total < self.best_time):
            self.best_time = total
            changed = True
        if self.collected_items > self.best_items:
            self.best_items = self.collected_items
            changed = True
        if changed:
            try:
                with SCORE_FILE.open("w", encoding="utf-8") as score_file:
                    json.dump({
                        "high_score": self.high_score,
                        "best_time": self.best_time,
                        "best_items": self.best_items,
                    }, score_file)
            except OSError:
                pass

    def reset(self):
        self.level_index = 0
        self.character = CHARACTERS[self.character_index]
        self.max_health = DIFFICULTIES[self.difficulty_name]["health"] + self.character["health_bonus"]
        self.health = self.max_health
        self.score = 0
        self.collected_items = 0
        self.damage_taken = 0
        self.completed_levels = 0
        self.shields = self.character["shield_bonus"]
        self.speed_upgrades = 0
        self.score_multiplier = 1.0
        self.wall_breakers = 0
        self.mist_bombs = 0
        self.item_counts = {item["key"]: 0 for item in SHOP_ITEMS}
        self.purchased_counts = {item["key"]: 0 for item in SHOP_ITEMS}
        self.shop_selection = 0
        self.level_times = []
        self.started_at = 0
        self.level_started_at = 0
        self.paused_at = 0
        self.total_paused = 0
        self.level_paused = 0
        self.finished_at = 0
        self.countdown_started = 0
        self.player = (0, 0)
        self.target = (0, 0)
        self.item = None
        self.enemies = []
        self.guard_enemies = set()
        self.exit_path = set()
        self.walls = set()
        self.debris = set()
        self.size = 0
        self.is_boss = False
        self.enemy_tick = 0
        self.guard_tick = 0

    def start_game(self):
        self.reset()
        self.state = "playing"
        self.started_at = time.time()
        self.start_music()
        self.load_level()

    def choose_difficulty(self, difficulty_name):
        self.difficulty_name = difficulty_name
        self.state = "character"

    def choose_character(self, character_index):
        self.character_index = character_index
        self.start_game()

    def load_level(self):
        data = BOSS_LEVEL if self.level_index == len(LEVELS) else LEVELS[self.level_index]
        _, _, base_walls, self.size = data[:4]
        self.walls = expand_walls(self.size, base_walls)
        self.debris = set()
        if self.wall_breakers > 0 and self.walls:
            removable_walls = [wall for wall in self.walls if wall != (0, 0)]
            if removable_walls:
                broken_wall = random.choice(removable_walls)
                self.walls.remove(broken_wall)
                self.debris.add(broken_wall)
                self.wall_breakers -= 1
                self.item_counts["wall"] = max(0, self.item_counts["wall"] - 1)
        enemy_count = data[4] if len(data) > 4 else 1
        self.is_boss = self.level_index == len(LEVELS)
        level_name = data[0]
        self.start_music("boss" if self.is_boss else self.get_music_theme(level_name))
        self.player = (0, 0)
        self.target = choose_exit_cell(self.size, self.walls, self.player)
        self.exit_path = find_path_cells(self.size, self.walls, self.player, self.target)
        self.item = free_cell(self.size, self.walls, {self.player, self.target})
        forbidden = {self.player, self.target, self.item}
        self.enemies = []
        for _ in range(enemy_count):
            enemy = distant_free_cell(self.size, self.walls, forbidden, self.player)
            self.enemies.append(enemy)
            forbidden.add(enemy)
        has_exit_guard = (
            self.difficulty_name == "Zor"
            or self.size >= 7
            or (self.size >= 6 and self.difficulty_name in ("Orta", "Zor"))
        )
        if has_exit_guard:
            guard = target_guard_cell(self.size, self.walls, forbidden, self.target, self.exit_path)
            if guard is not None:
                self.enemies.append(guard)
                self.guard_enemies.add(guard)
                forbidden.add(guard)
        self.level_started_at = 0
        self.level_paused = 0
        self.enemy_tick = 0
        self.guard_tick = 0
        self.countdown_started = time.time()
        self.state = "countdown"

    def update_countdown(self):
        if self.state != "countdown":
            return
        if time.time() - self.countdown_started >= 3:
            self.level_started_at = time.time()
            if self.started_at == 0:
                self.started_at = self.level_started_at
            self.state = "playing"

    def level_elapsed(self):
        current_pause = time.time() - self.paused_at if self.state == "paused" else 0
        return time.time() - self.level_started_at - self.level_paused - current_pause

    def time_bonus(self):
        return max(0, 150 - int(self.level_elapsed() * 5))

    def total_elapsed(self):
        current_pause = time.time() - self.paused_at if self.state == "paused" else 0
        end_time = self.finished_at if self.finished_at else time.time()
        return end_time - self.started_at - self.total_paused - current_pause

    def pause_game(self):
        if self.state == "playing":
            self.paused_at = time.time()
            self.state = "paused"

    def resume_game(self):
        if self.state == "paused":
            paused_duration = time.time() - self.paused_at
            self.total_paused += paused_duration
            self.level_paused += paused_duration
            self.paused_at = 0
            self.state = "playing"

    def buy_item(self, item_index):
        item = SHOP_ITEMS[item_index]
        if self.score < item["price"]:
            return False
        self.score -= item["price"]
        self.item_counts[item["key"]] += 1
        self.purchased_counts[item["key"]] += 1
        if item["key"] == "health":
            pass
        elif item["key"] == "shield":
            self.shields += 1
        elif item["key"] == "speed":
            self.speed_upgrades += 1
        elif item["key"] == "score":
            self.score_multiplier += 0.25
        elif item["key"] == "wall":
            self.wall_breakers += 1
        elif item["key"] == "mist":
            self.mist_bombs += 1
        return True

    def continue_from_shop(self):
        self.state = "playing"
        self.load_level()

    def use_health_potion(self):
        if self.item_counts["health"] <= 0 or self.health >= self.max_health:
            return
        self.item_counts["health"] -= 1
        self.health += 1

    def damage(self):
        self.play_sound(self.sound_damage)
        self.damage_taken += 1
        if self.shields > 0:
            self.shields -= 1
            self.item_counts["shield"] = max(0, self.item_counts["shield"] - 1)
            return
        self.health -= 1
        if self.health <= 0:
            self.finished_at = time.time()
            self.update_high_score()
            self.stop_music()
            self.state = "gameover"

    def move_player(self, dx, dy):
        if self.state != "playing":
            return
        next_position = (self.player[0] + dx, self.player[1] + dy)
        if not (0 <= next_position[0] < self.size and 0 <= next_position[1] < self.size):
            return
        if next_position in self.walls:
            return
        self.player = next_position
        if self.player == self.item:
            self.score += int((75 if self.is_boss else 50) * self.score_multiplier)
            self.item = None
            self.collected_items += 1
            self.play_sound(self.sound_item)
        if self.player in self.enemies:
            self.damage()
            return
        if self.player == self.target:
            elapsed = self.level_elapsed()
            name = BOSS_LEVEL[0] if self.is_boss else LEVELS[self.level_index][0]
            self.level_times.append((name, elapsed))
            self.completed_levels += 1
            completion_points = 250 if self.is_boss else 100
            self.score += int((completion_points + self.time_bonus()) * self.score_multiplier)
            self.play_sound(self.sound_complete)
            if self.is_boss:
                self.finished_at = time.time()
                self.update_high_score()
                self.stop_music()
                self.state = "summary"
                self.save_run_records()
            else:
                self.level_index += 1
                self.state = "shop"
                self.shop_selection = 0
                self.start_music("shop")

    def move_enemy(self, dt):
        if self.state != "playing" or not self.enemies:
            return
        self.enemy_tick += dt
        self.guard_tick += dt
        settings = DIFFICULTIES[self.difficulty_name]
        enemy_delay = settings["enemy_delay"] + self.speed_upgrades * 0.08 + self.character["speed_bonus"]
        if self.is_boss:
            enemy_delay = max(0.18, enemy_delay - 0.10)
        if self.enemy_tick < enemy_delay:
            return
        self.enemy_tick = 0
        guard_can_move = self.guard_tick >= settings["guard_delay"]
        if guard_can_move:
            self.guard_tick = 0
        updated_enemies = []
        updated_guards = set()
        for ex, ey in self.enemies:
            is_guard = (ex, ey) in self.guard_enemies
            if is_guard and not guard_can_move:
                updated_enemies.append((ex, ey))
                updated_guards.add((ex, ey))
                continue
            px, py = self.player
            distance = abs(px - ex) + abs(py - ey)
            chase_distance = max(1, settings["chase_distance"] - self.mist_bombs)
            if self.is_boss:
                chase_distance += 2
            if is_guard:
                moves = [(1, 0), (-1, 0), (0, 1), (0, -1)]
                random.shuffle(moves)
            elif distance <= chase_distance or self.is_boss:
                moves = []
                if px != ex:
                    moves.append((1 if px > ex else -1, 0))
                if py != ey:
                    moves.append((0, 1 if py > ey else -1))
                random.shuffle(moves)
            else:
                moves = [(1, 0), (-1, 0), (0, 1), (0, -1)]
                random.shuffle(moves)
            new_position = (ex, ey)
            for dx, dy in moves:
                candidate = (ex + dx, ey + dy)
                if candidate == self.target:
                    continue
                valid_candidate = (
                    0 <= candidate[0] < self.size
                    and 0 <= candidate[1] < self.size
                    and candidate not in self.walls
                    and candidate not in updated_enemies
                )
                if is_guard:
                    adjacent_count = sum(
                        1 for x, y in ((self.target[0] + 1, self.target[1]),
                                       (self.target[0] - 1, self.target[1]),
                                       (self.target[0], self.target[1] + 1),
                                       (self.target[0], self.target[1] - 1))
                        if 0 <= x < self.size and 0 <= y < self.size
                        and (x, y) not in self.walls
                    )
                    patrol_distance = 1 if adjacent_count >= 2 else 2
                    valid_candidate = valid_candidate and (
                        abs(candidate[0] - self.target[0]) + abs(candidate[1] - self.target[1]) <= patrol_distance
                        and candidate != self.target
                    )
                if valid_candidate:
                    new_position = candidate
                    break
            updated_enemies.append(new_position)
            if is_guard:
                updated_guards.add(new_position)
        updated_enemies = [enemy for enemy in updated_enemies if enemy != self.target]
        updated_guards.intersection_update(updated_enemies)
        self.enemies = updated_enemies
        self.guard_enemies = updated_guards
        if self.player in self.enemies:
            self.damage()

    def draw_button(self, rect, label, color):
        pygame.draw.rect(self.screen, color, rect, border_radius=8)
        pygame.draw.rect(self.screen, (255, 255, 255), rect, 2, border_radius=8)
        label_surface = self.body_font.render(label, True, TEXT)
        self.screen.blit(label_surface, label_surface.get_rect(center=rect.center))

    def draw_menu(self):
        self.screen.fill(BG)
        pygame.draw.rect(self.screen, PANEL, (48, 38, 904, 600), border_radius=18)
        pygame.draw.rect(self.screen, (55, 72, 88), (48, 38, 904, 600), 2, border_radius=18)
        pygame.draw.rect(self.screen, TARGET, (78, 92, 8, 110), border_radius=4)
        text(self.screen, self.small_font, "ARCADE LAB", (105, 70), MUTED)
        text(self.screen, self.title_font, self.tr("title"), (105, 105), TARGET)
        text(self.screen, self.body_font, "Cikis yolunu bul. Itemleri topla. Bossu yen.", (108, 166), TEXT)
        text(self.screen, self.small_font, f"{len(LEVELS)} bolum  /  rastgele haritalar  /  final boss", (108, 198), MUTED)

        pygame.draw.rect(self.screen, (22, 30, 41), (105, 245, 350, 175), border_radius=12)
        pygame.draw.rect(self.screen, GRID, (105, 245, 350, 175), 2, border_radius=12)
        text(self.screen, self.heading_font, "SEFER DURUMU", (130, 270), PLAYER)
        text(self.screen, self.body_font, f"En yuksek skor: {self.high_score}", (130, 320), TARGET)
        best_time_text = "-" if self.best_time == 0 else f"{self.best_time:.1f} sn"
        text(self.screen, self.small_font, f"En iyi sure: {best_time_text}", (130, 345), TEXT)
        text(self.screen, self.small_font, f"En cok item: {self.best_items}", (130, 370), TEXT)
        text(self.screen, self.small_font, "Zorluk seviyeni baslangicta sec.", (130, 395), MUTED)
        text(self.screen, self.small_font, "T: oyun rehberini tekrar ac", (130, 420), MUTED)

        pygame.draw.rect(self.screen, (22, 30, 41), (510, 245, 350, 175), border_radius=12)
        pygame.draw.rect(self.screen, GRID, (510, 245, 350, 175), 2, border_radius=12)
        text(self.screen, self.heading_font, "KONTROLLER", (535, 270), PLAYER)
        text(self.screen, self.small_font, "W A S D     hareket", (535, 320), TEXT)
        text(self.screen, self.small_font, "P             duraklat", (535, 350), TEXT)
        text(self.screen, self.small_font, "ESC           menu", (535, 380), TEXT)

        self.draw_button(pygame.Rect(105, 465, 300, 54), self.tr("start"), PLAYER)
        self.draw_button(pygame.Rect(430, 465, 220, 54), self.tr("exit"), ENEMY)
        self.draw_button(pygame.Rect(675, 465, 185, 54), self.tr("settings"), GRID)

    def draw_settings(self):
        self.screen.fill(BG)
        pygame.draw.rect(self.screen, PANEL, (95, 65, 810, 535), border_radius=16)
        pygame.draw.rect(self.screen, GRID, (95, 65, 810, 535), 2, border_radius=16)
        text(self.screen, self.title_font, self.tr("settings_title"), (140, 105), TARGET)
        text(self.screen, self.body_font, self.tr("language_help"), (143, 160), MUTED)
        music_status = self.tr("on") if self.settings["music_enabled"] else self.tr("off")
        text(self.screen, self.body_font, f"{self.tr('music')}: {music_status}", (150, 235), TEXT)
        text(self.screen, self.small_font, self.tr("music_help"), (150, 270), MUTED)
        self.draw_button(pygame.Rect(570, 225, 230, 52), self.tr("music_toggle"), PLAYER)
        text(self.screen, self.body_font, f"{self.tr('music_volume')}: %{int(self.settings['music_volume'] * 100)}", (150, 335), TEXT)
        self.draw_button(pygame.Rect(570, 325, 105, 52), "-", GRID)
        self.draw_button(pygame.Rect(695, 325, 105, 52), "+", GRID)
        text(self.screen, self.body_font, f"{self.tr('effects')}: %{int(self.settings['effects_volume'] * 100)}", (150, 425), TEXT)
        self.draw_button(pygame.Rect(570, 415, 105, 52), "-", GRID)
        self.draw_button(pygame.Rect(695, 415, 105, 52), "+", GRID)
        text(self.screen, self.body_font, f"{self.tr('language')}: {self.tr('turkish') if self.settings.get('language') == 'tr' else self.tr('english')}", (150, 500), TEXT)
        self.draw_button(pygame.Rect(470, 485, 145, 42), self.tr("turkish"), PLAYER if self.settings.get("language") == "tr" else GRID)
        self.draw_button(pygame.Rect(625, 485, 145, 42), self.tr("english"), PLAYER if self.settings.get("language") == "en" else GRID)
        self.draw_button(pygame.Rect(150, 550, 220, 42), self.tr("back"), TARGET)
        text(self.screen, self.small_font, self.tr("back_help"), (420, 560), MUTED)

    def draw_tutorial(self):
        self.screen.fill(BG)
        text(self.screen, self.title_font, "OYUN REHBERI", (70, 45), TARGET)
        text(self.screen, self.body_font, "Labirentte ilerle, cikisi bul ve dusmanlardan kac.", (74, 105), MUTED)
        sections = [
            ("HAREKET", "W A S D: hareket   H: can iksiri   P: duraklat", PLAYER),
            ("HARITA", "Yesil: oyuncu   Sari: cikis   Mor: item", TARGET),
            ("TEHLIKELER", "Kirmizi: dusman   Turuncu: cikis koruyucusu", ENEMY),
            ("MARKET", "Bolum bitince puanlarla item al, sonra SPACE ile devam et.", ITEM),
            ("AMAC", f"{len(LEVELS)} bolumu ve final bossu tamamla. Hiz bonusu kazan.", BOSS),
        ]
        for index, (heading, description, color) in enumerate(sections):
            top = 155 + index * 62
            text(self.screen, self.body_font, heading, (80, top), color)
            text(self.screen, self.small_font, description, (250, top + 4), TEXT)
        self.draw_button(pygame.Rect(75, 535, 250, 54), "Anladim, Basla", PLAYER)
        text(self.screen, self.small_font, "ENTER: devam et   T: tekrar goster", (350, 553), MUTED)

    def draw_shop(self):
        self.screen.fill(BG)
        text(self.screen, self.title_font, self.tr("shop"), (84, 75), TARGET)
        text(self.screen, self.body_font, f"Harcanabilir puan: {self.score}", (88, 135), TARGET)
        text(self.screen, self.small_font, "Bir item al veya devam et.", (88, 170), MUTED)
        for index, item in enumerate(SHOP_ITEMS):
            column = index % 2
            row = index // 2
            left = 55 + column * 470
            top = 210 + row * 115
            color = PLAYER if self.score >= item["price"] else GRID
            item_rect = pygame.Rect(left, top, 400, 58)
            self.draw_button(item_rect, f"{index + 1}  {item['name']} - {item['price']}", color)
            if index == self.shop_selection:
                pygame.draw.rect(self.screen, TARGET, item_rect.inflate(8, 8), 3, border_radius=10)
            text(self.screen, self.small_font, item["description"], (left + 4, top + 66), TEXT)
            text(self.screen, self.small_font, f"Alinan: {self.purchased_counts[item['key']]}  Kalan: {self.item_counts[item['key']]}", (left + 4, top + 88), MUTED)
        text(self.screen, self.small_font, f"Kalkan: {self.shields}   Hiz: {self.speed_upgrades}   Tilsim: {int((self.score_multiplier - 1) * 100)}%", (55, 555), MUTED)
        text(self.screen, self.small_font, f"Duvar: {self.wall_breakers}   Sis: {self.mist_bombs}", (55, 578), MUTED)
        self.draw_button(pygame.Rect(84, 540, 220, 52), self.tr("continue"), TARGET)
        text(self.screen, self.small_font, "YUKARI/ASAGI: sec   ENTER: satin al   SPACE: devam", (330, 615), MUTED)

    def draw_difficulty(self):
        self.screen.fill(BG)
        text(self.screen, self.title_font, self.tr("difficulty"), (84, 100), TARGET)
        text(self.screen, self.body_font, "Bir seviye sec ve maceraya basla.", (88, 160), MUTED)
        self.draw_button(pygame.Rect(84, 235, 250, 54), "1  " + self.tr("easy"), PLAYER)
        self.draw_button(pygame.Rect(84, 310, 250, 54), "2  " + self.tr("medium"), TARGET)
        self.draw_button(pygame.Rect(84, 385, 250, 54), "3  " + self.tr("hard"), ENEMY)
        text(self.screen, self.small_font, "ESC: menuye don", (88, 485), MUTED)

    def draw_character(self):
        self.screen.fill(BG)
        text(self.screen, self.title_font, self.tr("character"), (84, 90), TARGET)
        text(self.screen, self.body_font, f"Zorluk: {self.difficulty_name}", (88, 150), MUTED)
        for index, character in enumerate(CHARACTERS):
            left = 90 + index * 400
            panel = pygame.Rect(left, 220, 330, 240)
            pygame.draw.rect(self.screen, PANEL, panel, border_radius=14)
            pygame.draw.rect(self.screen, character["color"], panel, 3, border_radius=14)
            pygame.draw.circle(self.screen, character["color"], (left + 165, 285), 38)
            text(self.screen, self.heading_font, f"{index + 1}  {character['name']}", (left + 35, 345), character["color"])
            text(self.screen, self.small_font, character["description"], (left + 35, 385), TEXT)
            bonus = "Hiz bonusu" if index == 0 else "+1 can, +1 kalkan"
            text(self.screen, self.small_font, bonus, (left + 35, 415), MUTED)
        text(self.screen, self.small_font, "1/2 veya mouse: sec   ESC: geri", (90, 530), MUTED)

    def draw_board(self):
        cell = BOARD_SIZE // self.size
        board_left = 35
        board_top = 55
        pulse = (math.sin(time.time() * 4) + 1) / 2
        level_name = BOSS_LEVEL[0] if self.is_boss else LEVELS[self.level_index][0]
        theme = self.get_theme(level_name)
        board_rect = pygame.Rect(board_left - 10, board_top - 10, cell * self.size + 20, cell * self.size + 20)
        pygame.draw.rect(self.screen, (10, 15, 22), board_rect.move(0, 6), border_radius=14)
        pygame.draw.rect(self.screen, PANEL, board_rect, border_radius=14)
        pygame.draw.rect(self.screen, theme["wall"], board_rect, 2, border_radius=14)
        for y in range(self.size):
            for x in range(self.size):
                rect = pygame.Rect(board_left + x * cell, board_top + y * cell, cell, cell)
                tile_color = theme["tile_alt"] if (x + y) % 2 else theme["tile"]
                pygame.draw.rect(self.screen, tile_color, rect)
                pygame.draw.rect(self.screen, GRID, rect, 1)
                if (x, y) in self.walls:
                    wall_rect = rect.inflate(-10, -10)
                    self.draw_themed_wall(wall_rect, theme, level_name, cell)
                elif (x, y) in self.debris:
                    debris_rect = rect.inflate(-12, -12)
                    pygame.draw.rect(self.screen, (67, 51, 42), debris_rect, border_radius=5)
                    pygame.draw.line(self.screen, DEBRIS, debris_rect.topleft, debris_rect.bottomright, 4)
                    pygame.draw.line(self.screen, DEBRIS, debris_rect.topright, debris_rect.bottomleft, 4)
                    pygame.draw.circle(self.screen, (190, 147, 92), rect.center, max(2, cell // 12))
                elif (x, y) == self.target:
                    pygame.draw.rect(self.screen, (121, 96, 36), rect.inflate(-10, -10), border_radius=12)
                    pygame.draw.rect(self.screen, TARGET, rect.inflate(-18, -18), border_radius=9)
                    glow_size = int(cell * (0.28 + pulse * 0.08))
                    pygame.draw.circle(self.screen, (255, 232, 125), rect.center, glow_size, 2)
                    pygame.draw.polygon(self.screen, (255, 244, 170), [
                        (rect.centerx, rect.top + cell // 4),
                        (rect.right - cell // 4, rect.centery),
                        (rect.centerx, rect.bottom - cell // 4),
                        (rect.left + cell // 4, rect.centery),
                    ], 2)
                elif (x, y) == self.item:
                    pygame.draw.circle(self.screen, (115, 58, 145), rect.center, int(cell * (0.18 + pulse * 0.04)))
                    pygame.draw.polygon(self.screen, ITEM, [
                        (rect.centerx, rect.top + cell // 4),
                        (rect.right - cell // 4, rect.centery),
                        (rect.centerx, rect.bottom - cell // 4),
                        (rect.left + cell // 4, rect.centery),
                    ])
                    pygame.draw.circle(self.screen, (245, 190, 255), rect.center, max(2, cell // 14))
                else:
                    detail_color = tuple(min(255, channel + 20) for channel in tile_color)
                    if theme is THEMES["forest"] and (x + y) % 3 == 0:
                        pygame.draw.line(self.screen, detail_color, (rect.left + 8, rect.bottom - 10), (rect.left + 15, rect.bottom - 15), 2)
                        pygame.draw.line(self.screen, detail_color, (rect.left + 15, rect.bottom - 15), (rect.left + 19, rect.bottom - 9), 2)
                    elif theme is THEMES["ice"] and (x * 3 + y) % 4 == 0:
                        pygame.draw.line(self.screen, detail_color, (rect.centerx - 4, rect.centery), (rect.centerx + 4, rect.centery), 1)
                        pygame.draw.line(self.screen, detail_color, (rect.centerx, rect.centery - 4), (rect.centerx, rect.centery + 4), 1)
                    elif theme is THEMES["desert"] and (x + y * 2) % 4 == 0:
                        pygame.draw.arc(self.screen, detail_color, rect.inflate(-14, -18), 0.2, 2.8, 1)
                    elif theme is THEMES["cave"] and (x * 2 + y) % 5 == 0:
                        pygame.draw.circle(self.screen, detail_color, (rect.right - 11, rect.bottom - 11), 2)
                    elif theme is THEMES["lava"] and (x + y) % 4 == 0:
                        pygame.draw.line(self.screen, (155, 73, 42), (rect.left + 10, rect.bottom - 9), (rect.left + 17, rect.bottom - 13), 2)
                if (x, y) in self.enemies:
                    color = BOSS if self.is_boss else GUARD if (x, y) in self.guard_enemies else ENEMY
                    pygame.draw.ellipse(self.screen, (10, 14, 20), rect.inflate(-cell // 3, -cell // 5).move(0, cell // 5))
                    pygame.draw.circle(self.screen, color, rect.center, cell // 4)
                    if (x, y) in self.guard_enemies:
                        pygame.draw.circle(self.screen, (255, 203, 95), rect.center, int(cell * (0.32 + pulse * 0.04)), 2)
                    pygame.draw.circle(self.screen, (40, 20, 25), (rect.centerx - cell // 10, rect.centery - cell // 14), max(2, cell // 18))
                    pygame.draw.circle(self.screen, (40, 20, 25), (rect.centerx + cell // 10, rect.centery - cell // 14), max(2, cell // 18))
                if (x, y) == self.player:
                    pygame.draw.ellipse(self.screen, (10, 14, 20), rect.inflate(-cell // 3, -cell // 5).move(0, cell // 5))
                    pygame.draw.circle(self.screen, self.character["color"], rect.center, cell // 3)
                    pygame.draw.circle(self.screen, (220, 255, 235), rect.center, cell // 3, 2)
                    if self.item_counts["mist"] > 0:
                        fog_surface = pygame.Surface((cell * 2, cell * 2), pygame.SRCALPHA)
                        fog_center = (cell, cell)
                        pygame.draw.circle(fog_surface, (185, 190, 210, 42), fog_center, int(cell * 0.78))
                        pygame.draw.circle(fog_surface, (215, 220, 235, 72), fog_center, int(cell * 0.58), 3)
                        pygame.draw.circle(fog_surface, (150, 160, 185, 50), (cell // 2, cell), cell // 5)
                        pygame.draw.circle(fog_surface, (150, 160, 185, 50), (cell + cell // 2, cell), cell // 5)
                        self.screen.blit(fog_surface, (rect.left - cell // 2, rect.top - cell // 2))
                    if self.shields > 0:
                        shield_radius = int(cell * (0.43 + pulse * 0.05))
                        shield_rect = pygame.Rect(0, 0, shield_radius * 2, shield_radius * 2)
                        shield_rect.center = rect.center
                        pygame.draw.circle(self.screen, (255, 160, 48), rect.center, shield_radius, 3)
                        pygame.draw.arc(
                            self.screen,
                            (255, 225, 145),
                            shield_rect.inflate(8, 8),
                            time.time() * 3,
                            time.time() * 3 + math.pi * 1.2,
                            3,
                        )
                        pygame.draw.circle(self.screen, (255, 218, 130), rect.center, shield_radius + 5, 1)
        target_rect = pygame.Rect(
            board_left + self.target[0] * cell,
            board_top + self.target[1] * cell,
            cell,
            cell,
        )
        pygame.draw.rect(self.screen, (255, 244, 170), target_rect.inflate(-8, -8), 3, border_radius=10)
        pygame.draw.line(self.screen, TARGET, target_rect.topleft, target_rect.bottomright, 2)
        pygame.draw.line(self.screen, TARGET, target_rect.topright, target_rect.bottomleft, 2)
        text(self.screen, self.small_font, "CIKIS", (target_rect.left + 4, target_rect.top + 4), (255, 255, 210))
        text(self.screen, self.small_font, "P oyuncu   H hedef   I item   E/B dusman   X enkaz", (35, 665), MUTED)

    def get_theme(self, level_name):
        name = level_name.lower()
        if "orman" in name or "vadi" in name or "kayalik" in name:
            return THEMES["forest"]
        if "magara" in name or "golge" in name:
            return THEMES["cave"]
        if "col" in name:
            return THEMES["desert"]
        if "buz" in name or "kristal" in name:
            return THEMES["ice"]
        if "lav" in name or "firtina" in name:
            return THEMES["lava"]
        if "sehir" in name or "kapilar" in name:
            return THEMES["city"]
        if "tapinak" in name or "kalen" in name:
            return THEMES["temple"]
        return THEMES["default"]

    def get_music_theme(self, level_name):
        name = level_name.lower()
        if "orman" in name or "vadi" in name or "kayalik" in name:
            return "forest"
        if "magara" in name or "golge" in name:
            return "cave"
        if "col" in name:
            return "desert"
        if "buz" in name or "kristal" in name:
            return "ice"
        if "lav" in name or "firtina" in name:
            return "lava"
        if "sehir" in name or "kapilar" in name:
            return "city"
        if "tapinak" in name or "kalen" in name:
            return "temple"
        return "normal"

    def draw_themed_wall(self, wall_rect, theme, level_name, cell):
        name = level_name.lower()
        pygame.draw.rect(self.screen, theme["wall"], wall_rect, border_radius=6)
        if "orman" in name or "vadi" in name or "kayalik" in name:
            pygame.draw.rect(self.screen, (91, 54, 31), wall_rect.inflate(-cell // 3, -cell // 4), border_radius=4)
            pygame.draw.circle(self.screen, (38, 133, 64), (wall_rect.centerx, wall_rect.top + cell // 5), cell // 4)
            pygame.draw.circle(self.screen, (52, 164, 74), (wall_rect.centerx - cell // 6, wall_rect.top + cell // 4), cell // 6)
        elif "magara" in name or "golge" in name:
            pygame.draw.polygon(self.screen, (155, 158, 181), [wall_rect.midtop, wall_rect.topright, wall_rect.midbottom, wall_rect.bottomleft])
            pygame.draw.line(self.screen, (65, 67, 88), wall_rect.midtop, wall_rect.midbottom, 3)
        elif "buz" in name or "kristal" in name:
            pygame.draw.polygon(self.screen, (190, 248, 255), [wall_rect.midbottom, wall_rect.midtop, wall_rect.topright, wall_rect.bottomright])
        elif "lav" in name or "firtina" in name:
            pygame.draw.line(self.screen, (244, 104, 42), wall_rect.midleft, wall_rect.midright, 3)
            pygame.draw.line(self.screen, (193, 52, 30), wall_rect.topleft, wall_rect.bottomright, 3)
        elif "sehir" in name or "kapilar" in name:
            pygame.draw.line(self.screen, (205, 210, 220), wall_rect.midleft, wall_rect.midright, 2)
            pygame.draw.line(self.screen, (205, 210, 220), wall_rect.midtop, wall_rect.midbottom, 2)
        else:
            pygame.draw.line(self.screen, (220, 180, 115), wall_rect.topleft, wall_rect.topright, 2)

    def draw_playing(self):
        name = BOSS_LEVEL[0] if self.is_boss else LEVELS[self.level_index][0]
        theme = self.get_theme(name)
        self.screen.fill(theme["background"])
        prefix = "BOSS: " if self.is_boss else f"BOLUM {self.level_index + 1}: "
        text(self.screen, self.heading_font, prefix + name, (35, 15), BOSS if self.is_boss else theme["wall"])
        self.draw_board()
        pygame.draw.rect(self.screen, PANEL, (PANEL_X, 0, WIDTH - PANEL_X, HEIGHT))
        text(self.screen, self.heading_font, "DURUM", (690, 55), TARGET)
        progress = len(LEVELS) + 1 if self.is_boss else self.level_index + 1
        text(self.screen, self.body_font, f"Ilerleme: {progress}/{len(LEVELS) + 1}", (690, 85), TEXT)
        max_health = self.max_health
        text(self.screen, self.body_font, f"Zorluk: {self.difficulty_name}", (690, 125), TARGET)
        text(self.screen, self.body_font, f"Can: {self.health}/{max_health}", (690, 160), ENEMY)
        text(self.screen, self.body_font, f"Puan: {self.score}", (690, 195), TARGET)
        text(self.screen, self.body_font, f"Kalkan: {self.shields}", (690, 230), PLAYER)
        elapsed = self.level_elapsed()
        text(self.screen, self.body_font, f"Sure: {elapsed:05.1f} sn", (690, 265), TEXT)
        text(self.screen, self.small_font, f"Hiz bonusu: +{self.time_bonus()} puan", (690, 300), TARGET)
        pygame.draw.line(self.screen, GRID, (685, 325), (955, 325), 1)
        text(self.screen, self.small_font, "ENVANTER", (690, 338), ITEM)
        text(self.screen, self.small_font, f"Can iksiri: {self.item_counts['health']} (H)", (690, 365), TEXT)
        text(self.screen, self.small_font, f"Kalkan: {self.item_counts['shield']}  Duvar: {self.item_counts['wall']}", (690, 390), MUTED)
        text(self.screen, self.small_font, f"Sis: {self.item_counts['mist']}  Tilsim: {self.item_counts['score']}", (690, 415), MUTED)
        text(self.screen, self.small_font, f"Hiz: {self.item_counts['speed']}", (690, 440), MUTED)
        pygame.draw.line(self.screen, GRID, (685, 465), (955, 465), 1)
        text(self.screen, self.small_font, "WASD hareket   P duraklat", (690, 480), PLAYER)
        text(self.screen, self.small_font, "ESC menuye don", (690, 505), MUTED)
        progress_width = 230
        progress = (self.level_index + (1 if self.is_boss else 0)) / (len(LEVELS) + 1)
        pygame.draw.rect(self.screen, GRID, (690, 550, progress_width, 10), border_radius=5)
        pygame.draw.rect(self.screen, PLAYER, (690, 550, int(progress_width * progress), 10), border_radius=5)
        if self.is_boss:
            text(self.screen, self.small_font, "Boss seni takip ediyor!", (690, 580), BOSS)

    def draw_countdown(self):
        self.draw_playing()
        elapsed = time.time() - self.countdown_started
        remaining = max(1, 3 - int(elapsed))
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((5, 8, 12, 150))
        self.screen.blit(overlay, (0, 0))
        text(self.screen, self.title_font, str(remaining), (475, 245), TARGET)
        text(self.screen, self.body_font, "Hazir ol...", (440, 320), TEXT)

    def draw_pause(self):
        self.draw_playing()
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((5, 8, 12, 190))
        self.screen.blit(overlay, (0, 0))
        text(self.screen, self.title_font, "DURAKLATILDI", (330, 270), TARGET)
        text(self.screen, self.body_font, "P: devam et    ESC: menu", (350, 330), TEXT)

    def draw_summary(self, game_over=False):
        self.screen.fill(BG)
        heading = "OYUN BITTI" if game_over else "ZAFER!"
        color = ENEMY if game_over else PLAYER
        text(self.screen, self.title_font, heading, (90, 70), color)
        text(self.screen, self.body_font, f"Final puani: {self.score}", (95, 150), TARGET)
        text(self.screen, self.body_font, f"Zorluk: {self.difficulty_name}", (95, 185), MUTED)
        text(self.screen, self.body_font, f"Rekor: {self.high_score}", (95, 215), TARGET)
        total = self.total_elapsed()
        text(self.screen, self.body_font, f"Toplam sure: {total:.1f} sn", (95, 250), TEXT)
        text(self.screen, self.heading_font, "SEFER ISTATISTIKLERI", (500, 145), TARGET)
        text(self.screen, self.small_font, f"Tamamlanan bolum: {self.completed_levels}/{len(LEVELS) + 1}", (505, 190), TEXT)
        text(self.screen, self.small_font, f"Toplanan item: {self.collected_items}", (505, 220), TEXT)
        text(self.screen, self.small_font, f"Alinan hasar: {self.damage_taken}", (505, 250), TEXT)
        badge = "HIZ USTASI" if self.level_times and min(time_value for _, time_value in self.level_times) < 12 else "LABIRENT KASIFI"
        text(self.screen, self.small_font, f"Rozet: {badge}", (505, 280), PLAYER)
        y = 310
        for name, elapsed in self.level_times[-8:]:
            text(self.screen, self.small_font, f"{name}: {elapsed:.1f} sn", (100, y), MUTED)
            y += 27
        self.draw_button(pygame.Rect(95, 540, 210, 52), "Tekrar Oyna", PLAYER)
        self.draw_button(pygame.Rect(325, 540, 170, 52), "Menu", GRID)

    def run(self):
        while True:
            dt = self.clock.tick(FPS) / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if self.state == "menu":
                        if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                            self.state = "difficulty"
                        elif event.key == pygame.K_t:
                            self.state = "tutorial"
                        elif event.key == pygame.K_o:
                            self.state = "settings"
                        elif event.key == pygame.K_ESCAPE:
                            pygame.quit()
                            return
                    elif self.state == "tutorial":
                        if event.key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_t):
                            self.finish_tutorial()
                        elif event.key == pygame.K_ESCAPE:
                            self.finish_tutorial()
                    elif self.state == "settings":
                        if event.key == pygame.K_m:
                            self.toggle_music()
                        elif event.key == pygame.K_l:
                            self.toggle_language()
                        elif event.key == pygame.K_LEFT:
                            self.change_volume("music_volume", -0.05)
                        elif event.key == pygame.K_RIGHT:
                            self.change_volume("music_volume", 0.05)
                        elif event.key == pygame.K_DOWN:
                            self.change_volume("effects_volume", -0.05)
                        elif event.key == pygame.K_UP:
                            self.change_volume("effects_volume", 0.05)
                        elif event.key == pygame.K_ESCAPE:
                            self.state = "menu"
                    elif self.state == "difficulty":
                        if event.key == pygame.K_1:
                            self.choose_difficulty("Kolay")
                        elif event.key == pygame.K_2:
                            self.choose_difficulty("Orta")
                        elif event.key == pygame.K_3:
                            self.choose_difficulty("Zor")
                        elif event.key == pygame.K_ESCAPE:
                            self.stop_music()
                            self.state = "menu"
                    elif self.state == "character":
                        if event.key == pygame.K_1:
                            self.choose_character(0)
                        elif event.key == pygame.K_2:
                            self.choose_character(1)
                        elif event.key == pygame.K_ESCAPE:
                            self.state = "difficulty"
                    elif self.state == "countdown":
                        if event.key == pygame.K_ESCAPE:
                            self.stop_music()
                            self.state = "menu"
                    elif self.state == "shop":
                        if event.key == pygame.K_UP:
                            self.shop_selection = (self.shop_selection - 1) % len(SHOP_ITEMS)
                        elif event.key == pygame.K_DOWN:
                            self.shop_selection = (self.shop_selection + 1) % len(SHOP_ITEMS)
                        elif event.key == pygame.K_RETURN:
                            self.buy_item(self.shop_selection)
                        elif event.key == pygame.K_SPACE:
                            self.continue_from_shop()
                        if event.key == pygame.K_1:
                            self.buy_item(0)
                        elif event.key == pygame.K_2:
                            self.buy_item(1)
                        elif event.key == pygame.K_3:
                            self.buy_item(2)
                        elif event.key == pygame.K_ESCAPE:
                            self.stop_music()
                            self.state = "menu"
                    elif self.state == "playing":
                        if event.key == pygame.K_w:
                            self.move_player(0, -1)
                        elif event.key == pygame.K_a:
                            self.move_player(-1, 0)
                        elif event.key == pygame.K_s:
                            self.move_player(0, 1)
                        elif event.key == pygame.K_d:
                            self.move_player(1, 0)
                        elif event.key == pygame.K_h:
                            self.use_health_potion()
                        elif event.key == pygame.K_p:
                            self.pause_game()
                        elif event.key == pygame.K_ESCAPE:
                            self.state = "menu"
                    elif self.state == "paused":
                        if event.key == pygame.K_p:
                            self.resume_game()
                        elif event.key == pygame.K_ESCAPE:
                            self.state = "menu"
                    elif self.state in ("summary", "gameover"):
                        if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                            self.start_game()
                        elif event.key == pygame.K_ESCAPE:
                            self.state = "menu"
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.state == "tutorial":
                        if pygame.Rect(75, 535, 250, 54).collidepoint(event.pos):
                            self.finish_tutorial()
                    elif self.state == "settings":
                        if pygame.Rect(570, 225, 230, 52).collidepoint(event.pos):
                            self.toggle_music()
                        elif pygame.Rect(570, 325, 105, 52).collidepoint(event.pos):
                            self.change_volume("music_volume", -0.05)
                        elif pygame.Rect(695, 325, 105, 52).collidepoint(event.pos):
                            self.change_volume("music_volume", 0.05)
                        elif pygame.Rect(570, 415, 105, 52).collidepoint(event.pos):
                            self.change_volume("effects_volume", -0.05)
                        elif pygame.Rect(695, 415, 105, 52).collidepoint(event.pos):
                            self.change_volume("effects_volume", 0.05)
                        elif pygame.Rect(470, 485, 145, 42).collidepoint(event.pos):
                            self.set_language("tr")
                        elif pygame.Rect(625, 485, 145, 42).collidepoint(event.pos):
                            self.set_language("en")
                        elif pygame.Rect(150, 550, 220, 42).collidepoint(event.pos):
                            self.state = "menu"
                    elif self.state == "menu":
                        if pygame.Rect(105, 465, 300, 54).collidepoint(event.pos):
                            self.state = "difficulty"
                        elif pygame.Rect(430, 465, 220, 54).collidepoint(event.pos):
                            pygame.quit()
                            return
                        elif pygame.Rect(675, 465, 185, 54).collidepoint(event.pos):
                            self.state = "settings"
                    elif self.state == "difficulty":
                        if pygame.Rect(84, 235, 250, 54).collidepoint(event.pos):
                            self.choose_difficulty("Kolay")
                        elif pygame.Rect(84, 310, 250, 54).collidepoint(event.pos):
                            self.choose_difficulty("Orta")
                        elif pygame.Rect(84, 385, 250, 54).collidepoint(event.pos):
                            self.choose_difficulty("Zor")
                    elif self.state == "character":
                        if pygame.Rect(90, 220, 330, 240).collidepoint(event.pos):
                            self.choose_character(0)
                        elif pygame.Rect(490, 220, 330, 240).collidepoint(event.pos):
                            self.choose_character(1)
                    elif self.state == "shop":
                        for index in range(len(SHOP_ITEMS)):
                            column = index % 2
                            row = index // 2
                            item_rect = pygame.Rect(55 + column * 470, 210 + row * 115, 400, 58)
                            if item_rect.collidepoint(event.pos):
                                self.shop_selection = index
                                self.buy_item(index)
                                break
                        if pygame.Rect(84, 540, 220, 52).collidepoint(event.pos):
                            self.continue_from_shop()
                    elif self.state in ("summary", "gameover"):
                        if pygame.Rect(95, 540, 210, 52).collidepoint(event.pos):
                            self.start_game()
                        elif pygame.Rect(325, 540, 170, 52).collidepoint(event.pos):
                            self.state = "menu"
            self.update_countdown()
            self.move_enemy(dt)
            if self.state == "tutorial":
                self.draw_tutorial()
            elif self.state == "settings":
                self.draw_settings()
            elif self.state == "menu":
                self.draw_menu()
            elif self.state == "difficulty":
                self.draw_difficulty()
            elif self.state == "character":
                self.draw_character()
            elif self.state == "countdown":
                self.draw_countdown()
            elif self.state == "shop":
                self.draw_shop()
            elif self.state == "playing":
                self.draw_playing()
            elif self.state == "paused":
                self.draw_pause()
            else:
                self.draw_summary(self.state == "gameover")
            pygame.display.flip()


def main():
    Game().run()


if __name__ == "__main__":
    main()
