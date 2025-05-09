import pygame

# Color constants
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
        # Draws on the surface with the current state
        # Changes colour depending on whether it is pressed or not
        self.colour = DARK_BLUE if self.active else LIGHT_BLUE
        pygame.draw.rect(screen, self.colour, self.rect)
        # Draws text on button
        text_rect = self.text_surface.get_rect(center=self.rect.center)
        screen.blit(self.text_surface, text_rect)

    def is_clicked(self, event):
        # Checks if the button was clicked
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)
    
    def update_text(self, text):
        # Changes the text
        self.text_surface = self.font.render(text, True, TEXT_COLOR)

class TextBox:
    def __init__(self, pos, size,str_size, text):
        self.rect = pygame.Rect(pos, size)
        self.color = WHITE 
        self.font = pygame.font.Font(None, 24)
        self.text = text  
        self.active = False  
        self.rendered_text = self.font.render(self.text, True, TEXT_COLOR)
        self.str_size = str_size

    def draw(self, screen):
        # Draws the text box onto the surface
        pygame.draw.rect(screen, self.color, self.rect)
        # Draws the text inside the box
        text_surface = self.font.render(self.text, True, TEXT_COLOR)
        # Adjusts the text position to avoid overflow
        text_rect = text_surface.get_rect(midleft=(self.rect.x + 5, self.rect.centery))
        screen.blit(text_surface, text_rect)

    def is_clicked(self, event):
        # Activates the text box if clicked
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
                self.color = BLUE
            else:
                self.active = False
                self.color = WHITE
        return self.active

    def handle_event(self, event):
        # Handles text input when the text box is active
        if self.active and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:  # Handles backspace
                self.text = self.text[:-1]
            else:  # Adds the typed character to the text
                if len(self.text) < self.str_size:
                    self.text += event.unicode
            # Re-renders the text with the changes
            self.rendered_text = self.font.render(self.text, True, TEXT_COLOR)
