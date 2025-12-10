import pygame
from ui import UI

def main():
    clock = pygame.time.Clock()
    app = UI()

    running = True
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                app.handle_click(pygame.mouse.get_pos())
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        app.draw()

    pygame.quit()

if __name__ == "__main__":
    main()
