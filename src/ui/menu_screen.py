import pygame

class MenuScreen:
    def __init__(self):
        self.font = pygame.font.SysFont(None, 36)
        self.big_font = pygame.font.SysFont(None, 48)
        self.huge_font = pygame.font.SysFont(None, 120)

    def draw_start_screen(self, screen, width, height):
        screen.fill((255, 255, 255))
        message = self.big_font.render("Bienvenue dans le jeu de basket !", True, (0, 0, 0))
        msg_rect = message.get_rect(center=(width // 2, height // 2 - 100))
        screen.blit(message, msg_rect)

        button_rect = pygame.Rect(width // 2 - 100, height // 2, 200, 60)
        pygame.draw.rect(screen, (200, 200, 200), button_rect)
        pygame.draw.rect(screen, (0, 0, 0), button_rect, 2)
        text = self.font.render("Continuer", True, (0, 0, 0))
        text_rect = text.get_rect(center=button_rect.center)
        screen.blit(text, text_rect)

        return button_rect

    def draw_game_over(self, screen, width, height, score, high_scores):
        screen.fill((255, 255, 255))
        msg = self.big_font.render("Fin de la partie", True, (0, 0, 0))
        screen.blit(msg, msg.get_rect(center=(width // 2, height // 2 - 120)))

        score_msg = self.font.render(f"Score : {score}", True, (0, 0, 0))
        screen.blit(score_msg, score_msg.get_rect(center=(width // 2, height // 2 - 60)))

        label = self.font.render("Meilleurs scores :", True, (0, 0, 0))
        screen.blit(label, label.get_rect(center=(width // 2, height // 2)))

        high_scores_sorted = sorted(high_scores, reverse=True)[:3]
        y_offset = 40
        for i in range(3):
            if i < len(high_scores_sorted):
                text = f"{i+1}. {high_scores_sorted[i]}"
            else:
                text = f"{i+1}. -"
            score_line = self.font.render(text, True, (0, 0, 0))
            screen.blit(score_line, (width // 2 - 50, height // 2 + y_offset))
            y_offset += 40

        replay_btn = pygame.Rect(width - 160, height - 80, 140, 50)
        pygame.draw.rect(screen, (200, 200, 200), replay_btn)
        pygame.draw.rect(screen, (0, 0, 0), replay_btn, 2)
        text = self.font.render("Rejouer", True, (0, 0, 0))
        screen.blit(text, text.get_rect(center=replay_btn.center))

        return replay_btn