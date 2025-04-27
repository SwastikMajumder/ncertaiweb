from flask import Flask, Response, request, url_for, send_from_directory, redirect
import os
import mathai  # Your module for integration
import json
import urllib.parse

app = Flask(__name__)

@app.route('/stream')
def stream():
    equation = request.args.get('equation', '')
    equation = urllib.parse.unquote(equation)

    def event_stream():
        def sse_log(message):
            message_obj = {
                "type": "logging",
                "content": message
            }
            yield f"data: {json.dumps(message_obj)}\n\n"

        # Call your integration function
        yield from mathai.integrate_fx(equation, sse_log)

    return Response(event_stream(), mimetype="text/event-stream")


@app.route('/integration/')
def index():
    equation = request.args.get('equation', '')
    decoded_equation = urllib.parse.unquote(equation)

    return f"""
    <html>
    <head>
        <title>Integration Solver</title>
        <link rel="stylesheet" href="{url_for('static', filename='renderMath.css')}">
    </head>
    <body>
        <!-- Input and Button -->
        <div style="margin-bottom: 20px;">
            <input type="text" id="equation-input" style="padding: 5px; width: 600px;" value="{decoded_equation}">
            <button id="submit-button" style="padding: 5px;">Integrate</button>
        </div>

        <!-- Math Tree Render Area -->
        <div id="math-tree-output" style="border: 1px solid #ccc; padding: 10px; margin-bottom: 20px;">
            <div id="tree-area" class="math-container"></div>
        </div>

        <!-- Log Output Area -->
        <div id="log-output" style="border: 1px solid #aaa; padding: 10px;">
            <div id="output"></div>
        </div>

        <script src="{url_for('static', filename='renderMath.js')}"></script>
        <script>
            document.addEventListener('DOMContentLoaded', function() {{
                const equation = "{decoded_equation}";
                const outputDiv = document.getElementById('output');
                const treeDiv = document.getElementById('tree-area');
                const submitButton = document.getElementById('submit-button');
                const equationInput = document.getElementById('equation-input');

                submitButton.addEventListener('click', function() {{
                    
                    const url = '/integration/?equation=' + encodeURIComponent(equationInput.value);
                    if (url) {{
                        window.location.href = url;
                    }}
                }});

                if (equation) {{
                    const streamUrl = '/stream?equation=' + encodeURIComponent(equation);
                    const eventSource = new EventSource(streamUrl);

                    eventSource.onmessage = function(event) {{
                        let data;
                        try {{
                            data = JSON.parse(event.data);
                        }} catch (e) {{
                            console.error('Parse error:', e);
                            return;
                        }}

                        if (data.type === 'math_tree') {{
                            treeDiv.innerHTML = '';
                            renderMathTree(data.content, treeDiv);
                        }} else {{
                            outputDiv.innerHTML += '<p>' + data.content + '</p>';
                        }}
                    }};

                    eventSource.onerror = function(err) {{
                        console.error('Stream error:', err);
                        eventSource.close();
                    }};
                }}
            }});
        </script>
    </body>
    </html>
    """

@app.route('/images/<filename>')
def get_image(filename):
    return send_from_directory(os.path.join(app.root_path, 'static', 'images'), filename)

