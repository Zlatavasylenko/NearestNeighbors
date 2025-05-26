import matplotlib.pyplot as plt
import random
from math import dist

# Клас точки
class Point:
    def __init__(self, x, y, index):
        self.x = x
        self.y = y
        self.index = index
        self.nearest = None
        self.min_dist = float('inf')

    def __repr__(self):
        return f"({self.x:.2f}, {self.y:.2f})"

# Брутфорс для малих множин (<=3)
def brute_force(points):
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            d = dist((points[i].x, points[i].y), (points[j].x, points[j].y))
            if d < points[i].min_dist:
                points[i].min_dist = d
                points[i].nearest = points[j]
            if d < points[j].min_dist:
                points[j].min_dist = d
                points[j].nearest = points[i]
    return points

# Обробка смуги біля середини
def merge_neighbors(px, py, midpoint):
    strip = [p for p in py if abs(p.x - midpoint) < p.min_dist]
    for i in range(len(strip)):
        for j in range(i + 1, min(i + 7, len(strip))):
            p, q = strip[i], strip[j]
            d = dist((p.x, p.y), (q.x, q.y))
            if d < p.min_dist:
                p.min_dist = d
                p.nearest = q
            if d < q.min_dist:
                q.min_dist = d
                q.nearest = p

# Рекурсивна функція "Розділяй і пануй"
def divide_and_conquer(px, py):
    if len(px) <= 3:
        return brute_force(px)

    mid = len(px) // 2
    Qx = px[:mid]
    Rx = px[mid:]
    midpoint = px[mid].x

    Qy = list(filter(lambda p: p.x <= midpoint, py))
    Ry = list(filter(lambda p: p.x > midpoint, py))

    divide_and_conquer(Qx, Qy)
    divide_and_conquer(Rx, Ry)

    merge_neighbors(px, py, midpoint)
    return px

# Основна функція пошуку
def closest_neighbors(points):
    px = sorted(points, key=lambda p: p.x)
    py = sorted(points, key=lambda p: p.y)
    return divide_and_conquer(px, py)

# Функція візуалізації результату
def visualize(points):
    plt.figure(figsize=(10, 10))
    for p in points:
        plt.plot(p.x, p.y, 'bo')  # синя точка
        plt.text(p.x + 0.5, p.y + 0.5, f'{p.index}', fontsize=9)

        if p.nearest:
            dx = p.nearest.x - p.x
            dy = p.nearest.y - p.y
            plt.arrow(
                p.x, p.y, dx, dy,
                head_width=1.5, head_length=2.5,
                fc='red', ec='red', linestyle='dotted', length_includes_head=True, alpha=0.6
            )

    plt.title("Найближчі сусіди: стрілка до сусіда")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.grid(True)
    plt.axis("equal")
    plt.show()

# Функція для отримання введення від користувача
def get_user_input():
    print("Виберіть спосіб введення точок:")
    print("1. Ввести точки вручну (наприклад, (1, 2), (3, 4))")
    print("2. Автоматично згенерувати точки")
    choice = input("Введіть 1 або 2: ")

    points = []
    if choice == "1":
        print("Введіть координати точок у форматі (x, y), наприклад: (1, 2). Введіть 'done' для завершення.")
        i = 0
        while True:
            user_input = input(f"Точка {i}: ")
            if user_input.lower() == 'done':
                if len(points) < 2:
                    print("Потрібно ввести принаймні 2 точки!")
                    continue
                break
            try:
                # Очікуємо формат "(x, y)"
                x, y = map(float, user_input.strip("() ").split(","))
                points.append(Point(x, y, i))
                i += 1
            except ValueError:
                print("Некоректний формат! Введіть у форматі (x, y), наприклад: (1, 2)")
        return points
    elif choice == "2":
        while True:
            try:
                N = int(input("Введіть кількість точок (2–10000): "))
                if 2 <= N <= 10000:
                    break
                print("Кількість точок має бути від 2 до 10000!")
            except ValueError:
                print("Введіть ціле число!")
        random.seed(42)
        points = [Point(random.uniform(0, 100), random.uniform(0, 100), i) for i in range(N)]
        return points
    else:
        print("Невірний вибір! Використано автоматичну генерацію з N=30.")
        random.seed(42)
        return [Point(random.uniform(0, 100), random.uniform(0, 100), i) for i in range(30)]

# === Точка входу ===
def main():
    points = get_user_input()
    closest_neighbors(points)
    visualize(points)

if __name__ == "__main__":
    main()