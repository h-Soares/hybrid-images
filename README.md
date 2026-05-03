# Projeto final - Processamento de Imagens

Este repositório contém o meu projeto final da disciplina de Processamento de Imagens da Universidade de São Paulo.

O objetivo do projeto é desenvolver uma aplicação que possibilite ao usuário gerar imagens híbridas. Uma imagem híbrida é uma imagem gerada pela combinação das baixas frequências de uma imagem e das altas frequências de outra imagem, de tal forma que a imagem observada varia conforme a distância do observador. De perto observa-se a imagem de altas frequências, enquanto de longe a imagem de baixas frequências se torna evidente. O efeito de distanciamento da imagem pode ser simulado ao comprimir os olhos. 

A filtragem será aplicada no domínio da frequência com filtros Gaussianos.

## Funcionalidades

- Seleção interativa de duas imagens por janela gráfica.
- Aplicação de filtro passa-baixa Gaussiano em uma imagem.
- Aplicação de filtro passa-alta Gaussiano em outra imagem.
- Combinação das duas imagens filtaradas para formar a imagem híbrida.
- Exibição do resultado final em uma nova janela.

## Requisitos

As bibliotecas utilizadas no projeto estão listadas no arquivo `requirements.txt`:

- `numpy`
- `opencv-python`

O projeto também utiliza `tkinter`, que normalmente já vem instalado com o Python.

## Instalação

1. Crie e ative um ambiente virtual, se desejar:

   ```bash
   python -m venv .venv
   .venv\\Scripts\\activate
   ```

2. Instale as dependências do projeto:

   ```bash
   pip install -r requirements.txt
   ```

## Como usar

Execute o arquivo principal:

```bash
python hybrid_image.py
```

Em seguida, selecione a imagem para baixa frequência e a imagem para alta frequência nas janelas que forem abertas.

## Saída

Ao final da execução, o programa exibe a imagem híbrida em uma janela do OpenCV.
