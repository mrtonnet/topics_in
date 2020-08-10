* Draft: 2020-08-10 (Mon)

# Jupyter Lab 설치하기
이 내용은 [Installation](https://jupyterlab.readthedocs.io/en/stable/getting_started/installation.html) 문서에 있는 내용을 참고로 설명을 덧붙인 것입니다.

가장 간단한 설치 방법은 `pip`을 이용해서 현재 계정에 직접 설치하는 것입니다. 실전에서는 Conda 가상 환경이나 Docker 컨테이너 환경에 설치합니다.

## Linux 머신에 직접 설치하기

```bash
$ pip install jupyterlab
```

### 실행 화면
```bash
$ pip install jupyterlab
Collecting jupyterlab
  Downloading https://files.pythonhosted.org/packages/1b/1b/ce43d66010878f86e574ae94d4aa6f78028ba5dba7287e11ebbaea2b3c17/jupyterlab-0.33.12-py2.py3-none-any.whl (14.3MB)
    100% |████████████████████████████████| 14.3MB 125kB/s 
  ...
Successfully installed MarkupSafe-1.1.1 ... zipp-1.2.0
```

[TODO: 확인해볼 것]
## Conda 가상 환경에 설치하기

```bash
$ conda install -c conda-forge jupyterlab
```

## Docker 컨테이너 환경에 설치하기

```bash
$ jupyter serverextension enable --py jupyterlab --sys-prefix
```
