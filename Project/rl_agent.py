import cv2
import numpy as np
import heapq
import subprocess
import mss
import time
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from collections import deque, namedtuple
import random




# PROJECT



# ============================================================
# A* PATHFINDING SETTINGS
# ============================================================
PATH_COLOR = (100, 150, 220)     # Color for the path (BGR format)
PATH_THICKNESS = 2               # Line thickness for the path
GRID_RESOLUTION = 5              # Grid cell size in pixels (smaller = more precise but slower)
WALL_PADDING = 7



                 # Extra padding around walls to avoid touching them

# ============================================================
# REAL-TIME CAPTURE SETTINGS
# ============================================================
WINDOW_NAME = "Ruffle"           # Name of the Ruffle window to capture
FALLBACK_WINDOW_NAME = "az.swf"  # Fallback window name
TARGET_FPS = 240                  # Target frames per second
SHOW_DEBUG_INFO = True           # Show FPS and detection counts

# ============================================================
# DEEP Q LEARNING SETTINGS
# ============================================================
# Network settings
STATE_WIDTH = 84                 # Width of state image
STATE_HEIGHT = 84                # Height of state image
N_ACTIONS = 6                    # Number of possible actions
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Training hyperparameters
BATCH_SIZE = 32                  # Minibatch size for training
GAMMA = 0.99                     # Discount factor
EPS_START = 1.0                  # Starting epsilon for exploration
EPS_END = 0.05                   # Minimum epsilon
EPS_DECAY = 0.995                # Epsilon decay rate
TARGET_UPDATE = 10               # Update target network every N episodes
LEARNING_RATE = 0.00025          # Learning rate for optimizer
MEMORY_SIZE = 10000              # Replay buffer size
MIN_REPLAY_SIZE = 1000           # Minimum samples before training starts

# Model saving
MODEL_SAVE_PATH = "dqn_tank_model.pth"
SAVE_EVERY_N_EPISODES = 50       # Save model every N episodes

# ============================================================
# SETTINGS - These are now RELATIVE to maze size (percentages)
# ============================================================

# --- Region of Interest (ROI) - Game Area Only ---
ROI_X1 = 0       # Left boundary
ROI_Y1 = 10      # Top boundary (excludes toolbar)
ROI_X2 = 1060    # Right boundary
ROI_Y2 = 617     # Bottom boundary (excludes bottom UI)

# --- Wall Detection Settings (relative to maze size) ---
WALL_MIN_PERCENT = 0.08     # Wall min dimension = 9% of maze size
WALL_COLOR = (255, 0, 255)   # Purple color for walls (BGR format)
WALL_THICKNESS = 5           # Line thickness for wall outline

# --- Tank Detection Settings (relative to maze size) ---
TANK_MIN_PERCENT = 0.03      # Tank min dimension = 3% of maze size
TANK_MAX_PERCENT = 0.08      # Tank max dimension = 8% of maze size
RED_TANK_OUTLINE_COLOR = (0, 0, 255)    # Red color for red tank outline (BGR format)
GREEN_TANK_OUTLINE_COLOR = (0, 255, 0)  # Green color for green tank outline (BGR format)
TANK_THICKNESS = 2           # Line thickness for tank outline

# --- Powerup Detection Settings (relative to maze size) ---
POWERUP_MIN_PERCENT = 0.02   # Powerup min dimension = 2% of maze size
POWERUP_MAX_PERCENT = 0.07   # Powerup max dimension = 7% of maze size
POWERUP_OUTLINE_COLOR = (0, 255, 255)  # Yellow color for outline (BGR format)
POWERUP_THICKNESS = 2        # Line thickness for powerup outline

# --- Bullet Detection Settings ---
BULLET_MAX_DIMENSION = 12    # Maximum width AND height for bullets (pixels)
BULLET_MIN_DIMENSION = 5     # Minimum width AND height for bullets (pixels)
BULLET_OUTLINE_COLOR = (0, 165, 255)  # Orange color for outline (BGR format)
BULLET_THICKNESS = 2         # Line thickness for bullet outline

# --- Color Range for RED tanks (in HSV) ---
RED_LOWER1 = np.array([0, 100, 100])      # Lower red range
RED_UPPER1 = np.array([10, 255, 255])
RED_LOWER2 = np.array([160, 100, 100])    # Upper red range (wraps around)
RED_UPPER2 = np.array([180, 255, 255])

# --- Color Range for GREEN tanks (in HSV) ---
GREEN_LOWER = np.array([35, 100, 100])
GREEN_UPPER = np.array([85, 255, 255])

# --- Color Range for GRAY powerups (in HSV) ---
GRAY_LOWER = np.array([0, 0, 80])       # Low saturation, medium brightness
GRAY_UPPER = np.array([180, 50, 200])   # Any hue, low saturation

# --- Color Range for BLUE powerups (in HSV) ---
BLUE_LOWER = np.array([100, 100, 100])
BLUE_UPPER = np.array([130, 255, 255])

# --- Color Range for YELLOW powerups (in HSV) ---
YELLOW_LOWER = np.array([20, 100, 100])
YELLOW_UPPER = np.array([35, 255, 255])

