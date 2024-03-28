import pika,json
from converter import mp3converter
from mongodb import updatstatus

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    def callback(ch, method, properties, body):
        err = mp3converter(body)
        if err:
            updatstatus(json.loads(body),{"video_status":"Error"})
            ch.basic_nack(delivery_tag=method.delivery_tag)
        else:
            ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(queue="video-queue", on_message_callback=callback)
    print("Waitting for messages, to exit press CTRL+C")

    channel.start_consuming()
    
if __name__ == '__main__':
    main()