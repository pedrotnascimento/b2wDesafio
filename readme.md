# B2W Desafio Starwars

##### Requisitos:

- A API deve ser REST
- Para cada planeta, os seguintes dados devem ser obtidos do banco de dados da aplicação, sendo inserido manualmente:
Nome
Clima
Terreno
- Para cada planeta também devemos ter a quantidade de aparições em filmes, que podem ser obtidas pela API pública do [Star Wars](https://swapi.co/):

##### Funcionalidades desejadas:

- Adicionar um planeta (com nome, clima e terreno)
- Listar planetas
- Buscar por nome
- Buscar por ID
- Remover planeta
Linguagens que usamos: Java, Go, Clojure, Node, Python
Bancos que usamos: MongoDB, Cassandra, DynamoDB, Datomic

E lembre-se! Um bom software é um software bem testado.

# Como utilizar
### Requisitos

- [Python](https://www.python.org/downloads/)  3.6.3 ou maior 
- [MongoDB](https://www.mongodb.com/download-center)
- recomendável o uso de [virtualenv] (https://pythonacademy.com.br/blog/python-e-virtualenv-como-programar-em-ambientes-virtuais)
- execute no terminal, na raiz do projeto

> $ pip install -r requirements.txt

- (se estiver no virtualenv e o comando pip não for reconhecido, executar na pasta raiz do ambiente virtual, no caso:

> $ pip install -r b2w\requirements.txt


### Execução
na raiz do projeto, execute:

>$ python manage.py runserver

Para ver a interface amigável da api entre no browser com endereço:
localhost:8000/planets/

### Teste
na raiz do projeto, execute:
>$ python manage.py test
### Documentacão Django
Para interagir com a documentação e as APIs acessar:
> localhost:8000/docs/

No entanto, é recomendável tomar como referência de uso a seção **Métodos** deste readme

### Métodos
##### Obter todos os planetas:
> GET: localhost:8000/planets/

Exemplo:    

    [{
    "name": "nome-planeta",
    "climate": "clima",
    "terrain": "terreno",
    "appearance_qnt": numero
    }]

É retornado uma lista com todos os planetas

- name: nome do planeta do universo Star Wars
- climate: clima do planeta
- terrain: terreno do planeta
- appearance_qnt: quantidade de vezes que o planeta é citado no filme, este valor é obtido da API [https://swapi.co/](https://swapi.co/):

##### Obter um planeta
> GET: localhost:8000/planets/id-do-planeta/

Exemplo:    

    {
    "name": "nome-planeta",
    "climate": "clima",
    "terrain": "terreno",
    "appearance_qnt": numero
    }

##### Criar um novo planeta:
> POST: localhost:8000/planets/

INPUT JSON:

    {
    "name": "nome-planeta",
    "climate": "clima",
    "terrain": "terreno"
    }


##### Atualizar um Planeta:
> PUT: localhost:8000/planets/id-do-planeta/

INPUT JSON:

    {
    "name": "nome-planeta",
    "climate": "clima",
    "terrain": "terreno"
    }


##### Deletar um Planeta:
> DELETE: localhost:8000/planets/id-do-planeta/


##### Paginar quantidade de planetas
> GET: localhost:8000/planets/?page=numero-da-pagina[&count=quantidade-por-pagina]

* o parametro count é opcional
* O resultado é uma lista de planetas, assim como um get sem filtros.
    

Exemplo:

    [{
    "name": "nome-planeta",
    "climate": "clima",
    "terrain": "terreno",
    "appearance_qnt": numero
    }]


##### Pesquisar planeta pelo nome
> GET: localhost:8000/planets/?search=nome-planeta

* A pesquisa é _case-insensitive_. 
* Para pesquisa que contém parte do nome, a api irá buscar todos os resultados que contém este nome.
* O resultado é uma lista de planetas, assim como um get sem filtros
    

Exemplo:

    [{
    "name": "nome-planeta",
    "climate": "clima",
    "terrain": "terreno",
    "appearance_qnt": numero
    }]