# --- Color Range for BLACK bullets (in HSV) ---
BLACK_LOWER = np.array([0, 0, 0])        # Any hue, any saturation, very dark
BLACK_UPPER = np.array([180, 255, 50])   # Any hue, any saturation, low brightness

# --- Color Range for WALLS (in HSV) ---
# Walls are dark colored objects - low value/brightness
WALL_LOWER = np.array([0, 0, 0])         # Any hue, any saturation, very dark
WALL_UPPER = np.array([180, 255, 80])    # Any hue, any saturation, low brightness (walls are dark)


# ============================================================
# WINDOW CAPTURE FUNCTIONS
# ============================================================

def find_ruffle_window():
    """Find the Ruffle window using xdotool (Linux)."""
    try:
        # Try finding window named "Ruffle"
        result = subprocess.run(
            ['xdotool', 'search', '--name', WINDOW_NAME],
            capture_output=True, text=True, timeout=5
        )
        window_ids = result.stdout.strip().split('\n')
        if window_ids and window_ids[0]:
            return window_ids[0]
        
        # Fallback: try finding window named "az.swf"
        result = subprocess.run(
            ['xdotool', 'search', '--name', FALLBACK_WINDOW_NAME],
            capture_output=True, text=True, timeout=5
        )
        window_ids = result.stdout.strip().split('\n')
        if window_ids and window_ids[0]:
            return window_ids[0]
    except Exception as e:
        print(f"Error finding Ruffle window: {e}")
    return None


def get_window_geometry(window_id):
    """Get window position and size using xdotool."""
    try:
        result = subprocess.run(
            ['xdotool', 'getwindowgeometry', '--shell', window_id],
            capture_output=True, text=True, timeout=5
        )
        geometry = {}
        for line in result.stdout.strip().split('\n'):
            if '=' in line:
                key, value = line.split('=')
                geometry[key] = int(value)
        return geometry
    except Exception as e:
        print(f"Error getting window geometry: {e}")
    return None


def capture_window(window_id):
    """Capture a screenshot of the specified window using mss."""
    geometry = get_window_geometry(window_id)
    if not geometry:
        return None
    
    x = geometry.get('X', 0)
    y = geometry.get('Y', 0)
    width = geometry.get('WIDTH', 800)
    height = geometry.get('HEIGHT', 600)
    
    with mss.mss() as sct:
        monitor = {"top": y, "left": x, "width": width, "height": height}
        screenshot = sct.grab(monitor)
        img = np.array(screenshot)
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        return img


# ============================================================
# DEEP Q NETWORK IMPLEMENTATION
# ============================================================

# Experience tuple for replay buffer
Experience = namedtuple('Experience', ['state', 'action', 'reward', 'next_state', 'done'])


class DQN(nn.Module):
    """Deep Q Network with CNN architecture for processing game frames."""
    
    def __init__(self, n_actions):
        super(DQN, self).__init__()
        
        # Convolutional layers
        self.conv1 = nn.Conv2d(4, 32, kernel_size=8, stride=4)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=4, stride=2)
        self.conv3 = nn.Conv2d(64, 64, kernel_size=3, stride=1)
        
        # Calculate size after convolutions: (84 -> 20 -> 9 -> 7)
        conv_output_size = 64 * 7 * 7
        
        # Fully connected layers
        self.fc1 = nn.Linear(conv_output_size, 512)
        self.fc2 = nn.Linear(512, n_actions)
        
    def forward(self, x):
        """Forward pass through the network."""
        x = F.relu(self.conv1(x))
        x = F.relu(self.conv2(x))
        x = F.relu(self.conv3(x))
        x = x.view(x.size(0), -1)  # Flatten
        x = F.relu(self.fc1(x))
        return self.fc2(x)


class ReplayMemory:
    """Experience Replay Buffer for storing and sampling experiences."""
    
    def __init__(self, capacity):
        self.memory = deque(maxlen=capacity)
    
    def push(self, *args):
        """Save an experience."""
        self.memory.append(Experience(*args))
    
    def sample(self, batch_size):
        """Sample a batch of experiences."""
        return random.sample(self.memory, batch_size)
    
    def __len__(self):
        return len(self.memory)


