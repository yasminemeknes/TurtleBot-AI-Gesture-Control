import rclpy # type: ignore
from rclpy.node import Node # pyright: ignore[reportMissingImports]
from geometry_msgs.msg import TwistStamped # pyright: ignore[reportMissingImports]
import cv2 # pyright: ignore[reportMissingImports]
from ultralytics import YOLO # pyright: ignore[reportMissingImports]
import threading

class GestureController(Node):
    def __init__(self):
        super().__init__('gesture_controller')
        self.publisher_ = self.create_publisher(TwistStamped, 'cmd_vel', 10)
        self.model = YOLO('yolov8n.pt')
        
        # --- CONFIGURATION CAMERA ---
        self.url = 'http://10.23.96.218:8080/video' # Remplacez par votre IP
        self.cap = cv2.VideoCapture(self.url)
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1) 
        
        self.latest_frame = None
        self.running = True
        self.thread = threading.Thread(target=self.update_frame, daemon=True)
        self.thread.start()
        self.create_timer(0.1, self.timer_callback)

    def update_frame(self):
        while self.running:
            ret, frame = self.cap.read()
            if ret: self.latest_frame = frame

    def timer_callback(self):
        if self.latest_frame is None: return
        frame = cv2.flip(self.latest_frame, 1)
        results = self.model(frame, verbose=False, imgsz=160) # Inférence rapide
        
        msg = TwistStamped()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'base_link'
        head, hand = None, None

        for r in results:
            for box in r.boxes:
                x1, y1, x2, y2 = box.xyxy[0]
                cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
                if int(box.cls[0]) == 0: head = (cx, y1 + 40)
                else: hand = (cx, cy)

        if head and hand:
            dx = hand[0] - head[0]
            if dx > 70: msg.twist.angular.z = -1.0 # Droite
            elif dx < -70: msg.twist.angular.z = 1.0 # Gauche
            else: msg.twist.linear.x = 0.5 # Avance
        
        self.publisher_.publish(msg)
        cv2.imshow('Pilotage IA', frame)
        cv2.waitKey(1)

def main():
    rclpy.init()
    node = GestureController()
    try: rclpy.spin(node)
    except KeyboardInterrupt: pass
    finally:
        node.running = False
        cv2.destroyAllWindows()
        rclpy.shutdown()