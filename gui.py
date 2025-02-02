import pygame

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BUTTON_COLOR = (70, 130, 180) 
TEXT_COLOR = WHITE

class Button:
    def __init__(self, text, pos, size):
        self.text = text
        self.rect = pygame.Rect(pos, size)
        self.color = BUTTON_COLOR
        self.font = pygame.font.Font(None, 24)
        self.text_surf = self.font.render(text, True, TEXT_COLOR)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, border_radius=8)  # Rounded corners
        text_rect = self.text_surf.get_rect(center=self.rect.center)
        screen.blit(self.text_surf, text_rect)

    def is_clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)

class TextBox:
    def __init__(self, pos, size):
        self.rect = pygame.Rect(pos, size)
        self.color = WHITE
        self.text = ""
        self.font = pygame.font.Font(None, 36)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                self.active = False
                return self.text
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode
        return None

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, 2 if self.active else 1)
        text_surf = self.font.render(self.text, True, BLACK)
        screen.blit(text_surf, (self.rect.x + 5, self.rect.y + 5))
