import pygame
import sys


class ScrollingTextDisplay:
    def __init__(self, screen, title_text, content_lines, font_path='./fonts/PressStart2P-Regular.ttf', font_size=20, logo_path=None):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(font_path, font_size)
        self.title_text = title_text
        self.content_lines = content_lines
        self.logo = pygame.image.load(logo_path) if logo_path else None
        if self.logo:
            self.logo = pygame.transform.scale(self.logo, (300, 100))  # Adjust logo size as needed

        # Render and wrap text
        self.max_text_width = self.screen.get_width() - 40  # Padding
        self.rendered_text = self.wrap_and_render_text(self.content_lines)
        
        # Initial scroll positions and controls
        self.scroll_y = self.screen.get_height() // 2
        self.scroll_speed = 5
        self.scroll_acceleration = 1
        self.key_up_pressed = False
        self.key_down_pressed = False

    def wrap_and_render_text(self, text_lines):
        wrapped_text = []
        for line in text_lines:
            wrapped_lines = self.wrap_text(line, self.font, self.max_text_width)
            wrapped_text.extend(wrapped_lines)
        return [self.font.render(line, True, (255, 255, 0)) for line in wrapped_text]  # Pac-Man yellow color

    def wrap_text(self, text, font, max_width):
        words = text.split(' ')
        lines = []
        while words:
            line = ''
            while words and font.size(line + words[0])[0] <= max_width:
                line += words.pop(0) + ' '
            lines.append(line.strip())
        return lines

    def scroll_content(self):
        if self.key_up_pressed:
            self.scroll_y += self.scroll_speed
            self.scroll_speed += self.scroll_acceleration  # Accelerate scrolling
        elif self.key_down_pressed:
            self.scroll_y -= self.scroll_speed
            self.scroll_speed += self.scroll_acceleration  # Accelerate scrolling
        else:
            self.scroll_speed = 5  # Reset scroll speed

    def render(self):
        self.screen.fill((0, 0, 0))  # Black background
        # Display logo if available
        if self.logo:
            self.screen.blit(self.logo, (self.screen.get_width() // 2 - self.logo.get_width() // 2, 20))
        
        # Display text
        y_offset = self.scroll_y + 150  # Offset below the logo
        for text_surface in self.rendered_text:
            self.screen.blit(text_surface, (20, y_offset))  # Padding on the left
            y_offset += 40  # Vertical spacing

        pygame.display.flip()
        self.clock.tick(60)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:  # Scroll up
                    self.key_up_pressed = True
                elif event.key == pygame.K_DOWN:  # Scroll down
                    self.key_down_pressed = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    self.key_up_pressed = False
                elif event.key == pygame.K_DOWN:
                    self.key_down_pressed = False
