import os
import sys
import time
from base import channel

def main():
    def listener(ch, method, properties, body):
          print(f" [x] Recibido notificacion sesion id:  {body.decode()}")
          time.sleep(body.count(b'.'))
          print(" [x] Done")
    
    channel.basic_consume(queue='notification_queue', on_message_callback=listener, auto_ack=True)
    print(' [*] Waiting for more notifications. To exit press CTRL+C')
    channel.start_consuming()
    
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)