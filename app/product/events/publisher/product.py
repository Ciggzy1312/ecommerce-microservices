from events.publisher.base import basePublisher

async def productCreatedPublisher(topicName: str, data):
    message, error = await basePublisher(topicName, data)

    if error:
        print(error)

    print(message)
    return

async def productUpdatedPublisher(topicName: str, data):
    message, error = await basePublisher(topicName, data)

    if error:
        print(error)

    print(message)
    return