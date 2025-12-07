import unittest
import json
import sys
import os
import app as tested_app

class AppPyTest(unittest.TestCase):

    def setUp(self):
        tested_app.app.config['TESTING'] = True
        self.app = tested_app.app.test_client()
    
    def test_get_home(self):
        retVal = self.app.get('/')
        self.assertEqual(retVal.status_code, 200)
        retVal_text = retVal.data.decode('utf-8')
        self.assertIn('Hello, world!', retVal_text)
    
    def test_post_home(self):
        retVal = self.app.post('/')
        self.assertEqual(retVal.status_code, 405)
    
    def test_user_route(self):
        retVal = self.app.get('/user/Sasha')
        self.assertEqual(retVal.status_code, 200)
        self.assertIn(b'Hello, Sasha', retVal.data)
    
    def test_post_route(self):
        retVal = self.app.get('/post/123')
        self.assertEqual(retVal.status_code, 200)
        self.assertIn(b'123', retVal.data)
    
    def test_login_get(self):
        retVal = self.app.get('/login')
        self.assertEqual(retVal.status_code, 200)
        retVal_text = retVal.data.decode('utf-8')
        self.assertIn('Логин:', retVal_text)
        self.assertIn('Пароль:', retVal_text)
        self.assertIn('Войти', retVal_text)
    
    def test_login_post(self):
        retVal = self.app.post('/login', data={
            'username': 'testuser',
            'password': 'testpass'
        })
        self.assertEqual(retVal.status_code, 200)
        retVal_text = retVal.data.decode('utf-8')
        self.assertIn('Попытка входа: testuser', retVal_text)

    # ТЕСТЫ КАЛЬКУЛЯТОРА     
    def test_calculator_page_get(self):
        """Тест загрузки страницы калькулятора (GET)"""
        retVal = self.app.get('/calculator')
        self.assertEqual(retVal.status_code, 200)
        retVal_text = retVal.data.decode('utf-8')
        
        # Проверяем наличие основных элементов на странице
        self.assertIn('Калькулятор', retVal_text)
        self.assertIn('Первое число', retVal_text)
        self.assertIn('Второе число', retVal_text)
        self.assertIn('Вычислить', retVal_text)
        self.assertIn('+', retVal_text)
        self.assertIn('-', retVal_text)
        self.assertIn('×', retVal_text)
        self.assertIn('÷', retVal_text)
    
    def test_calculator_addition_post(self):
        """Тест операции сложения через форму"""
        retVal = self.app.post('/calculator', data={
            'num1': '10',
            'num2': '5',
            'operation': '+'
        })
        
        self.assertEqual(retVal.status_code, 200)
        retVal_text = retVal.data.decode('utf-8')

        self.assertIn('Результат:', retVal_text)
        self.assertIn('10.0 + 5.0 =', retVal_text)
        self.assertIn('<strong>15</strong>', retVal_text)
    
    def test_calculator_subtraction_post(self):
        """Тест операции вычитания"""
        retVal = self.app.post('/calculator', data={
            'num1': '20',
            'num2': '7',
            'operation': '-'
        })
        
        self.assertEqual(retVal.status_code, 200)
        retVal_text = retVal.data.decode('utf-8')
        self.assertIn('Результат:', retVal_text)
        self.assertIn('20.0 - 7.0 =', retVal_text)
        self.assertIn('<strong>13</strong>', retVal_text)
    
    def test_calculator_multiplication_post(self):
        """Тест операции умножения"""
        retVal = self.app.post('/calculator', data={
            'num1': '6',
            'num2': '7',
            'operation': '*'
        })
        
        self.assertEqual(retVal.status_code, 200)
        retVal_text = retVal.data.decode('utf-8')
        self.assertIn('Результат:', retVal_text)
        self.assertIn('6.0 * 7.0 =', retVal_text)
        self.assertIn('<strong>42</strong>', retVal_text)
    
    def test_calculator_division_post(self):
        """Тест операции деления"""
        retVal = self.app.post('/calculator', data={
            'num1': '15',
            'num2': '3',
            'operation': '/'
        })
        
        self.assertEqual(retVal.status_code, 200)
        retVal_text = retVal.data.decode('utf-8')
        self.assertIn('Результат:', retVal_text)
        self.assertIn('15.0 / 3.0 =', retVal_text)
        self.assertIn('<strong>5</strong>', retVal_text)
    
    def test_calculator_division_by_zero(self):
        """Тест деления на ноль"""
        retVal = self.app.post('/calculator', data={
            'num1': '10',
            'num2': '0',
            'operation': '/'
        })
        
        self.assertEqual(retVal.status_code, 200)
        retVal_text = retVal.data.decode('utf-8')
        self.assertIn('Ошибка:', retVal_text)
        self.assertIn('Нас в школе учили: делить на ноль нельзя!', retVal_text)
    
    def test_calculator_invalid_input(self):
        """Тест некорректного ввода (не числа)"""
        retVal = self.app.post('/calculator', data={
            'num1': 'abc',
            'num2': '5',
            'operation': '+'
        })
        
        self.assertEqual(retVal.status_code, 200)
        retVal_text = retVal.data.decode('utf-8')
        self.assertIn('Ошибка:', retVal_text)
        self.assertIn('введите числа', retVal_text)
    
    def test_calculator_decimal_numbers(self):
        """Тест работы с десятичными числами"""
        retVal = self.app.post('/calculator', data={
            'num1': '3.14',
            'num2': '2.5',
            'operation': '+'
        })
        
        self.assertEqual(retVal.status_code, 200)
        retVal_text = retVal.data.decode('utf-8')
        self.assertIn('Результат:', retVal_text)
        self.assertIn('3.14 + 2.5 =', retVal_text)
        self.assertIn('5.64', retVal_text)
    
    def test_get_api(self):
        retVal = self.app.get('/api/car/ABC123456')
        self.assertEqual(retVal.status_code, 200)

        data = json.loads(retVal.data.decode('utf-8'))
        self.assertIn('brand', data)
        self.assertIn('model', data)
        self.assertIn('year', data)        
      
        self.assertEqual(data['brand'], 'BMW')
        self.assertEqual(data['model'], 'X1')
        self.assertEqual(data['year'], 2018)

if __name__ == '__main__':
    unittest.main()
