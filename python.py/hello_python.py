import time
import random

RENK_SIFIRLA = "\033[0m"
RENK_MAVI = "\033[94m"
RENK_YESIL = "\033[92m"
RENK_SARI = "\033[93m"
RENK_KIRMIZI = "\033[91m"
RENK_MAGENTA = "\033[95m"
RENK_GRI = "\033[90m"


def renkli(metin, renk):
    return f"{renk}{metin}{RENK_SIFIRLA}"


def oyun():
    print(renkli("╔══════════════════════════╗", RENK_MAVI))
    print(renkli("║      LABİRENT MACERASI  ║", RENK_MAVI))
    print(renkli("╚══════════════════════════╝", RENK_MAVI))
    print(renkli("[1] Başla", RENK_YESIL))
    print(renkli("[2] Çıkış", RENK_KIRMIZI))
    secim = input(renkli("Seçiminiz: ", RENK_SARI)).strip()

    if secim == "2":
        print("Oyundan çıktın.")
        return

    if secim != "1":
        print("Geçersiz seçim! Lütfen 1 veya 2 girin.")
        return

    can = 3
    puan = 0
    bolumler = [
        {"isim": "Bölüm 1: Giriş", "hedef": (2, 2), "engeller": {(1, 1), (2, 1), (1, 2)}, "boyut": 4},
        {"isim": "Bölüm 2: Orman", "hedef": (3, 3), "engeller": {(1, 0), (2, 1), (1, 2), (2, 3)}, "boyut": 5},
        {"isim": "Bölüm 3: Mağara", "hedef": (4, 0), "engeller": {(1, 1), (2, 2), (3, 2), (1, 3)}, "boyut": 5},
        {"isim": "Bölüm 4: Dağ", "hedef": (0, 4), "engeller": {(1, 1), (2, 1), (2, 3), (3, 3)}, "boyut": 5},
        {"isim": "Bölüm 5: Vadi", "hedef": (4, 4), "engeller": {(0, 2), (2, 2), (3, 1), (3, 3)}, "boyut": 5},
        {"isim": "Bölüm 6: Nehir", "hedef": (3, 0), "engeller": {(0, 1), (1, 1), (2, 2), (3, 3)}, "boyut": 5},
        {"isim": "Bölüm 7: Kayalık", "hedef": (4, 3), "engeller": {(1, 2), (2, 2), (3, 1), (1, 4)}, "boyut": 5},
        {"isim": "Bölüm 8: Çöl", "hedef": (2, 4), "engeller": {(1, 1), (2, 1), (3, 2), (1, 3)}, "boyut": 5},
        {"isim": "Bölüm 9: Orman Kalesi", "hedef": (4, 4), "engeller": {(0, 1), (1, 1), (2, 2), (3, 2), (2, 3)}, "boyut": 6},
        {"isim": "Bölüm 10: Son Sınav", "hedef": (5, 5), "engeller": {(1, 0), (2, 1), (3, 2), (2, 4), (4, 3)}, "boyut": 6}
    ]

    boss_bolum = {
        "isim": "Boss: Karanlık Efendi",
        "hedef": (4, 4),
        "engeller": {(0, 2), (1, 2), (2, 1), (2, 3), (3, 2), (4, 1), (4, 3)},
        "boyut": 6,
    }

    print(renkli("10 bölümlük oyun başlıyor!", RENK_YESIL))
    print(renkli("Kontroller: W = yukarı, A = sol, S = aşağı, D = sağ, Q = çıkış", RENK_GRI))
    print(f"{renkli('Can', RENK_KIRMIZI)}: {can} | {renkli('Puan', RENK_SARI)}: {puan}")

    toplam_baslangic_zamani = time.time()
    bolum_sureleri = []

    for indeks, bolum in enumerate(bolumler, start=1):
        boyut = bolum["boyut"]
        player_x, player_y = 0, 0
        hedef_x, hedef_y = bolum["hedef"]
        engeller = bolum["engeller"]
        baslama_zamani = time.time()

        item_x = random.randint(0, boyut - 1)
        item_y = random.randint(0, boyut - 1)
        while (item_x, item_y) in engeller or (item_x, item_y) == (player_x, player_y) or (item_x, item_y) == (hedef_x, hedef_y):
            item_x = random.randint(0, boyut - 1)
            item_y = random.randint(0, boyut - 1)

        enemy_x = random.randint(0, boyut - 1)
        enemy_y = random.randint(0, boyut - 1)
        while (enemy_x, enemy_y) in engeller or (enemy_x, enemy_y) == (player_x, player_y) or (enemy_x, enemy_y) == (hedef_x, hedef_y) or (enemy_x, enemy_y) == (item_x, item_y):
            enemy_x = random.randint(0, boyut - 1)
            enemy_y = random.randint(0, boyut - 1)

        print("\n" + renkli("═" * 30, RENK_MAVI))
        print(renkli(bolum["isim"], RENK_MAVI))
        print(renkli("═" * 30, RENK_MAVI))

        def harita_yazdir():
            for y in range(boyut):
                satir = []
                for x in range(boyut):
                    if (x, y) == (player_x, player_y):
                        satir.append(renkli("P", RENK_YESIL))
                    elif (x, y) == (hedef_x, hedef_y):
                        satir.append(renkli("H", RENK_SARI))
                    elif (x, y) == (item_x, item_y):
                        satir.append(renkli("I", RENK_MAGENTA))
                    elif (x, y) == (enemy_x, enemy_y):
                        satir.append(renkli("E", RENK_KIRMIZI))
                    elif (x, y) in engeller:
                        satir.append(renkli("#", RENK_GRI))
                    else:
                        satir.append(renkli("·", RENK_GRI))
                print(" ".join(satir))
            print()

        while True:
            harita_yazdir()
            print(f"{renkli('Can', RENK_KIRMIZI)}: {can} | {renkli('Puan', RENK_SARI)}: {puan}")
            hareket = input(renkli("Hamle girin: ", RENK_SARI)).lower()

            if hareket == "q":
                print("Oyundan çıktın.")
                return

            if hareket not in ["w", "a", "s", "d"]:
                print("Geçersiz tuş! W, A, S, D veya Q kullanın.")
                can -= 1
                print(f"Can kaybettin! Kalan can: {can}")
                if can <= 0:
                    print("Canın bitti! Oyun bitti.")
                    print("\n1. Tekrar Oyna")
                    print("2. Çıkış")
                    tekrar = input("Seçiminiz: ").strip()
                    if tekrar == "1":
                        oyun()
                    return
                continue

            yeni_x, yeni_y = player_x, player_y
            if hareket == "w":
                yeni_y -= 1
            elif hareket == "a":
                yeni_x -= 1
            elif hareket == "s":
                yeni_y += 1
            elif hareket == "d":
                yeni_x += 1

            if not (0 <= yeni_x < boyut and 0 <= yeni_y < boyut):
                print("Duvarın dışında kalamazsın!")
                can -= 1
                print(f"Can kaybettin! Kalan can: {can}")
                if can <= 0:
                    print("Canın bitti! Oyun bitti.")
                    print("\n1. Tekrar Oyna")
                    print("2. Çıkış")
                    tekrar = input("Seçiminiz: ").strip()
                    if tekrar == "1":
                        oyun()
                    return
                continue

            if (yeni_x, yeni_y) in engeller:
                print("Bu karede engel var!")
                can -= 1
                print(f"Can kaybettin! Kalan can: {can}")
                if can <= 0:
                    print("Canın bitti! Oyun bitti.")
                    print("\n1. Tekrar Oyna")
                    print("2. Çıkış")
                    tekrar = input("Seçiminiz: ").strip()
                    if tekrar == "1":
                        oyun()
                    return
                continue

            player_x, player_y = yeni_x, yeni_y

            if (player_x, player_y) == (item_x, item_y):
                puan += 50
                print("İtem topladın! +50 puan")
                item_x, item_y = -1, -1

            enemy_nx, enemy_ny = enemy_x, enemy_y
            dusman_mesafesi = abs(player_x - enemy_x) + abs(player_y - enemy_y)
            if dusman_mesafesi <= 4:
                if player_x != enemy_x:
                    enemy_nx += 1 if player_x > enemy_x else -1
                elif player_y != enemy_y:
                    enemy_ny += 1 if player_y > enemy_y else -1
            else:
                gemi = random.choice(["w", "a", "s", "d"])
                if gemi == "w":
                    enemy_ny -= 1
                elif gemi == "a":
                    enemy_nx -= 1
                elif gemi == "s":
                    enemy_ny += 1
                elif gemi == "d":
                    enemy_nx += 1

            if 0 <= enemy_nx < boyut and 0 <= enemy_ny < boyut and (enemy_nx, enemy_ny) not in engeller and (enemy_nx, enemy_ny) != (hedef_x, hedef_y):
                enemy_x, enemy_y = enemy_nx, enemy_ny

            if (player_x, player_y) == (enemy_x, enemy_y):
                can -= 1
                print("Düşmana çarptın! Can kaybettin.")
                print(f"Kalan can: {can}")
                if can <= 0:
                    print("Canın bitti! Oyun bitti.")
                    print("\n1. Tekrar Oyna")
                    print("2. Çıkış")
                    tekrar = input("Seçiminiz: ").strip()
                    if tekrar == "1":
                        oyun()
                    return

            if (player_x, player_y) == (hedef_x, hedef_y):
                gecen_sure = time.time() - baslama_zamani
                bolum_sureleri.append((bolum["isim"], gecen_sure))
                puan += 100
                print(f"{bolum['isim']} tamamlandı! 🎉")
                print(f"Bu bölümü {gecen_sure:.2f} saniyede bitirdin.")
                print(f"Puan: {puan}")
                break

            print(f"Yeni konum: x={player_x}, y={player_y}")

    son_toplam_sure = time.time() - toplam_baslangic_zamani

    print("\n" + renkli("╔══════════════════════════╗", RENK_KIRMIZI))
    print(renkli("║       BOSS BÖLÜMÜ        ║", RENK_KIRMIZI))
    print(renkli("╚══════════════════════════╝", RENK_KIRMIZI))
    boyut = boss_bolum["boyut"]
    player_x, player_y = 0, 0
    hedef_x, hedef_y = boss_bolum["hedef"]
    engeller = boss_bolum["engeller"]
    boss_baslama_zamani = time.time()

    item_x = random.randint(0, boyut - 1)
    item_y = random.randint(0, boyut - 1)
    while (item_x, item_y) in engeller or (item_x, item_y) == (player_x, player_y) or (item_x, item_y) == (hedef_x, hedef_y):
        item_x = random.randint(0, boyut - 1)
        item_y = random.randint(0, boyut - 1)

    boss_x = 5
    boss_y = 0
    while (boss_x, boss_y) in engeller or (boss_x, boss_y) == (player_x, player_y) or (boss_x, boss_y) == (hedef_x, hedef_y):
        boss_x = random.randint(0, boyut - 1)
        boss_y = random.randint(0, boyut - 1)

    def harita_yazdir_boss():
        for y in range(boyut):
            satir = []
            for x in range(boyut):
                if (x, y) == (player_x, player_y):
                    satir.append(renkli("P", RENK_YESIL))
                elif (x, y) == (hedef_x, hedef_y):
                    satir.append(renkli("H", RENK_SARI))
                elif (x, y) == (item_x, item_y):
                    satir.append(renkli("I", RENK_MAGENTA))
                elif (x, y) == (boss_x, boss_y):
                    satir.append(renkli("B", RENK_KIRMIZI))
                elif (x, y) in engeller:
                    satir.append(renkli("#", RENK_GRI))
                else:
                    satir.append(renkli("·", RENK_GRI))
            print(" ".join(satir))
        print()

    while True:
        harita_yazdir_boss()
        print(f"{renkli('Can', RENK_KIRMIZI)}: {can} | {renkli('Puan', RENK_SARI)}: {puan}")
        hareket = input(renkli("Boss bölümünde hamle girin: ", RENK_SARI)).lower()

        if hareket == "q":
            print("Oyundan çıktın.")
            return

        if hareket not in ["w", "a", "s", "d"]:
            print("Geçersiz tuş! W, A, S, D veya Q kullanın.")
            can -= 1
            print(f"Can kaybettin! Kalan can: {can}")
            if can <= 0:
                print("Canın bitti! Oyun bitti.")
                print("\n1. Tekrar Oyna")
                print("2. Çıkış")
                tekrar = input("Seçiminiz: ").strip()
                if tekrar == "1":
                    oyun()
                return
            continue

        yeni_x, yeni_y = player_x, player_y
        if hareket == "w":
            yeni_y -= 1
        elif hareket == "a":
            yeni_x -= 1
        elif hareket == "s":
            yeni_y += 1
        elif hareket == "d":
            yeni_x += 1

        if not (0 <= yeni_x < boyut and 0 <= yeni_y < boyut):
            print("Sınır dışına çıkamazsın!")
            can -= 1
            print(f"Can kaybettin! Kalan can: {can}")
            if can <= 0:
                print("Canın bitti! Oyun bitti.")
                print("\n1. Tekrar Oyna")
                print("2. Çıkış")
                tekrar = input("Seçiminiz: ").strip()
                if tekrar == "1":
                    oyun()
                return
            continue

        if (yeni_x, yeni_y) in engeller:
            print("Engel var, ilerleyemezsin!")
            can -= 1
            print(f"Can kaybettin! Kalan can: {can}")
            if can <= 0:
                print("Canın bitti! Oyun bitti.")
                print("\n1. Tekrar Oyna")
                print("2. Çıkış")
                tekrar = input("Seçiminiz: ").strip()
                if tekrar == "1":
                    oyun()
                return
            continue

        player_x, player_y = yeni_x, yeni_y

        if (player_x, player_y) == (item_x, item_y):
            puan += 75
            print("Boss bölümünde özel item topladın! +75 puan")
            item_x, item_y = -1, -1

        mesafe = abs(player_x - boss_x) + abs(player_y - boss_y)
        if mesafe <= 3:
            if player_x != boss_x:
                boss_x += 1 if player_x > boss_x else -1
            elif player_y != boss_y:
                boss_y += 1 if player_y > boss_y else -1
        else:
            hamleler = ["w", "a", "s", "d"]
            hareket_boss = random.choice(hamleler)
            bx, by = boss_x, boss_y
            if hareket_boss == "w":
                by -= 1
            elif hareket_boss == "a":
                bx -= 1
            elif hareket_boss == "s":
                by += 1
            elif hareket_boss == "d":
                bx += 1

            if 0 <= bx < boyut and 0 <= by < boyut and (bx, by) not in engeller and (bx, by) != (hedef_x, hedef_y):
                boss_x, boss_y = bx, by

        if (player_x, player_y) == (boss_x, boss_y):
            can -= 1
            print("Boss sana yetişti! Can kaybettin.")
            print(f"Kalan can: {can}")
            if can <= 0:
                print("Canın bitti! Oyun bitti.")
                print("\n1. Tekrar Oyna")
                print("2. Çıkış")
                tekrar = input("Seçiminiz: ").strip()
                if tekrar == "1":
                    oyun()
                return

        if (player_x, player_y) == (hedef_x, hedef_y):
            gecen_sure = time.time() - boss_baslama_zamani
            bolum_sureleri.append((boss_bolum["isim"], gecen_sure))
            puan += 250
            print("Boss bölümü tamamlandı! 🎉")
            print(f"Boss'u {gecen_sure:.2f} saniyede yendin.")
            print(f"Toplam puan: {puan}")
            break

    son_toplam_sure = time.time() - toplam_baslangic_zamani

    print("\n=== Oyun Özeti ===")
    for isim, sure in bolum_sureleri:
        print(f"{isim}: {sure:.2f} saniye")
    print(f"Toplam süre: {son_toplam_sure:.2f} saniye")
    print(f"Final puanı: {puan}")

    if bolum_sureleri:
        en_hizli = min(sure for _, sure in bolum_sureleri)
        print(f"En hızlı bölüm: {en_hizli:.2f} saniye")

    print("\nTüm bölümler tamamlandı! Tebrikler!")

    print("\n1. Tekrar Oyna")
    print("2. Çıkış")
    tekrar = input("Seçiminiz: ").strip()

    if tekrar == "1":
        oyun()
    else:
        print("Başka oyunlarda görüşürüz!")

if __name__ == "__main__":
    from pygame_labirent import Game

    Game().run()