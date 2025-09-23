# blackjack_ui.py
# Blackjack con UI moderna en pygame
# - Mensajes centrados (fase/turno/ganador) con banner
# - set_fonts(scale) para ajustar tamaños de texto
# - Turnos garantizados: ambos jugadores pueden Hit/Stand
# - Nombres, apuestas por input, botón Salir, Nueva ronda / Jugar de nuevo

import random, pygame
from typing import List, Tuple, Dict

# ------------------------------
# LÓGICA DEL JUEGO
# ------------------------------
SUITS = ["♠", "♥", "♦", "♣"]
RANKS = ["A","2","3","4","5","6","7","8","9","10","J","Q","K"]
VALUES: Dict[str,int] = {"A":11,"2":2,"3":3,"4":4,"5":5,"6":6,"7":7,"8":8,"9":9,"10":10,"J":10,"Q":10,"K":10}
Card = Tuple[str,str]

def build_deck() -> List[Card]:
    return [(r,s) for s in SUITS for r in RANKS]

def shuffle_deck(deck: List[Card]) -> None:
    random.shuffle(deck)

def deal_card(deck: List[Card]) -> Card:
    if not deck:
        deck.extend(build_deck()); shuffle_deck(deck)
    return deck.pop()

def hand_value(hand: List[Card]) -> int:
    total = sum(VALUES[r] for r,_ in hand)
    aces = sum(1 for r,_ in hand if r=="A")
    while total>21 and aces:
        total -= 10; aces -= 1
    return total

def resolve_round(j1: str, h1: List[Card], j2: str, h2: List[Card]) -> str:
    v1, v2 = hand_value(h1), hand_value(h2)
    if v1>21 and v2>21: return "draw"
    if v1>21: return j2
    if v2>21: return j1
    if v1>v2: return j1
    if v2>v1: return j2
    return "draw"

def apply_payments(credits: Dict[str,int], bets: Dict[str,int], result: str) -> str:
    if result=="draw": return "Empate: se devuelven las apuestas."
    loser = [j for j in credits if j!=result][0]
    pot = bets[result] + bets[loser]
    credits[result] += pot
    credits[loser]  -= bets[loser]
    return f"{result} gana {pot} créditos."

# ------------------------------
# PYGAME — UI BASICS
# ------------------------------
pygame.init()
W,H = 1280, 720
screen = pygame.display.set_mode((W,H))
pygame.display.set_caption("Blackjack — UI")

# Paleta
C_BG1 = (7, 66, 46)
C_BG2 = (24,120,84)
C_TEXT = (240,240,240)
C_ACCENT = (255,206,84)
C_DANGER = (244,88,88)
C_BTN = (28,28,33)
C_BTN_H = (40,40,48)
C_BTN_P = (18,18,22)
C_PANEL = (16,16,18)

# Fuentes (ajústalas con set_fonts() más abajo)
FONT      = pygame.font.SysFont("arial", 20)
FONT_MED  = pygame.font.SysFont("arial", 22, bold=True)
FONT_BIG  = pygame.font.SysFont("arial", 40, bold=True)
FONT_CARD = pygame.font.SysFont("arial", 30, bold=True)
FONT_PIP  = pygame.font.SysFont("arial", 64, bold=True)
FONT_HUGE = pygame.font.SysFont("arial", 56, bold=True)  # banner

def set_fonts(scale: float = 1.0):
    """Ajusta TODOS los tamaños de texto a la vez (1.0 = por defecto)."""
    global FONT, FONT_MED, FONT_BIG, FONT_CARD, FONT_PIP, FONT_HUGE
    FONT      = pygame.font.SysFont("arial", int(20*scale))
    FONT_MED  = pygame.font.SysFont("arial", int(22*scale), bold=True)
    FONT_BIG  = pygame.font.SysFont("arial", int(40*scale), bold=True)
    FONT_CARD = pygame.font.SysFont("arial", int(30*scale), bold=True)
    FONT_PIP  = pygame.font.SysFont("arial", int(64*scale), bold=True)
    FONT_HUGE = pygame.font.SysFont("arial", int(46*scale), bold=True)

# Cambia este factor si quieres subir/bajar todos los textos:
SCALE_FONTS = 1.0
set_fonts(SCALE_FONTS)

CARD_SIZE = (110, 160)
CARD_W, CARD_H = CARD_SIZE

