"""
FAQ Chatbot - CodeAlpha Internship Task 2
Author: Built with Python, NLTK, Flask
Description: NLP-powered FAQ chatbot using cosine similarity for intent matching
"""

import json
import re
import math
import string
from collections import Counter
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse

# ─────────────────────────────────────────────
#  FAQ DATA  (topic: Python Programming)
# ─────────────────────────────────────────────
FAQ_DATA = [
    {
        "id": 1,
        "question": "What is Python?",
        "answer": "Python is a high-level, interpreted programming language known for its clean, readable syntax. Created by Guido van Rossum in 1991, it supports multiple programming paradigms — procedural, object-oriented, and functional. Python is widely used in web development, data science, AI/ML, automation, and scripting."
    },
    {
        "id": 2,
        "question": "How do I install Python?",
        "answer": "To install Python: 1) Visit python.org/downloads and download the latest version. 2) Run the installer and check 'Add Python to PATH'. 3) Verify installation by typing 'python --version' in your terminal. On Linux/macOS, Python is often pre-installed or available via package managers like apt or brew."
    },
    {
        "id": 3,
        "question": "What is a variable in Python?",
        "answer": "A variable in Python is a named container that stores a value. Unlike other languages, Python uses dynamic typing — you don't need to declare the type. Example: name = 'Alice', age = 25, is_active = True. Variables can hold any data type and can be reassigned at any time."
    },
    {
        "id": 4,
        "question": "What are Python data types?",
        "answer": "Python's built-in data types include: int (integers like 42), float (decimals like 3.14), str (text like 'hello'), bool (True/False), list (ordered mutable collection), tuple (ordered immutable collection), dict (key-value pairs), and set (unique unordered items). Use type() to check a variable's type."
    },
    {
        "id": 5,
        "question": "What is a list in Python?",
        "answer": "A list is an ordered, mutable collection of items enclosed in square brackets. Example: fruits = ['apple', 'banana', 'cherry']. Lists can hold mixed data types, support indexing (fruits[0]), slicing, and methods like .append(), .remove(), .sort(), and .len(). They're one of Python's most versatile data structures."
    },
    {
        "id": 6,
        "question": "What is a dictionary in Python?",
        "answer": "A dictionary (dict) stores data as key-value pairs in curly braces. Example: person = {'name': 'Ali', 'age': 22}. Keys must be unique and immutable. Access values with person['name'], add items with person['city'] = 'Karachi', and iterate with .items(), .keys(), or .values() methods."
    },
    {
        "id": 7,
        "question": "How do I write a function in Python?",
        "answer": "Define a function using the 'def' keyword: def greet(name): return f'Hello, {name}!'. Call it with greet('Ali'). Functions can have default parameters (def add(a, b=0)), accept *args for variable arguments, and **kwargs for keyword arguments. Functions help organize reusable code blocks."
    },
    {
        "id": 8,
        "question": "What is a loop in Python?",
        "answer": "Python has two main loops: FOR loops iterate over sequences — 'for i in range(5): print(i)'. WHILE loops run as long as a condition is true — 'while x < 10: x += 1'. Use 'break' to exit a loop early, 'continue' to skip to the next iteration, and 'else' for code that runs after the loop finishes normally."
    },
    {
        "id": 9,
        "question": "What is object oriented programming in Python?",
        "answer": "OOP in Python uses classes and objects. A class is a blueprint: class Dog: def __init__(self, name): self.name = name. Objects are instances: my_dog = Dog('Rex'). Python supports encapsulation (hiding data), inheritance (child classes), and polymorphism (same method, different behavior). OOP helps organize complex programs."
    },
    {
        "id": 10,
        "question": "What are Python libraries?",
        "answer": "Python libraries are collections of pre-written code. Popular ones: NumPy (numerical computing), Pandas (data analysis), Matplotlib (plotting), Scikit-learn (machine learning), Flask/Django (web development), Requests (HTTP calls), and NLTK/SpaCy (NLP). Install them with pip: 'pip install library-name'."
    },
    {
        "id": 11,
        "question": "What is pip in Python?",
        "answer": "pip is Python's package installer. Use it to install, update, or remove packages from PyPI. Common commands: 'pip install package', 'pip uninstall package', 'pip list' (see installed packages), 'pip freeze > requirements.txt' (save dependencies), 'pip install -r requirements.txt' (install from file)."
    },
    {
        "id": 12,
        "question": "What is exception handling in Python?",
        "answer": "Exception handling uses try-except blocks to catch and handle errors gracefully. Example: try: result = 10/0 except ZeroDivisionError: print('Cannot divide by zero'). Use 'finally' for code that always runs, 'else' for code when no exception occurs, and 'raise' to throw custom exceptions."
    },
    {
        "id": 13,
        "question": "What is a lambda function in Python?",
        "answer": "A lambda is an anonymous one-line function. Syntax: lambda arguments: expression. Example: square = lambda x: x**2; square(5) returns 25. Lambdas are often used with map(), filter(), and sorted(). Example: sorted(names, key=lambda name: len(name)) sorts a list by string length."
    },
    {
        "id": 14,
        "question": "What is list comprehension in Python?",
        "answer": "List comprehension is a concise way to create lists. Syntax: [expression for item in iterable if condition]. Example: squares = [x**2 for x in range(10)] creates a list of squares. It's faster and more Pythonic than a traditional for loop. You can also do dict comprehensions {k:v for k,v in items} and set comprehensions."
    },
    {
        "id": 15,
        "question": "How do I read and write files in Python?",
        "answer": "Use the open() function with modes: 'r' (read), 'w' (write, overwrites), 'a' (append), 'rb'/'wb' (binary). Best practice uses 'with': with open('file.txt', 'r') as f: content = f.read(). For writing: with open('file.txt', 'w') as f: f.write('Hello!'). The 'with' statement automatically closes the file."
    },
    {
        "id": 16,
        "question": "What is the difference between append and extend in Python lists?",
        "answer": ".append() adds a single item to the end of a list: list.append(4) adds the value 4. .extend() adds multiple items by iterating over another iterable: list.extend([4,5,6]) adds three items. Using append([4,5,6]) would add the entire list as a single nested element instead of three separate items."
    },
    {
        "id": 17,
        "question": "What is a Python tuple?",
        "answer": "A tuple is an ordered, immutable sequence in parentheses: coords = (10, 20). Unlike lists, tuples can't be changed after creation. They're faster and used for fixed data like coordinates, RGB values, or database records. Tuples support indexing, slicing, and unpacking: x, y = coords."
    },
    {
        "id": 18,
        "question": "What is string formatting in Python?",
        "answer": "Python offers several ways to format strings: 1) f-strings (modern): f'Hello {name}'. 2) .format(): 'Hello {}'.format(name). 3) % operator (old style): 'Hello %s' % name. f-strings are the recommended approach — they're fast, readable, and support expressions directly: f'Result: {2 + 2}' or f'{value:.2f}' for floats."
    },
    {
        "id": 19,
        "question": "What is recursion in Python?",
        "answer": "Recursion is when a function calls itself. Example: def factorial(n): return 1 if n == 0 else n * factorial(n-1). Every recursive function needs a base case to stop. Python's default recursion limit is 1000 (changeable with sys.setrecursionlimit()). Recursion is elegant for tree traversal, sorting algorithms, and mathematical sequences."
    },
    {
        "id": 20,
        "question": "How do I use virtual environments in Python?",
        "answer": "Virtual environments isolate project dependencies. Create one: 'python -m venv myenv'. Activate it: Windows: 'myenv\\Scripts\\activate', Mac/Linux: 'source myenv/bin/activate'. Now pip installs only affect this environment. Deactivate with 'deactivate'. Use requirements.txt to share dependencies: 'pip freeze > requirements.txt'."
    }
]


