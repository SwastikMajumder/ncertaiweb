from flask import Flask, render_template, request, jsonify, send_from_directory, redirect, url_for
import os
import uuid
import mathai
from base import *
import parser
import time

app = Flask(__name__)

log_messages = []

@app.route('/integration/get_logs')
def get_logs():
    global log_messages
    tmp = log_messages
    log_messages = []
    return jsonify({"logs": tmp})

def solveneg(eq):
    if eq.name == "f_neg" and "f_neg" not in str_form(eq.children[0]) and "f_div" not in str_form(eq.children[0]):
        return mathai.solve(eq.children[0]).fx("neg")
    return TreeNode(eq.name, [solveneg(child) for child in eq.children])

def create_math_tree(eqstr):
    try:
        eq = eqstr
        eq = mathai.powermerge(eq)
        eq = conv(eq)
        eq = mathai.simplify(eq)
        alpha = ["x", "y", "z"]+[chr(x+ord("a")) for x in range(0,23)]
        eq2 = str_form(eq)
        for i in range(26):
            if "v_"+str(i) in eq2:
                eq = replace(eq, tree_form("v_"+str(i)), tree_form("v_"+alpha[i]))
        return eq.to_dict()
    except Exception as e:
        print(f"Error creating math tree: {e}")
        return {"error": str(e)}

def conv(eq):
    if eq.name in ["f_mul", "f_pow"]:
        lst = mathai.factorgen(eq)
        deno = [item.children[0] for item in lst if item.name == "f_pow" and item.children[1] == tree_form("d_-1")]
        if deno != []:
            num = [item for item in lst if item.name != "f_pow" or item.children[1] != tree_form("d_-1")]
            if num == []:
                num = [tree_form("d_1")]
            return TreeNode("f_div", [mathai.solve(mathai.product(num)), mathai.solve(mathai.product(deno))])
    return TreeNode(eq.name, [conv(child) for child in eq.children])

@app.route('/integration/integrate', methods=['POST'])
def integrate():
    global log_messages
    data = request.get_json()
    equation = data.get('expression')
    
    try:
        log_messages = []
        mathai.fxlog = send_log
        result = mathai.integratex(parser.take_input(equation), 3)
        result = mathai.solve(mathai.expand2(result))
        mathai.plog([mathai.tab, "the solution is ", result])
        send_log("END_LOG_COLLECTION")
        tree = create_math_tree(result)
        return jsonify({"tree": tree})
    except Exception as e:
        send_log(f"Error integrating: {e}")
        print(f"Error integrating: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/integration/integrate_url/<equation>')
def integrate_url(equation):
    global log_messages
    try:
        log_messages = []
        mathai.fxlog = send_log
        result = mathai.integratex(parser.take_input(equation), 3)
        result = mathai.solve(mathai.expand2(result))
        mathai.plog([mathai.tab, "the solution is ", result])
        send_log("END_LOG_COLLECTION")
        tree = create_math_tree(result)
        return jsonify({"tree": tree})
    except Exception as e:
        send_log(f"Error integrating: {e}")
        print(f"Error integrating: {e}")
        return jsonify({"error": str(e)}), 500

def send_log(message):
    log_messages.append(message)

@app.route('/integration/')
def index():
    return render_template('index.html')
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
                        'image': '/images/question1.png'
                    },
                    'Question 2': {
                        'url': '/integration/?equation=cos(3*x)',
                        'image': '/images/question2.png'
                    },
                    'Question 3': {
                        'url': '/integration/?equation=e^(2*x)',
                        'image': '/images/question3.png'
                    },
                    'Question 4': {
                        'url': '/integration/?equation=%28a%2Ax%20%2B%20b%29%5E2',
                        'image': '/images/question4.png'
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
    app.run(debug=True)
