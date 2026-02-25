# 🏡 Previsão de Preços de Imóveis na Califórnia (California Housing)

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-Machine%20Learning-orange.svg)
![GeoPandas](https://img.shields.io/badge/GeoPandas-Spatial%20Analysis-green.svg)

## 📖 Contextualização
O mercado imobiliário é impulsionado por uma complexa rede de fatores, desde as características físicas do imóvel até a sua localização geográfica e o perfil socioeconômico da vizinhança. Este projeto utiliza os dados do censo da Califórnia (1990) para explorar e entender a fundo essas dinâmicas.

A base de dados não avalia casas individuais, mas sim quarteirões/distritos, fornecendo uma visão macroeconômica fascinante sobre como a distribuição de renda, a densidade populacional e a proximidade com o oceano moldam o custo de vida no estado.

## 🎯 Objetivos do Projeto
1. **Desenvolver um Modelo Preditivo:** Criar e otimizar um modelo de Machine Learning capaz de prever com precisão o valor mediano das casas (`median_house_value`) em diferentes distritos da Califórnia.
2. **Análise de Importância de Variáveis (Feature Importance):** Identificar e quantificar quais características têm o maior impacto (positivo ou negativo) no preço final do imóvel, extraindo insights de negócios acionáveis.
3. **Análise Geoespacial:** Mapear a distribuição de preços e cruzar os dados com limites administrativos (condados) para entender a correlação espacial utilizando mapas interativos e estáticos.

## 🛠️ Tecnologias e Bibliotecas Utilizadas
* **Manipulação de Dados:** `pandas`, `numpy`
* **Análise Geoespacial:** `geopandas`, `folium`, `contextily`
* **Visualização:** `matplotlib`, `seaborn`
* **Machine Learning:** `scikit-learn` (Pipelines, ColumnTransformer, GridSearchCV, Modelos de Regressão)

## 🔍 Destaques da Análise (Feature Engineering)
Durante o desenvolvimento, variáveis brutas foram transformadas em métricas mais representativas da realidade imobiliária:
* **Proporções de Cômodos:** Criação de variáveis como `bedrooms_per_room` e `rooms_per_household` para medir o padrão do imóvel (casas de luxo vs. apartamentos compactos).
* **Densidade Habitacional:** Análise da `population_per_household` para identificar áreas de superlotação vs. bairros residenciais amplos.
* **Distância de Centros Administrativos:** Cálculo de distância espacial (em metros/km) entre os imóveis e os centroides dos condados da Califórnia.



## 📂 Organização do projeto

```
├── .env               <- Arquivo de variáveis de ambiente (não versionar)
├── .gitignore         <- Arquivos e diretórios a serem ignorados pelo Git
├── ambiente.yml       <- O arquivo de requisitos para reproduzir o ambiente de análise
├── LICENSE            <- Licença de código aberto se uma for escolhida
├── README.md          <- README principal para desenvolvedores que usam este projeto.
|
├── dados              <- Arquivos de dados para o projeto.
|
├── modelos            <- Modelos treinados e serializados, previsões de modelos ou resumos de modelos
|
├── notebooks          <- Cadernos Jupyter. A convenção de nomenclatura é um número (para ordenação),
│                         as iniciais do criador e uma descrição curta separada por `-`, por exemplo
│                         `01-fb-exploracao-inicial-de-dados`.
│
|   └──src             <- Código-fonte para uso neste projeto.
|      │
|      ├── __init__.py  <- Torna um módulo Python
|      ├── config.py    <- Configurações básicas do projeto
|      └── graficos.py  <- Scripts para criar visualizações exploratórias e orientadas a resultados
|
├── referencias        <- Dicionários de dados, manuais e todos os outros materiais explicativos.
|
├── relatorios         <- Análises geradas em HTML, PDF, LaTeX, etc.
│   └── imagens        <- Gráficos e figuras gerados para serem usados em relatórios
```

## 🚀 Configuração do ambiente

1. Faça o clone do repositório que será criado a partir deste modelo.

    ```bash
    git clone ENDERECO_DO_REPOSITORIO
    ```

2. Crie um ambiente virtual para o seu projeto utilizando o gerenciador de ambientes de sua preferência.

    a. Caso esteja utilizando o `conda`, exporte as dependências do ambiente para o arquivo `ambiente.yml`:

      ```bash
      conda env export > ambiente.yml
      ```

    b. Caso esteja utilizando outro gerenciador de ambientes, exporte as dependências
    para o arquivo `requirements.txt` ou outro formato de sua preferência. Adicione o
    arquivo ao controle de versão, removendo o arquivo `ambiente.yml`.

3. Verifique o arquivo `notebooks/01-fb-exemplo.ipynb` para exemplos
de uso do código.
4. Renomeie o arquivo `notebooks/01-fb-exemplo.ipynb` para um nome
mais apropriado ao seu projeto. E siga a convenção de nomenclatura para os demais
notebooks.
5. Remova arquivos de exemplo e adicione os arquivos de dados e notebooks do seu
projeto.
6. Verifique o arquivo `notebooks/src/config.py` para configurações básicas do projeto.
Modifique conforme necessário, adicionando ou removendo caminhos de arquivos e
diretórios.
7. Atualize o arquivo `referencias/01_dicionario_de_dados.md` com o dicionário de dados
do seu projeto.
8. Atualize o `README.md` com informações sobre o seu projeto.
9. Adicione uma licença ao projeto. Clique
[aqui](https://docs.github.com/pt/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository)
se precisar de ajuda para escolher uma licença.
10. Renomeie o arquivo `.env.exemplo` para `.env`
11. Adicione variáveis de ambiente sensíveis ao arquivo `.env`.

Por padrão, o arquivo `.gitignore` já está configurado para ignorar arquivos de dados e
arquivos de Notebook (para aqueles que usam ferramentas como
[Jupytext](https://jupytext.readthedocs.io/en/latest/) e similares). Adicione ou remova
outros arquivos e diretórios do `.gitignore` conforme necessário. Caso deseje adicionar
forçadamente um Notebook ao controle de versão, faça um commit forçado com o
comando `git add --force NOME_DO_ARQUIVO.ipynb`.

Para mais informações sobre como usar Git e GitHub, [clique aqui](https://cienciaprogramada.com.br/2021/09/guia-definitivo-git-github/). Sobre ambientes virtuais, [clique aqui](https://cienciaprogramada.com.br/2020/08/ambiente-virtual-projeto-python/).
