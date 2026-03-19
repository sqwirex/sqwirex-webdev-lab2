from flask import Flask, render_template, request, make_response
import re

app = Flask(__name__)
application = app

FULL_NAME = "Николаев Алексей Владимирович"
GROUP = "241-3211"


def normalize_phone(raw: str) -> str:
    digits = ''.join(ch for ch in raw if ch.isdigit())
    if len(digits) == 11 and digits[0] in '78':
        digits = '8' + digits[1:]
    elif len(digits) == 10:
        digits = '8' + digits
    return f"{digits[0]}-{digits[1:4]}-{digits[4:7]}-{digits[7:9]}-{digits[9:11]}"


def validate_phone(raw: str):
    allowed = set('0123456789-+(). ')
    if any(ch not in allowed for ch in raw):
        return False, 'Недопустимый ввод. В номере телефона встречаются недопустимые символы.'

    digits = ''.join(ch for ch in raw if ch.isdigit())
    starts_with_plus7_or_8 = raw.strip().startswith('+7') or raw.strip().startswith('8')

    if starts_with_plus7_or_8:
        if len(digits) != 11:
            return False, 'Недопустимый ввод. Неверное количество цифр.'
    else:
        if len(digits) != 10:
            return False, 'Недопустимый ввод. Неверное количество цифр.'

    return True, ''


@app.context_processor
def inject_user_data():
    return {'full_name': FULL_NAME, 'group_number': GROUP}


@app.route('/')
def index():
    return render_template('index.html', title='Лабораторная работа №2')


@app.route('/request/url')
def show_url_params():
    params = list(request.args.items())
    return render_template('request_data.html', title='Параметры URL', data_title='Параметры URL', rows=params)


@app.route('/request/headers')
def show_headers():
    headers = list(request.headers.items())
    return render_template('request_data.html', title='Заголовки запроса', data_title='Заголовки запроса', rows=headers)


@app.route('/request/cookies')
def show_cookies():
    cookies = list(request.cookies.items())
    response = make_response(render_template('request_data.html', title='Cookie', data_title='Cookie', rows=cookies))
    if 'demo_cookie' not in request.cookies:
        response.set_cookie('demo_cookie', 'flask-lab2')
    return response


@app.route('/login', methods=['GET', 'POST'])
def login():
    submitted = False
    form_data = {}
    if request.method == 'POST':
        submitted = True
        form_data = {
            'login': request.form.get('login', ''),
            'password': request.form.get('password', ''),
        }
    return render_template('login.html', title='Форма авторизации', submitted=submitted, form_data=form_data)


@app.route('/phone', methods=['GET', 'POST'])
def phone():
    phone_value = ''
    normalized = None
    error = None

    if request.method == 'POST':
        phone_value = request.form.get('phone', '')
        is_valid, error = validate_phone(phone_value)
        if is_valid:
            normalized = normalize_phone(phone_value)
            error = None

    return render_template('phone.html', title='Проверка телефона', phone_value=phone_value, normalized=normalized, error=error)


if __name__ == '__main__':
    app.run(debug=True)