def draw_vertical_gradient(surf, rect, top_color, bottom_color):
    x,y,w,h = rect
    for i in range(h):
        t = i/max(1,h-1)
        col = (
            int(top_color[0]*(1-t)+bottom_color[0]*t),
            int(top_color[1]*(1-t)+bottom_color[1]*t),
            int(top_color[2]*(1-t)+bottom_color[2]*t)
        )
        pygame.draw.line(surf, col, (x, y+i), (x+w, y+i))

def rounded_rect(surf, rect, color, radius=18, width=0):
    pygame.draw.rect(surf, color, rect, width, border_radius=radius)

def shadow_rect(surf, rect, radius=18, blur=10, color=(0,0,0,160)):
    r = pygame.Rect(rect).inflate(blur*2, blur*2)
    sh = pygame.Surface(r.size, pygame.SRCALPHA)
    pygame.draw.rect(sh, color, (blur,blur, r.w-2*blur, r.h-2*blur), border_radius=radius)
    surf.blit(sh, (r.x, r.y))

def suit_color(s:str):
    return (220,50,50) if s in ("♥","♦") else (22,22,22)

def draw_card_surface(card: Card, size=CARD_SIZE) -> pygame.Surface:
    r,s = card
    w,h = size
    surf = pygame.Surface((w,h), pygame.SRCALPHA)
    rounded_rect(surf, (0,0,w,h), (247,247,247), radius=14)
    pygame.draw.rect(surf, (210,210,210), (0,0,w,h), 2, border_radius=14)
    idx = FONT_CARD.render(r, True, suit_color(s))
    pip = FONT_CARD.render(s, True, suit_color(s))
    surf.blit(idx, (10,6)); surf.blit(pip, (10, 34))
    idx2 = pygame.transform.rotate(idx, 180)
    pip2 = pygame.transform.rotate(pip, 180)
    surf.blit(idx2, (w-10-idx2.get_width(), h-6-idx2.get_height()))
    surf.blit(pip2, (w-10-pip2.get_width(), h-34-pip2.get_height()))
    big = FONT_PIP.render(s, True, suit_color(s))
    surf.blit(big, big.get_rect(center=(w//2, h//2+6)))
    return surf

def blit_card_with_shadow(dest, card: Card, pos, angle=0):
    card_surf = draw_card_surface(card)
    shadow = pygame.Surface((card_surf.get_width(), card_surf.get_height()), pygame.SRCALPHA)
    rounded_rect(shadow, shadow.get_rect(), (0,0,0,120), radius=14)
    shadow = pygame.transform.rotate(shadow, angle)
    dest.blit(shadow, (pos[0]+8, pos[1]+10))
    card_surf = pygame.transform.rotate(card_surf, angle)
    dest.blit(card_surf, pos)

def draw_hand(name, hand, x, y):
    # 1–2 cartas: completas; 3+: abanico suave
    if len(hand) <= 2:
        gap = 16
        for i, card in enumerate(hand):
            pos_x = x + i * (CARD_W + gap)
            blit_card_with_shadow(screen, card, (pos_x, y), angle=0)
    else:
        spread = 34
        for i, card in enumerate(hand):
            ang = -3 + (i % 3) * 3
            blit_card_with_shadow(screen, card, (x + i * spread, y), ang)

    total = hand_value(hand)
    label = FONT_MED.render(f"{name} — Total: {total}", True, C_TEXT)
    screen.blit(label, (x, y + CARD_H + 12))

def draw_center_banner(title: str, subtitle: str | None = None, variant: str = "accent"):
    """Panel central con sombra y borde (accent/neutral/danger)."""
    if variant == "danger":
        border = C_DANGER; title_col = C_DANGER
    elif variant == "neutral":
        border = (180, 200, 210); title_col = (230, 240, 245)
    else:
        border = C_ACCENT; title_col = C_ACCENT

    t1 = FONT_HUGE.render(title, True, title_col)
    pad_x, pad_y = 12, 2
    width = t1.get_width() + pad_x*2
    height = t1.get_height() + pad_y*2

    t2 = None
    if subtitle:
        t2 = FONT_MED.render(subtitle, True, (225,225,225))
        height += t2.get_height() + 10
        width = max(width, t2.get_width() + pad_x*2)

    rect = pygame.Rect(0,0,width,height); rect.center = (W//2, H//2)
    shadow_rect(screen, rect, radius=20, blur=20, color=(0,0,0,160))
    rounded_rect(screen, rect, (18, 18, 22, 220), radius=20)
    pygame.draw.rect(screen, border, rect, 3, border_radius=20)

    y = rect.y + pad_y
    screen.blit(t1, (rect.centerx - t1.get_width()//2, y))
    if t2:
        y += t1.get_height() + 10
        screen.blit(t2, (rect.centerx - t2.get_width()//2, y))

# ------------------------------
# WIDGETS (Botón e Input)
# ------------------------------
class Button:
    def __init__(self, x,y,w,h, text):
        self.rect = pygame.Rect(x,y,w,h)
        self.text = text
        self.hover = False
        self.pressed = False
        self.enabled = True
    def draw(self, surf):
        base = C_BTN_P if self.pressed else (C_BTN_H if self.hover else C_BTN)
        shadow_rect(surf, self.rect.move(0,6), radius=20, blur=12, color=(0,0,0,120))
        rounded_rect(surf, self.rect, base, radius=20)
        txt = FONT_MED.render(self.text, True, C_TEXT if self.enabled else (170,170,170))
        surf.blit(txt, txt.get_rect(center=self.rect.center))
    def handle(self, event):
        if not self.enabled: return False
        if event.type == pygame.MOUSEMOTION:
            self.hover = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button==1:
            if self.rect.collidepoint(event.pos): self.pressed = True
        elif event.type == pygame.MOUSEBUTTONUP and event.button==1:
            was = self.pressed and self.rect.collidepoint(event.pos)
            self.pressed = False
            return was
        return False

class TextInput:
    """Input simple; si numeric=True, valida rango [1..limit]."""
    def __init__(self, x, y, w, h, placeholder="", numeric=False):
        self.rect = pygame.Rect(x,y,w,h)
        self.text = ""
        self.placeholder = placeholder
        self.active = False
        self.caret_on = True
        self.numeric = numeric
        self.limit = 10
    def set_limit(self, limit:int):
        self.limit = max(1, int(limit))
    def value(self):
        if not self.numeric:
            return self.text.strip()
        if self.text.isdigit():
            v = int(self.text)
            if 1 <= v <= self.limit:
                return v
        return None
    def clear(self):
        self.text = ""
    def handle(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button==1:
            self.active = self.rect.collidepoint(event.pos)
        elif self.active and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                pass
            else:
                ch = event.unicode
                if self.numeric:
                    if ch.isdigit() and len(self.text) < 3:
                        self.text += ch
                else:
                    if ch.isprintable() and len(self.text) < 18:
                        self.text += ch
        if event.type == pygame.USEREVENT:
            self.caret_on = not self.caret_on
    def draw(self, surf, label, hint=""):
        valid = True
        if self.numeric and self.text != "":
            valid = self.value() is not None
        border = C_ACCENT if self.active else ((90,90,90) if valid else C_DANGER)
        shadow_rect(surf, self.rect.move(0,6), radius=14, blur=10, color=(0,0,0,100))
        rounded_rect(surf, self.rect, C_PANEL, radius=14)
        pygame.draw.rect(surf, border, self.rect, 2, border_radius=14)
        surf.blit(FONT.render(label, True, C_TEXT), (self.rect.x, self.rect.y-26))
        display = self.text if self.text != "" else self.placeholder
        color = C_TEXT if self.text != "" else (170,170,170)
        txt = FONT_MED.render(display, True, color)
        tx = self.rect.right - 14 - txt.get_width() if self.numeric else self.rect.x + 14
        ty = self.rect.y + (self.rect.h - txt.get_height())//2
        surf.blit(txt, (tx, ty))
        if self.active and self.caret_on:
            pygame.draw.rect(surf, C_TEXT, (tx + txt.get_width() + 2, ty+4, 2, txt.get_height()-8))
        if hint:
            hint_txt = FONT.render(hint, True, (200,200,200))
            surf.blit(hint_txt, (self.rect.x, self.rect.bottom + 6))

# ------------------------------
# ESTADO + UI INSTANCIAS
# ------------------------------
state = "NOMBRES"   # NOMBRES | APUESTAS | JUEGO | FIN_RONDA
J1, J2 = "Jugador 1", "Jugador 2"
credits: Dict[str,int] = {J1:50, J2:50}
bets: Dict[str,int] = {J1:0, J2:0}
deck: List[Card] = []
hand1: List[Card] = []
hand2: List[Card] = []
turn = J1
first_player = J1
second_player = J2
first_done = False
round_msg = ""
game_over = False

# UI: Nombres
name1 = TextInput(W//2 - 440, H//2 - 40, 380, 52, placeholder="Nombre jugador 1")
name2 = TextInput(W//2 + 60,  H//2 - 40, 380, 52, placeholder="Nombre jugador 2")
btn_start = Button(W//2 - 130, H//2 + 40, 260, 52, "Continuar")

# UI: Apuestas
bet1 = TextInput(W-300, 250, 260, 48, placeholder="Ingresa apuesta", numeric=True)
bet2 = TextInput(W-300, 350, 260, 48, placeholder="Ingresa apuesta", numeric=True)
btn_deal  = Button(W-300, 100,   260, 48, "Repartir / Iniciar ronda")
btn_reset = Button(W-300, 160,   260, 48, "Reiniciar partida")

# UI: Juego / Final
btn_hit   = Button(W-320, H-180, 260, 50, "Pedir (Hit)")
btn_stand = Button(W-320, H-120, 260, 50, "Plantarse (Stand)")
btn_new   = Button(W-320, H-120, 260, 50, "Nueva ronda")
btn_play_again = Button(W//2 - 140, H-120, 280, 54, "Jugar de nuevo")
btn_exit  = Button(W-180, 20, 160, 44, "Salir")  # arriba derecha

pygame.time.set_timer(pygame.USEREVENT, 500)
clock = pygame.time.Clock()

# ------------------------------
# HELPERS DE ESTADO
# ------------------------------
def other(p: str) -> str:
    return J2 if p == J1 else J1

def hand_of(player: str) -> List[Card]:
    return hand1 if player == J1 else hand2

def reinit_tables():
    """Reinicia estructuras (conserva nombres)."""
    global credits, bets, hand1, hand2, deck, turn, first_player, second_player, first_done, game_over, round_msg, state
    credits = {J1:50, J2:50}
    bets    = {J1:0,  J2:0}
    hand1, hand2 = [], []
    deck = []
    first_player = J1
    second_player = J2
    first_done = False
    turn = first_player
    game_over = False
    round_msg = ""
    state = "APUESTAS"

def start_round():
    """Reparte y define quién juega primero/segundo. Garantiza que ambos tengan turno."""
    global deck, hand1, hand2, turn, state, round_msg, first_player, second_player, first_done
    deck = build_deck(); shuffle_deck(deck)
    hand1, hand2 = [deal_card(deck), deal_card(deck)], [deal_card(deck), deal_card(deck)]
    turn = random.choice([J1,J2])
    first_player = turn
    second_player = other(first_player)
    first_done = False
    state = "JUEGO"
    round_msg = f"Turno: {turn}"
    # 21 natural del primero -> pasa al segundo; si el segundo también tiene 21, terminar.
    if hand_value(hand_of(first_player)) == 21:
        finish_current_turn()
        if hand_value(hand_of(second_player)) == 21:
            end_round()

def finish_current_turn():
    """Cierra el turno actual: si era el primero, pasa al segundo; si era el segundo, cierra la ronda."""
    global turn, first_done, round_msg
    if turn == first_player:
        first_done = True
        turn = second_player
        round_msg = f"Turno: {turn}"
    else:
        end_round()

def end_round():
    global state, round_msg, credits, bets
    result = resolve_round(J1, hand1, J2, hand2)
    round_msg = apply_payments(credits, bets, result)
    bets[J1]=bets[J2]=0
    bet1.clear(); bet2.clear()
    state = "FIN_RONDA"

def check_game_over():
    return (not all(c>0 for c in credits.values())) or (not all(c<100 for c in credits.values()))

# ------------------------------
# LOOP
# ------------------------------
running = True
while running:
    dt = clock.tick(60)
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False

        # hover/pressed de botones
        if e.type in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN):
            for b in [btn_start, btn_deal, btn_reset, btn_hit, btn_stand, btn_new, btn_play_again, btn_exit]:
                b.handle(e)

        # inputs
        if state == "NOMBRES":
            name1.handle(e); name2.handle(e)
            if e.type == pygame.KEYDOWN and e.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                J1 = name1.value() or "Jugador 1"
                J2 = name2.value() or "Jugador 2"
                reinit_tables()
        else:
            bet1.handle(e); bet2.handle(e)

        # clicks (UP)
        if e.type == pygame.MOUSEBUTTONUP and e.button == 1:
            if btn_exit.handle(e):
                running = False
                continue

            if state == "NOMBRES":
                if btn_start.handle(e):
                    J1 = name1.value() or "Jugador 1"
                    J2 = name2.value() or "Jugador 2"
                    reinit_tables()

            elif state == "APUESTAS" and not game_over:
                bet1.set_limit(min(10, credits[J1]))
                bet2.set_limit(min(10, credits[J2]))
                if btn_deal.handle(e):
                    v1, v2 = bet1.value(), bet2.value()
                    if v1 is not None and v2 is not None:
                        bets[J1], bets[J2] = v1, v2
                        start_round()
                if btn_reset.handle(e):
                    reinit_tables()

            elif state == "JUEGO" and not game_over:
                # HIT
                if turn == J1 and btn_hit.handle(e):
                    hand1.append(deal_card(deck))
                    if hand_value(hand1) >= 21:
                        finish_current_turn()
                elif turn == J2 and btn_hit.handle(e):
                    hand2.append(deal_card(deck))
                    if hand_value(hand2) >= 21:
                        finish_current_turn()
                # STAND
                if btn_stand.handle(e):
                    finish_current_turn()

            elif state == "FIN_RONDA":
                if btn_new.handle(e):
                    game_over = check_game_over()
                    if not game_over:
                        state = "APUESTAS"
                if check_game_over() and btn_play_again.handle(e):
                    reinit_tables()

    # fondo
    draw_vertical_gradient(screen, (0,0,W,H), C_BG1, C_BG2)

    # HUD superior (créditos), excepto en la pantalla de nombres
    if state != "NOMBRES":
        stats = FONT_MED.render(f"{J1}: {credits[J1]} créditos   |   {J2}: {credits[J2]} créditos", True, C_TEXT)
        screen.blit(stats, (W//2 - stats.get_width()//2, 20))

    # --- Render por estado ---
    if state == "NOMBRES":
        title = FONT_BIG.render("Escribe los nombres", True, C_TEXT)
        screen.blit(title, (W//2 - title.get_width()//2, H//2 - 120))
        name1.draw(screen, "Jugador 1")
        name2.draw(screen, "Jugador 2")
        btn_start.draw(screen)

    elif state=="APUESTAS":
        draw_hand(J1, hand1,40, 110)
        draw_hand(J2, hand2,40, 390)
        bet1.set_limit(min(10, credits[J1])); bet2.set_limit(min(10, credits[J2]))
        bet1.draw(screen, f"{J1}", f"Rango: 1–{bet1.limit}")
        bet2.draw(screen, f"{J2}", f"Rango: 1–{bet2.limit}")
        btn_deal.enabled = (bet1.value() is not None) and (bet2.value() is not None)
        btn_deal.draw(screen)
        btn_reset.draw(screen)
        # Banner central (fase)
        draw_center_banner("Fase de apuestas", "Ajusta las apuestas y pulsa Repartir", variant="accent")

    elif state=="JUEGO":
        draw_hand(J1, hand1,40, 110)
        draw_hand(J2, hand2,40, 390)
        btn_hit.draw(screen); btn_stand.draw(screen)
        # Banner central con el turno
        draw_center_banner(f"Turno: {turn}", None, variant="neutral")

    elif state=="FIN_RONDA":
        draw_hand(J1, hand1,40, 110)
        draw_hand(J2, hand2,40, 390)
        is_over = check_game_over()
        if not is_over:
            # Resultado de la RONDA en el centro
            draw_center_banner(round_msg, "Pulsa «Nueva ronda» para continuar", variant="neutral")
            btn_new.draw(screen)
        else:
            # Ganador de la PARTIDA en el centro
            game_over = True
            if credits[J1]>credits[J2]:
                final_msg = f"¡{J1} gana la partida!"
            elif credits[J2]>credits[J1]:
                final_msg = f"¡{J2} gana la partida!"
            else:
                final_msg = "Empate final."
            draw_center_banner(final_msg, "Pulsa «Jugar de nuevo» para reiniciar", variant="danger")
            btn_play_again.draw(screen)

    # botón global "Salir"
    btn_exit.draw(screen)
    pygame.display.flip()

pygame.quit()
