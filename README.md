<div align="center">
    <h1> 🏦 BNDS - <img alt="Comunicred logo" src="https://raw.githubusercontent.com/itsaleplets/comunicred/main/src/images/Group.png?token=GHSAT0AAAAAABYY75KO6NBUSQUH6GJQIAOAY2DISRA" /> 👩🏽‍🔧🧑🏽‍🌾👩🏽‍🏫 </h1>
</div>


### O Projeto
Nós da Comunicred, gamificamos a forma de acesso ao crédito através de um app super simples e prático. Atualizando o fluxo de notas e de caixa de maneira rápida e simples o empreendedor pode acumular moedas no app da Comunicred. Além disso, caso o pequeno empresário realize cursos de capacitação para auxiliá-lo em seu próprio negócio, ela pode acumular ainda mais moedas!

Agora... O que o empreendedor pode fazer com essas moedas?
Acumulando as moedas, ele pode subir no ranking dos empreendedores da região e conseguir cada vez mais acesso ao crédito, flexibilização em prazos de pagamento e taxa de juros ou até mesmo liberação de crédito continua para fomentar o seu próprio negócio. Sendo assim, através da gameficação, nós da Comunicred premiamos os empreendedores e fortalecemos os laços entre os pequenos negócios e o microcrédito, como ferramenta para fomentar o desenvolvimento da região.
### As Ferramentas

A parte back-end do projeto foi construída em Django para gerenciamento da API e do Painel Administrativo.

### Site

https://comunicred.fly.dev/

Rota ADM

https://comunicred.fly.dev/admin/


### Instalação do Projeto:

```
pip install -r requirements.txt
```


Aplicar as migrações no banco de dados

```
python manage.py migrate
```

Criar o usuario Admin

```
python manage.py createsuperuser
```




### Iniciar o Servidor:


```
python manage.py runserver
```



### Rotas:

Essa é a rota onde tem todos os dados de todos os clientes cadastrado.
Rota somente pra visualização de como os dados estão indo pro APP

```bash
Method: GET
URL: http://localhost:8000/
```

Rota para o Painel Administrativo

```bash
Method: GET
URL: http://localhost:8000/admin/
```
