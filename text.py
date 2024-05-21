class Text:
    def __init__(self, text, color, x, y, font):
        self.text = str(text)
        self.color = color 
        self.x = x 
        self.y = y 
        self.font = font
        
    def update(self):
        self.image = self.font.render(self.text, 1, self.color)
        self.rect = self.image.get_rect()
        self.rect.center = self.x, self.y
        
        
    def draw(self, surface):
        self.update()
        surface.blit(self.image, self.rect)