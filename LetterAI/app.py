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
    elif data['page_id'] == 'info-menu':
        content = render_template('info.html')
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
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": data['message']}
            ]
        )
    except Exception as e:
        app.logger.error(f'Exception occurred: {e}')
        return jsonify({'error': str(e)}), 500

    return jsonify({'message': response['choices'][0]['message']['content']})

if __name__ == '__main__':
    app.run(port=5000, debug=True)