# ─────────────────────────────────────────────
#  NLP PREPROCESSING  (using built-in + manual)
# ─────────────────────────────────────────────

# Basic English stop words (no external dependency needed)
STOP_WORDS = {
    'a', 'an', 'the', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
    'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
    'should', 'may', 'might', 'shall', 'can', 'need', 'dare', 'ought',
    'used', 'to', 'of', 'in', 'on', 'at', 'by', 'for', 'with', 'about',
    'against', 'between', 'into', 'through', 'during', 'before', 'after',
    'above', 'below', 'from', 'up', 'down', 'out', 'off', 'over', 'under',
    'again', 'further', 'then', 'once', 'and', 'but', 'or', 'nor', 'not',
    'so', 'yet', 'both', 'either', 'neither', 'if', 'because', 'as', 'while',
    'this', 'that', 'these', 'those', 'i', 'me', 'my', 'myself', 'we', 'our',
    'you', 'your', 'he', 'him', 'his', 'she', 'her', 'it', 'its', 'they',
    'them', 'their', 'what', 'which', 'who', 'whom', 'when', 'where', 'why',
    'how', 'all', 'each', 'every', 'more', 'most', 'other', 'some', 'such',
    'no', 'nor', 'only', 'own', 'same', 'than', 'too', 'very', 's', 't',
    'just', 'don', 'also', 'well', 'much', 'make', 'use', 'using', 'used',
    'tell', 'explain', 'describe', 'show', 'give', 'me', 'please', 'help'
}

