    bullet_OG = pygame.image.load("pbullet_small.png")
        bullet_rect = bullet_OG.get_rect(midtop=(self.rect.centerx, self.rect.centery))

        if keys[pygame.K_a]:
            screen.blit(bullet_OG, bullet_rect)
            bullet_speed = 3  # Adjust the bullet speed as needed
            bullet_rect.y -= bullet_speed  # Update the bullet position along the y-axis
            screen.blit(bullet_OG, bullet_rect)