from flask import Flask, request, jsonify, render_template
import openai

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/get_page_content', methods=['POST'])
def get_page_content():
    data = request.get_json()

    if 'page_id' not in data:
        return jsonify({'error': 'No page ID provided'}), 400

    if data['page_id'] == 'home-menu':
        content = render_template('home.html')
    elif data['page_id'] == 'settings-menu':
        content = render_template('settings.html')
    else:
        return jsonify({'error': 'Invalid page ID'}), 400

    return jsonify({'content': content})


@app.route('/api/gpt', methods=['POST'])
def generate_text():
    data = request.get_json()

    if 'message' not in data or 'api_key' not in data:
        return jsonify({'error': 'No message or API key provided'}), 400

    try:
        openai.api_key = data['api_key']
        response = openai.ChatCompletion.create(
          model="gpt-3.5-turbo",
          messages=[
                {
                    "role": "system", 
                    "content": "당신은 프로페셔널 편지 작성자입니다. 제가 상황을 제시하겠습니다. 당신은 해당 상황에 알맞은 정중하고 적절한 편지를 작성해야 합니다. 이 편지는 주어진 상황에 대한 이해와 배려를 반영하며, 적절한 어조와 맞춤법,  너무 정중하지 않고, 내용을 이해하기 쉽고 간결하게 100 ~ 500글자 수의 문장 구조를 사용해야 합니다."
                },
                {
                    "role": "user", 
                    "content": data['message']
                }
            ]
        )
        app.logger.debug(jsonify({'message': response['choices'][0]['message']['content']}))
    except Exception as e:
        app.logger.error(f'Exception occurred: {e}')
        return jsonify({'error': str(e)}), 500

    return jsonify({'message': response['choices'][0]['message']['content']})

if __name__ == '__main__':
    app.run(port=5000, debug=True)