class DQNAgent:
    """Deep Q Learning Agent."""
    
    def __init__(self, n_actions, load_model=False):
        self.n_actions = n_actions
        self.epsilon = EPS_START
        
        # Policy network and target network
        self.policy_net = DQN(n_actions).to(DEVICE)
        self.target_net = DQN(n_actions).to(DEVICE)
        
        # Load model if requested
        if load_model:
            try:
                self.policy_net.load_state_dict(torch.load(MODEL_SAVE_PATH, map_location=DEVICE))
                print(f"Loaded model from {MODEL_SAVE_PATH}")
            except FileNotFoundError:
                print(f"No saved model found at {MODEL_SAVE_PATH}, starting fresh")
        
        self.target_net.load_state_dict(self.policy_net.state_dict())
        self.target_net.eval()
        
        # Optimizer and memory
        self.optimizer = optim.Adam(self.policy_net.parameters(), lr=LEARNING_RATE)
        self.memory = ReplayMemory(MEMORY_SIZE)
        
        # Frame stacking (keep last 4 frames)
        self.frame_stack = deque(maxlen=4)
        
    def preprocess_frame(self, frame):
        """Preprocess frame: grayscale, resize, normalize."""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        resized = cv2.resize(gray, (STATE_WIDTH, STATE_HEIGHT))
        normalized = resized.astype(np.float32) / 255.0
        return normalized
    
    def get_state(self, frame):
        """Get state from frame (stack 4 frames)."""
        processed = self.preprocess_frame(frame)
        self.frame_stack.append(processed)
        
        # If we don't have 4 frames yet, repeat the current frame
        while len(self.frame_stack) < 4:
            self.frame_stack.append(processed)
        
        # Stack frames along channel dimension
        state = np.stack(self.frame_stack, axis=0)
        return state
    
    def select_action(self, state, training=True):
        """Select action using epsilon-greedy policy."""
        if training and random.random() < self.epsilon:
            return random.randrange(self.n_actions)
        else:
            with torch.no_grad():
                state_tensor = torch.FloatTensor(state).unsqueeze(0).to(DEVICE)
                q_values = self.policy_net(state_tensor)
                return q_values.argmax().item()
    
    def optimize_model(self):
        """Perform one step of optimization."""
        if len(self.memory) < MIN_REPLAY_SIZE:
            return None
        
        # Sample batch
        experiences = self.memory.sample(BATCH_SIZE)
        batch = Experience(*zip(*experiences))
        
        # Convert to tensors
        state_batch = torch.FloatTensor(np.array(batch.state)).to(DEVICE)
        action_batch = torch.LongTensor(batch.action).to(DEVICE)
        reward_batch = torch.FloatTensor(batch.reward).to(DEVICE)
        next_state_batch = torch.FloatTensor(np.array(batch.next_state)).to(DEVICE)
        done_batch = torch.FloatTensor(batch.done).to(DEVICE)
        
        # Compute Q(s, a)
        q_values = self.policy_net(state_batch).gather(1, action_batch.unsqueeze(1))
        
        # Compute V(s') for all next states using target network
        with torch.no_grad():
            next_q_values = self.target_net(next_state_batch).max(1)[0]
            expected_q_values = reward_batch + (GAMMA * next_q_values * (1 - done_batch))
        
        # Compute loss
        loss = F.smooth_l1_loss(q_values.squeeze(), expected_q_values)
        
        # Optimize
        self.optimizer.zero_grad()
        loss.backward()
        # Gradient clipping for stability
        torch.nn.utils.clip_grad_norm_(self.policy_net.parameters(), 1.0)
        self.optimizer.step()
        
        return loss.item()
    
    def update_target_network(self):
        """Update target network with policy network weights."""
        self.target_net.load_state_dict(self.policy_net.state_dict())
    
    def decay_epsilon(self):
        """Decay epsilon for exploration."""
        self.epsilon = max(EPS_END, self.epsilon * EPS_DECAY)
    
    def save_model(self, path=MODEL_SAVE_PATH):
        """Save the model."""
        torch.save(self.policy_net.state_dict(), path)
        print(f"Model saved to {path}")


def send_key_to_window(window_id, key):
    """Send a keyboard input to the Ruffle window using xdotool."""
    try:
        # First focus the window, then send key with delay for proper registration
        subprocess.run(['xdotool', 'windowactivate', '--sync', window_id], 
                      timeout=0.2, check=False)
        subprocess.run(['xdotool', 'keydown', key], 
                      timeout=0.1, check=False)
        time.sleep(0.03)  # Hold key briefly
        subprocess.run(['xdotool', 'keyup', key], 
                      timeout=0.1, check=False)
    except Exception as e:
        pass  # Silently fail to avoid slowdowns


def execute_action(window_id, action):
    """
    Execute the action in the game.
    Actions: 0=Up, 1=Down, 2=Left, 3=Right, 4=Shoot, 5=No action
    """
    action_map = {
        0: 'Up',
        1: 'Down',
        2: 'Left',
        3: 'Right',
        4: 'space',
        5: None  # No action
    }
    
    key = action_map.get(action)
    if key:
        send_key_to_window(window_id, key)


