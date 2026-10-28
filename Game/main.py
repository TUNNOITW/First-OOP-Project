import pygame
import math
import time
import random
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

class CollectibleItem:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.costPrice = random.randint(1, 3)
        if self.costPrice == 1:
            self.color = (255, 128, 0)
        elif self.costPrice == 2:
            self.color = (160, 160, 160)
        else:
            self.color = (225, 225, 51)

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
            coefficient = math.hypot(dx, dy) #coefficient = (dx**2 + dy**2) ** 0.5 то же самое, только чуть быстрее
            dx /= coefficient
            dy /= coefficient

            self.player.rect.x += dx * self.player.speed * dt
            self.player.rect.y += dy * self.player.speed * dt


class CollectibleItemsController:
    def CreateNewCollectibleItems(self, gameState):
        if gameState.nowTime - gameState.lastCreateCollectibleItemTime > 3:
            gameState.lastCreateCollectibleItemTime = gameState.nowTime
            gameState.collectibleItems.append(CollectibleItem(
                random.randint(0, 800), random.randint(0, 800),
                random.randint(50, 100), random.randint(50, 100)))

    def CollisionCollectibleItems(self, gameState):
        count = 0
        collisionedCollectibleItemsId = []
        for item in gameState.collectibleItems:
            if gameState.player.rect.colliderect(item.rect):
                collisionedCollectibleItemsId.append(count)
            count += 1

        count = 0
        for collectibleItemId in collisionedCollectibleItemsId:
            gameState.score += gameState.collectibleItems[collectibleItemId - count].costPrice
            gameState.DeleteCollectibleItem(collectibleItemId - count)
            count += 1

class ScoreController:
    def TimeHandler(self, gameState):
        if gameState.nowTime - gameState.lastUpdateTime >= 1:
            gameState.UpdateScore(1)
            gameState.lastUpdateTime = gameState.nowTime


#--------Handler/Обработчик--------
class Handler:
    def __init__(self, gameState):
        self.playerController = gameState.playerController
        self.scoreController = gameState.scoreController
        self.collectibleItemsController = gameState.collectibleItemsController
        self.gameState = gameState

    def Handler(self, dt):
        self.playerController.KeysHandler(self.gameState.keysPressed, dt)
        self.scoreController.TimeHandler(self.gameState)

        self.collectibleItemsController.CreateNewCollectibleItems(self.gameState)
        self.collectibleItemsController.CollisionCollectibleItems(self.gameState)


#--------Render/Рендер--------
class Render:
    def __init__(self, screen, gameState):
        self.screen = screen
        self.gameState = gameState
        self.font = pygame.font.SysFont("Arial", 50)

    def Render(self):
        self.screen.fill((0, 0, 0))
        pygame.draw.rect(self.screen, self.gameState.player.color, self.gameState.player.rect)

        scoreText = self.font.render("Score: " + str(self.gameState.score), True, (255, 255, 255))
        self.screen.blit(scoreText, (0, 0))

        for Item in self.gameState.collectibleItems:
            pygame.draw.rect(self.screen, Item.color, Item.rect)

        pygame.display.flip()

#--------GameState/Состояние игры--------
class GameState:
    def __init__(self):
        self.player = Player(100, 100, 50, 50, [225, 225, 225], 300)
        self.playerController = PlayerController(self.player)
        self.scoreController = ScoreController()
        self.collectibleItemsController = CollectibleItemsController()

        self.keysPressed = pygame.key.get_pressed()

        self.score = 0
        self.collectibleItems = []

        self.startTime = time.time()
        self.lastUpdateTime = time.time()
        self.lastCreateCollectibleItemTime = time.time()
        self.nowTime = time.time()

    def EveryTickUpdate(self):
        self.keysPressed = pygame.key.get_pressed()
        self.UpdateTime("nowTime")

    def UpdateTime(self, type):
        if type == "lastUpdateTime":
            self.lastUpdateTime = time.time()
        if type == "nowTime":
            self.nowTime = time.time()

    def UpdateScore(self, score):
        self.score += score

    def AddCollectibleItem(self, item):
        self.collectibleItems.append(item)

    def DeleteCollectibleItem(self, id):
        self.collectibleItems.pop(id)

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
            self.gameState.EveryTickUpdate()
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