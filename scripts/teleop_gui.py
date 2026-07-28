#!/usr/bin/env python3
import os
import sys
import threading
import tkinter as tk
from geometry_msgs.msg import Twist
import rclpy
from rclpy.node import Node

# --- CONFIGURABLE SPEED CONSTANTS ---
DEFAULT_LINEAR_SPEED = 0.15   # m/s
DEFAULT_ANGULAR_SPEED = 0.8   # rad/s
PUBLISH_FREQUENCY_HZ = 10     # Hz (publish rate when held)


class TeleopGuiNode(Node):
    def __init__(self):
        super().__init__('teleop_gui')
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        self.linear_speed = DEFAULT_LINEAR_SPEED
        self.angular_speed = DEFAULT_ANGULAR_SPEED
        self.current_twist = Twist()
        self.lock = threading.Lock()

        # Timer to publish velocity at 10 Hz
        timer_period = 1.0 / PUBLISH_FREQUENCY_HZ
        self.timer = self.create_timer(timer_period, self.publish_velocity)
        self.get_logger().info('Teleop GUI Node initialized, publishing to /cmd_vel')

    def set_cmd_vel(self, linear_x, angular_z):
        with self.lock:
            self.current_twist.linear.x = float(linear_x)
            self.current_twist.angular.z = float(angular_z)

    def stop_robot(self):
        with self.lock:
            self.current_twist.linear.x = 0.0
            self.current_twist.linear.y = 0.0
            self.current_twist.linear.z = 0.0
            self.current_twist.angular.x = 0.0
            self.current_twist.angular.y = 0.0
            self.current_twist.angular.z = 0.0

    def publish_velocity(self):
        with self.lock:
            msg = Twist()
            msg.linear.x = self.current_twist.linear.x
            msg.angular.z = self.current_twist.angular.z
            self.publisher_.publish(msg)