def calculate_reward(detections, prev_detections, green_tank_pos, red_tank_pos, prev_red_distance, stuck_counter=0, window_id=None):
    """
    Calculate reward based on game state.
    
    Rewards:
    - Moving closer to enemy: +1.0
    - Stuck (wall collision): -1.0
    - Moving away from enemy: -0.5
    - Survival: +0.01 per frame
    - Path found to enemy: +0.5
    - Reaching target and firing: +5.0
    """
    reward = 0.01  # Base survival reward
    info = {'status': 'neutral', 'distance': None, 'stuck_counter': stuck_counter}
    
    # Distance threshold to consider "reached target" (in pixels)
    TARGET_REACH_THRESHOLD = 50
    # Threshold to detect if stuck (distance change less than this)
    STUCK_THRESHOLD = 2
    # How many frames of no movement = stuck
    STUCK_FRAMES = 5
    
    # Check if we have both tanks
    if green_tank_pos and red_tank_pos:
        # Calculate current distance
        distance = np.sqrt((green_tank_pos[0] - red_tank_pos[0])**2 + 
                          (green_tank_pos[1] - red_tank_pos[1])**2)
        info['distance'] = distance
        
        # Check if reached target - press "m" to fire!
        if distance < TARGET_REACH_THRESHOLD:
            info['status'] = 'reached_target'
            reward += 5.0  # Big reward for reaching target
            # Fire at the target!
            if window_id:
                send_key_to_window(window_id, 'm')
            print(f"[TARGET REACHED] Distance: {distance:.1f}px - FIRING!")
        
        # Check distance changes
        elif prev_red_distance is not None:
            distance_change = prev_red_distance - distance
            
            if distance_change > STUCK_THRESHOLD:
                # Distance is decreasing - moving towards target
                info['status'] = 'approaching'
                info['stuck_counter'] = 0  # Reset stuck counter
                reward += 1.0  # Positive reward for moving closer
                
            elif abs(distance_change) <= STUCK_THRESHOLD:
                # Distance not changing - possibly stuck/colliding with wall
                info['stuck_counter'] = stuck_counter + 1
                if info['stuck_counter'] >= STUCK_FRAMES:
                    info['status'] = 'stuck'
                    reward -= 1.0  # Penalty for being stuck
                    print(f"[STUCK] Distance unchanged for {info['stuck_counter']} frames - wall collision?")
                else:
                    info['status'] = 'stalling'
                    reward -= 0.1  # Small penalty for not making progress
                    
            else:
                # Distance is increasing - moving away from target
                info['status'] = 'retreating'
                info['stuck_counter'] = 0  # Reset stuck counter
                reward -= 0.5  # Penalty for moving away
        
        # Bonus for finding path
        if detections.get('path_found', False):
            reward += 0.5
        
        return reward, distance, info
    
    info['status'] = 'no_tanks'
    return reward, prev_red_distance, info


# ============================================================
# A* PATHFINDING ALGORITHM
# ============================================================

def create_obstacle_map(hsv_img, tank_contours=None, padding=WALL_PADDING):
    """Create a binary obstacle map - walls (by color) become obstacles."""
    # Use HSV color mask for walls instead of grayscale threshold
    obstacle_map = cv2.inRange(hsv_img, WALL_LOWER, WALL_UPPER)
    
    if padding > 0:
        kernel = np.ones((padding * 2 + 1, padding * 2 + 1), np.uint8)
        obstacle_map = cv2.dilate(obstacle_map, kernel, iterations=1)
    
    if tank_contours:
        for contour in tank_contours:
            x, y, w, h = cv2.boundingRect(contour)
            margin = 15
            x1, y1 = max(0, x - margin), max(0, y - margin)
            x2, y2 = min(obstacle_map.shape[1], x + w + margin), min(obstacle_map.shape[0], y + h + margin)
            obstacle_map[y1:y2, x1:x2] = 0
    
    return obstacle_map


def get_tank_center(contour):
    """Get the center point of a tank contour."""
    M = cv2.moments(contour)
    if M["m00"] != 0:
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])
    else:
        x, y, w, h = cv2.boundingRect(contour)
        cx, cy = x + w // 2, y + h // 2
    return (cx, cy)


