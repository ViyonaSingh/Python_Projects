import pygame
import random
import time

pygame.init()
pygame.display.set_caption("Typing Speed Game")

# Screen settings
WIDTH, HEIGHT = 1200, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
font = pygame.font.SysFont("consolas", 30)
clock = pygame.time.Clock()

# Complete sentences to choose from
texts = [
    "The quick brown fox jumps over the lazy dog.",
    "Practice makes perfect when learning to type faster.",
    "Python is a powerful programming language for everyone.",
    "Typing games can boost both your speed and your accuracy.",
    "Debugging is like being the detective in a crime movie.",
    "Code is like humor. When you have to explain it, it’s bad.",
    "You miss 100 percent of the bugs you don’t test for.",
    "Stay focused and keep improving your coding skills.",
]


def draw_colored_text(reference, user_input, y):
    x = 20
    for i, char in enumerate(reference):
        if i < len(user_input):
            if user_input[i] == char:
                color = (0, 255, 0)  # Green
            else:
                color = (255, 0, 0)  # Red
        else:
            color = (255, 255, 255)  # White (not typed yet)
        rendered = font.render(char, True, color)
        screen.blit(rendered, (x, y))
        x += rendered.get_width()


def main():
    input_text = ""
    sentence = random.choice(texts)
    start_time = None
    finished = False
    wpm = 0

    running = True
    while running:
        screen.fill((30, 30, 30))

        # Instructions
        instruction = font.render("Type the following:", True, (200, 200, 200))
        screen.blit(instruction, (20, 20))

        # Draw sentence with color highlighting
        draw_colored_text(sentence, input_text, 70)

        if finished:
            result = font.render(f"Your speed: {wpm:.2f} WPM", True, (0, 255, 255))
            screen.blit(result, (20, 150))
            again = font.render("Press ENTER to try another one.", True, (180, 180, 180))
            screen.blit(again, (20, 190))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if finished:
                    if event.key == pygame.K_RETURN:
                        main()
                        return
                else:
                    if start_time is None:
                        start_time = time.time()

                    if event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    elif event.key == pygame.K_RETURN:
                        pass
                    else:
                        input_text += event.unicode

                    # Check for completion
                    if input_text == sentence:
                        elapsed_time = time.time() - start_time
                        word_count = len(sentence.split())
                        wpm = (word_count / elapsed_time) * 60
                        finished = True

        pygame.display.flip()
        clock.tick(60)


main()
pygame.quit()
