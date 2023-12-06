from Dados.GerarDados import GerarDados
from Testes.Verificar import Verificar
from URLS.GerarUrls import VerificarLinks


verificar_links = VerificarLinks()
verificar_links.processar_urls("urls.txt", "dominios.txt")
verificar_links.finalizar()

verificador = Verificar()
verificador.iniciar("dominios.txt")
verificador.finalizar()
gerador = GerarDados("resultados.json", "dadosFinais.json")
gerador.gerar_dados()
