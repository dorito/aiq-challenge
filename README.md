## Como rodar o projeto
- Para rodar o projeto na sua máquina, você vai precisar do `docker` instalado e funcionando corretamente.
- Idealmente, sua máquina possui a porta 8883 desocupada; Caso não seja o caso, favor alterar a porta no arquivo `.env.dev` para refletir uma porta não ocupada na sua máquina.
- Após ter o docker rodando, execute os seguintes comandos:
  - `docker compose -f docker-compose.dev.yaml up -d`
  - `docker exec -ti aiq_challenge_api aerich upgrade`

## Onde estão as docs / que endpoints e payloads posso usar:
- Caso você esteja utilizando a porta padrão as docs podem ser vistas em http://localhost:8883/docs

## Como rodar os testes
- Execute o seguinte comando: `docker exec -ti aiq_challenge_api pytest`

## Principais tecnologias utilizadas
- Python
- FastAPI para servir os endpoints de maneira assíncrona
- Redis como cache
- TortoiseORM como ORM
- PostgreSQL como banco de dados
- Pydantic para serialização dos dados
- Pytest para os testes

## Estrutura do projeto
- Pasta `app`: possui coisas ligadas a configuração de cache, API, database e middlewares
- Pasta `data`: possui os modelos de data (na pasta `models`), os schemas (na pasta `schemas`) e os enums (na pasta `enums`)
- Pasta `migrations`: possui as migrações de banco de dados
- Pasta `client`: possui os dados referentes aos fluxos de adição/edição/remoção/listagem/login de clientes
- Pasta `product`: possui os dados referentes aos fluxos de listagem/detalhamento de produtos
- Pasta `favorite_product`: possui os dados referentes aos fluxos de adição/remoção de favoritos
- Pasta `tests`: possui os testes unitários e de integração

## Detalhes de implementação
- As rotas ligadas a usuários foram feitas sem autenticação ou sistema de roles para adição/remoção de clientes
  - O motivo é tornar mais fácil a validação do que foi feito.
- As rotas ligadas a produto possuem um cache de 5 minutos, tanto pra listagem como pro detalhamento de um produto quaisquer
  - Num cenário ideal, esses dados teriam um cache mais inteligente, afim de tornar o mesmo ''quente''; Uma forma de fazer isso seria com o serviço que gera os dados se comunicando com esse serviço aqui (pra aí forçar a atualização do cache), outra com algum outro serviço fazendo pooling dos dados e sendo o gatilho para o cache.