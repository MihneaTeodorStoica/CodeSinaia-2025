from probability import get_response

while True:
    user_input = input('You: ').strip()
    if user_input == 'exit':
        break
    else: 
        print('Bot: ' + get_response(user_input))