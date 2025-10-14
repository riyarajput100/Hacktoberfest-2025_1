#!/usr/bin/env python3
"""
🎮 Interactive Snake Game with AI 
A complete Snake game implementation with multiple features:
- Classic Snake gameplay
- AI-powered Snake (auto-play)
- Score tracking and high scores
- Beautiful console graphics
- Multiple difficulty levels

Features:
- Classic Snake game mechanics
- AI Snake with pathfinding
- Score system with high score tracking
- Multiple difficulty levels
- Beautiful ASCII graphics
- Interactive controls
"""

import random
import time
import os
import json
from typing import List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

class Direction(Enum):
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)

@dataclass
class Position:
    row: int
    col: int
    
    def __add__(self, other):
        return Position(self.row + other.row, self.col + other.col)
    
    def __eq__(self, other):
        return self.row == other.row and self.col == other.col

class SnakeGame:
    def __init__(self, width: int = 20, height: int = 15):
        """Initialize the Snake game"""
        self.width = width
        self.height = height
        self.snake = [Position(height // 2, width // 2)]
        self.direction = Direction.RIGHT
        self.food = self.generate_food()
        self.score = 0
        self.game_over = False
        self.ai_mode = False
        self.difficulty = 0.1  # Delay between moves
        self.high_score = self.load_high_score()
        
    def clear_screen(self):
        """Clear the console screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def generate_food(self) -> Position:
        """Generate food at random position"""
        while True:
            food = Position(
                random.randint(0, self.height - 1),
                random.randint(0, self.width - 1)
            )
            if food not in self.snake:
                return food
    
    def draw_game(self):
        """Draw the game board"""
        self.clear_screen()
        
        print("🐍 SNAKE GAME - HACKTOBERFEST 2025")
        print("=" * 50)
        print(f"Score: {self.score} | High Score: {self.high_score}")
        print(f"Mode: {'AI' if self.ai_mode else 'Manual'}")
        print("=" * 50)
        
        # Create game board
        board = [[' ' for _ in range(self.width)] for _ in range(self.height)]
        
        # Draw snake
        for i, segment in enumerate(self.snake):
            if i == 0:  # Head
                board[segment.row][segment.col] = '🐍'
            else:  # Body
                board[segment.row][segment.col] = '🟢'
        
        # Draw food
        board[self.food.row][self.food.col] = '🍎'
        
        # Draw borders and board
        print("┌" + "─" * (self.width * 2) + "┐")
        for row in board:
            print("│" + "".join(row) + "│")
        print("└" + "─" * (self.width * 2) + "┘")
        
        if self.game_over:
            print("\n💀 GAME OVER!")
            print(f"Final Score: {self.score}")
            if self.score > self.high_score:
                print("🎉 NEW HIGH SCORE!")
                self.save_high_score(self.score)
    
    def move_snake(self):
        """Move the snake in current direction"""
        if self.game_over:
            return
        
        head = self.snake[0]
        new_head = Position(
            head.row + self.direction.value[0],
            head.col + self.direction.value[1]
        )
        
        # Check wall collision
        if (new_head.row < 0 or new_head.row >= self.height or
            new_head.col < 0 or new_head.col >= self.width):
            self.game_over = True
            return
        
        # Check self collision
        if new_head in self.snake:
            self.game_over = True
            return
        
        self.snake.insert(0, new_head)
        
        # Check food collision
        if new_head == self.food:
            self.score += 10
            self.food = self.generate_food()
        else:
            self.snake.pop()
    
    def change_direction(self, new_direction: Direction):
        """Change snake direction (prevent reverse)"""
        opposite_directions = {
            Direction.UP: Direction.DOWN,
            Direction.DOWN: Direction.UP,
            Direction.LEFT: Direction.RIGHT,
            Direction.RIGHT: Direction.LEFT
        }
        
        if opposite_directions.get(new_direction) != self.direction:
            self.direction = new_direction
    
    def ai_move(self):
        """AI-powered snake movement using simple pathfinding"""
        if len(self.snake) == 1:
            # Simple movement for single segment
            head = self.snake[0]
            if head.col < self.food.col:
                self.change_direction(Direction.RIGHT)
            elif head.col > self.food.col:
                self.change_direction(Direction.LEFT)
            elif head.row < self.food.row:
                self.change_direction(Direction.DOWN)
            elif head.row > self.food.row:
                self.change_direction(Direction.UP)
        else:
            # More complex AI for longer snake
            head = self.snake[0]
            
            # Calculate distances for each direction
            directions = {
                Direction.UP: Position(head.row - 1, head.col),
                Direction.DOWN: Position(head.row + 1, head.col),
                Direction.LEFT: Position(head.row, head.col - 1),
                Direction.RIGHT: Position(head.row, head.col + 1)
            }
            
            # Find safe directions
            safe_directions = []
            for direction, new_pos in directions.items():
                if (0 <= new_pos.row < self.height and 
                    0 <= new_pos.col < self.width and 
                    new_pos not in self.snake):
                    safe_directions.append(direction)
            
            if safe_directions:
                # Choose direction closest to food
                best_direction = min(safe_directions, 
                    key=lambda d: abs(directions[d].row - self.food.row) + 
                                 abs(directions[d].col - self.food.col))
                self.change_direction(best_direction)
    
    def load_high_score(self) -> int:
        """Load high score from file"""
        try:
            with open('snake_high_score.json', 'r') as f:
                data = json.load(f)
                return data.get('high_score', 0)
        except FileNotFoundError:
            return 0
    
    def save_high_score(self, score: int):
        """Save high score to file"""
        self.high_score = score
        with open('snake_high_score.json', 'w') as f:
            json.dump({'high_score': score}, f)
    
    def reset_game(self):
        """Reset the game"""
        self.snake = [Position(self.height // 2, self.width // 2)]
        self.direction = Direction.RIGHT
        self.food = self.generate_food()
        self.score = 0
        self.game_over = False

class SnakeGameInterface:
    def __init__(self):
        """Initialize the game interface"""
        self.game = SnakeGame()
    
    def show_menu(self):
        """Show main menu"""
        self.game.clear_screen()
        print("🐍 SNAKE GAME - HACKTOBERFEST 2025")
        print("=" * 40)
        print("1. Play Game (Manual)")
        print("2. Watch AI Play")
        print("3. Settings")
        print("4. High Scores")
        print("5. Exit")
        print("=" * 40)
    
    def play_manual_game(self):
        """Play game with manual controls"""
        self.game.reset_game()
        self.game.ai_mode = False
        
        print("\n🎮 MANUAL MODE")
        print("Controls: w(up) s(down) a(left) d(right) q(quit)")
        print("Press Enter to start...")
        input()
        
        while not self.game.game_over:
            self.game.draw_game()
            
            # Get user input
            try:
                key = input("Move (w/s/a/d/q): ").lower()
                
                if key == 'w':
                    self.game.change_direction(Direction.UP)
                elif key == 's':
                    self.game.change_direction(Direction.DOWN)
                elif key == 'a':
                    self.game.change_direction(Direction.LEFT)
                elif key == 'd':
                    self.game.change_direction(Direction.RIGHT)
                elif key == 'q':
                    break
                
                self.game.move_snake()
                time.sleep(self.game.difficulty)
                
            except KeyboardInterrupt:
                break
        
        self.game.draw_game()
        input("\nPress Enter to continue...")
    
    def play_ai_game(self):
        """Play game with AI"""
        self.game.reset_game()
        self.game.ai_mode = True
        
        print("\n🤖 AI MODE")
        print("Watch the AI snake play automatically!")
        print("Press Enter to start...")
        input()
        
        while not self.game.game_over:
            self.game.draw_game()
            self.game.ai_move()
            self.game.move_snake()
            time.sleep(self.game.difficulty * 2)  # Slower for AI
        
        self.game.draw_game()
        input("\nPress Enter to continue...")
    
    def show_settings(self):
        """Show settings menu"""
        while True:
            self.game.clear_screen()
            print("⚙️ SETTINGS")
            print("=" * 20)
            print(f"Current Difficulty: {self.game.difficulty:.2f}")
            print("1. Easy (0.2s)")
            print("2. Medium (0.1s)")
            print("3. Hard (0.05s)")
            print("4. Back to Menu")
            
            choice = input("\nSelect option (1-4): ").strip()
            
            if choice == "1":
                self.game.difficulty = 0.2
                print("Difficulty set to Easy")
            elif choice == "2":
                self.game.difficulty = 0.1
                print("Difficulty set to Medium")
            elif choice == "3":
                self.game.difficulty = 0.05
                print("Difficulty set to Hard")
            elif choice == "4":
                break
            else:
                print("Invalid choice!")
            
            time.sleep(1)
    
    def show_high_scores(self):
        """Show high scores"""
        self.game.clear_screen()
        print("🏆 HIGH SCORES")
        print("=" * 20)
        print(f"Current High Score: {self.game.high_score}")
        print(f"Current Score: {self.game.score}")
        
        if self.game.score > self.game.high_score:
            print("🎉 You have a new high score!")
        
        input("\nPress Enter to continue...")
    
    def run(self):
        """Run the main game loop"""
        while True:
            self.show_menu()
            choice = input("Select option (1-5): ").strip()
            
            if choice == "1":
                self.play_manual_game()
            elif choice == "2":
                self.play_ai_game()
            elif choice == "3":
                self.show_settings()
            elif choice == "4":
                self.show_high_scores()
            elif choice == "5":
                print("👋 Thanks for playing Snake Game!")
                break
            else:
                print("❌ Invalid choice!")
                time.sleep(1)

def main():
    """Main function"""
    print("🐍 Welcome to Snake Game!")
    print("Features: Manual play, AI mode, Score tracking")
    
    game_interface = SnakeGameInterface()
    game_interface.run()

if __name__ == "__main__":
    main()
