import pyrender
import trimesh
import numpy as np

class HomeAutomationSystem:
    def __init__(self):
        self.lights_on = False
        self.door_open = False
        self.scene = pyrender.Scene()

    def create_room(self):
       
        
        floor = trimesh.primitives.Box(extents=[10, 0.1, 10])
        floor_mesh = pyrender.Mesh.from_trimesh(floor, smooth=False)
        floor_pose = np.eye(4)
        floor_pose[1, 3] = -0.05
        self.scene.add(floor_mesh, pose=floor_pose)

       
        wall = trimesh.primitives.Box(extents=[10, 5, 0.1])  # Single wall
        wall_mesh = pyrender.Mesh.from_trimesh(wall, smooth=False)

        
        for position, rotation in [([0, 2.5, -5], [0, 0, 0]),  # Back wall
                                    ([5, 2.5, 0], [0, np.pi / 2, 0]),  # Right wall
                                    ([-5, 2.5, 0], [0, -np.pi / 2, 0]),  # Left wall
                                    ([0, 5, 0], [np.pi / 2, 0, 0])]:  # Ceiling
            wall_pose = np.eye(4)
            wall_pose[:3, 3] = position
            wall_pose[:3, :3] = trimesh.transformations.euler_matrix(*rotation)[:3, :3]
            self.scene.add(wall_mesh, pose=wall_pose)

    def add_furniture(self, model_path, position):
        """Loads and adds furniture to the scene."""
        try:
            furniture = trimesh.load(model_path)
            furniture_mesh = pyrender.Mesh.from_trimesh(furniture, smooth=False)
            furniture_pose = np.eye(4)
            furniture_pose[:3, 3] = position
            self.scene.add(furniture_mesh, pose=furniture_pose)
        except Exception as e:
            print(f"Error loading furniture from {model_path}: {e}")

    


    def toggle_door(self):
        """Toggles the door state."""
        self.door_open = not self.door_open
        print(f"Door {'open' if self.door_open else 'closed'}.")

        # Add logic to animate or reposition the door here if applicable

    def visualize(self):
        """Visualizes the home and allows interaction."""
        self.create_room()

        # Add furniture
        self.add_furniture("chair.obj", [2, 0, 2])
        self.add_furniture("table.obj", [0, 0, 0])

        # Add a light source
        light = pyrender.PointLight(color=np.ones(3), intensity=1500.0 if self.lights_on else 0.0)
        light_pose = np.eye(4)
        light_pose[1, 3] = 5  # Position above the room
        self.scene.add(light, pose=light_pose)

        # Add a camera
        camera = pyrender.PerspectiveCamera(yfov=np.pi / 4)
        camera_pose = np.eye(4)
        camera_pose[2, 3] = 15  # Move back to view the scene
        camera_pose[1, 3] = 5  # Raise camera for a better angle
        self.scene.add(camera, pose=camera_pose)

        # Launch viewer
        pyrender.Viewer(self.scene, use_raymond_lighting=True)

    def start_automation(self):
        """Starts the automation system and listens for user commands."""
        print("Starting Home Automation System...")
        print("Commands: 'lights', 'door', 'exit'")

        while True:
            command = input("Enter command: ").strip().lower()
            if command == "lights":
                self.toggle_lights()
            elif command == "door":
                self.toggle_door()
            elif command == "exit":
                print("Exiting Home Automation System.")
                break
            else:
                print("Unknown command. Try 'lights', 'door', or 'exit'.")

# Initialize and run the system
home = HomeAutomationSystem()
home.start_automation()
