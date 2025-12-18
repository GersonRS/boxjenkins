# Publicação no PyPI

## Configuração Inicial

### 1. Criar conta no PyPI
- PyPI oficial: https://pypi.org/account/register/
- TestPyPI (teste): https://test.pypi.org/account/register/

### 2. Configurar Trusted Publishing no PyPI

#### No PyPI oficial (pypi.org):
1. Acesse: https://pypi.org/manage/account/publishing/
2. Clique em "Add a new pending publisher"
3. Preencha:
   - **PyPI Project Name**: `boxjenkins`
   - **Owner**: `GersonRS`
   - **Repository name**: `boxjenkins`
   - **Workflow name**: `publish-to-pypi.yml`
   - **Environment name**: `pypi`
4. Salve

#### No TestPyPI (test.pypi.org):
1. Acesse: https://test.pypi.org/manage/account/publishing/
2. Repita o processo acima com:
   - **Environment name**: `testpypi`

### 3. Configurar Environments no GitHub

1. Acesse: https://github.com/GersonRS/boxjenkins/settings/environments
2. Crie dois environments:
   - `pypi`
   - `testpypi`
3. Para cada environment, configure:
   - **Deployment protection rules**: Adicione revisores se desejar
   - **Environment secrets**: Não é necessário com Trusted Publishing

## Uso

### Publicar no TestPyPI (para testes)

1. Vá até: https://github.com/GersonRS/boxjenkins/actions/workflows/publish-to-pypi.yml
2. Clique em "Run workflow"
3. Selecione `testpypi`
4. Execute

Após publicado, instale para testar:
```bash
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ boxjenkins
```

### Publicar no PyPI oficial

#### Método 1: Via Release (Recomendado)
1. Crie uma tag:
   ```bash
   git tag v0.1.0
   git push origin v0.1.0
   ```

2. Vá até: https://github.com/GersonRS/boxjenkins/releases/new
3. Selecione a tag `v0.1.0`
4. Preencha:
   - **Release title**: `v0.1.0 - Primeira versão`
   - **Description**: Descreva as mudanças
5. Clique em "Publish release"

O workflow será acionado automaticamente e publicará no PyPI.

#### Método 2: Manual
1. Vá até: https://github.com/GersonRS/boxjenkins/actions/workflows/publish-to-pypi.yml
2. Clique em "Run workflow"
3. Selecione `pypi`
4. Execute

### Instalar do PyPI oficial

Após publicado:
```bash
pip install boxjenkins
```

## Atualizar Versão

Antes de publicar uma nova versão:

1. Atualize a versão em `boxjenkins/__init__.py`:
   ```python
   __version__ = "0.1.1"
   ```

2. Atualize a versão em `setup.py`:
   ```python
   version="0.1.1",
   ```

3. Commit e push:
   ```bash
   git add boxjenkins/__init__.py setup.py
   git commit -m "chore: Bump version to 0.1.1"
   git push
   ```

4. Crie nova tag e release:
   ```bash
   git tag v0.1.1
   git push origin v0.1.1
   ```

## Versionamento Semântico

Seguir o padrão [Semantic Versioning](https://semver.org/):
- **MAJOR** (X.0.0): Mudanças incompatíveis na API
- **MINOR** (0.X.0): Nova funcionalidade compatível
- **PATCH** (0.0.X): Correções de bugs

Exemplos:
- `0.1.0` → `0.1.1`: Correção de bug
- `0.1.1` → `0.2.0`: Nova feature (gráficos statsmodels)
- `0.2.0` → `1.0.0`: API estável, mudanças breaking

## Troubleshooting

### Erro: "Project name already exists"
O nome `boxjenkins` pode já estar em uso. Opções:
1. Escolher outro nome (ex: `boxjenkins-arima`, `pybj`)
2. Atualizar `setup.py` e `pyproject.toml` com novo nome

### Erro: "Invalid or non-existent authentication"
- Verifique se configurou Trusted Publishing corretamente
- Confirme que os nomes do workflow e environment estão corretos

### Erro: "Version already exists"
- Não é possível reenviar a mesma versão
- Incremente a versão antes de publicar novamente

## Verificar Publicação

Após publicar com sucesso:
- PyPI: https://pypi.org/project/boxjenkins/
- TestPyPI: https://test.pypi.org/project/boxjenkins/

## Segurança

✅ **Trusted Publishing** (OIDC): Método recomendado, não requer tokens
❌ **API Tokens**: Não use se possível, Trusted Publishing é mais seguro

## Recursos

- [PyPI Trusted Publishing](https://docs.pypi.org/trusted-publishers/)
- [GitHub Actions PyPI Publish](https://github.com/pypa/gh-action-pypi-publish)
- [Python Packaging Guide](https://packaging.python.org/)
