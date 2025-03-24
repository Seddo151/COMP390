import pygame

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (70, 130, 180)
LIGHT_BLUE = (173,216,230)
DARK_BLUE = 	(70,130,180)
TEXT_COLOR = BLACK

class Button:
    def __init__(self, text, pos, size):
        self.rect = pygame.Rect(pos, size)
        self.colour = LIGHT_BLUE
        self.font = pygame.font.Font(None, 24)
        self.text = text
        self.active = False
        self.text_surface = self.font.render(text, True, TEXT_COLOR)

    def draw(self, screen):
        self.colour = DARK_BLUE if self.active else LIGHT_BLUE
        pygame.draw.rect(screen, self.colour, self.rect)
        text_rect = self.text_surface.get_rect(center=self.rect.center)
        screen.blit(self.text_surface, text_rect)

    def is_clicked(self, event):
        
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)
    
    def update_text(self, text):
        self.text_surface = self.font.render(text, True, TEXT_COLOR)

class TextBox:
    def __init__(self, pos, size,str_size, text):
        self.rect = pygame.Rect(pos, size)
        self.color = WHITE  # Default color
        self.font = pygame.font.Font(None, 24)
        self.text = text  # The current text in the box
        self.active = False  # Whether the text box is active (clicked)
        self.rendered_text = self.font.render(self.text, True, TEXT_COLOR)  # Render the text
        self.str_size = str_size

    def draw(self, screen):
        # Draw the text box
        pygame.draw.rect(screen, self.color, self.rect)
        # Draw the text inside the box
        text_surface = self.font.render(self.text, True, TEXT_COLOR)
        # Adjust text position to avoid overflow
        text_rect = text_surface.get_rect(midleft=(self.rect.x + 5, self.rect.centery))
        screen.blit(text_surface, text_rect)

    def is_clicked(self, event):
        # Activate the text box if clicked
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
                self.color = BLUE
            else:
                self.active = False
                self.color = WHITE
        return self.active

    def handle_event(self, event):
        # Handle text input when the text box is active
        if self.active and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:  # Handle backspace
                self.text = self.text[:-1]
            else:  # Add the typed character to the text
                if len(self.text) < self.str_size:
                    self.text += event.unicode
            # Re-render the text
            self.rendered_text = self.font.render(self.text, True, TEXT_COLOR)
