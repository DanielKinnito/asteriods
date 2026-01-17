import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT


class CircleShape(pygame.sprite.Sprite):
    """
    Base class for circular game objects.
    Provides position, velocity, collision detection, and screen wrapping.
    """
    
    def __init__(self, x, y, radius):
        if hasattr(self, 'containers'):
            super().__init__(self.containers)
        else:
            super().__init__()
        
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.radius = radius
    
    def draw(self, screen):
        pass
    
    def update(self, dt):
        pass
    
    def collides_with(self, other):
        """Circle-to-circle collision detection."""
        distance = self.position.distance_to(other.position)
        return distance <= (self.radius + other.radius)
    
    def collides_with_polygon(self, vertices):
        """
        Check if this circle collides with a polygon.
        Uses point-in-polygon and closest-edge distance.
        """
        # First check if circle center is inside polygon
        if self._point_in_polygon(self.position, vertices):
            return True
        
        # Then check distance to each edge
        for i in range(len(vertices)):
            p1 = pygame.Vector2(vertices[i])
            p2 = pygame.Vector2(vertices[(i + 1) % len(vertices)])
            
            # Get closest point on edge to circle center
            closest = self._closest_point_on_segment(self.position, p1, p2)
            distance = self.position.distance_to(closest)
            
            if distance <= self.radius:
                return True
        
        return False
    
    def _point_in_polygon(self, point, vertices):
        """Ray casting algorithm for point-in-polygon test."""
        n = len(vertices)
        inside = False
        
        j = n - 1
        for i in range(n):
            xi, yi = vertices[i]
            xj, yj = vertices[j]
            
            if ((yi > point.y) != (yj > point.y)) and \
               (point.x < (xj - xi) * (point.y - yi) / (yj - yi) + xi):
                inside = not inside
            j = i
        
        return inside
    
    def _closest_point_on_segment(self, point, seg_start, seg_end):
        """Find the closest point on a line segment to a given point."""
        seg_vec = seg_end - seg_start
        seg_len_sq = seg_vec.length_squared()
        
        if seg_len_sq == 0:
            return seg_start
        
        # Project point onto line, clamped to segment
        t = max(0, min(1, (point - seg_start).dot(seg_vec) / seg_len_sq))
        return seg_start + seg_vec * t

    def wrap_screen(self):
        """Wrap position around screen edges."""
        if self.position.x < -self.radius:
            self.position.x = SCREEN_WIDTH + self.radius
        elif self.position.x > SCREEN_WIDTH + self.radius:
            self.position.x = -self.radius
        
        if self.position.y < -self.radius:
            self.position.y = SCREEN_HEIGHT + self.radius
        elif self.position.y > SCREEN_HEIGHT + self.radius:
            self.position.y = -self.radius


def polygon_collides_circle(vertices, circle_pos, circle_radius):
    """
    Check if a polygon collides with a circle.
    Utility function for external use (e.g., player triangle vs asteroid).
    """
    # Check if circle center is inside polygon
    n = len(vertices)
    inside = False
    j = n - 1
    for i in range(n):
        xi, yi = vertices[i][0], vertices[i][1]
        xj, yj = vertices[j][0], vertices[j][1]
        
        if ((yi > circle_pos.y) != (yj > circle_pos.y)) and \
           (circle_pos.x < (xj - xi) * (circle_pos.y - yi) / (yj - yi) + xi):
            inside = not inside
        j = i
    
    if inside:
        return True
    
    # Check distance to each edge
    for i in range(len(vertices)):
        p1 = pygame.Vector2(vertices[i])
        p2 = pygame.Vector2(vertices[(i + 1) % len(vertices)])
        
        # Get closest point on edge
        seg_vec = p2 - p1
        seg_len_sq = seg_vec.length_squared()
        
        if seg_len_sq == 0:
            closest = p1
        else:
            t = max(0, min(1, (circle_pos - p1).dot(seg_vec) / seg_len_sq))
            closest = p1 + seg_vec * t
        
        if circle_pos.distance_to(closest) <= circle_radius:
            return True
    
    return False


def triangles_intersect(tri1, tri2):
    """
    Check if two triangles intersect using Separating Axis Theorem.
    tri1 and tri2 are lists of 3 pygame.Vector2 or tuples.
    """
    def get_axes(triangle):
        """Get perpendicular axes for SAT."""
        axes = []
        for i in range(3):
            p1 = pygame.Vector2(triangle[i])
            p2 = pygame.Vector2(triangle[(i + 1) % 3])
            edge = p2 - p1
            # Perpendicular
            axes.append(pygame.Vector2(-edge.y, edge.x).normalize() if edge.length() > 0 else pygame.Vector2(1, 0))
        return axes
    
    def project(triangle, axis):
        """Project triangle onto axis, return min/max."""
        dots = [pygame.Vector2(v).dot(axis) for v in triangle]
        return min(dots), max(dots)
    
    def overlap(proj1, proj2):
        """Check if projections overlap."""
        return proj1[0] <= proj2[1] and proj2[0] <= proj1[1]
    
    # Check all axes from both triangles
    axes = get_axes(tri1) + get_axes(tri2)
    
    for axis in axes:
        proj1 = project(tri1, axis)
        proj2 = project(tri2, axis)
        if not overlap(proj1, proj2):
            return False  # Separating axis found
    
    return True  # No separating axis = collision
