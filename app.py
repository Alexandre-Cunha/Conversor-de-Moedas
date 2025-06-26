from flask import Flask, render_template, request #type: ignore
import requests #type: ignore
from decimal import Decimal, InvalidOperation

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def conversor():
    valor_convertido = None
    cotacao_utilizada = None
    erro = None
    
    if request.method == 'POST':
        try:
            # Request para ligar ao formulário do front
            moeda_entrada = request.form.get('moeda_entrada', '').upper()
            moeda_saida = request.form.get('moeda_saida', '').upper()
            valor_digitado = request.form.get('valor_digitado', '')
            
            # Validar se o valor é numérico
            try:
                valor_decimal = Decimal(valor_digitado.replace(',', '.'))
                if valor_decimal <= 0:
                    erro = 'O valor deve ser maior que zero!'
                    return render_template('index.html', erro=erro)
            except (InvalidOperation, ValueError):
                erro = 'Por favor, digite um valor numérico válido!'
                return render_template('index.html', erro=erro)
            
            # Consulta na API
            entrada_dados = f"{moeda_entrada}{moeda_saida}"
            
            try:
                response = requests.get(
                    f'https://economia.awesomeapi.com.br/json/last/{moeda_entrada}-{moeda_saida}',
                    timeout=10
                )
                response.raise_for_status()
                dados = response.json()
                
                # Verificar se a conversão é válida
                if entrada_dados in dados:
                    cotacao_utilizada = float(dados[entrada_dados]['ask'])
                    valor_convertido = float(valor_decimal) * cotacao_utilizada
                    
                    # Formatação da cotação para exibição
                    cotacao_utilizada = round(cotacao_utilizada, 4)
                    valor_convertido = round(valor_convertido, 2)
                else:
                    erro = f'Par de moedas {moeda_entrada}-{moeda_saida} não encontrado!'
                    
            except requests.exceptions.RequestException as e:
                erro = 'Erro ao consultar a API. Tente novamente mais tarde.'
                print(f"Erro na API: {e}")
            except ValueError as e:
                erro = 'Erro ao processar dados da API.'
                print(f"Erro no processamento: {e}")
                
        except Exception as e:
            erro = f'Ocorreu um erro inesperado. Tente novamente.{e}'
            print(f"Erro geral: {e}")
    
    return render_template('index.html', 
                         valor_convertido=valor_convertido,
                         cotacao=cotacao_utilizada,
                         erro=erro)

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)