# Synonyms / alternate words → canonical FAQ keyword mapping
SYNONYM_MAP = {
    'dict':          'dictionary',
    'dictionaries':  'dictionary',
    'dicts':         'dictionary',
    'lists':         'list',
    'tuples':        'tuple',
    'funcs':         'function',
    'func':          'function',
    'def':           'function',
    'oop':           'object',
    'classes':       'class',
    'objs':          'object',
    'venv':          'virtual',
    'virtualenv':    'virtual',
    'env':           'environment',
    'pkgs':          'packages',
    'pkg':           'package',
    'libs':          'library',
    'lib':           'library',
    'str':           'string',
    'int':           'integer',
    'nums':          'integer',
    'excep':         'exception',
    'err':           'exception',
    'error':         'exception',
    'try':           'exception',
    'catch':         'exception',
    'comprehensions':'comprehension',
    'recursive':     'recursion',
    'recurse':       'recursion',
    'stem':          'stemmer',
}


def tokenize(text):
    """Tokenize text into words (simple word-level tokenizer)."""
    # Lowercase and remove punctuation
    text = text.lower()
    text = re.sub(r'[^\w\s]', ' ', text)
    tokens = text.split()
    return tokens


def remove_stopwords(tokens):
    """Filter out common stop words."""
    return [t for t in tokens if t not in STOP_WORDS and len(t) > 1]


def simple_stem(word):
    """
    Very lightweight rule-based stemmer.
    Handles common English suffixes without any library.
    """
    # Protect important domain words from being mangled
    PROTECTED = {
        'python', 'pip', 'loop', 'loops', 'list', 'lists', 'dict',
        'dictionary', 'dictionaries', 'function', 'functions', 'class',
        'classes', 'object', 'objects', 'string', 'strings', 'tuple',
        'tuples', 'variable', 'variables', 'install', 'exception',
        'recursion', 'lambda', 'comprehension', 'environment', 'virtual',
        'type', 'types', 'format', 'formatting', 'module', 'modules',
        'package', 'packages', 'library', 'libraries', 'operator', 'file',
        'files', 'write', 'read', 'data', 'method', 'methods', 'index',
        'inherit', 'inheritance', 'oop', 'boolean', 'integer', 'float'
    }
    word = word.lower()
    if word in PROTECTED:
        return word
    suffixes = ['ing', 'tion', 'tions', 'ness', 'ment', 'ments',
                'ers', 'ings', 'ed', 'ly', 'es', 's']
    for suffix in suffixes:
        if word.endswith(suffix) and len(word) - len(suffix) >= 3:
            return word[:-len(suffix)]
    return word


def preprocess(text):
    """Full NLP pipeline: tokenize → remove stopwords → synonym map → stem."""
    tokens = tokenize(text)
    tokens = remove_stopwords(tokens)
    tokens = [SYNONYM_MAP.get(t, t) for t in tokens]  # synonym expansion
    tokens = [simple_stem(t) for t in tokens]
    return tokens


# ─────────────────────────────────────────────
#  TF-IDF + COSINE SIMILARITY ENGINE
# ─────────────────────────────────────────────

