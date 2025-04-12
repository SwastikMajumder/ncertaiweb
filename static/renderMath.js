// renderMath.js

class TreeNode {
    constructor(name, children = []) {
        this.name = name;
        this.children = children;
    }
}

function renderMathTree(node, parentElement) {
    console.log("Rendering node:", node);

    if (!node) {
        return;
    }

    let nodeElement = document.createElement('span');

    if (node.name === 'f_div') {
        renderFraction(node.children[0], node.children[1], parentElement);
    } else if (node.name === 'f_pow') {
        renderMathTree(node.children[0], nodeElement);
        let exponentValue = document.createElement('span');
        renderMathTree(node.children[1], exponentValue);
        exponentValue.classList.add('exponent');
        nodeElement.appendChild(exponentValue);
    } else if (node.name === 'f_mul') {
        renderMathTree(node.children[0], nodeElement);
        renderMathTree(node.children[1], nodeElement); // Removed multiplication sign logic
    } else if (node.name === 'f_add') {
        for (let i = 0; i < node.children.length; i++) {
            if (node.children[i].name === 'f_neg') {
                let negativeSign = document.createElement('span');
                negativeSign.textContent = '-';
                negativeSign.classList.add('operator', 'add-sub', 'negative');
                nodeElement.appendChild(negativeSign);
                renderMathTree(node.children[i].children[0], nodeElement);
            } else {
                if (i > 0) {
                    let plusSign = document.createElement('span');
                    plusSign.textContent = '+';
                    plusSign.classList.add('operator', 'add-sub');
                    nodeElement.appendChild(plusSign);
                }
                renderMathTree(node.children[i], nodeElement);
            }
        }
    } else if (node.name.startsWith('f_') && node.children.length === 1) {
        let functionName = document.createElement('span');
        functionName.textContent = node.name.substring(2);
        functionName.classList.add('function');
        nodeElement.appendChild(functionName);
        let openingParen = document.createElement('span');
        openingParen.textContent = '(';
        nodeElement.appendChild(openingParen);
        renderMathTree(node.children[0], nodeElement);
        let closingParen = document.createElement('span');
        closingParen.textContent = ')';
        nodeElement.appendChild(closingParen);
    } else if (node.name.startsWith('v_')) {
        nodeElement.textContent = node.name.substring(2);
        nodeElement.classList.add("variable");
    } else if (node.name.startsWith('d_')) {
        nodeElement.textContent = node.name.substring(2);
    } else if (node.name.startsWith('s_')) {
        nodeElement.textContent = node.name.substring(2);
    } else if (node.name === 'f_neg') { // Handle standalone negation
        let negativeSign = document.createElement('span');
        negativeSign.textContent = '-';
        negativeSign.classList.add('operator', 'add-sub', 'negative');
        nodeElement.appendChild(negativeSign);
        renderMathTree(node.children[0], nodeElement);
    } else {
        nodeElement.textContent = node.name;
    }

    parentElement.appendChild(nodeElement);
}

function renderFraction(numeratorNode, denominatorNode, parentElement) {
    let fractionDiv = document.createElement('div');
    fractionDiv.classList.add('fraction');

    let numeratorDiv = document.createElement('div');
    numeratorDiv.classList.add('numerator');
    renderMathTree(numeratorNode, numeratorDiv);
    fractionDiv.appendChild(numeratorDiv);

    let hr = document.createElement('hr');
    fractionDiv.appendChild(hr);

    let denominatorDiv = document.createElement('div');
    denominatorDiv.classList.add('denominator');
    renderMathTree(denominatorNode, denominatorDiv);
    fractionDiv.appendChild(denominatorDiv);

    parentElement.appendChild(fractionDiv);
}