def heuristic(a, b):
    """Manhattan distance heuristic for A*."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def astar(obstacle_map, start, goal, resolution=GRID_RESOLUTION):
    """
    A* pathfinding algorithm.
    
    Args:
        obstacle_map: Binary image where 255 = obstacle, 0 = free
        start: (x, y) starting position
        goal: (x, y) goal position
        resolution: Grid cell size for pathfinding (larger = faster but less precise)
    
    Returns:
        List of (x, y) points representing the path, or empty list if no path found
    """
    height, width = obstacle_map.shape
    
    start_grid = (start[0] // resolution, start[1] // resolution)
    goal_grid = (goal[0] // resolution, goal[1] // resolution)
    
    grid_width = width // resolution
    grid_height = height // resolution
    
    # Priority queue: (f_score, counter, node)
    open_set = []
    counter = 0
    heapq.heappush(open_set, (0, counter, start_grid))
    
    came_from = {}
    g_score = {start_grid: 0}
    f_score = {start_grid: heuristic(start_grid, goal_grid)}
    
    # 8-directional movement (including diagonals)
    directions = [
        (0, 1), (1, 0), (0, -1), (-1, 0),  # Cardinal
        (1, 1), (1, -1), (-1, 1), (-1, -1)  # Diagonal
    ]
    
    while open_set:
        current = heapq.heappop(open_set)[2]
        
        if current == goal_grid:
            # Reconstruct path
            path = []
            while current in came_from:
                pixel_x = current[0] * resolution + resolution // 2
                pixel_y = current[1] * resolution + resolution // 2
                path.append((pixel_x, pixel_y))
                current = came_from[current]
            path.append(start)
            path.reverse()
            path.append(goal)
            return path
        
        for dx, dy in directions:
            neighbor = (current[0] + dx, current[1] + dy)
            
            if not (0 <= neighbor[0] < grid_width and 0 <= neighbor[1] < grid_height):
                continue
            
            pixel_x = neighbor[0] * resolution + resolution // 2
            pixel_y = neighbor[1] * resolution + resolution // 2
            
            pixel_x = min(max(pixel_x, 0), width - 1)
            pixel_y = min(max(pixel_y, 0), height - 1)
            
            if obstacle_map[pixel_y, pixel_x] == 255:
                continue
            
            move_cost = 1.414 if dx != 0 and dy != 0 else 1.0
            tentative_g = g_score[current] + move_cost
            
            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score[neighbor] = tentative_g + heuristic(neighbor, goal_grid)
                counter += 1
                heapq.heappush(open_set, (f_score[neighbor], counter, neighbor))
    
    return []


def draw_path(img, path, color=PATH_COLOR, thickness=PATH_THICKNESS):
    """Draw the path on the image."""
    if len(path) < 2:
        return
    
    for i in range(len(path) - 1):
        pt1 = path[i]
        pt2 = path[i + 1]
        cv2.line(img, pt1, pt2, color, thickness)
    
    if path:
        cv2.circle(img, path[0], 8, (255, 255, 0), -1)   # Cyan circle at start
        cv2.circle(img, path[-1], 8, (255, 0, 255), -1)  # Magenta circle at end


# ============================================================
# DETECTION FUNCTIONS
# ============================================================

def detect_maze_size(gray):
    """Detect the maze border and return maze dimensions."""
    _, thresh_border = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)
    kernel_border = np.ones((7, 7), np.uint8)
    closed_border = cv2.morphologyEx(thresh_border, cv2.MORPH_CLOSE, kernel_border)
    border_contours, _ = cv2.findContours(closed_border, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if border_contours:
        maze_border = max(border_contours, key=cv2.contourArea)
        mx, my, mw, mh = cv2.boundingRect(maze_border)
        maze_size = max(mw, mh)
        return maze_size, (mx, my, mw, mh)
    return None, None


def detect_walls(hsv, maze_size):
    """Detect walls in the maze using color-based detection."""
    wall_min_dimension = int(maze_size * WALL_MIN_PERCENT)
    
    # Use HSV color mask instead of grayscale threshold
    mask_walls = cv2.inRange(hsv, WALL_LOWER, WALL_UPPER)
    
    kernel_wall = np.ones((7, 7), np.uint8)
    closed = cv2.morphologyEx(mask_walls, cv2.MORPH_CLOSE, kernel_wall)
    kernel_open = np.ones((5, 5), np.uint8)
    cleaned = cv2.morphologyEx(closed, cv2.MORPH_OPEN, kernel_open)
    wall_contours, _ = cv2.findContours(cleaned, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    
    walls = []
    for contour in wall_contours:
        x, y, w, h = cv2.boundingRect(contour)
        if w >= wall_min_dimension or h >= wall_min_dimension:
            walls.append(contour)
    
    return walls


def detect_red_tanks(hsv):
    """Detect red tanks by color only."""
    mask_red1 = cv2.inRange(hsv, RED_LOWER1, RED_UPPER1)
    mask_red2 = cv2.inRange(hsv, RED_LOWER2, RED_UPPER2)
    mask_red = cv2.bitwise_or(mask_red1, mask_red2)
    
    kernel_tank = np.ones((3, 3), np.uint8)
    mask_red = cv2.morphologyEx(mask_red, cv2.MORPH_CLOSE, kernel_tank)
    mask_red = cv2.morphologyEx(mask_red, cv2.MORPH_OPEN, kernel_tank)
    
    red_contours, _ = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    return list(red_contours)


def detect_green_tanks(hsv):
    """Detect green tanks by color only."""
    mask_green = cv2.inRange(hsv, GREEN_LOWER, GREEN_UPPER)
    
    kernel_tank = np.ones((3, 3), np.uint8)
    mask_green = cv2.morphologyEx(mask_green, cv2.MORPH_CLOSE, kernel_tank)
    mask_green = cv2.morphologyEx(mask_green, cv2.MORPH_OPEN, kernel_tank)
    
    green_contours, _ = cv2.findContours(mask_green, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    return list(green_contours)


def detect_powerups(hsv, maze_size):
    """Detect powerups (gray, blue, yellow)."""
    powerup_min = int(maze_size * POWERUP_MIN_PERCENT)
    powerup_max = int(maze_size * POWERUP_MAX_PERCENT)
    
    mask_gray = cv2.inRange(hsv, GRAY_LOWER, GRAY_UPPER)
    mask_blue = cv2.inRange(hsv, BLUE_LOWER, BLUE_UPPER)
    mask_yellow = cv2.inRange(hsv, YELLOW_LOWER, YELLOW_UPPER)
    
    mask_powerups = cv2.bitwise_or(mask_gray, mask_blue)
    mask_powerups = cv2.bitwise_or(mask_powerups, mask_yellow)
    
    kernel_powerup = np.ones((3, 3), np.uint8)
    mask_powerups = cv2.morphologyEx(mask_powerups, cv2.MORPH_CLOSE, kernel_powerup)
    mask_powerups = cv2.morphologyEx(mask_powerups, cv2.MORPH_OPEN, kernel_powerup)
    
    powerup_contours, _ = cv2.findContours(mask_powerups, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    powerups = []
    for contour in powerup_contours:
        x, y, w, h = cv2.boundingRect(contour)
        if powerup_min <= w <= powerup_max and powerup_min <= h <= powerup_max:
            powerups.append(contour)
    
    return powerups


def detect_bullets(hsv):
    """Detect bullets (black objects)."""
    mask_bullets = cv2.inRange(hsv, BLACK_LOWER, BLACK_UPPER)
    
    kernel_bullet = np.ones((3, 3), np.uint8)
    mask_bullets = cv2.morphologyEx(mask_bullets, cv2.MORPH_CLOSE, kernel_bullet)
    mask_bullets = cv2.morphologyEx(mask_bullets, cv2.MORPH_OPEN, kernel_bullet)
    
    bullet_contours, _ = cv2.findContours(mask_bullets, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    bullets = []
    for contour in bullet_contours:
        x, y, w, h = cv2.boundingRect(contour)
        if BULLET_MIN_DIMENSION <= w <= BULLET_MAX_DIMENSION and BULLET_MIN_DIMENSION <= h <= BULLET_MAX_DIMENSION:
            bullets.append(contour)
    
    return bullets


def process_frame(img, return_positions=False):
    """Process a single frame and return the annotated result with detections."""
    # Crop to ROI (game area only)
    roi_height = min(ROI_Y2, img.shape[0]) - ROI_Y1
    roi_width = min(ROI_X2, img.shape[1]) - ROI_X1
    
    if roi_height <= 0 or roi_width <= 0:
        if return_positions:
            return img, {}, None, None
        return img, {}
    
    img_roi = img[ROI_Y1:ROI_Y1+roi_height, ROI_X1:ROI_X1+roi_width]
    
    # Create copies for different conversions
    gray = cv2.cvtColor(img_roi, cv2.COLOR_BGR2GRAY)
    hsv = cv2.cvtColor(img_roi, cv2.COLOR_BGR2HSV)
    result = img_roi.copy()
    
    # Detect maze size
    maze_size, maze_rect = detect_maze_size(gray)
    if maze_size is None:
        maze_size = max(img_roi.shape[0], img_roi.shape[1])
    
    # Detect all objects
    walls = detect_walls(hsv, maze_size)
    red_tanks = detect_red_tanks(hsv)
    green_tanks = detect_green_tanks(hsv)
    tanks = green_tanks + red_tanks  # Combined list for compatibility
    powerups = detect_powerups(hsv, maze_size)
    bullets = detect_bullets(hsv)
    
    # Get tank positions for DQN
    green_tank_pos = None
    red_tank_pos = None
    if len(green_tanks) >= 1:
        green_tank_pos = get_tank_center(green_tanks[0])
    if len(red_tanks) >= 1:
        red_tank_pos = get_tank_center(red_tanks[0])
    
    # Draw walls
    for contour in walls:
        cv2.drawContours(result, [contour], -1, WALL_COLOR, thickness=WALL_THICKNESS)
    
    # Draw red tanks with red border
    for contour in red_tanks:
        x, y, w, h = cv2.boundingRect(contour)
        cv2.drawContours(result, [contour], -1, RED_TANK_OUTLINE_COLOR, thickness=TANK_THICKNESS)
        cv2.rectangle(result, (x, y), (x + w, y + h), RED_TANK_OUTLINE_COLOR, thickness=TANK_THICKNESS)
    
    # Draw green tanks with green border
    for contour in green_tanks:
        x, y, w, h = cv2.boundingRect(contour)
        cv2.drawContours(result, [contour], -1, GREEN_TANK_OUTLINE_COLOR, thickness=TANK_THICKNESS)
        cv2.rectangle(result, (x, y), (x + w, y + h), GREEN_TANK_OUTLINE_COLOR, thickness=TANK_THICKNESS)
    
    # Draw powerups
    for contour in powerups:
        x, y, w, h = cv2.boundingRect(contour)
        cv2.drawContours(result, [contour], -1, POWERUP_OUTLINE_COLOR, thickness=POWERUP_THICKNESS)
        cv2.rectangle(result, (x, y), (x + w, y + h), POWERUP_OUTLINE_COLOR, thickness=POWERUP_THICKNESS)
    
    # Draw bullets
    for contour in bullets:
        x, y, w, h = cv2.boundingRect(contour)
        cv2.drawContours(result, [contour], -1, BULLET_OUTLINE_COLOR, thickness=BULLET_THICKNESS)
        cv2.rectangle(result, (x, y), (x + w, y + h), BULLET_OUTLINE_COLOR, thickness=BULLET_THICKNESS)
    
    # Pathfinding between tanks (green to red)
    path = []
    if len(green_tanks) >= 1 and len(red_tanks) >= 1:
        tank1_center = get_tank_center(green_tanks[0])
        tank2_center = get_tank_center(red_tanks[0])
        
        # Always draw the start and end dots regardless of path finding
        cv2.circle(result, tank1_center, 8, (255, 255, 0), -1)   # Cyan circle at green tank (start)
        cv2.circle(result, tank2_center, 8, (255, 0, 255), -1)   # Magenta circle at red tank (end)
        
        obstacle_map = create_obstacle_map(hsv, tank_contours=tanks, padding=WALL_PADDING)
        path = astar(obstacle_map, tank1_center, tank2_center)
        
        if path:
            draw_path(result, path)
    
    detections = {
        'walls': len(walls),
        'tanks': len(tanks),
        'powerups': len(powerups),
        'bullets': len(bullets),
        'path_found': len(path) > 0,
        'path_length': len(path)
    }
    
    if return_positions:
        return result, detections, green_tank_pos, red_tank_pos
    return result, detections


def train_dqn(num_episodes=1000, load_existing=False):
    """Train the DQN agent on the tank game."""
    print("=" * 60)
    print("DEEP Q LEARNING - Tank Game Training")
    print("=" * 60)
    print(f"\nDevice: {DEVICE}")
    print(f"Episodes: {num_episodes}")
    print(f"Learning Rate: {LEARNING_RATE}")
    print(f"Batch Size: {BATCH_SIZE}")
    print(f"Memory Size: {MEMORY_SIZE}")
    print("=" * 60)
    
    # Initialize agent
    agent = DQNAgent(N_ACTIONS, load_model=load_existing)
    
    # Find window
    print("\nSearching for Ruffle window...")
    window_id = find_ruffle_window()
    if not window_id:
        print("\nERROR: Could not find Ruffle window!")
        print("Make sure Ruffle is running with your game loaded.")
        print("\nTry running: ruffle ./az.swf")
        return
    
    print(f"Found Ruffle window: {window_id}")
    
    # Training statistics
    episode_rewards = []
    episode_losses = []
    
    for episode in range(num_episodes):
        print(f"\n{'='*60}")
        print(f"Episode {episode + 1}/{num_episodes} | Epsilon: {agent.epsilon:.4f}")
        print(f"{'='*60}")
        
        # Capture initial frame
        frame = capture_window(window_id)
        if frame is None:
            print("Failed to capture frame, skipping episode...")
            continue
        
        # Get initial state
        state = agent.get_state(frame)
        episode_reward = 0
        episode_loss = 0
        step_count = 0
        prev_detections = {}
        prev_red_distance = None
        stuck_counter = 0  # Track consecutive frames without distance change
        
        # Episode loop (max 500 steps per episode)
        for step in range(500):
            # Select action
            action = agent.select_action(state, training=True)
            
            # Execute action
            execute_action(window_id, action)
            time.sleep(0.05)  # Small delay for action to take effect
            
            # Capture next frame
            next_frame = capture_window(window_id)
            if next_frame is None:
                break
            
            # Process frame
            result, detections, green_pos, red_pos = process_frame(next_frame, return_positions=True)
            
            # Calculate reward with distance tracking and firing logic
            reward, prev_red_distance, reward_info = calculate_reward(
                detections, prev_detections, green_pos, red_pos, prev_red_distance,
                stuck_counter=stuck_counter, window_id=window_id
            )
            stuck_counter = reward_info.get('stuck_counter', 0)  # Update stuck counter
            
            # Get next state
            next_state = agent.get_state(next_frame)
            
            # Check if episode is done (only if no tanks for multiple frames)
            # Using 0 tanks as game over since 1 tank could be detection issue
            done = detections.get('tanks', 0) == 0
            
            # Store experience
            agent.memory.push(state, action, reward, next_state, done)
            
            # Move to next state
            state = next_state
            episode_reward += reward
            prev_detections = detections
            step_count += 1
            
            # Optimize model
            loss = agent.optimize_model()
            if loss is not None:
                episode_loss += loss
            
            # Display frame with DQN info
            if SHOW_DEBUG_INFO:
                info_y = 30
                cv2.putText(result, f"Episode: {episode + 1}/{num_episodes}", (10, info_y), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                info_y += 25
                cv2.putText(result, f"Step: {step + 1}", (10, info_y), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                info_y += 25
                cv2.putText(result, f"Action: {action}", (10, info_y), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                info_y += 25
                cv2.putText(result, f"Reward: {reward:.2f}", (10, info_y), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                info_y += 25
                cv2.putText(result, f"Epsilon: {agent.epsilon:.4f}", (10, info_y), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                info_y += 25
                cv2.putText(result, f"Memory: {len(agent.memory)}/{MEMORY_SIZE}", (10, info_y), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                # Display distance tracking info
                info_y += 25
                dist_val = reward_info.get('distance')
                dist_str = f"{dist_val:.1f}px" if dist_val else "N/A"
                cv2.putText(result, f"Distance: {dist_str}", (10, info_y), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
                info_y += 25
                status = reward_info.get('status', 'unknown')
                status_color = (0, 255, 0) if status == 'approaching' else (0, 0, 255) if status in ['stuck', 'retreating'] else (255, 255, 0)
                cv2.putText(result, f"Status: {status}", (10, info_y), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, status_color, 2)
            
            cv2.imshow('DQN Training', result)
            
            # Check for quit
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q') or key == ord('Q'):
                print("\nTraining interrupted by user")
                agent.save_model()
                cv2.destroyAllWindows()
                return
            
            if done:
                break
        
        # Episode statistics
        avg_loss = episode_loss / max(step_count, 1)
        episode_rewards.append(episode_reward)
        episode_losses.append(avg_loss)
        
        print(f"Steps: {step_count} | Reward: {episode_reward:.2f} | Avg Loss: {avg_loss:.4f}")
        
        # Update target network
        if (episode + 1) % TARGET_UPDATE == 0:
            agent.update_target_network()
            print(f"Target network updated!")
        
        # Decay epsilon
        agent.decay_epsilon()
        
        # Save model periodically
        if (episode + 1) % SAVE_EVERY_N_EPISODES == 0:
            agent.save_model()
            print(f"Model saved at episode {episode + 1}")
            
            # Print statistics
            if len(episode_rewards) >= 10:
                recent_avg_reward = np.mean(episode_rewards[-10:])
                print(f"Recent 10 episodes avg reward: {recent_avg_reward:.2f}")
    
    # Final save
    agent.save_model()
    cv2.destroyAllWindows()
    
    print("\n" + "=" * 60)
    print("TRAINING COMPLETED")
    print("=" * 60)
    print(f"Total episodes: {num_episodes}")
    print(f"Final epsilon: {agent.epsilon:.4f}")
    if episode_rewards:
        print(f"Average reward: {np.mean(episode_rewards):.2f}")
        print(f"Best reward: {np.max(episode_rewards):.2f}")
    print(f"Model saved to: {MODEL_SAVE_PATH}")


def main():
    """Main real-time processing loop."""
    print("=" * 60)
    print("REAL-TIME PATHFINDING - Ruffle Window Capture")
    print("=" * 60)
    print("\nSearching for Ruffle window...")
    
    window_id = find_ruffle_window()
    
    if not window_id:
        print("\nERROR: Could not find Ruffle window!")
        print("Make sure Ruffle is running with your game loaded.")
        print("\nTry running: ruffle ./az.swf")
        return
    
    print(f"Found Ruffle window: {window_id}")
    geometry = get_window_geometry(window_id)
    if geometry:
        print(f"Window size: {geometry.get('WIDTH', '?')}x{geometry.get('HEIGHT', '?')}")
    
    print("\nStarting real-time capture...")
    print("Press 'Q' to quit, 'S' to save current frame")
    print("-" * 60)
    
    frame_count = 0
    fps_start_time = time.time()
    fps = 0
    
    while True:
        loop_start = time.time()
        
        # Capture frame from Ruffle window
        frame = capture_window(window_id)
        
        if frame is None:
            print("Warning: Failed to capture frame. Window may have closed.")
            time.sleep(0.5)
            # Try to find window again
            window_id = find_ruffle_window()
            if not window_id:
                print("Ruffle window not found. Exiting...")
                break
            continue
        
        # Process the frame
        result, detections = process_frame(frame)
        
        # Calculate FPS
        frame_count += 1
        elapsed = time.time() - fps_start_time
        if elapsed >= 1.0:
            fps = frame_count / elapsed
            frame_count = 0
            fps_start_time = time.time()
        
        # Draw debug info
        if SHOW_DEBUG_INFO:
            info_y = 30
            cv2.putText(result, f"FPS: {fps:.1f}", (10, info_y), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            info_y += 25
            cv2.putText(result, f"Walls: {detections.get('walls', 0)}", (10, info_y), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, WALL_COLOR, 2)
            info_y += 22
            cv2.putText(result, f"Tanks: {detections.get('tanks', 0)}", (10, info_y), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, GREEN_TANK_OUTLINE_COLOR, 2)
            info_y += 22
            cv2.putText(result, f"Powerups: {detections.get('powerups', 0)}", (10, info_y), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, POWERUP_OUTLINE_COLOR, 2)
            info_y += 22
            cv2.putText(result, f"Bullets: {detections.get('bullets', 0)}", (10, info_y), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, BULLET_OUTLINE_COLOR, 2)
            info_y += 22
            path_status = "Found" if detections.get('path_found') else "Not found"
            cv2.putText(result, f"Path: {path_status}", (10, info_y), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, PATH_COLOR, 2)
        
        # Display the result
        cv2.imshow('Real-Time Pathfinding', result)
        
        # Handle keyboard input
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q') or key == ord('Q'):
            print("\nExiting...")
            break
        elif key == ord('s') or key == ord('S'):
            filename = f"capture_{int(time.time())}.png"
            cv2.imwrite(filename, result)
            print(f"Saved: {filename}")
        
        # Frame rate limiting
        elapsed_frame = time.time() - loop_start
        target_frame_time = 1.0 / TARGET_FPS
        if elapsed_frame < target_frame_time:
            time.sleep(target_frame_time - elapsed_frame)
    
    cv2.destroyAllWindows()
    print("\n=== SESSION ENDED ===")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == 'train':
        # DQN Training mode
        num_episodes = int(sys.argv[2]) if len(sys.argv) > 2 else 1000
        load_existing = '--load' in sys.argv
        train_dqn(num_episodes=num_episodes, load_existing=load_existing)
    else:
        # Regular pathfinding visualization mode
        main()
