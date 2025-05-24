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

# === Точка входу ===
def main():
    random.seed(42)
    N = 50  # Кількість точок
    points = [Point(random.uniform(0, 100), random.uniform(0, 100), i) for i in range(N)]

    closest_neighbors(points)
    visualize(points)

if __name__ == "__main__":
    main()