database_data = {
    'Class 12': {
        'Mathematics': {
            'Chapter 7 - Integrals': {
                'Exercise 7.1': {
                    'Question 1': {
                        'url': '/integration/?equation=sin(2*x)',
                        'image': '/images/question1.PNG'
                    },
                    'Question 2': {
                        'url': '/integration/?equation=cos(3*x)',
                        'image': '/images/question2.PNG'
                    },
                    'Question 3': {
                        'url': '/integration/?equation=e^(2*x)',
                        'image': '/images/question3.PNG'
                    },
                    'Question 4': {
                        'url': '/integration/?equation=%28a%2Ax%20%2B%20b%29%5E2',
                        'image': '/images/question4.PNG'
                    },
                    'Question 5': {
                        'url': '/integration/?equation=sin%282*x%29-4*e%5E%283*x%29',
                        'image': '/images/question5.PNG'
                    },
                    'Question 6': {
                        'url': '/integration/?equation=4*e%5E%283*x%29%2B1',
                        'image': '/images/question6.PNG'
                    },
                    'Question 7': {
                        'url': '/integration/?equation=x%5E2*(1-1%2Fx%5E2)',
                        'image': '/images/question7.PNG'
                    },
                    'Question 8': {
                        'url': '/integration/?equation=a*x%5E2%2Bb*x%2Bc',
                        'image': '/images/question8.PNG'
                    },
                    'Question 9': {
                        'url': '/integration/?equation=2*x%5E2%2Be%5Ex',
                        'image': '/images/question9.PNG'
                    },
                    'Question 10': {
                        'url': '/integration/?equation=%28x%5E%281%2F2%29-x%5E%28-1%2F2%29%29%5E2',
                        'image': '/images/question10.PNG'
                    },
                    'Question 11': {
                        'url': '/integration/?equation=%28x%5E3%2B5*x%5E2-4%29%2Fx%5E2',
                        'image': '/images/question11.PNG'
                    },
                    'Question 12': {
                        'url': '/integration/?equation=%28x%5E3%2B3*x%2B4%29%2F%28x%5E%281%2F2%29%29',
                        'image': '/images/question12.PNG'
                    },
                    'Question 13': {
                        'url': '/integration/?equation=%28x%5E3-x%5E2%2Bx-1%29%2F%28x-1%29',
                        'image': '/images/question13.PNG'
                    },
                    'Question 14': {
                        'url': '/integration/?equation=%281-x%29*x%5E%281%2F2%29',
                        'image': '/images/question14.PNG'
                    },
                    'Question 15': {
                        'url': '/integration/?equation=x%5E%281%2F2%29%20*%20%283*x%5E2%20%2B%202*x%20%2B%203%29',
                        'image': '/images/question15.PNG'
                    },
                    'Question 16': {
                        'url': '/integration/?equation=2*x%20-%203*cos%28x%29%20%2B%20e%5Ex',
                        'image': '/images/question16.PNG'
                    },
                    'Question 17': {
                        'url': '/integration/?equation=2*x%5E2-3*sin%28x%29%2B5*x%5E%281%2F2%29',
                        'image': '/images/question17.PNG'
                    },
                    'Question 18': {
                        'url': '/integration/?equation=sec%28x%29%28sec%28x%29%2Btan%28x%29%29',
                        'image': '/images/question18.PNG'
                    },
                    'Question 19': {
                        'url': '/integration/?equation=sec%28x%29%5E2%2Fcosec%28x%29%5E2',
                        'image': '/images/question19.PNG'
                    },
                    'Question 20': {
                        'url': '/integration/?equation=%282-3*sin%28x%29%29%2F%28cos%28x%29%5E2%29',
                        'image': '/images/question20.PNG'
                    },
                    'Question 21': {
                        'url': '/integration/?equation=x%5E%281%2F2%29%20%2B%201%2Fx%5E%281%2F2%29',
                        'image': '/images/question21.PNG'
                    }
                }
            }
        }
    }
}

def generate_accordion(data, level=0):
    """Generates accordion-style collapsible sections from the data recursively."""
    html = ''
    if level == 0:
        html += '<div class="accordion">'

    for key, value in data.items():
        if isinstance(value, dict) and 'url' not in value:
            # This is a nested section like a chapter or subject
            html += f'''
                <div class="accordion-item">
                    <button class="accordion-button">{"  " * level + key}</button>
                    <div class="panel">
                        {generate_accordion(value, level + 1)}
                    </div>
                </div>
            '''
        else:
            # This is a leaf node with actual question data
            url = value.get('url', '')
            image = value.get('image', '')
            html += f'''
                <div class="question-item">
                    <h4>{key}</h4>
                    <a href="#" onclick="showContent('{url}', '{image}'); return false;">View Solution</a><br/>
                </div>
            '''

    if level == 0:
        html += '</div>'
    return html

@app.route('/')
def home():
    return redirect(url_for('ncert_index'))

@app.route('/ncert/')
def ncert_index():
    accordion = generate_accordion(database_data)
    return f'''
    <html>
    <head>
        <title>NCERT Solutions</title>
        <link rel="stylesheet" href="/static/ncert/ncert_style.css">
        <script src="/static/ncert/ncert_script.js"></script>
    </head>
    <body>
        {accordion}
        <div class="content-area" style="margin-top: 30px;">
            <img id="contentImage" src="" style="max-width: 100%; display: none; margin-bottom: 15px;" />
            <iframe id="contentIframe" src="" style="width: 100%; height: 500px; border: 1px solid #ccc; display: none;"></iframe>
        </div>
    </body>
    </html>
    '''

@app.route('/ncert/<path:filename>')
def ncert_files(filename):
    return send_from_directory('ncert', filename)

@app.route('/static/ncert/<path:filename>')
def serve_ncert_static(filename):
    return send_from_directory('static/ncert', filename)

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

@app.route('/images/<path:filename>')
def serve_images(filename):
    return send_from_directory('static/images', filename)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
