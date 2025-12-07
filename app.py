from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route('/user/<username>')
def show_user(username):
    return f"Hello, {username}"

@app.route('/post/<int:post_id>')
def show_post(post_id):
    return f"Это пост под номером: {post_id}"

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        return f'Попытка входа: {username}'
    else:
        return '''
            <form method="post">
                Логин: <input name="username"><br>
                Пароль: <input name="password" type="password"><br>
                <button type="submit">Войти</button>
            </form>
        '''
cars = {
    'ABC123456' : {"brand" : "BMW", "model" : "X1", "year" : 2018},
    'XYZ789654' : {"brand" : "Ford", "model" : "Focus", "year" : 2018},
    'XYZ789123' : {"brand" : "Honda", "model" : "Civic", "year" : 2018}
    }

@app.route('/api/car/<vin>', methods=['GET'])
def get_car(vin):
    car = cars.get(vin)

    if car:
        return jsonify(car), 200
    else:
        return jsonify(message='Car not found'), 404

# Калькулятор
@app.route('/calculator', methods=['GET', 'POST'])
def calculator():
    result = None
    error = False
    num1 = num2 = operation = ""
    
    if request.method == 'POST':
        try:
            num1_str = request.form.get('num1', '0')
            num2_str = request.form.get('num2', '0')
            
            if not num1_str.strip() or not num2_str.strip():
                result = "Ошибка: введите оба числа"
                error = True
            else:
                num1 = float(num1_str)
                num2 = float(num2_str)
                operation = request.form.get('operation', '+')
                
                if operation == '+':
                    result = num1 + num2
                elif operation == '-':
                    result = num1 - num2
                elif operation == '*':
                    result = num1 * num2
                elif operation == '/':
                    if num2 == 0:
                        result = "Нас в школе учили: делить на ноль нельзя!"
                        error = True
                    else:
                        result = num1 / num2
                else:
                    result = "Неизвестная операция"
                    error = True

                if result and not error and isinstance(result, float):
                    result = round(result, 10)
                    if result == int(result):
                        result = int(result)
                    
        except ValueError:
            result = "Ошибка: введите числа"
            error = True
        except Exception as e:
            result = f"Ошибка: {str(e)}"
            error = True
    
    return render_template('calculator.html', 
                          result=result, 
                          error=error,
                          num1=num1 if num1 != "" else "",
                          num2=num2 if num2 != "" else "",
                          operation=operation)

if __name__ == '__main__':
    app.run()
