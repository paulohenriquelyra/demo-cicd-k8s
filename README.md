_template_: | 
 # Demo: Pipeline CI/CD com GitHub Actions para Kubernetes

 Este projeto demonstra um pipeline completo de CI/CD para construir uma imagem Docker de uma aplicação web simples, enviá-la para o Docker Hub e fazer o deploy em um cluster Kubernetes. 

 ## Estrutura do Projeto

 ```
 demo-cicd-k8s/
 |-- .github/
 |   |-- workflows/
 |       |-- cicd.yaml       # Workflow do GitHub Actions
 |-- app/
 |   |-- main.py           # Aplicação Flask
 |   |-- Dockerfile        # Dockerfile da aplicação
 |   |-- requirements.txt  # Dependências Python
 |   |-- templates/
 |       |-- index.html    # Template HTML
 |-- k8s/
 |   |-- deployment.yaml   # Manifesto de Deployment do K8s
 |   |-- service.yaml      # Manifesto de Service do K8s
 |-- README.md             # Documentação do projeto
 ```

 ## Pré-requisitos

 1. **Cluster Kubernetes**: Um cluster Kubernetes local (ex: Minikube, Kind, Docker Desktop) ou na nuvem.
 2. **kubectl**: Ferramenta de linha de comando para interagir com o cluster.
 3. **Conta no Docker Hub**: Para armazenar a imagem Docker da aplicação.
 4. **Conta no GitHub**: Para hospedar o repositório e usar o GitHub Actions.

 ## Como Configurar e Rodar

 ### 1. Crie um Repositório no GitHub

 Envie o conteúdo deste projeto para um novo repositório no seu GitHub.

 ### 2. Configure os Secrets no GitHub

 Para que o pipeline funcione, você precisa configurar os seguintes secrets nas configurações do seu repositório (`Settings > Secrets and variables > Actions`):

 - `DOCKER_HUB_USERNAME`: Seu nome de usuário do Docker Hub.
 - `DOCKER_HUB_TOKEN`: Um token de acesso do Docker Hub. Você pode criar um em `Account Settings > Security`.
 - `KUBECONFIG`: O conteúdo do seu arquivo `~/.kube/config`, codificado em Base64. Use o comando abaixo para obter o valor:

   ```bash
   cat ~/.kube/config | base64
   ```

   **Atenção**: O uso do `KUBECONFIG` como secret é uma simplificação para este demo. Em um ambiente de produção, é recomendado usar um runner auto-hospedado (self-hosted runner) que tenha acesso seguro ao cluster.

 ### 3. Inicie o Pipeline

 Faça um `push` para a branch `main` do seu repositório. O workflow do GitHub Actions será acionado automaticamente.

 ## O Pipeline de CI/CD (`cicd.yaml`)

 O pipeline é dividido em dois jobs principais:

 1. **`build-and-push`**: 
    - Faz o checkout do código.
    - Realiza o login no Docker Hub usando os secrets.
    - Constrói a imagem Docker da aplicação, usando o SHA do commit como tag para garantir uma versão única.
    - Envia a imagem para o seu repositório no Docker Hub.

 2. **`deploy`**:
    - Depende do sucesso do job `build-and-push`.
    - Faz o checkout do código.
    - Configura o `kubectl` com o `KUBECONFIG` do secret para acessar seu cluster.
    - Atualiza o arquivo `k8s/deployment.yaml`, substituindo o placeholder `__IMAGE_NAME__` pelo nome e tag da imagem recém-criada.
    - Aplica os manifestos do Kubernetes (`deployment.yaml` e `service.yaml`) no cluster.

 ## Acessando a Aplicação

 Após o deploy, a aplicação estará rodando no seu cluster. Para acessá-la, você pode usar `port-forward` ou verificar o NodePort do serviço.

 ### Usando Port Forward

 ```bash
 kubectl port-forward service/demo-app-service 8080:80
 ```

 Agora, acesse http://localhost:8080 no seu navegador.

 ### Usando NodePort (com Minikube)

 Se estiver usando Minikube, execute:

 ```bash
 minikube service demo-app-service
 ```

 Este comando abrirá a aplicação diretamente no seu navegador.

