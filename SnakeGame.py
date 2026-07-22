import random
import tkinter as tk


class SnakeGame:
    WIDTH = 600
    HEIGHT = 600
    CELL_SIZE = 25
    DELAY = 120

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Snake Game")
        self.root.resizable(False, False)

        self.canvas = tk.Canvas(
            self.root,
            width=self.WIDTH,
            height=self.HEIGHT,
            bg="black",
            highlightthickness=0
        )
        self.canvas.pack()

        self.root.bind("<KeyPress>", self.handle_key)
        self.root.focus_set()

        self.delay = self.DELAY
        self.running = False
        self.score = 0
        self.snake = []
        self.food = None
        self.direction = (1, 0)

        self.start_game()
        self.root.mainloop()

    def start_game(self):
        self.score = 0
        self.direction = (1, 0)
        self.snake = [
            (100, 100),
            (75, 100),
            (50, 100)
        ]
        self.spawn_food()
        self.running = True
        self.draw()
        self.root.after(self.delay, self.step)

    def spawn_food(self):
        while True:
            x = random.randrange(0, self.WIDTH, self.CELL_SIZE)
            y = random.randrange(0, self.HEIGHT, self.CELL_SIZE)

            if (x, y) not in self.snake:
                self.food = (x, y)
                break

    def step(self):
        if not self.running:
            return

        self.move_snake()
        self.draw()

        if self.running:
            self.root.after(self.delay, self.step)

    def move_snake(self):
        head_x, head_y = self.snake[0]
        new_head = (
            head_x + self.direction[0] * self.CELL_SIZE,
            head_y + self.direction[1] * self.CELL_SIZE
        )

        if self.is_collision(new_head):
            self.end_game()
            return

        self.snake.insert(0, new_head)

        if new_head == self.food:
            self.score += 1
            self.spawn_food()
        else:
            self.snake.pop()

    def is_collision(self, head):
        x, y = head

        if x < 0 or x >= self.WIDTH or y < 0 or y >= self.HEIGHT:
            return True

        if head in self.snake[1:]:
            return True

        return False

    def end_game(self):
        self.running = False
        self.draw()

    def draw(self):
        self.canvas.delete("all")

        # Background
        self.canvas.create_rectangle(0, 0, self.WIDTH, self.HEIGHT, fill="black")

        # Draw food
        if self.food:
            x, y = self.food
            self.canvas.create_oval(
                x, y, x + self.CELL_SIZE, y + self.CELL_SIZE,
                fill="green", outline="green"
            )

        # Draw snake
        for index, (x, y) in enumerate(self.snake):
            fill_color = "#ff69b4" if index == 0 else "#ff1493"
            outline_color = "#ffffff"
            self.canvas.create_rectangle(
                x, y, x + self.CELL_SIZE, y + self.CELL_SIZE,
                fill=fill_color, outline=outline_color
            )

        # Score
        self.canvas.create_text(
            15, 10, anchor="nw",
            text=f"Score: {self.score}",
            fill="white",
            font=("Arial", 16, "bold")
        )

        if not self.running:
            self.canvas.create_text(
                self.WIDTH // 2, self.HEIGHT // 2 - 40,
                text="GAME OVER",
                fill="white",
                font=("Arial", 28, "bold")
            )
            self.canvas.create_text(
                self.WIDTH // 2, self.HEIGHT // 2,
                text=f"Final Score: {self.score}",
                fill="white",
                font=("Arial", 20, "bold")
            )
            self.canvas.create_text(
                self.WIDTH // 2, self.HEIGHT // 2 + 40,
                text="Press SPACE to Restart",
                fill="white",
                font=("Arial", 16)
            )

    def handle_key(self, event):
        key = event.keysym.lower()

        if key in {"space", "return", "r"}:
            if not self.running:
                self.start_game()
            return

        direction_map = {
            "left": (-1, 0),
            "right": (1, 0),
            "up": (0, -1),
            "down": (0, 1)
        }

        if key in direction_map:
            new_direction = direction_map[key]

            if self.is_opposite_direction(new_direction):
                return

            self.direction = new_direction

    def is_opposite_direction(self, new_direction):
        return ( 
            self.direction[0] != 0 and new_direction[0] == -self.direction[0] and new_direction[1] == 0
        ) or (
            self.direction[1] != 0 and new_direction[1] == -self.direction[1] and new_direction[0] == 0
        )


if __name__ == "__main__":
    SnakeGame() 