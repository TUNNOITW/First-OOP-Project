import pygame
pygame.init()

#--------Player/Игрок--------
class Player:
    def __init__(self, x, y, width, height, color, speed):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.speed = speed

        self.movingUp = False
        self.movingDown = False
        self.movingLeft = False
        self.movingRight = False

    def moveUp(self):
        self.rect.y -= self.speed

    def moveDown(self):
        self.rect.y += self.speed

    def moveLeft(self):
        self.rect.x -= self.speed

    def moveRight(self):
        self.rect.x += self.speed

#--------Controllers/Контроллеры--------
class PlayerController:
    def __init__(self, player):
        self.player = player

    def KeysHandler(self, keys, dt):
        dx = 0
        dy = 0

        if keys[pygame.K_w]:
            dy -= 1
        if keys[pygame.K_s]:
            dy += 1
        if keys[pygame.K_a]:
            dx -= 1
        if keys[pygame.K_d]:
            dx += 1

        if dx != 0 or dy != 0:
            length = (dx * dx + dy * dy) ** 0.5
            dx /= length
            dy /= length

            self.player.rect.x += dx * self.player.speed * dt
            self.player.rect.y += dy * self.player.speed * dt


#--------Handler/Обработчик--------
class Handler:
    def __init__(self, gameState):
        self.playerController = gameState.controller
        self.gameState = gameState

    def Handler(self, dt):
        self.playerController.KeysHandler(self.gameState.keysPressed, dt)

#--------Render/Рендер--------
class Render:
    def __init__(self, screen, gameState):
        self.screen = screen
        self.gameState = gameState

    def Render(self):
        self.screen.fill((0, 0, 0))
        pygame.draw.rect(self.screen, self.gameState.player.color, self.gameState.player.rect)
        pygame.display.flip()

#--------GameState/Состояние игры--------
class GameState:
    def __init__(self):
        self.player = Player(100, 100, 50, 50, [225, 225, 225], 300)
        self.controller = PlayerController(self.player)
        self.keysPressed = pygame.key.get_pressed()

    def Update(self):
        self.keysPressed = pygame.key.get_pressed()

#--------Game/Игра--------
class Game:
    def __init__(self):
        self.clock = pygame.time.Clock()

        self.screen = pygame.display.set_mode((700, 700))
        self.gameState = GameState()

        self.render = Render(self.screen, self.gameState)
        self.handler = Handler(self.gameState)

    def run(self):
        while True:
            self.gameState.Update()
            dt = self.clock.tick(60) / 1000.0
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    exit()
            self.handler.Handler(dt)
            self.render.Render()

if __name__ == "__main__":
    game = Game()
    game.run()