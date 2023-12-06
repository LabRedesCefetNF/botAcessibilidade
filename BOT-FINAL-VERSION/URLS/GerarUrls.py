from selenium.webdriver.common.by import By
from urllib.parse import urlparse

from Drive.DriverFactory import WebDriverFactory


class VerificarLinks:
    def __init__(self):
        self.web_driver_factory = WebDriverFactory()
        self.driver = self.web_driver_factory.create_driver()
        self.redes_sociais = [
            "facebook",
            "instagram",
            "linkedin",
            "youtube",
            "twitter",
            "maps",
        ]

    def extrair_links(self, url):
        self.driver.get(url)
        links = self.driver.find_elements(By.TAG_NAME, "a")
        lista_links = [link.get_attribute("href") for link in links]
        return lista_links

    def normalize_url(self, url):
        parsed_url = urlparse(url)
        return f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"

    def processar_urls(self, input_file, output_file):
        with open(input_file, "r") as file:
            urls = file.read().splitlines()

        with open(output_file, "w") as dominios_file:
            seen_urls = set()  # Set to store unique normalized URLs

            for i, url in enumerate(urls):
                dominio = urlparse(url).hostname
                # dominios_file.write(f"Domínio {i + 1} - {dominio}:\n")

                links = self.extrair_links(url)

                for link in links:
                    if link.startswith("http") or link.startswith("https"):
                        if not any(
                            rede_social in link for rede_social in self.redes_sociais
                        ):
                            normalized_link = self.normalize_url(link)
                            if (
                                normalized_link not in seen_urls
                                and dominio in normalized_link
                            ):  # Check if normalized URL is not seen before and has the same domain
                                dominios_file.write(f"  {link}\n")
                                seen_urls.add(
                                    normalized_link
                                )  # Add normalized URL to the set

                dominios_file.write("\n")

    def finalizar(self):
        self.driver.quit()
