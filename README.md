# TCC Control

TCC Control, um sistema de gerenciamento de TCC, projeto desenvolvido pelos orientandos Lucas Frutuozo Braga e Willian Matiussi durante as disciplinas de TCC I e II do ano de 2023 do curso de engenharia de software. Tendo como orientador e consultor do projeto o professor Felipe Perez.

O projeto consiste em um sistema de gerenciamento que utiliza a estrutura do Django para o desenvolvimento web, o Django Rest Framework para construir uma API robusta, o MySQL para armazenamento de dados e o Celery para a execução de tarefas em segundo plano.

## Tecnologias Utilizadas

- Django 4.2
- Django rest framework 3.14.0
- Mysql 8.0
- Celery 5.3.1

## Executando em Desenvolvimento

1. Certifique-se de ter o Docker instalado.

2. Adeque os arquivos `.env` com os valores corretos.

3. Realize o build do container através do comando `docker-compose build`.

4. Execute `docker-compose up` para iniciar o servidor de desenvolvimento.

## Executando em Produção

1. Certifique-se de ter o Docker instalado.

2. Adeque os arquivos `.env` com os valores corretos.

3. Realize o build do container através do comando `docker-compose build`.

4. Execute docker-compose -f docker-compose.prod.yaml up para iniciar o servidor em modo de produção.

## Estrutura dos endpoints

- Endereço raiz (`/`): Este é o ponto de entrada principal para as views síncronas do sistema. Aqui, você encontrará a interface do usuário tradicional, permitindo interações diretas e imediatas;

- Endereço API Rest (`api/`): Navegue para este endpoint para acessar os recursos oferecidos pela API REST. É a interface ideal para operações assíncronas, troca de dados e integração com outros sistemas. Em modo de desenvolvimento o sistema possui uma interface mais intuita, no entanto, em produção, apenas é possível consumir dados em formato JSON;

- Endereço de administração (`admin/`): Dirija-se a este local para acessar a seção de administração dedicada. Aqui, você pode realizar operações de gerenciamento em entidades do sistema de forma eficiente, simplificando a administração e manutenção;

## Criação de usuário administrador

```bash
# Utilize o comando utilitário do django para criação de admin.
docker-compose exec django ./manage.py createsuperuser
```

O sistema solicitará que você insira um nome de usuário, endereço de e-mail e senha para o novo superusuário. Após fornecer as informações necessárias, o superusuário será criado e você poderá usá-lo para fazer login na seção de administração do seu aplicativo.