class TeleopApp:
    def __init__(self, root, ros_node):
        self.root = root
        self.ros_node = ros_node
        self.root.title("TurtleBot3 Teleop Controller")
        self.root.geometry("380x520")
        self.root.resizable(False, False)
        self.root.configure(bg="#1E1E2E")

        # Styling
        btn_font = ("Helvetica", 12, "bold")
        lbl_font = ("Helvetica", 13, "bold")

        title_lbl = tk.Label(root, text="TurtleBot3 Teleop", font=lbl_font, fg="#CDD6F4", bg="#1E1E2E")
        title_lbl.pack(pady=8)

        # Gamepad Grid Container
        grid_frame = tk.Frame(root, bg="#1E1E2E")
        grid_frame.pack(pady=5)

        # UP Button
        btn_up = tk.Button(grid_frame, text="▲\nUP", font=btn_font, width=6, height=2,
                           bg="#89B4FA", fg="#11111B", activebackground="#B4BEFE", relief="raised", bd=3)
        btn_up.grid(row=0, column=1, padx=5, pady=5)
        self._bind_button(btn_up, 'lin', 1.0)

        # LEFT Button
        btn_left = tk.Button(grid_frame, text="◄\nLEFT", font=btn_font, width=6, height=2,
                            bg="#89B4FA", fg="#11111B", activebackground="#B4BEFE", relief="raised", bd=3)
        btn_left.grid(row=1, column=0, padx=5, pady=5)
        self._bind_button(btn_left, 'ang', 1.0)

        # STOP Button
        btn_stop = tk.Button(grid_frame, text="STOP", font=btn_font, width=6, height=2,
                            bg="#F38BA8", fg="#11111B", activebackground="#F5E0DC", relief="raised", bd=3,
                            command=self.on_stop_click)
        btn_stop.grid(row=1, column=1, padx=5, pady=5)

        # RIGHT Button
        btn_right = tk.Button(grid_frame, text="►\nRIGHT", font=btn_font, width=6, height=2,
                             bg="#89B4FA", fg="#11111B", activebackground="#B4BEFE", relief="raised", bd=3)
        btn_right.grid(row=1, column=2, padx=5, pady=5)
        self._bind_button(btn_right, 'ang', -1.0)

        # DOWN Button
        btn_down = tk.Button(grid_frame, text="DOWN\n▼", font=btn_font, width=6, height=2,
                             bg="#89B4FA", fg="#11111B", activebackground="#B4BEFE", relief="raised", bd=3)
        btn_down.grid(row=2, column=1, padx=5, pady=5)
        self._bind_button(btn_down, 'lin', -1.0)

        # --- SPEED SLIDERS CONTAINER ---
        slider_frame = tk.Frame(root, bg="#1E1E2E")
        slider_frame.pack(pady=10, fill="x", padx=20)

        # Linear Speed Slider
        self.slider_lin = tk.Scale(
            slider_frame, from_=0.02, to=0.50, resolution=0.01, orient=tk.HORIZONTAL,
            label="Linear Speed (m/s)", font=("Helvetica", 9, "bold"),
            bg="#1E1E2E", fg="#CDD6F4", highlightbackground="#1E1E2E",
            troughcolor="#313244", activebackground="#89B4FA",
            command=self.on_linear_slider_change
        )
        self.slider_lin.set(DEFAULT_LINEAR_SPEED)
        self.slider_lin.pack(fill="x", pady=4)

        # Angular Speed Slider
        self.slider_ang = tk.Scale(
            slider_frame, from_=0.10, to=2.00, resolution=0.05, orient=tk.HORIZONTAL,
            label="Angular Speed (rad/s)", font=("Helvetica", 9, "bold"),
            bg="#1E1E2E", fg="#CDD6F4", highlightbackground="#1E1E2E",
            troughcolor="#313244", activebackground="#89B4FA",
            command=self.on_angular_slider_change
        )
        self.slider_ang.set(DEFAULT_ANGULAR_SPEED)
        self.slider_ang.pack(fill="x", pady=4)

        # Keyboard bindings for arrow keys
        root.bind("<KeyPress-Up>", lambda e: self.ros_node.set_cmd_vel(self.ros_node.linear_speed, 0.0))
        root.bind("<KeyRelease-Up>", lambda e: self.ros_node.stop_robot())
        root.bind("<KeyPress-Down>", lambda e: self.ros_node.set_cmd_vel(-self.ros_node.linear_speed, 0.0))
        root.bind("<KeyRelease-Down>", lambda e: self.ros_node.stop_robot())
        root.bind("<KeyPress-Left>", lambda e: self.ros_node.set_cmd_vel(0.0, self.ros_node.angular_speed))
        root.bind("<KeyRelease-Left>", lambda e: self.ros_node.stop_robot())
        root.bind("<KeyPress-Right>", lambda e: self.ros_node.set_cmd_vel(0.0, -self.ros_node.angular_speed))
        root.bind("<KeyRelease-Right>", lambda e: self.ros_node.stop_robot())
        root.bind("<space>", lambda e: self.on_stop_click())

        root.protocol("WM_DELETE_WINDOW", self.on_close)

    def _bind_button(self, button, move_type, direction):
        def on_press(event):
            if move_type == 'lin':
                self.ros_node.set_cmd_vel(direction * self.ros_node.linear_speed, 0.0)
            elif move_type == 'ang':
                self.ros_node.set_cmd_vel(0.0, direction * self.ros_node.angular_speed)

        def on_release(event):
            self.ros_node.stop_robot()

        button.bind("<ButtonPress-1>", on_press)
        button.bind("<ButtonRelease-1>", on_release)

    def on_linear_slider_change(self, val):
        self.ros_node.linear_speed = float(val)

    def on_angular_slider_change(self, val):
        self.ros_node.angular_speed = float(val)

    def on_stop_click(self):
        self.ros_node.stop_robot()

    def on_close(self):
        self.ros_node.stop_robot()
        self.root.destroy()


def main(args=None):
    rclpy.init(args=args)
    node = TeleopGuiNode()

    spin_thread = threading.Thread(target=rclpy.spin, args=(node,), daemon=True)
    spin_thread.start()

    root = tk.Tk()
    app = TeleopApp(root, node)

    try:
        root.mainloop()
    except KeyboardInterrupt:
        pass
    finally:
        node.stop_robot()
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
