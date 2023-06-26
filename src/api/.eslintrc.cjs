module.exports = {
    'env': {
        'node': true,
        'es2021': true,
    },
    'extends': [
        'eslint:recommended',
        "plugin:@typescript-eslint/recommended"
    ],
    'overrides': [
    ],
    'parserOptions': {
        'ecmaVersion': 'latest',
        'sourceType': 'module'
    },
    'rules': {
        'indent': [
            'error',
            4
        ],
        'linebreak-style': [
            'error',
            'unix'
        ],
        'quotes': [
            'error',
            'single'
        ],
        'semi': [
            'error',
            'never'
        ]
    }
}