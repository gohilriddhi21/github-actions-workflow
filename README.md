# How do GitHub actions work?

Impl in setting up a basic GitHub Actions workflow for a simple Python project.

### Steps to Set Up GitHub Actions

1. **Clone a GitHub Repository**

    Clone the repository to your local machine:

    ```sh
    git clone https://github.com/your-username/your-repository.git
    cd your-repository
    ```

2. **Create a Basic Python Application**

    Inside the repository, create a simple Python application. For example, create a file named `main.py` with the following content:

    ```python
    print("Hello, world!")
    ```

3. **Add, Commit, and Push Changes to GitHub**

    ```sh
    git add .
    git commit -m "Added basic Python application"
    git push origin main
    ```

4. **Configure GitHub Workflow**

    Through GitHub remote, configure the GitHub Actions workflow by clicking on to the **Actions** Tab.

5. **Create a `.github/workflows` Directory**

    Inside your cloned repository, create a directory to store your workflow YAML file:

    ```sh
    mkdir -p .github/workflows
    ```

6. **Create a Workflow YAML File**

    Create a file named `actions.yml`, workflow file, inside the `.github/workflows` directory with the necessary workflow configuration.

3. **Add, Commit, and Push Changes to GitHub**

    ```sh
    git add .
    git commit -m "Added Workflow YAML"
    git push origin main
    ```

### Note:

To manually trigger the workflow, you can add the following line under the `on` section of the workflow YAML:

```yaml
on:
  workflow_dispatch:
```

