import pygame, math

class COLORS:
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

res = (800, 600)

scr_arr = []
for y in range(res[1]):
    row = []
    for x in range(res[0]):
        row.append('')
    scr_arr.append(row)

def main():
    pygame.init()
    screen = pygame.display.set_mode(res)
    pygame.display.set_caption("Blit Text Example")
    font = pygame.font.Font(None, 36)  # Default font, size 36
    text = font.render("Hello, Pygame!", True, COLORS.WHITE)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill(COLORS.BLACK)
 
        mx, my = pygame.mouse.get_pos()

        for y in range(res[1]):
            for x in range(res[0]):
                scr_arr[y-1][x-1] = str(round(math.sqrt((mx - x)**2 + (my - y)**2), 1))

        text = font.render(''.join([''.join(row) for row in scr_arr]), True, COLORS.WHITE)
        screen.blit(text, (0, 0))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()