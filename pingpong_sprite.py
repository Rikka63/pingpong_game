import pygame
import sys
import random
import time
import os

# Inisialisasi Pygame
pygame.init()
pygame.mixer.init()

# Konstanta
WIDTH, HEIGHT = 800, 600
PADDLE_WIDTH, PADDLE_HEIGHT = 15, 100
BALL_SIZE = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_BLUE = (173, 216, 230)  # Warna background cerah
RED = (255, 0, 0)
GREEN = (0, 255, 0)
FPS = 60
WINNING_SCORE = 5

# Kecepatan
PADDLE_SPEED = 7
INITIAL_BALL_SPEED = 5
MAX_BALL_SPEED = 15
SPEED_INCREASE = 0.1

# Membuat layar
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong 2 Player")
clock = pygame.time.Clock()

# Kelas untuk tombol menu
class Button:
    def __init__(self, x, y, width, height, text, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False
        self.font = pygame.font.Font(None, 36)
    
    def draw(self, surface):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        pygame.draw.rect(surface, BLACK, self.rect, 2, border_radius=10)
        
        text_surface = self.font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
    
    def check_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)
        return self.is_hovered
    
    def is_clicked(self, pos, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(pos)
        return False

# Kelas GameSprite (parent class)
class GameSprite(pygame.sprite.Sprite):
    def __init__(self, image_path, x, y, width, height):
        super().__init__()
        try:
            self.image = pygame.image.load(image_path)
            self.image = pygame.transform.scale(self.image, (width, height))
        except:
            # Jika gambar tidak ditemukan, buat rectangle warna putih
            self.image = pygame.Surface((width, height))
            self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Kelas Player (turunan dari GameSprite)
class Player(GameSprite):
    def __init__(self, image_path, x, y, width, height, up_key, down_key):
        super().__init__(image_path, x, y, width, height)
        self.up_key = up_key
        self.down_key = down_key
        self.speed = PADDLE_SPEED
        self.score = 0
    
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[self.up_key] and self.rect.y > 0:
            self.rect.y -= self.speed
        if keys[self.down_key] and self.rect.y < HEIGHT - self.rect.height:
            self.rect.y += self.speed

# Kelas Ball (turunan dari GameSprite)
class Ball(GameSprite):
    def __init__(self, image_path, x, y, size):
        super().__init__(image_path, x, y, size, size)
        self.reset()
    
    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        
        # Deteksi tumbukan dengan dinding atas/bawah
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.speed_y *= -1
        
        # Tingkatkan kecepatan secara gradual
        current_time = time.time()
        if current_time - self.start_time > 1:  # Setiap 1 detik
            self.start_time = current_time
            if abs(self.speed_x) < MAX_BALL_SPEED:
                self.speed_x *= (1 + SPEED_INCREASE)
                self.speed_y *= (1 + SPEED_INCREASE)
    
    def reset(self):
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.speed_x = INITIAL_BALL_SPEED * random.choice((1, -1))
        self.speed_y = INITIAL_BALL_SPEED * random.choice((1, -1))
        self.start_time = time.time()

# Fungsi untuk menampilkan teks di tengah layar
def draw_text_center(text, size, color, y_offset=0):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(WIDTH//2, HEIGHT//2 + y_offset))
    screen.blit(text_surface, text_rect)

# Fungsi untuk menampilkan skor
def display_score(score1, score2):
    font = pygame.font.Font(None, 74)
    text1 = font.render(str(score1), True, BLACK)
    text2 = font.render(str(score2), True, BLACK)
    screen.blit(text1, (WIDTH // 4, 20))
    screen.blit(text2, (3 * WIDTH // 4, 20))

# Fungsi menu utama
def main_menu():
    play_button = Button(WIDTH//2 - 100, HEIGHT//2, 200, 50, "PLAY", GREEN, (200, 255, 200))
    quit_button = Button(WIDTH//2 - 100, HEIGHT//2 + 70, 200, 50, "QUIT", RED, (255, 200, 200))
    
    while True:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if play_button.is_clicked(mouse_pos, event):
                return "play"
            if quit_button.is_clicked(mouse_pos, event):
                pygame.quit()
                sys.exit()
        
        # Update button hover state
        play_button.check_hover(mouse_pos)
        quit_button.check_hover(mouse_pos)
        
        # Draw menu
        screen.fill(LIGHT_BLUE)
        draw_text_center("PING PONG GAME", 72, BLACK, -100)
        
        play_button.draw(screen)
        quit_button.draw(screen)
        
        # Kontrol instruksi
        font = pygame.font.Font(None, 36)
        controls_text1 = font.render("Player 1: W (Up) and S (Down)", True, BLACK)
        controls_text2 = font.render("Player 2: Arrow Up and Arrow Down", True, BLACK)
        
        screen.blit(controls_text1, (WIDTH//2 - controls_text1.get_width()//2, HEIGHT - 120))
        screen.blit(controls_text2, (WIDTH//2 - controls_text2.get_width()//2, HEIGHT - 80))
        
        pygame.display.flip()
        clock.tick(FPS)

# Fungsi game over
def game_over(winner):
    play_again_button = Button(WIDTH//2 - 120, HEIGHT//2 + 50, 240, 50, "PLAY AGAIN", GREEN, (200, 255, 200))
    menu_button = Button(WIDTH//2 - 120, HEIGHT//2 + 120, 240, 50, "MAIN MENU", (200, 200, 255), (230, 230, 255))
    
    while True:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if play_again_button.is_clicked(mouse_pos, event):
                return "play_again"
            if menu_button.is_clicked(mouse_pos, event):
                return "menu"
        
        # Update button hover state
        play_again_button.check_hover(mouse_pos)
        menu_button.check_hover(mouse_pos)
        
        # Draw game over screen
        screen.fill(LIGHT_BLUE)
        draw_text_center(f"PLAYER {winner} WINS!", 72, BLACK, -100)
        
        play_again_button.draw(screen)
        menu_button.draw(screen)
        
        pygame.display.flip()
        clock.tick(FPS)

# Fungsi utama game
def game_loop():
    # Cari gambar di folder yang sama
    current_dir = os.path.dirname(os.path.abspath(__file__))
    racket_path = os.path.join(current_dir, "racket.png")
    ball_path = os.path.join(current_dir, "tenis_ball.png")

    # Buat sprite group
    all_sprites = pygame.sprite.Group()

    # Buat player 1 (kiri)
    player1 = Player(racket_path, 20, HEIGHT//2 - PADDLE_HEIGHT//2, 
                    PADDLE_WIDTH, PADDLE_HEIGHT, pygame.K_w, pygame.K_s)

    # Buat player 2 (kanan)
    player2 = Player(racket_path, WIDTH - 20 - PADDLE_WIDTH, HEIGHT//2 - PADDLE_HEIGHT//2,
                    PADDLE_WIDTH, PADDLE_HEIGHT, pygame.K_UP, pygame.K_DOWN)

    # Buat bola
    ball = Ball(ball_path, WIDTH//2 - BALL_SIZE//2, HEIGHT//2 - BALL_SIZE//2, BALL_SIZE)

    # Tambahkan ke sprite group
    all_sprites.add(player1)
    all_sprites.add(player2)
    all_sprites.add(ball)

    # Reset skor
    player1.score = 0
    player2.score = 0

    # Game loop
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        # Update semua sprite
        all_sprites.update()
        
        # Deteksi tumbukan bola dengan paddle
        if pygame.sprite.collide_rect(ball, player1) or pygame.sprite.collide_rect(ball, player2):
            ball.speed_x *= -1
            # Tambahkan sedikit variasi pada sudut pantulan
            ball.speed_y += random.uniform(-2, 2)
        
        # Deteksi gol
        if ball.rect.left <= 0:
            player2.score += 1
            ball.reset()
            # Cek jika ada pemenang
            if player2.score >= WINNING_SCORE:
                return "player2"
        elif ball.rect.right >= WIDTH:
            player1.score += 1
            ball.reset()
            # Cek jika ada pemenang
            if player1.score >= WINNING_SCORE:
                return "player1"
        
        # Render
        screen.fill(LIGHT_BLUE)  # Background cerah
        all_sprites.draw(screen)
        display_score(player1.score, player2.score)
        
        # Gambar garis tengah
        pygame.draw.aaline(screen, BLACK, (WIDTH//2, 0), (WIDTH//2, HEIGHT))
        
        # Update layar
        pygame.display.flip()
        clock.tick(FPS)

# Main program
def main():
    while True:
        # Tampilkan menu utama
        menu_action = main_menu()
        
        if menu_action == "play":
            # Jalankan game loop
            winner = game_loop()
            
            # Tampilkan layar game over
            game_action = game_over(winner[-1])  # Ambil angka player (1 atau 2)
            
            if game_action == "menu":
                continue
            elif game_action == "play_again":
                continue

if __name__ == "__main__":
    main()