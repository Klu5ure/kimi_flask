from flask import Flask, request, Response, stream_with_context
from application import client
from flask_cors import CORS

app = Flask(__name__)  # 创建一个Flask应用实例
CORS(app)

@app.route('/')  
def get_test():
    question = request.args.get('question')
    return f'Hello, World! {question}'

@app.route('/test')
def test():
    return Response('test', content_type='image/png')


# http://127.0.0.1:5000/stream?query=%E4%BD%A0%E5%A5%BD%E5%95%8A
@app.route('/stream')
def stream():
    print('enter')
    query = request.args.get('query', '')  # 假设问题是通过 GET 参数传递的

    def generate_response():
        response = client.chat.completions.create(
            model="moonshot-v1-8k",
            messages=[
                # {"role": "system", "content": kaguya},
                {"role": "user", "content": query}
            ],
            temperature=0.3,
            stream=True,
        )
        for idx, chunk in enumerate(response):
            chunk_message = chunk.choices[0].delta
            if not chunk_message.content:
                continue
            answer = chunk_message.content
            yield "data: %s\n\n" % answer.replace("\n","<br>")
        yield "data: [DONE]\n\n"

    return Response(stream_with_context(generate_response()), content_type="text/event-stream")


if __name__ == '__main__':
    app.run(debug=True)  # 运行应用，debug=True表示开启调试模式