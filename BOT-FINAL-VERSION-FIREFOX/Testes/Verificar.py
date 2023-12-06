import json
import re
import time
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

from Drive.DriverFactory import WebDriverFactory


class Verificar:
    def __init__(self):
        try:
            self.web_driver_factory = WebDriverFactory()
            self.driver = self.web_driver_factory.create_driver()
            self.driver.set_page_load_timeout(
                15
            )  # Defina o tempo limite de 15 segundos
        except Exception as e:
            print(f"Erro ao iniciar o WebDriver: {str(e)}")
            raise

    def iniciar(self, arquivo_urls):
        try:
            with open(arquivo_urls, "r") as file:
                urls = [
                    url.strip() for url in file.read().splitlines() if url.strip()
                ]  # Ignora linhas em branco
            resultados = []
            for url in urls:
                url = url.strip()  # Remove espaços em branco em excesso, se houver
                resultado = {"url": url}
                self.acessarSite(url)
                (
                    resultado["imagens_com_alt"],
                    resultado["imagens_sem_alt"],
                    resultado["todas_com_alt"],
                ) = self.verificarImagens()
                resultado["total_de_imagens"] = (
                    resultado["imagens_com_alt"] + resultado["imagens_sem_alt"]
                )
                resultado["tag_main"] = self.verificarTagMain()
                resultado["texto_ajustavel"] = self.textoAjustavel()
                resultado["navegacao_teclado"] = self.testarNavegacaoTeclado()
                resultado["estrutura_semantica"] = self.verificarEstruturaSemantica()
                resultado[
                    "legendas_ou_audiodescricao"
                ] = self.testarLegendasAudiodescricao()
                resultado["rotulos_adequados"] = self.verificar_rotulos_adequados()
                resultado["botao_libras"] = self.verificarPalavrasNoCodigoFonte()
                resultados.append(resultado)
            # Salva os resultados em um arquivo JSON
            with open("resultados.json", "w") as json_file:
                json.dump(resultados, json_file, indent=2)
        except Exception as e:
            print(f"Erro ao iniciar a verificação: {str(e)}")

    def acessarSite(self, url):
        try:
            self.driver.get(url)
        except Exception as e:
            print(f"Erro ao acessar a URL {url}: {str(e)}")

    def verificarImagens(self):
        try:
            imgAlt = self.driver.find_elements(By.TAG_NAME, "img")
            imagensComAlt = 0
            imagensSemAlt = 0
            for img_element in imgAlt:
                altAttribute = img_element.get_attribute("alt")
                if altAttribute:
                    print(
                        f"Encontrou uma imagem com o atributo alt preenchido: {altAttribute}"
                    )
                    imagensComAlt += 1
                else:
                    print("Encontrou uma imagem sem o atributo alt preenchido.")
                    imagensSemAlt += 1
            print(f"Total de imagens com atributo alt preenchido: {imagensComAlt}")
            print(f"Total de imagens sem atributo alt preenchido: {imagensSemAlt}")
            todasComAlt = imagensSemAlt == 0
            return imagensComAlt, imagensSemAlt, todasComAlt
        except Exception as e:
            print(f"Erro ao verificar imagens: {str(e)}")
            return 0, 0, False

    def verificarTagMain(self):
        try:
            self.driver.find_element(By.TAG_NAME, "main")
            print("Tag Main encontrada na página.")
            return True
        except NoSuchElementException:
            print("Tag Main não encontrada na página.")
            return False

    def textoAjustavel(self, tamanho_minimo=10, tamanho_maximo=22):
        try:
            body = self.driver.find_element(By.TAG_NAME, "body")
            font_size = int(
                body.value_of_css_property("font-size")[:-2]
            )  # Remove 'px' e converte para inteiro
            if tamanho_minimo <= font_size <= tamanho_maximo:
                print("O texto é ajustável.")
            else:
                print("O texto não é ajustável.")
            return tamanho_minimo <= font_size <= tamanho_maximo
        except Exception as e:
            print(f"Erro ao verificar texto ajustável: {str(e)}")
            return False

    def testarNavegacaoTeclado(self):
        try:
            body = self.driver.find_element(By.TAG_NAME, "body")
            body.send_keys(Keys.TAB)
            elemento_com_foco = self.driver.switch_to.active_element
            if elemento_com_foco:
                print("Elemento com foco encontrado após pressionar a tecla TAB.")
            else:
                print(
                    "Nenhum elemento com foco encontrado após pressionar a tecla TAB."
                )
            return elemento_com_foco is not None
        except Exception as e:
            print(f"Erro ao testar navegação por teclado: {str(e)}")
            return False

    def verificarEstruturaSemantica(self):
        try:
            titulos = self.driver.find_elements(
                By.XPATH,
                "//*[self::h1 or self::h2 or self::h3 or self::h4 or self::h5 or self::h6]",
            )
            marcadores_semanticos = self.driver.find_elements(
                By.XPATH, "//*[self::nav or self::main or self::article]"
            )
            if bool(titulos) and bool(marcadores_semanticos):
                print(
                    "Elementos de título (h1-h6) e marcadores semânticos (nav, main, article) estão presentes."
                )
            else:
                print(
                    "Pelo menos um dos elementos de título (h1-h6) ou marcadores semânticos (nav, main, article) não está presente."
                )
            return bool(titulos) and bool(marcadores_semanticos)
        except Exception as e:
            print(f"Erro ao verificar estrutura semântica: {str(e)}")
            return False

    def testarLegendasAudiodescricao(self):
        try:
            elementos_de_video = self.driver.find_elements(By.TAG_NAME, "video")
            elementos_de_audio = self.driver.find_elements(By.TAG_NAME, "audio")
            for video in elementos_de_video:
                legenda = video.get_attribute("subtitles")
                if legenda:
                    print(f"Legendas encontradas para um vídeo.")
                    return True
            for audio in elementos_de_audio:
                audiodescricao = audio.get_attribute("aria-describedby")
                if audiodescricao:
                    print(f"Descrição de áudio encontrada para um elemento de áudio.")
                    return True
            return False
        except Exception as e:
            print(f"Erro ao testar legendas/audiodescrição: {str(e)}")
            return False

    def verificar_rotulos_adequados(self):
        try:
            input_elements = self.driver.find_elements(By.TAG_NAME, "input")

            for input_element in input_elements:
                input_id = input_element.get_attribute("id")
                input_aria_labelledby = input_element.get_attribute("aria-labelledby")
                input_aria_label = input_element.get_attribute("aria-label")

                print(f"ID: {input_id}")
                print(f"aria-labelledby: {input_aria_labelledby}")
                print(f"aria-label: {input_aria_label}")

                if input_id:
                    matching_label = self.driver.find_element(
                        By.CSS_SELECTOR, f'label[for="{input_id}"]'
                    )
                    if not matching_label:
                        print("Label not found for ID.")
                    return False
                elif input_aria_labelledby:
                    labelledby_element = self.driver.find_element(
                        By.ID, input_aria_labelledby
                    )
                    if not labelledby_element:
                        print("Labelledby element not found.")
                    return False
                elif not input_aria_label:
                    print("No label or aria-labelledby specified.")
                return False
            return True
        except Exception as e:
            print(f"Erro ao verificar rótulos adequados: {str(e)}")
        return False

    def verificarPalavrasNoCodigoFonte(self):
        try:
            # Obtém o código fonte da página
            page_source = self.driver.page_source
            # Define as palavras que você deseja procurar
            palavras = [
                "VLibras",
                "Vlibras",
                "accessibility",
                "Libras",
                "libras",
                "LIBRAS",
            ]
            # Verifique se pelo menos uma das palavras está presente no código fonte
            for palavra in palavras:
                regex = re.compile(palavra, re.IGNORECASE)
                if regex.search(page_source):
                    return True
            # Se nenhuma das palavras for encontrada, retorne False
            return False
        except Exception as e:
            print(f"Erro ao verificar palavras no código fonte: {str(e)}")
            return False

    def finalizar(self):
        try:
            self.driver.quit()
        except Exception as e:
            print(f"Erro ao finalizar o WebDriver: {str(e)}")
