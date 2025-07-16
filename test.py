import pygame
import random
import sys
import time

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
PINK = (255, 192, 203)
CYAN = (0, 255, 255)

# Funny messages for different situations
STARTUP_MESSAGES = [
    "🐍 Warning: This snake has commitment issues!",
    "🎮 Deploying digital danger noodle...",
    "🚀 Loading pixels and poor life choices...",
    "⚡ Initializing procrastination simulator...",
    "🎯 Calibrating your future disappointment...",
    "🌟 Starting the most productive thing you'll do today!",
    "🔥 Warming up the rage-quit engine...",
    "💎 Polishing your gaming skills (spoiler: they're rough)",
    "🎪 Welcome to the circus of broken dreams!",
    "🎨 Painting the screen with your tears of joy... or sorrow"
]

FOOD_EATEN_MESSAGES = [
    "Nom nom nom! 🍎",
    "That's some gourmet pixel food! 👨‍🍳",
    "Your snake is getting thicc! 🐍",
    "Nutrition facts: 100% digital, 0% calories 📊",
    "Snake.exe is growing successfully 💾",
    "Achievement unlocked: Professional food vacuumer! 🏆",
    "Your snake's dating profile: 'Looking for someone who feeds me' 💕",
    "Breaking news: Local snake discovers fast food! 📰",
    "That food was worth the carpal tunnel! 🖱️"
]

GAME_OVER_MESSAGES = [
    "💀 Your snake had an existential crisis!",
    "🎭 Plot twist: The snake was actually a boomerang!",
    "🚨 Breaking: Snake discovers walls are not edible!",
    "🤦‍♂️ Your snake just tried to eat itself... again!",
    "🎪 Ladies and gentlemen, the snake has left the building!",
    "📚 Today's lesson: Cannibalism is bad for snakes too!",
    "🔄 Your snake just performed an illegal U-turn!",
    "🏁 Congratulations! You've mastered the art of creative self-destruction!",
    "🎨 Your snake just became abstract art!",
    "🔥 That was more chaotic than a Python developer's first day!"
]

HIGH_SCORE_MESSAGES = [
    "🏆 NEW HIGH SCORE! Your parents are finally proud!",
    "⭐ HIGH SCORE ACHIEVED! Time to update your resume!",
    "🎉 RECORD BROKEN! You're now professionally unemployable!",
    "🚀 HIGH SCORE! NASA wants to recruit your snake!",
    "💪 BEAST MODE ACTIVATED! Your snake is now legendary!",
    "🎯 PERFECTION! Your snake just got a PhD in Food Consumption!"
]

class SnakeGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("🐍 Snake Game: Now with 100% more chaos!")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        # Print random startup message
        print(random.choice(STARTUP_MESSAGES))
        
        self.reset_game()
        
    def reset_game(self):
        # Snake starts in the middle, moving right
        start_x = GRID_WIDTH // 2
        start_y = GRID_HEIGHT // 2
        self.snake = [(start_x, start_y)]
        self.direction = (1, 0)  # (dx, dy)
        self.next_direction = (1, 0)
        
        # Generate first food
        self.food = self.generate_food()
        
        # Game state
        self.score = 0
        self.high_score = self.load_high_score()
        self.game_over = False
        self.paused = False
        
        # Speed control
        self.base_speed = 10  # FPS
        self.speed_increase = 0.5  # Speed increase per food eaten
        
        # Message system
        self.current_message = ""
        self.message_timer = 0
        
    def load_high_score(self):
        try:
            with open('high_score.txt', 'r') as f:
                return int(f.read().strip())
        except (FileNotFoundError, ValueError):
            return 0
            
    def save_high_score(self):
        with open('high_score.txt', 'w') as f:
            f.write(str(self.high_score))
            
    def generate_food(self):
        while True:
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)
            if (x, y) not in self.snake:
                return (x, y)
                
    def show_message(self, message, duration=2000):
        self.current_message = message
        self.message_timer = duration
        print(message)  # Also print to console for extra laughs
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                elif event.key == pygame.K_SPACE:
                    if self.game_over:
                        self.reset_game()
                    else:
                        self.paused = not self.paused
                elif event.key == pygame.K_r and self.game_over:
                    self.reset_game()
                elif not self.game_over and not self.paused:
                    # Movement controls (WASD and arrow keys)
                    if event.key in [pygame.K_LEFT, pygame.K_a]:
                        if self.direction != (1, 0):  # Can't go right if moving left
                            self.next_direction = (-1, 0)
                    elif event.key in [pygame.K_RIGHT, pygame.K_d]:
                        if self.direction != (-1, 0):  # Can't go left if moving right
                            self.next_direction = (1, 0)
                    elif event.key in [pygame.K_UP, pygame.K_w]:
                        if self.direction != (0, 1):  # Can't go down if moving up
                            self.next_direction = (0, -1)
                    elif event.key in [pygame.K_DOWN, pygame.K_s]:
                        if self.direction != (0, -1):  # Can't go up if moving down
                            self.next_direction = (0, 1)
        return True
        
    def update(self):
        if self.game_over or self.paused:
            return
            
        # Update direction (prevents immediate reverse)
        self.direction = self.next_direction
        
        # Move snake
        head_x, head_y = self.snake[0]
        new_head = (head_x + self.direction[0], head_y + self.direction[1])
        
        # Check wall collision
        if (new_head[0] < 0 or new_head[0] >= GRID_WIDTH or 
            new_head[1] < 0 or new_head[1] >= GRID_HEIGHT):
            self.game_over = True
            self.show_message(random.choice(GAME_OVER_MESSAGES))
            return
            
        # Check self collision
        if new_head in self.snake:
            self.game_over = True
            self.show_message(random.choice(GAME_OVER_MESSAGES))
            return
            
        # Add new head
        self.snake.insert(0, new_head)
        
        # Check food collision
        if new_head == self.food:
            self.score += 10
            self.show_message(random.choice(FOOD_EATEN_MESSAGES))
            self.food = self.generate_food()
            
            # Check for high score
            if self.score > self.high_score:
                self.high_score = self.score
                self.save_high_score()
                self.show_message(random.choice(HIGH_SCORE_MESSAGES), 3000)
        else:
            # Remove tail if no food eaten
            self.snake.pop()
            
    def draw(self):
        # Clear screen
        self.screen.fill(BLACK)
        
        # Draw snake with rainbow colors
        for i, segment in enumerate(self.snake):
            x, y = segment
            # Make head a different color
            if i == 0:
                color = YELLOW  # Head is yellow
            else:
                # Body has rainbow colors
                colors = [GREEN, BLUE, PURPLE, ORANGE, PINK, CYAN]
                color = colors[i % len(colors)]
                
            pygame.draw.rect(self.screen, color, 
                           (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE - 1, GRID_SIZE - 1))
            
            # Draw eyes on the head
            if i == 0:
                eye_size = 3
                eye_offset = 5
                pygame.draw.circle(self.screen, BLACK, 
                                 (x * GRID_SIZE + eye_offset, y * GRID_SIZE + eye_offset), eye_size)
                pygame.draw.circle(self.screen, BLACK, 
                                 (x * GRID_SIZE + GRID_SIZE - eye_offset, y * GRID_SIZE + eye_offset), eye_size)
        
        # Draw food (animated)
        food_x, food_y = self.food
        pulse = abs(pygame.time.get_ticks() % 1000 - 500) / 500  # Pulse between 0 and 1
        food_size = int(GRID_SIZE * (0.8 + 0.2 * pulse))
        offset = (GRID_SIZE - food_size) // 2
        pygame.draw.rect(self.screen, RED, 
                       (food_x * GRID_SIZE + offset, food_y * GRID_SIZE + offset, food_size, food_size))
        
        # Draw score
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        # Draw high score
        high_score_text = self.font.render(f"High Score: {self.high_score}", True, WHITE)
        self.screen.blit(high_score_text, (10, 50))
        
        # Draw current message
        if self.message_timer > 0:
            message_text = self.small_font.render(self.current_message, True, CYAN)
            text_rect = message_text.get_rect(center=(WINDOW_WIDTH // 2, 100))
            self.screen.blit(message_text, text_rect)
            self.message_timer -= self.clock.get_time()
        
        # Draw game over screen
        if self.game_over:
            overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
            overlay.set_alpha(128)
            overlay.fill(BLACK)
            self.screen.blit(overlay, (0, 0))
            
            game_over_text = self.font.render("GAME OVER!", True, RED)
            text_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 60))
            self.screen.blit(game_over_text, text_rect)
            
            final_score_text = self.font.render(f"Final Score: {self.score}", True, WHITE)
            text_rect = final_score_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 20))
            self.screen.blit(final_score_text, text_rect)
            
            restart_text = self.small_font.render("Press SPACE or R to restart, ESC to quit", True, WHITE)
            text_rect = restart_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 20))
            self.screen.blit(restart_text, text_rect)
            
        # Draw pause screen
        elif self.paused:
            overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
            overlay.set_alpha(128)
            overlay.fill(BLUE)
            self.screen.blit(overlay, (0, 0))
            
            pause_text = self.font.render("PAUSED", True, WHITE)
            text_rect = pause_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            self.screen.blit(pause_text, text_rect)
            
            resume_text = self.small_font.render("Press SPACE to resume", True, WHITE)
            text_rect = resume_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 40))
            self.screen.blit(resume_text, text_rect)
        
        # Draw controls
        if not self.game_over and not self.paused:
            controls_text = self.small_font.render("WASD/Arrow Keys: Move | SPACE: Pause | ESC: Quit", True, WHITE)
            self.screen.blit(controls_text, (10, WINDOW_HEIGHT - 25))
        
        pygame.display.flip()
        
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            
            # Dynamic speed based on score
            current_speed = self.base_speed + (self.score // 50) * self.speed_increase
            self.clock.tick(current_speed)
            
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    print("🎮 Starting Snake Game...")
    print("🐍 Prepare for digital chaos!")
    print("📝 Pro tip: Don't run into walls or yourself. Revolutionary advice, I know.")
    print("🎯 Good luck! You'll need it... seriously.")
    
    game = SnakeGame()
    game.run()
