import json


class GerarDados:
    def __init__(self, arquivo_entrada, arquivo_saida):
        self.arquivo_entrada = arquivo_entrada
        self.arquivo_saida = arquivo_saida

    def gerar_dados(self):
        try:
            # Carregando o JSON original
            with open(self.arquivo_entrada, "r") as json_file:
                dados = json.load(json_file)

            # Supondo que 'data' seja a lista de dicionários que você forneceu
            dados_por_url = {}  # Para armazenar os dados por URL

            for item in dados:
                url = item["url"]
                true_keys = []
                false_keys = []

                for key, value in item.items():
                    if value == True:
                        true_keys.append(key)
                    elif value == False:
                        false_keys.append(key)

                # Adicionando uma verificação para evitar a divisão por zero
                total_de_imagens = item["total_de_imagens"]
                porcentagem_imagens_com_alt = (
                    (item["imagens_com_alt"] / total_de_imagens * 100)
                    if total_de_imagens != 0
                    else 0
                )
                porcentagem_imagens_com_alt = round(porcentagem_imagens_com_alt, 2)

                url_true_counts = len(true_keys)
                url_false_counts = len(false_keys)

                url_teste_count = url_true_counts + url_false_counts
                porcentagem = (url_true_counts / url_teste_count) * 100

                # Criar um dicionário com todos os dados por URL
                if url not in dados_por_url:
                    dados_por_url[url] = {
                        "Testes Aprovados": url_true_counts,
                        "Testes Reprovados": url_false_counts,
                        "Porcentagem de imagens com alt": porcentagem_imagens_com_alt,
                        "Total de testes": url_teste_count,
                        "Porcentagem dos testes Aprovados": porcentagem,
                    }

            true_keys_all = []  # Para armazenar as chaves com valor True
            false_keys_all = []  # Para armazenar as chaves com valor False
            for item in dados:
                for key, value in item.items():
                    if value == True:
                        true_keys_all.append(key)
                    elif value == False:
                        false_keys_all.append(key)
            true_data = len(true_keys_all)  # Para armazenar as chaves com valor True
            false_data = len(false_keys_all)
            todos_testes = true_data + false_data

            todos_dados_porcentagem = (true_data / todos_testes) * 100
            todos_dados_porcentagem = round(todos_dados_porcentagem, 3)
            dados_de_todas_urls = {
                "Testes Aprovados": true_data,
                "Testes Reprovados": false_data,
                "Total de Testes": todos_testes,
                "Porcentagem do Testes Aprovados": todos_dados_porcentagem,
            }

            dados_finais = {
                "metricas_gerais": dados_de_todas_urls,
                "metricas_por_url": dados_por_url,
            }

            # Salvar os dados em um arquivo JSON
            with open(self.arquivo_saida, "w") as json_output:
                json.dump(dados_finais, json_output, indent=4)

        except Exception as e:
            print(f"Erro ao gerar dados: {str(e)}")