class FAQMatcher:
    def __init__(self, faqs):
        self.faqs = faqs
        self.faq_vectors = []
        self.vocab = set()
        self._build_index()

    def _build_index(self):
        """Pre-process all FAQs and build TF-IDF index."""
        # Weight question tokens 3x to make question-matching dominant
        processed_docs = []
        for faq in self.faqs:
            q_tokens = preprocess(faq['question']) * 3   # boost question weight
            a_tokens = preprocess(faq['answer'])
            combined = q_tokens + a_tokens
            processed_docs.append(combined)
            self.vocab.update(combined)

        self.vocab = list(self.vocab)
        vocab_index = {w: i for i, w in enumerate(self.vocab)}

        # Calculate IDF
        n_docs = len(processed_docs)
        df = Counter()
        for tokens in processed_docs:
            for word in set(tokens):
                df[word] += 1

        idf = {}
        for word in self.vocab:
            idf[word] = math.log((n_docs + 1) / (df.get(word, 0) + 1)) + 1

        # Calculate TF-IDF vectors for each FAQ
        for tokens in processed_docs:
            tf = Counter(tokens)
            total = len(tokens) if tokens else 1
            vector = {}
            for word in self.vocab:
                if tf[word] > 0:
                    vector[word] = (tf[word] / total) * idf[word]
            self.faq_vectors.append(vector)

    def _vectorize_query(self, tokens):
        """Convert user query tokens to a sparse TF-IDF vector."""
        tf = Counter(tokens)
        total = len(tokens) if tokens else 1
        vector = {}
        for word in tokens:
            if word in self.vocab:
                vector[word] = tf[word] / total
        return vector

    def _cosine_similarity(self, vec_a, vec_b):
        """Compute cosine similarity between two sparse vectors."""
        dot_product = sum(vec_a.get(k, 0) * vec_b.get(k, 0) for k in vec_a)
        mag_a = math.sqrt(sum(v ** 2 for v in vec_a.values()))
        mag_b = math.sqrt(sum(v ** 2 for v in vec_b.values()))
        if mag_a == 0 or mag_b == 0:
            return 0.0
        return dot_product / (mag_a * mag_b)

    def find_best_match(self, user_query, top_n=1):
        """Find the most similar FAQ to the user's query."""
        tokens = preprocess(user_query)
        if not tokens:
            return None, 0.0

        query_vec = self._vectorize_query(tokens)
        if not query_vec:
            return None, 0.0

        scores = []
        for i, faq_vec in enumerate(self.faq_vectors):
            score = self._cosine_similarity(query_vec, faq_vec)

            # Bonus: exact keyword match in FAQ question title
            faq_q_tokens = set(preprocess(self.faqs[i]['question']))
            overlap = sum(1 for t in tokens if t in faq_q_tokens)
            if overlap > 0:
                score += 0.10 * overlap   # small bonus per overlapping token

            scores.append((score, i))

        scores.sort(reverse=True)
        best_score, best_idx = scores[0]

        if best_score < 0.05:
            return None, best_score

        return self.faqs[best_idx], best_score


# Initialize the matcher once
matcher = FAQMatcher(FAQ_DATA)

CONFIDENCE_THRESHOLD = 0.08

# ─────────────────────────────────────────────
#  HTTP SERVER  (no Flask needed — pure stdlib)
# ─────────────────────────────────────────────

HTML_PAGE = open("index.html", encoding="utf-8").read()


class ChatHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        # Suppress default request logs
        pass

    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(HTML_PAGE.encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == '/chat':
            length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(length)
            try:
                data = json.loads(body)
                user_message = data.get('message', '').strip()

                if not user_message:
                    reply = {"answer": "Please type a question!", "confidence": 0, "matched": ""}
                else:
                    faq, score = matcher.find_best_match(user_message)
                    if faq and score >= CONFIDENCE_THRESHOLD:
                        reply = {
                            "answer": faq['answer'],
                            "confidence": round(score * 100, 1),
                            "matched": faq['question']
                        }
                    else:
                        reply = {
                            "answer": "I'm not sure about that one! 🤔 Try asking about Python topics like variables, loops, functions, lists, dictionaries, OOP, or pip.",
                            "confidence": 0,
                            "matched": ""
                        }

            except Exception as e:
                reply = {"answer": f"Error processing your message: {str(e)}", "confidence": 0, "matched": ""}

            response_bytes = json.dumps(reply).encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', str(len(response_bytes)))
            self.end_headers()
            self.wfile.write(response_bytes)

        else:
            self.send_response(404)
            self.end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()


if __name__ == '__main__':
    import os
    # Make sure we're in the right directory so index.html is found
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    PORT = 5000
    server = HTTPServer(('localhost', PORT), ChatHandler)
    print(f"\n{'='*50}")
    print(f"  🤖  FAQ Chatbot Server is RUNNING!")
    print(f"{'='*50}")
    print(f"  Open your browser and visit:")
    print(f"  http://localhost:{PORT}")
    print(f"{'='*50}")
    print(f"  Topic: Python Programming FAQs")
    print(f"  Questions loaded: {len(FAQ_DATA)}")
    print(f"  Press Ctrl+C to stop the server")
    print(f"{'='*50}\n")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n  Server stopped. Goodbye!")
        server.server_close()
